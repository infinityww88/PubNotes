# Control

deadZone 是不触发操作的微小区域，类似冷启动区域，使得在其中的移动不触发操作，例如游戏手柄摇杆初始位置周围的一小块区域。

actuated 是指一个 Control 操作的显著程度。例如一个摇杆摇晃到一半和完全摇到另一边，后者更显著。如果设置 maxValue 为 1，则前置返回 0.5，后者返回 1.0。

一个 InputControl 表示一个 values 的 source。这个 values 可以是任何结构化或基础的类型。唯一的需求是，这个 type 必须是 blittable 的，块拷贝。

Controls 只用于 input。Input Device 上的 Output 和 configuration items 不表示为 Controls。

每个 Control 被 InputControl.name 标识，并可具有一个 display name，和 shortDislayName。例如 PS4 手柄（gamepad）的 buttonWest(name) 具有 display name（Square）

除此以外，一个 Control 可能有一个或多个 aliases 为 Control 提供另外的名字。InputControl.aliases 属性。

## Control Hierarchies

Controls 可以形成 hierarchies。Control hierarchy 的 root 是 Device。

Hierarchies 设置是通过 layouts 唯一控制。

InputControl.parent InputControl.children。InputDevice.allControls 以 flattened hierarchy 访问 Device 上的全部 Controls。

## Control Types

所有的 controls 基于 InputControl<TValue> 实现。

| Control Type | Description | Example |
| --- | --- | --- |
| AxisControl | 1D floating-point axis | Gamepad.leftStick.x |
| ButtonControl | 以 floating-point value 表达的 button。button 是否可以具有 0 或 1 之外的 value 依赖于底层表示。例如 gamepad trigger buttons 可以有 0 或 1 之外的 value，但是 gamepad face button 通常不能 | Mouse.leftButton | 
| KeyControl | 表示 keyboard key 的特殊 button。Keys 有一个关联的 keyCode | Keyboard.aKey |
| Vector2Control | 2D floting-point vector | Pointer.position |
| Vector3Control | 3D floating-point vector | Accelerometer.acceleration |
| QuaternionControl | 3D rotation | AttitudeSensor.attitude |
| IntegerControl | int value | Touchscreen.primaryTouch.touchId |
| StickControl | 2D stick control | Gamepad.rightStick |
| DpadControl | 4-way button 就像 gamepads 上的 D-pad | Gamepad.dpad |
| TouchControl | 表示一个 touch screen 上一个 touch 所有属性的 control | Touchscreen.primaryTouch |

## Control usages

一个 Control 可以有一个或多个关联的 usages。一个 usage 是一个 string，表示 Control 预期的用法，例如 Submit，标记一个 Control 通常用于确认 UI 上的一个 selection。在 gamepad 上，这个 usage 通常是 buttonSouth Control。

InputControl.usages

Usages 可以是任意字符串。但是通常有一组常见的 usages，并在 CommonUsages 类中预定义了一些 usage。

## Control paths

<Gamepad>/leftStick/x 意味着 gamepad 的 left stick 上的 X Control。

Input System可以使用文本 paths 查找 Controls。Input Actions 上的 Binding 依赖这个功能来确定它们用来读取输入的 Controls。

然而，你还可以使用它们来直接在 Controls 和 Devices 查找，或者使用 InputSystem.FindControls 让 InputSystem 在所有 devices 上搜索 Control。

```C#
var gamepad = Gamepad.all[0];
var leftStickX = gamepad["leftStick/x"];
var submitButton = gamepad["{Submit}"];
var allSubmitButtons = InputSystem.FindControls("*/{Submit}");
```

每个 path 组件使用相同的语法，由多个字段组成。每个字段时可选的，但至少要出现一个字段。所有字段都是大小写不敏感的。

<layoutName>{usageName}controlName#(displayName)

InputControl.path

## Control state

每个 Control 连接到一个内存块，它被认为是 Control 的 state。你可以查询内存块的 size，format，location，使用 InputControl.stateBlock

Controls 的 state 存储在 unmanaged memory，Input System 在内部处理它。所有添加到系统的 Devices 共享一个 unmanaged memeory block，它包含这些 Devices 上的所有 Controls 的 state。

一个 Control state 可能不以自然格式存储。例如，system 通常将 buttons 为 bitfields，而将 axis controls 表示为 8-bit 或 16-bit 整数。这个格式是被 platform，hardware，drivers 的组合决定的。每个 Control 知道它的存储的格式，以及如何转换 values。Input System 使用 layouts 来理解格式。

可以通过 ReadValue 方法访问 Control 的当前状态。

Gamepad.current.leftStick.x.ReadValue();

每个 Control 类型返回特定类型 value。InputControl.valueType

从 Control 读取的 value 可以应用一个或多个 Processors。

### Recording state history

你可能想要访问一个 Control 上的 value change 历史（例如，为了计算 touch release 时的 exist velocity）。

要记录随时间变化的 record state，使用 InputStateHistory 或 InputStateHistory <TValue>。

```C#
// Create history that records Vector2 control value changes.
// NOTE: You can also pass controls directly or use paths that match multiple
//       controls (e.g. "<Gamepad>/<Button>").
// NOTE: The unconstrained InputStateHistory class can record changes on controls
//        of different value types.
var history = new InputStateHistory<Vector2>("<Touchscreen>/primaryTouch/position");

// To start recording state changes of the controls to which the history
// is attached, call StartRecording.
history.StartRecording();

// To stop recording state changes, call StopRecording.
history.StopRecording();

// Recorded history can be accessed like an array.
for (var i = 0; i < history.Count; ++i)
{
    // Each recorded value provides information about which control changed
    // value (in cases state from multiple controls is recorded concurrently
    // by the same InputStateHistory) and when it did so.

    var time = history[i].time;
    var control = history[i].control;
    var value = history[i].ReadValue();
}

// Recorded history can also be iterated over.
foreach (var record in history)
    Debug.Log(record.ReadValue());
Debug.Log(string.Join(",\n", history));

// You can also record state changes manually, which allows
// storing arbitrary histories in InputStateHistory.
// NOTE: This records a value change that didn't actually happen on the control.
history.RecordStateChange(Touchscreen.current.primaryTouch.position,
    new Vector2(0.123f, 0.234f));

// State histories allocate unmanaged memory and need to be disposed.
history.Dispose();
```

例如，如果你想获得 gamepad left stick 最后 100 个 samples：

```C#
var history = new InputStateHistory<Vector2>(Gamepad.current.leftStick);
history.historyDepth = 100;
history.StartRecording();
```

## Coontrol actuation

一个 Control 被认为是 actuated，如果它从默认状态移动走（moved away），并影响了 Control 的实际值。可以使用 IsActuated 查询一个 Control 当前是否 actuated。

```C#
// Check if leftStick is currently actuated.
if (Gamepad.current.leftStick.IsActuated())
    Debug.Log("Left Stick is actuated");
```

这不仅可以用于决定一个 Control 是否是 actuated（从默认状态移动开并改变 Control 的状态值），还能得到它 actuated 的程度（即 magnitude）。例如，对一个 Vector2Control，这将是 vector 的长度，而对于 button，它是 raw，absolute floating-point value。

通常， Control 当前的 magnitude 总是 >= 0。然而，一个 Control 可能没有一个有意义的 magnitude，此时它返回 -1。任何负值都应该被认为是一个无效的 magnitude。

你可以使用 EvaluateMagnitude 查询当前 actuation 的 amount。

```C#
// Check if left stick is actuated more than a quarter of its motion range.
if (Gamepad.current.leftStick.EvaluateMagnitude() > 0.25f)
    Debug.Log("Left Stick actuated past 25%");
```

有两种机制非常明显地使用 Control actuation：

- Interactive rebinding（InputActionRebindingExceptions.RebindOperation）使用它来在多个适合的 Controls 之间选择一个 actuated 最大的
- 在绑定到同一个 action 的多个 Controls 之间 Disambiguation，使用它决定哪个 Control 用来驱动 action

## Noisy Controls

Input System 可以标记一个 Control 为 noisy。InputControl.noisy。

Noisy Controls 是那些不需要实际或故意的 player 交互就能改变 value 的 Control。例如手机上的重力感应器。即使在手机完全静止时，重力值也是波动起伏的。另一个例子是从 HMD 读取的 orientation。

如果一个 Control 被标记为 noisy，它意味着：

1. Control 不被考虑为 interactive rebinding。InputActionRebindingExceptions.RebindingOperation 默认忽略这个 Control（可以使用 WithoutIgnoringNoisyControls 绕过这个）
2. 如果在 Project Settings 开启，system 执行额外的 event filtering，然后调用 InputDevice.MakeCurrent。如果 Device 的 input event 没有包含 non-noisy Control 上的 state change，则 Device 将不会因这个 event 称为 current。这避免了 plugged in 的 PS4 控制器 总是保持为 current gamepad（Gamepad.current），因为他的 sensors 总是想 system feeding 数据。
3. 当 Application 失去焦点，并且 Device 因此被重置，noisy Controls 的 state 将被保留。这确保 sensor 读取者保留它们最后的值，而不是被重置为默认状态。

如果任何 Control 是 noisy，则 Device 自身被标记为 noisy。

和 Input System 为当前所有 Devices 保持的 input state，default state 一起，它还维护一个 noise mask，在其中只有不是 noise 的 state 的 bits 被设置。这可以被用于非常有效地 mask out input 中的 noise。

## Synthetic Controls

一个 syncthetic Control 是一个不响应实际物理 device 上的 control 的 Control。这些 Controls 合成其他实际物理 Control 的 input，并以不同的方式呈现（例如，它允许你将一个单独的方向 stick 当作 buttons）。

InputControl.synthetic 标识这个 control 是合成的。

System 在 interactive rebinding 中考虑 synthetic Controls，但总是更倾向 non-synthetic Controls。如果一个 synthetic 和一个 non-synthetic Control 同时是可能的匹配，non-synthetic Control 优先。
