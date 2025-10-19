# Interactions

一个 Interaction 表示一个特定 input pattern。例如，一个 hold 是一个 Interaction，它需要一个 Control 被按下至少一个最小的时间值。

Interactions 驱动 Actions 上的响应。你可以在单独的 Binding 或者整个 Action（所有 Bindings）上放置他们（Interactions），应用到整个 Action 时，Interactions 应用到 Action 上所有的 Binding。在运行时，当一个特定 interaction 完成，它触发这个 Action。

![InteractionProperties](../../../Image/InteractionProperties.png)

## Operation

一个 Interaction 有一组它可以经历的不同的阶段 phases，以响应接受的输入：

- Waiting：Interaction 正在等待输入
- Started：Interaction 已经开始（即它接收到一些它期望的 input），但是还没有完成
- Performed：Interaction 完成了
- Canceled：Interaction 被中断并取消。例如，如果 player 按下 button 并在 hold interaction 完成需要的最小时间前释放。

不是每个 Interaction 都触发每个 phase，Interaction 触发的 phases 的 pattern 依赖于 Interaction type。

Performed 通常是触发一个 Interaction 实际响应的 phase，Started 和 Canceled 可以用于在 Interaction 进行时提供 UI 反馈。例如，当一个 hold 开始时，app 可以显示一个进度条直到达到 hold time。然而，如果 hold 在完成前被 cancel，app 可以重置进度条重新开始。

下面这个例子展示一个 fire Action 的这种设置，player 可以 tap 来立即 fire，或者 hold 来充电 charge：

```C#
var fireAction = new InputAction("fire");
fireAction.AddBinding("<Gamepad>/buttonSouth")
    // Tap fires, slow tap charges. Both act on release.
    .WithInteractions("tap;slowTap");

fireAction.started +=
    context =>
    {
        if (context.Interaction is SlowTapInteraction)
            ShowChargingUI();
    };

fireAction.performed +=
    context =>
    {
        if (context.Interaction is SlowTapInteraction)
            ChargedFire();
        else
            Fire();
    };

fireAction.canceled +=
    _ => HideChargingUI();
```

### Multiple Controls on an Action

如果你有多个 Controls 绑定到一个具有 Interaction 的 Binding 或者 Action，则 Input System 先应用 Control disambiguation 逻辑来为 Action 得到一个 value。然后它 feeds 到 Interaction logic。任何 bound Controls 都可以执行 Interaction。

### Multiple Interactions on a Binding

如果多个 Interactions 出现在一个 Binding 或 Action，则 Input System 以出现在 Binding 上的顺序来检查 Interactions。上面的 code example 展示了这个例子。这个 fireAction Action 上的 Binding 有两个 Interactions：WithInteractions("tap;slowTap")。这个 tap Interaction 在解释 input 时获得首先获得机会。如果 button 被按下，Action 调用 tap Interaction 上的 Started callback。如果 player 保持按下这个 button，tap interaction 时间超过，Action 为 tap Interaction 调用 Canceled callback，并开始 slow tap Interaction（它现在接收到一个 Started callback）。

## Using Interactions

你可以在 Bindings 或 Actions 按照 Interactions。

### Interactions on Bindings

当你为你的 Actions 创建 Binding，你可以为这些 Bindings 添加 Interactions。

如果你使用 Input Action Assets，你可以添加任何 Interaction 到 Input Action Editor 中的 Bindings。如果 Interaction 有任何参数，也可以编辑它们。

在 code 中添加 Interactions：

```C#
var Action = new InputAction();
action.AddBinding("<Gamepad>/leftStick").WithInteractions("tap(duration=0.8)");
```

### Interactions on Actions

Actions 上的 Interactions 影响绑定到 Action 上的所有 Controls，而不只是一个指定 Binding 中的 Control。如果在 Binding 和 Action 上都有 Interactions，Input System 先处理 binding 中的。

你可以在 Input Action Assets editor window 添加和编辑 Actions 上的 Interactions。

在 code 为 Action 添加 Interactions：

```C#
var Action = new InputAction(Interactions: "tap(duration=0.8)");
```

## Predefined Interactions

Input System package 带有一组基本的 Interactions。如果 Action 没有 Interactions set，系统使用它的默认 Interaction。

内置 Interactions 操作在 Control actuation 上，并不直接使用 Control values。Input System 对 Control actuation 的 magnitude 评估 pressPoint 参数。这意味着你可以在具有一个 magnitude 的任何 Control 使用这些 Interactions，例如 sticks，而不只是 buttons。

- Default Interaction

  如果你没有明确添加一个 Interaction 到一个 Binding 或者它的 Action，默认的 Interaction 应用到 Binding。

  Value 或 Button type 有以下行为：

  - 一旦绑定的 Control 成为 actuated（离开默认状态），Actions 从 Waiting 变成 Started，然后立即 Performed 并回到 Started。先执行 InputAction.started 上的 Callback，后面跟着 InputAction.performed 上的 Callback
  - 只要绑定的 Control 保持 actuated，Action 保持 Started 并且无论何时 Control 的 value 发生改变触发一个 Performed
  - 当绑定的 Control 停止 actuated（回到默认状态），Action 成为 Canceled 并返回 Waiting，并触发 InputAction.canceled 的回调

  PassThrough 类型 Actions 具有一个相同的行为。Input System 不试图追踪任何 Interaction 状态（如果分别追踪多个 Controls，这将是无意义的）。相反，它为每一个 value change 触发一个 Performed 回调。

  | Callbacks / InputAction.type | Value or Button | PassThrough |
  | --- | --- | --- |
  | started | Control 成为 actuated | 不使用 |
  | performed | Controls 改变了 actuation。它还在 started 触发时触发 | Control 改变 value 时 |
  | canceled | Control 不在 actuated | 不使用 |

- Press

  你可以使用一个 PressInteraction 来显式强制 button-like interactions。使用 behaviour 参数来选择 Interaction 是否应该在 press，release 或者二者都触发。

  pressPoint 是一个 actuated control 被认为是 pressed 必须超过的 magnitude 阈值。

  | Parameters | Type | Default value |
  | --- | --- | --- |
  | pressPoint | float | InputSettings.defaultButtonPressPoint |
  | behavior | PressBehavior | PressOnly |

  | Callbacks / behavior | PressOnly | ReleaseOnly | PressAndRelease |
  | --- | --- | --- | --- |
  | started | Control magnitude 超过 pressPoint 时调用 | same | same |
  | performed | Control magnitude 超过 pressPoint 时调用 | Control magnitude 返回到 pressPoint 以下时调用 | or |
  | canceled| not used | not used | not used |

- Hold

  HoldInteraction 需要 player 在 InputSystem 触发一个 Action 按下一个 Control 超过一个 duration seconds。

  | Parameters | Type | Default value |
  | --- | --- | --- |
  | duration | float | InputSettings.defaultHoldTime |
  | pressPoint | float | InputSettings.defaultButtonPressPoint |

  | Callbacks | When |
  | --- | --- |
  | started | Control magnitude 超过 pressPoint 时调用 |
  | performed | Control magnitude 超过 pressPoint >= duration 时间时调用 |
  | canceled | Control magnitude 在 duration 之前返回到 pressPoint 之下时调用（即 button 没有按下足够长的时间 |

- Tap

  TapInteraction 需要用户在 duration seconds 内按下并释放一个 Control 来触发一个 Action。

  | Parameters | Type | Default Value |
  | --- | --- | --- |
  | duration | float | InputSettings.defaultTapTime |
  | pressPoint | float | InputSettings.defaultButtonPressPoint |

  | Callbacks | When |
  | --- | --- |
  | started | Control magnitude 超过 pressPoint 时调用 |
  | performed | Control magnitude 在 duration 之前回到 pressPoint 之下时调用 |
  | canceled | Control magnitude 超过 pressPoint >= duration（即 tap 太慢了） |

- SlowTap

  SlowTapInteraction 需要 player 在触发一个 Action 之前按下并保持一个 Control 超过一个最小的 duration。

  SlowTap 是在 Hold Interaction 之后 release 触发的。

  | Parameters | Type | Default Value |
  | --- | --- | --- |
  | duration | float | InputSettings.defaultSlowTapTime |
  | pressPoint | float | InputSettings.defaultButtonPressPoint |

  | Callbacks | When |
  | --- | --- |
  | started | Control magnitude 超过 pressPoint 时调用 |
  | performed | Control magnitude 在 duration 之后回到 pressPoint 之下时调用 |
  | canceled | Control magnitude 在 duration 之前返回到 pressPoint 之下时调用（即 tap 太快了）|

- MultiTap

  MultiTapInteraction 需要 player 在 tapTime seconds 内按下并释放一个 Control, tap tapCount 次，并且 taps 之间不超过 tapDelay，以触发一个 Action。可以使用这个 Interaction 检测 double-click 或 multi-click 手势。

  | Parameters | Type | Default value |
  | --- | --- | --- |
  | tapTime | float | InputSettings.defaultTapTime，一个 tapTime 的时间上限 |
  | tapDelay | float | 2 * tapTime，两个 taps 之间的最大延迟 |
  | tapCount | int | 2 |
  | pressPoint | float | InputSettings.defaultButtonPressPoint |

  | Callbacks | When |
  | --- | --- |
  | started | Control magnitude 超过 pressPoint 时调用 |
  | performed | Control magnitude 回到 pressPoint 之下然后重新回到 pressPoint 之上时调用，重复调用 tapCount 次 |
  | canceled | 回到 pressPoint 之后，在 tapDelay 之内不再回到 pressPoint 之上，或者超过 pressPoint 并在 tapTime 之内不再回到 pressPoint 之下 |

## Writing Custom Interactions

可以编写自定义 Interaction。可以在 UI 和 code 中以 built-in Interaction 的方式使用自定义 Interaction。

实现 IInputInteraction：

```C#
// Interaction which performs when you quickly move an
// axis all the way from extreme to the other.
public class MyWiggleInteraction : IInputInteraction
{
    public float duration = 0.2;

    void Process(ref InputInteractionContext context)
    {
        if (context.timerHasExpired)
        {
            context.Canceled();
            return;
        }

        switch (context.phase)
        {
            case InputActionPhase.Waiting:
                if (context.Control.ReadValue<float>() == 1)
                {
                    context.Started();
                    context.SetTimeout(duration);
                }
                break;

            case InputActionPhase.Started:
                if (context.Control.ReadValue<float>() == -1)
                    context.Performed();
                break;
        }
    }

    // Unlike processors, Interactions can be stateful, meaning that you can keep a
    // local state that mutates over time as input is received. The system might
    // invoke the Reset() method to ask Interactions to reset to the local state
    // at certain points.
    void Reset()
    {
    }
}
```

向 Input System 注册 Interaction：

```C#
InputSystem.RegisterInteraction<MyWiggleInteraction>();
```

现在 new Interaction 在 Input Action Asset Editor Window 中可用，或者在 code 中使用：

```C#
var Action = new InputAction(Interactions: "MyWiggle(duration=0.5)");
```