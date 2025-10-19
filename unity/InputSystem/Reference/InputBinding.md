# Input Bindings

一个 InputBinding 代表一个 Action 和一个或多个 Controls 之间的连接，Control 通过 Control path 指定。

一个 Action 可以有任意数量的 Binding 指向它。Multiple Binding 可以引用同一个 Control。

每个 Binding 有以下属性：

- path

  Control Path 标识 control，这个 Action 从这里接受输入。例如 <Gamepad>/leftStick

- overridePath

  覆盖 path 的 Control path。不像 path，overridePath 不是持久的，因此你可以使用非破坏性地覆盖一个 Binding 上的 path。如果它设置为 non-null，则它覆盖 path 并生效。要获得当前生效的 path（path 或 overridePath），查询 effectivePath 属性

- action

  Action 的 name 或 Id，Binding 应该 trigger。可以为空，非大小写敏感，例如 “fire”

- groups

  分号分割的 Binding groups，Binding 所属的 groups。可以为空，但是通常用于 Control Schemes。非大小写敏感。例如 “Keyboard&Mouse; Gamepad”

- interactions

  分号分割的 Interactions 列表，应用到这个 Binding 的输入。Unity 将应用到 Action 自身的 Interactions 追加到这个列表。非大小写敏感。例如，“slowTap;hold(duration=0.75)”

- processors

  分号分割的 Processors 列表，应用到这个 Binding 的输入。Unity 将应用到 Action 自身的 Processor 追加到这个列表。非大小写敏感。

  Binding 上的 Processors 应用到提供 values 的 Controls 的 Processors 上面。例如，如果你在 Binding 上放一个 stickDeadZone Processor，然后绑定到 <Gamepad>/leftStick，你将应用 deadzones 两次：一次来自 leftStick Control 上的 deadzone Processor，一次来自 Binding。

  例如，“invert;axisDeadzone(min=0.1,max=0.95)”

- id

- name

  在 Composites Binding 中标识部分名字。

  例如 “Positive”

- isComposite：Binding 是否是一个 Composite

- isPartOfComposite：Binding 是否是一个 Composite 的部分

要查询一个特定 Action 的 Binding，你可以使用 InputAction.bindings。要查询一个 ActionMap 中所有 Actinos 的 Binding 的 flat 列表，使用 InputActionMap.bindings。

## Composite Bindings

有时你可能想要使用一些 Controls 共同模拟一个不同类型的 Control。最常见的例子是使用键盘上 W A S D keys 来形成一个 2D Vector Control，等价 mouse deltas 或 gamepad sticks。另一个例子是使用两个 keys 来形成一个 1D axis 等价于 scroll axis。

这使用正常的 Binding 很难实现。你可以 Bind 一个 ButtonControl 到一个 action 并期望一个 Vector2，当这样做将在运行时导致一个异常，Input System 试图从一个只能提供 float 的 Control 读取一个 Vector2。

Composite Bindings（即由其他 Bindings 组成的 Bindings）可以解决这个问题。Composites 自己不直接绑定到 Controls；相反，它从子 Bindings 读取数据，然后基于那些数据合成 input。

要在 code 中创建 composites，你可以使用 AddCompositeBinding 语法：

```C#
myAction.AddCompositeBinding("Axis")
    .With("Positive", "<Gamepad>/rightTrigger")
    .With("Negative", "<Gamepad>/leftTrigger");
```

每个 Composite 有一个具有 InputBinding.isComposite = true 的 Binding，跟随一个或多个 InputBinding.isPartOfComposite = true 的 Bindings 组成。换句话说，InputActionMap.bindings 中一些连续的 entries 或 InputAction.bindings 一起形成一个 Composite。

Composite 可以具有参数，就像 Interactions 和 Processors。

myAction.AddCompositeBinding("Axis(whichSideWins=1"))

当前 Input System 开箱提供了 4 种 Composite types

- 1D-Axis

  由两个 buttons 组成的 Composite，一个在 1D axis negative 方向 pull，另一个在 positive direction。返回一个 float；

  ```C#
  myAction.AddCompositeBinding("1DAxis") // Or just "Axis"
    .With("Positive", "<Gamepad>/rightTrigger")
    .With("Negative", "<Gamepad>/leftTrigger");
  ```
  
  这个 axis Composite 有两个 part bindings：

  - positive：Button Type，在 positive 方向 pull，朝向 maxValue
  - negative：Button Type，在 nagative 方向 pull，朝向 minValue
  
  你可以在一个 axis Composite 设置一下参数：

  - whichSideWins：如果 positive 和 negative 都 actuated 会发生什么
  - minValue：如果 negative side actuated（最大控制） 返回的值，默认 -1
  - maxValue：如果 positive side actuated（最大控制） 返回的值，默认 1

  如果 positive 和 negative side 都是 actuated，axis Composite 的最终值依赖于 whichSideWin 参数：

  - Neither：返回 minValue 和 maxValue 的中间值，对于默认设置，返回0.
  - Positive：positive side 优先，Composite 返回 maxValue
  - Negative：negative side 优先，Composite 返回 minValue

- 2D-Vector

  一个表示 4-way button 的 Composite，例如 gamepads 上的 D-pad。每个 button 代表一个主要方向。返回一个 Vector2

  主要用于表示 上下左右 controls，例如键盘上的 WASD。

  ```C#
  myAction.AddCompositeBinding("2DVector") // Or "Dpad"
    .With("Up", "<Keyboard>/w")
    .With("Down", "<Keyboard>/s")
    .With("Left", "<Keyboard>/a")
    .With("Right", "<Keyboard>/d");

  // To set mode (2=analog, 1=digital, 0=digitalNormalized):
  myAction.AddCompositeBinding("2DVector(mode=2)")
    .With("Up", "<Gamepad>/leftStick/up")
    .With("Down", "<Gamepad>/leftStick/down")
    .With("Left", "<Gamepad>/leftStick/left")
    .With("Right", "<Gamepad>/leftStick/right");
  ```

  2D Vector Composite 有 4 个 part Bindings。

  - up：Button type，表示 (0, 1) +Y
  - down：Button type，表示（0, -1) -Y
  - left：Button type，表示（-1, 0）-X
  - right：Button type，表示（1, 0）+X

  除此以外，你可以在一个 2D vector Composite 上设置以下参数

  - mode
  
    将 inputs 作为 digital 还是 analog Control

    - Mode.DigitalNormalized（默认）
    
      inputs 被作为 buttons（小于 defaultButtonPressPoint 关闭，大于或等于 开启）。每个输入根据 button 是否按下返回 0 或 1。

      从 up/down/left/right part 返回的 vector 被 normalized。结果是一个菱形 2D 输入范围。
    
    - Mode.Digital
    
      和上面一样，只是返回的 vector 不标准化
    
    - Mode.Analog

      输入被当做 analog（连续的 float 值）

- Button with One Modifier

  按下 button 和 modifier button（例如 Shift + Space）触发 Action 的 Composite。Button 可以在任何 device 上。可以是 toggle buttons 或 full-range buttons 例如 gamepad triggers。返回一个 float。

  ```C#
  myAction.AddCompositeBinding("ButtonWithOneModifier")
    .With("Button", "<Keyboard>/1")
    .With("Modifier", "<Keyboard>/leftCtrl")
    .With("Modifier", "<Keyboard>/rightCtrl");
  ```

  button with one modifier Composite 具有两个 part Bindings，没有参数。

  - modifier：Button type
  - button：Button type

- Button with Two Modifiers

  Ctrl+Shift+1

  Buttons 可以在任何设备上，可以是 toggle buttons，或者 full-range buttons 就像 gamepad triggers。返回 float。

  ```C#
  myAction.AddCompositeBinding("ButtonWithTwoModifiers")
    .With("Button", "<Keyboard>/1")
    .With("Modifier1", "<Keyboard>/leftCtrl")
    .With("Modifier1", "<Keyboard>/rightCtrl")
    .With("Modifier2", "<Keyboard>/leftShift")
    .With("Modifier2", "<Keyboard>/rightShift");
  ```

  button with one modifier Composite 具有三个 part Bindings，没有参数。

  - modifier1：Button type
  - modifier2：Button type
  - button：Button type

- Writing custom Composites

  你可以定义新的 Composites 类型，使用 API 注册它们。

  基于 InputBindingComposites<TValue> 创建一个新的 class。

  新创建的 Composite 将会出现在 editor UI 上，你可以在 scripts 中使用它。

  要为 Composite 定义自定义参数，使用 InputParameterEditor<TObject>

## Binding resolution

当 Input System 第一次访问绑定到 Action 的 Controls，Action 解析它的 Bindings 来匹配它们到现有设备上的 Controls。在这个过程中，Acitons 为每个 Action bindings 的 Binding path 调用 InputSystem.FindControls<>()（如果存在的话，过滤赋予 InputActionMap 的 devices）。这创建了一个 resolved Controls，其现在绑定到 Action。

一个 Binding Path 可以匹配多个 Controls：

- 一个特定 Device path 例如 <DualShockGamepad>/buttonEast 匹配一个 PlayStation controller 上的 Circle button。如果你有多个连接的 PlayStation，它解析为这些 controllers 的每一个 Circle button
- 一个抽象 Device path 例如 <Gamepad>/buttonEast 匹配任何连接的 gamepad 上的 right action button。如果你有一个 PlayStation controller 和一个 Xbox controller 连接，它解析为 PlayerState controller 的 Circle button，和 Xbox controller 的 B button
- 一个 Binding path 还可以包含 wildcards，例如 <Gamepad>/button*。这匹配任何 gamepad 上名字以 button 开始的 任何 control，它匹配任何连接的 gamepad 的全部4个 action buttons。*/{Submit} 则匹配任何 Device 上的任何标记为 Submit 用途的 Control。

要查询一个 Action 解析到的 Controls，可以使用 InputAction.controls。即使 Action disabled，你也可以运行这个查询。

## 选择使用哪些 Devices

默认地，Actions 对 InputSystem 中出现的所有 Devices 解析它们的 Binding（即 InputSystem.devices）。例如，如果在系统中有两个 gamepads，一个 Binding <Gamepad>/buttonSouth 采用两个 gamepads 并允许从其中任何一个触发 Action。

你可以通过限制 InputActionAssets 或单独的 InputActionMaps 来覆盖这个行为到一个指定的 Devices 集合。如果你这样做，Binding resolution 将只考虑给定 Devices 的 Controls。

```C#
var actionMap = new InputActionMap();

// Restrict the action map to just the first gamepad.
actionMap.devices = new[] { Gamepad.all[0] };
```

InputUser 和 PlayerInput 自动使用这个能力。它们基于配对 player 的 Devices 自动设置 InputActionMap.devices。

## Disambiguation

如果多个 Controls 被绑定到一个 Action，Input System 监控来自每个绑定 Control 的 Input 来 feed Action。Input System 必须还定义哪个 bound controls 用于 action 的 value。例如，如果你有一个对 <Gamepad>/leftStick 的绑定，并且你有多个连接的 gamepads，InputSystem 必须决定哪个 gamepad 的摇杆为 Action 提供 input value。

驱动 Action 的 Control 称为 driving Control。Unity 在一个称为 disambiguation 的过程决定哪个 Control 当前驱动 Action。

在 disambiguation 过程中，Input System 查看绑定到 Action 上的每个 Control 的 value。如果任何 Control 的 magnitude 比当前驱动 Action 的 Control 的 magnitude 更高，则具有更高 magnitude 的 Control 将称为驱动 Action 的新 Control。

在 <Gamepad>/leftStick 绑定到多个 gamepads，驱动 Action 的 Control 是所有 gamepads 中移动得最远的 left stick。你可以查询哪个 Control 当前驱动 Action，通过在 Action callback 检查 InputAction.CallbackContext.control。

如果你不想你的 Action 来执行 disambiguation，你可以设置 Action type 为 Pass-Through。Pass-Through Actions 跳过 disambiguation，并且改变为任何 bound control 触发它们的。一个 Pass-Through Action 的 value 是任何最近改变的 bound control 的 value。

## Initial state check

Value type 的 Actions 在它们第一次 enable 时，执行一个 initial state check，来检查任何 bound control 的当前 state，并且设置 Action 的 value 为所有 bound Control 中的最高值。

Button type 的 Actions 不执行任何 initial state check，因此只有 Action enable 之后按下 button 才能触发 Action。

## Runtime rebinding

Runtime rebinding 允许你的 application 的 users 设置它们自己的 Bindings。

这允许 users 选择它们自己的 Bindings，使用 InputActionRebindingExtensions.RebindingOperation 类。在一个 Action 上调用 PerformInteractiveRebinding() 方法来创建一个 rebinding operation。这个 operation 等待 Input System 注册匹配 Action Control Type 的任何 Device 的任何 Input，然后使用 InputBinding.overridePath 为这个 Action Binding 的 Control 赋予 Control path。如果 player actuates 多个 Controls，rebinding operation 选择具有最高 magnitude 的 Control。

你必须使用 Dispose() dispose InputActionRebindingExtensions.RebindingOperation 实例，使得它们不会泄露 unmanaged memory heap 上的内存。

```C#
void RemapButtonClicked(InputAction actionToRebind)
{
    var rebindOperation = actionToRebind.PerformInteractiveRebinding().Start();
}
```

InputActionRebindingExtensions.RebindingOperation API 是高度可配置的，来匹配你的需求。例如，你可以：

- 选择期望的 Control types(WithExpectedControlType())
- 排除特定 Controls(WithControlsExcluding())
- 设置一个 Control 来取消这个 operation(WithCancelingThrough())
- 如果 Action 有多个 Bindings，选择哪些 Bindings 来应用 Operation(WithTargetBinding(), WithBindingGroup(), WithBindingMask())

PerformInteractiveRebing() 基于给定的 action 和 targeted binding 自动应用一个默认的 configurations 集合。

### Showing current Bindings

当 rebinding UIs 时，以及在程序运行时显示 on-screen 提示，让 player 知道一个 Action 当前绑定到什么（考虑任何潜在可能的 active rebinding）会很有用。你可以使用 InputBinding.effectivePath 来获得Binding 当前的 active path（overridePath 或者 path）。

为一个 action 获得一个 display string 最简单的方式是调用 InputActionRebindingExtensions.GetBindingDisplayString，它是 InputAction 的一个扩展方法。

```C#
// Get a binding string for the action as a whole. This takes into account which
// bindings are currently active and the actual controls bound to the action.
m_RebindButton.GetComponentInChildren<Text>().text = action.GetBindingDisplayString();

// Get a binding string for a specific binding on an action by index.
m_RebindButton.GetComponentInChildren<Text>().text = action.GetBindingDisplayString(1);

// Look up binding indices with GetBindingIndex.
var bindingIndex = action.GetBindingIndex(InputBinding.MaskByGroup("Gamepad"));
m_RebindButton.GetComponentInChildren<Text>().text =
    action.GetBindingDisplayString(bindingIndex);
```

你还可以使用这个方法使用 images 替换 text string。

```C#
// Call GetBindingDisplayString() such that it also returns information about the
// name of the device layout and path of the control on the device. This information
// is useful for reliably associating imagery with individual controls.
var bindingString = action.GetBindingDisplayString(out deviceLayout, out controlPath);

// If it's a gamepad, look up an icon for the control.
Sprite icon = null;
if (!string.IsNullOrEmpty(deviceLayout)
    && !string.IsNullOrEmpty(controlPath)
    && InputSystem.IsFirstLayoutBasedOnSecond(deviceLayout, "Gamepad"))
{
    switch (controlPath)
    {
        case "buttonSouth": icon = aButtonIcon; break;
        case "dpad/up": icon = dpadUpIcon; break;
        //...
    }
}

// If you have an icon, display it instead of the text.
var text = m_RebindButton.GetComponentInChildren<Text>();
var image = m_RebindButton.GetComponentInChildren<Image>();
if (icon != null)
{
    // Display icon.
    text.gameObject.SetActive(false);
    image.gameObject.SetActive(true);
    image.sprite = icon;
}
else
{
    // Display text.
    text.gameObject.SetActive(true);
    image.gameObject.SetActive(false);
    text.text = bindingString;
}
```

除此以外，每个 binding 有一个 toDisplayString 方法，你可以用于将 bindings 转换成 display strings。还有一个 control paths 的通用格式化方法，InputControlPath.ToHumanReadableString，你可以使用任意 control path strings。

注意，一个 binding 解析的 controls 在任何时间都可以改变，因此 controls 的 display strings 可能动态改变。例如，如果 player 切换当前 active keyboard layout，Keyboard 上的每个单独的 key 的 display string 可能改变。

## Control Schemes

一个 Binding 可能属于任意数量的 Binding groups。Unity 将这些 groups 存储到 InputBinding 类中，表示为一个分号分割的字符串，在 InputBinding.groups 属性。要为一个 InputActionMap 或 InputActionAsset enable 不同的 binding groups 集合，你可以使用 InputActionMap.bindingMask / InputActionAsset.bindingMask 属性。Input System 使用它来实现 grouping Bindings 的概念为 InputControlSchemes（成组 enable disable Action Bindings）。

Control Schemes 使用 Binding groups 来映射一个 InputActionMap 或 InputActionAsset 中的 Bindings 到不同类型的 Devices。PlayerInput 类使用这些为一个新加入到游戏的 player 来 enable 一个匹配的 Control Scheme，基于他们使用的 Device。

