有两种注意的方式可以响应 Actions：polling 或 event-driven。

- Polling 方式每帧检测 actions 的当前状态，通常在 Update() 方法中
- Event-driven 方式在 code 创建自己的方法作为 event handler，然后在 Action 中设置注册回调方法

在大多数常见场景中，尤其是动作类游戏（即玩家输入需要对游戏角色产生持续影响）的情况下，使用轮询（Polling）方式通常更简单且易于实现。

而对于其他输入较少发生、且需要将输入指向场景中多个不同游戏对象（GameObject）的情况，事件驱动（event-driven）的方式可能更为合适。

# Polling Actions

使用 InputAction.ReadValue<>() 来的读取 Aciton 的 value。

```C#
using UnityEngine;
using UnityEngine.InputSystem;

public class Example : MonoBehaviour
{
    InputAction moveAction;

    private void Start()
    {
        moveAction = InputSystem.actions.FindAction("Move");
    }

    void Update()
    {
        Vector2 moveValue = moveAction.ReadValue<Vector2>();
        // your code would then use moveValue to apply movement
        // to your GameObject
    }
}
```

Value 的类型必须对应与 control 的类型，1D control 返回 float，2D control 返回 vector2。Trigger 类型的 control（例如 button）使用 IsPressed()、WasPressedThisFrame()、WasReleaseThisFrame() 读取，使用 ReadValue。ReadValue 用于读取连续产生 value 的 control。

有两种方法可以轮询 performed，来确定 action 是否在当前帧 performed 或 stopped performing。

这些方法与 `InputAction.WasPressedThisFrame()` 和 `InputAction.WasReleasedThisFrame()` 不同，因为后两者直接依赖于驱动该 action 的交互（Interactions），包括在没有为 action 或 binding 添加特定交互时使用的默认交互。这意味着 `WasPressedThisFrame` 和 `WasReleasedThisFrame` 是基于具体的交互行为来检测输入是否在当前帧被按下或释放，而其他方法可能不直接依赖于这些具体的交互行为。这样设计可以提供更精确的控制和更细致的输入处理方式。

- InputAction.WasPerformedThisFrame()

  如果 action 的 InputAction.phase 在当前帧的任意时刻改变为 Performed，返回 true

  输入事件被交互逻辑（Interaction）判定为执行完成的当前帧（如长按、双击）。

- InputAction.WasCompletedThisFrame()

  如果 action 的 InputAction.phase 在当前帧的任意时刻从 Preformed 改变为其他 phase，返回 true。

  输入事件完整生命周期结束的当前帧（仅限特定交互类型，如SlowTap释放后）。

  当你要检测某个交互（如 Press 或 Hold）在哪个帧停止执行时，这种方法对于按钮动作（Button Action）或带有交互的值动作（Value Action）非常有用。  

  但对于使用默认交互的动作来说，该方法在值类型（Value）action 和直通类型（Pass-Through）action 中始终会返回 `false` —— 因为对于值类型动作，其阶段状态会一直保持在 `Started`；而对于直通类型动作，阶段状态则会一直保持在 `Performed`，不会进入“已取消”或“已完成”状态。
  
下面的示例使用了默认动作中的 **Interact** 动作，它带有一个 **Hold** 交互（interaction），使得该动作只有在绑定的控件被持续按住一段时间后才会触发（例如 0.4 秒）：

```C#
using UnityEngine;
using UnityEngine.InputSystem;

public class Example : MonoBehaviour
{
    InputAction interactAction;

    private void Start()
    {
        interactAction = InputSystem.actions.FindAction("Interact");
    }

    void Update()
    {
        if (interactAction.WasPerformedThisFrame())
        {
            // your code to respond to the first frame that the Interact action is held for enough time
        }

        if (interactAction.WasCompletedThisFrame())
        {
            // your code to respond to the frame that the Interact action is released after being held for enough time
        }
    }
}
```

有 3 个方法可以轮询 button presses 和 releases：

- InputAction.IsPressed()

  检测输入当前是否处于持续按下状态​（无论是否在本帧按下）。

- InputAction.WasPressedThisFrame()

  检测输入是否在本帧被按下​（仅触发一次）。

  输入信号首次超过按下阈值的当前帧（如按键按下瞬间）。

- InputAction.WasReleasedThisFrame()

  检测输入是否在本帧被释放​（仅触发一次）。

  输入信号首次低于释放阈值的当前帧（如按键松开瞬间）。

Aciton Bindings 的 Interaction 为输入定义了更高层的抽象，例如长按、双击、SlowTap 等，Performed 和 Completed 是判断这些更高层抽象输入是否在本帧执行的，这些高层抽象的输入要定义一些 duration 的。而 Pressed 和 Released 只是简单地判断基本的输入（默认 Interaction），即是否在当前帧按下和抬起。

在Unity Input System中，`WasPerformedThisFrame()`、`WasCompleteThisFrame()`与`WasPressedThisFrame()`、`WasReleasedThisFrame()`是两组不同层级的输入检测方法，核心区别如下：

---

## **1. 方法功能对比**
| 方法                      | 触发条件                                                                 | 适用场景                     |
|---------------------------|--------------------------------------------------------------------------|-----------------------------|
| **`WasPressedThisFrame()`** | 输入信号**首次超过按下阈值**的当前帧（如按键按下瞬间）                     | 单次触发动作（跳跃、射击）   |
| **`WasReleasedThisFrame()`**| 输入信号**首次低于释放阈值**的当前帧（如按键松开瞬间）                     | 结束动作（取消技能、停止移动）|
| **`WasPerformedThisFrame()`** | 输入事件**被交互逻辑（Interaction）判定为执行完成**的当前帧（如长按、双击） | 复合输入（蓄力攻击、连击）   |
| **`WasCompleteThisFrame()`** | 输入事件**完整生命周期结束**的当前帧（仅限特定交互类型，如SlowTap释放后）  | 特殊交互（长按后释放触发）   |

---

## **2. 核心差异**
- **检测逻辑不同**  
  - `Pressed/Released`：基于**物理输入信号阈值**（如按键压力值超过`pressPoint`）  
  - `Performed/Complete`：基于**交互逻辑**（如Hold长按时间达标或Tap点击次数满足）  

- **交互支持**  
  - `Pressed/Released`：适用于所有绑定，无论是否有Interaction（如普通按键检测）  
  - `Performed/Complete`：需配合Interaction（如`Hold`、`Tap`）使用，否则与`Pressed/Released`行为一致  

- **生命周期**  
  - `Performed`可能在长按期间多次触发（如`Hold`的循环执行），而`Complete`仅在交互结束时触发一次  

---

## **3. 代码示例**
```csharp
// 普通按键检测（无Interaction）
if (inputAction.WasPressedThisFrame()) {
    Debug.Log("按键按下"); // 每按一次触发一次
}

// 带Hold交互的检测
inputAction.performed += ctx => {
    if (ctx.interaction is HoldInteraction) {
        Debug.Log("长按执行中"); // 长按期间可能多次触发
    }
};
inputAction.canceled += ctx => {
    if (ctx.interaction is HoldInteraction) {
        Debug.Log("长按完成"); // 相当于WasCompleteThisFrame()
    }
};
```

---

## **4. 何时使用？**
- **简单输入**：优先用`Pressed/Released`（如跳跃、射击）  
- **复杂交互**：用`Performed/Complete`配合Interaction（如蓄力、连击）  

如需更精确控制，可参考Unity官方文档中的[Interaction设计](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/Interactions.html)。

# Event-driven

当为 action 设置 callback，Action 通知你的 code 发生特定类型的输入，然后 code 就可以相应地进行响应。

有几种方式来设置 callback：

- 使用 PlayerInput 组件，在 Inspector 中设置
- 每个 Action 有 started，performed，canceled 回调
- 每个 Action Map 有一个 actionTriggered callback
- InputSystem 有一个全局的 InputSystem.onActionChange callback
- InputActionTrace 可以记录 Actions 上发生的改变

## PlayerInput 组件

PlayerInput 是设置 Action Callback 最简单的方法。它在 Inspector 中设置 callback，不需要中间代码。

## Action Callbacks

每个动作（Action）在接收到输入时，都会经历一组明确的阶段（phases）。这些阶段描述了动作从开始到结束过程中可能经过的不同状态。

- Disabled：Action 被 disabled，不能接收输入
- Waiting：Action 被 enabled，当前等待输入
- Started：Input System 已接收到启动了与该 Action 交互（Interaction）的输入
- Performed：与该 Action 的交互（Interaction）已完成
- Canceled：与该 Action 的交互（Interaction）已完成

可以使用 InputAction.phase 读取 action 的当前 phase。

Started，Performed，Canceled phase 每个都有与其关联的 callback：

```C#
var action = new InputAction();

action.started += context => /* Action was started */;
action.performed += context => /* Action was performed */;
action.canceled += context => /* Action was canceled */;
```

每个 callback 接收一个 InputAction.CallbackContext 结构体，它保存了上下文信息，你可以用来查询 Action 的当前状态，以及从触发 Action 的 Controls 读取 values（InputAction.CallbackContext.ReadValue）。

结构体的内容值在 callback 期间有效，存储它并准备稍后使用是不安全的。

Callback 何时以及如何触发，依赖于 Bindings 上的 Interations。如果 Bindings 没有应用任何 Interactions，则使用 default Interaction。

`InputActionMap.actionTriggered` 回调：除了监听单个动作（Action）之外，你还可以在整个动作映射（Action Map）上监听其内部任意动作的状态变化。通过 `actionTriggered` 回调，你可以捕获该动作映射中的所有动作触发事件，而无需为每个动作单独添加监听器。这在需要统一处理多个动作输入的情况下非常有用，例如角色控制或界面交互等场景。

```C#
var actionMap = new InputActionMap();
actionMap.AddAction("action1", "<Gamepad>/buttonSouth");
actionMap.AddAction("action2", "<Gamepad>/buttonNorth");

actionMap.actionTriggered += context => { ... };
```

接收的参数和 started, performed, canceled 回调接收的 InputAction.CallbackContext 结构体一样。

Input System 对 Action 上的全部 3 个单个 callbacks 调用 InputActionMap.actionTriggered，即在一个 callback 上调用全部 started，performed，canceled。

InputSystem.onActionChange 回调类似 InputSystem.onDeviceChange，app 可以全局监听任何 action 相关的变化。

```C#
InputSystem.onActionChange += (obj, change) =>
{
    // obj can be either an InputAction or an InputActionMap
    // depending on the specific change.
    switch (change)
    {
        case InputActionChange.ActionStarted:
        case InputActionChange.ActionPerformed:
        case InputActionChange.ActionCanceled:
            Debug.Log($"{((InputAction)obj).name} {change}");
            break;
    }
}
```

InputActionTrace

你可以通过 Trace Actions 来生成日志，记录特定动作集合上发生的所有活动。为此，可以使用 `InputActionTrace`。它的行为与用于输入事件的 `InputEventTrace` 类似。

注意：`InputActionTrace` 会分配非托管内存（unmanaged memory），因此在使用完毕后需要手动释放，以避免造成内存泄漏。

```C#
var trace = new InputActionTrace();

// Subscribe trace to single Action.
// (Use UnsubscribeFrom to unsubscribe)
trace.SubscribeTo(myAction);

// Subscribe trace to entire Action Map.
// (Use UnsubscribeFrom to unsubscribe)
trace.SubscribeTo(myActionMap);

// Subscribe trace to all Actions in the system.
trace.SubscribeToAll();

// Record a single triggering of an Action.
myAction.performed += ctx =>
{
    if (ctx.ReadValue<float>() > 0.5f)
        trace.RecordAction(ctx);
};

// Output trace to console.
Debug.Log(string.Join(",\n", trace));

// Walk through all recorded Actions and then clear trace.
foreach (var record in trace)
{
    Debug.Log($"{record.action} was {record.phase} by control {record.control}");

    // To read out the value, you either have to know the value type or read the
    // value out as a generic byte buffer. Here, we assume that the value type is
    // float.

    Debug.Log("Value: " + record.ReadValue<float>());

    // If it's okay to accept a GC hit, you can also read out values as objects.
    // In this case, you don't have to know the value type.

    Debug.Log("Value: " + record.ReadValueAsObject());
}
trace.Clear();

// Unsubscribe trace from everything.
trace.UnsubscribeFromAll();

// Release memory held by trace.
trace.Dispose();

```

一旦记录完成，只要没有同时进行写入操作，并且动作（Action）的设置（即追踪器所访问的配置数据）在主线程上没有被同时修改，该追踪记录就可以安全地在多个线程中读取。

# Action Types

每个 Action 可以是三种不同 action type 中的一种。你可以在 Input Action 编辑器窗口中选择 action type，或者在调用 `InputAction()` 构造函数时通过指定 `type` 参数来设置。  

Action Type 会影响输入系统如何处理该 action 的状态变化。默认的动作类型是 **Value**（值类型）。

- Value

  这是默认的动作（Action）类型，适用于需要跟踪控件（Control）状态连续变化的输入。

  **值类型（Value）**动作会持续监控所有绑定到该动作的控件，并从中选择一个被激活程度最高的控件作为驱动该动作的主控件。然后，该动作会在每次值发生变化时通过回调报告该控件的值。如果另一个绑定控件的激活程度更高，则它将成为新的主控件，动作将开始报告该控件的值。这个过程被称为**冲突解决（conflict resolution）**。当你希望允许不同的控件控制同一个动作，但在同一时间只从一个控件接收输入时，这种方式非常有用。

  当动作最初启用时，它会对所有绑定的控件执行一次初始状态检查。如果有任何控件已经被激活，则动作会触发一个带有当前值的回调。

- Button

  这种类型与 **Value（值类型）** 非常相似，但 **Button（按钮类型）** 动作只能绑定到 `ButtonControl` 类型的控件，并且不会像值类型动作那样执行**初始状态检查**（参见上面的“Value”部分）。

  你应该将此类型用于那些每次按下时触发一次动作的输入。在这种情况下，初始状态检查通常并不适用，因为如果在启用该动作时，按钮仍处于之前按下后未释放的状态，就可能会导致意外触发动作。

- Pass-Through

  **直通类型动作（Pass-Through Actions）** 会绕过上述值类型动作中所描述的**冲突解决（conflict resolution）**过程，并且不使用“由某个特定 Control 驱动 Action”的概念。  

  相反，任何一个绑定控件的状态发生变化时，都会直接触发一个回调，并携带该控件的当前值。  

  这种方式在你希望处理来自一组控件的所有输入时非常有用。例如，你希望分别响应多个按钮或多个轴输入，而不是让系统选择其中一个作为主控件。

# Debugging Actions

要查看当前已启用的动作（Actions）及其绑定的控件（Controls），可以使用 **输入调试器（Input Debugger）**。

你还可以从 **Visualizers 示例** 中使用 **InputActionVisualizer** 组件，在屏幕上实时显示某个动作的值（value）和交互状态（Interaction state）。这对于调试和可视化输入行为非常有帮助。

# Using Actions with multiple players

你可以在多个本地玩家之间使用相同动作（Action）定义（例如，在本地合作模式的游戏中）。