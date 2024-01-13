# Input System

## Control Schemes

用于定义玩家控制游戏时使用不同类型的设备或一组设备，例如键盘鼠标，手柄，方向盘等等。

可以通过设置多种类型的 Control Schemes 保持不同类型的控制系统分离。也可以不用 Schemes，只用不同的 Action，然后绑定好 Control。

使用多个 Control Schemes 的目的是，方便切换设备操作模式，比如单人、双人，又或者不同设备的控制。

## Action Maps

Action Maps 包含特定目的行为的所有动作。例如所有角色的通用动作放在一个 Map（移动，跳跃，开火），所有 UI 操作放在另一个 Map。

为什么要用多个 Action Map？例如在一个第一人称游戏中，包含射击和驾驶的功能，玩家同一时间只能处于一种状态。但是两个状态中的按键可能有冲突（例如同一个键在射击状态中触发开火，在驾驶状态中则触发刹车）。程序中不能同时开启两种控制。因此可以将射击和驾驶各自的操作分别添加到一个 Map 中，然后再不同的模式切换不同的 Action Maps 就可以。

通过脚本切换 Action Maps：

```C#
playerInput.SwitchCurrentActionMap("Menu");
```

## Actions

InputSystem 中，Action 连接控制设备的物理输入和游戏内的事件。

有 3 中不同类型的 Action：

- Button：默认设置，包括按钮或按键
- Value：连续变化的状态，可以读取数值（例如 float，Vector2），可以用于模拟控制，例如移动
- Pass Through：和 Value 类似

Pass Through 和 Value 类似，但是如果设置了多个输入，Values 会返回最大的输入值，而 Pass Through 则返回最近的输入值，不管它有多大。

Value 或 Pass Through 有一个额外选项 Control Type。这允许指定期望从输入中获得什么类型的输入，并影响哪些 bindings 可用。Control Type 包括：

- Any
- Analog
- Bone
- Digital
- Double
- Dpad
- Eyes
- Integer
- Pose
- Quaternion
- Stick
- Touch
- Vector2
- Vector3

## Bindings

Binding 就是物理输入与事件的绑定。除了通过界面绑定，还可以通过代码在运行时绑定：

```C#
using UnityEngine;
using UnityEngine.InputSystem;

public class BasicRebinding : MonoBehaviour
{
    public InputActionReference triggerAction;

    void ChangeBinding()
    {
        InputBinding binding = triggerAction.action.bindings[0];
	binding.overridePath = "<Keyboard>/#(g)";
	triggerAction.action.ApplyBindingOverride(0, binding);
    }
}
```

## 如何识别两个按钮同时按下

创建 Button with One Modifier Composite 或者 Button with Two Modifiers Composite。

## 如何避免两个动作同时触发

Input System 不能屏蔽其他输入。例如绑定 Jump 动作和 B 键，绑定 Dive 动作与 Left Trigger + B 键。按下 Left Trigger + B 时，两个动作都会触发。为避免这个问题，在触发时，做一个检测判断，看另一个按键有没有触发。

## Interactions and Processors

Interactions 和 Processors 可以改变输入的解释方法，比如轻点还是长按。

Interactions：

- Hold：按下一段时间才会触发
- Multi Tap：重复使用 Tap，可以实现双击操作
- Press：按下或释放触发
- Slow Tap：与 Tap 相比具有更长的时间周期
- Tap：快速按压和释放

Processors：

- Axis Deadzone
- Clamp
- Invert
- Normalize
- Scale

对设备的输入值进行后处理，然后再返回。

## Player Input 组件

Input System 为了方便使用提供了多种方式，最简单的方法是使用 Player Input Component。

- 切换 Action Maps

  PlayerInput.SwitchCurrentActionMap("Menu")

- Behaviour 与脚本通信的方式

  - Send Messages：调用 MonoBehaviour.SendMessage，脚本中定义 On{Message} 的函数。
  - Broadcast Message：调用 MonoBehaviour.BroadcastMessage，在 GameObject Hierarchy 向下 Send Message
  - Invoke Unity Events：PlayerInput 内部定义 UnityEvent，在 Inspector 中选择回调函数
  - Invoke C Sharp Events：不在 Inspector 中设置回调函数，而在 Script 中手动设置回调

使用 PlayerInput + UnityEvent 调用 action callback 时，回调函数会触发 3 个事件，分别时 start，performed，cancel。但是如果使用 InputAction 轮询 phase，只会得到 performed 事件，没有 performed 时是 waiting。


