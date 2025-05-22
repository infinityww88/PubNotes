虽然所有操作本质上运行机制相同，但其对绑定控件数值变化的响应方式存在差异。

最直接的行为类型是直通模式（PassThrough），该模式不预设任何数值变化规律，只是简单地在每次数值变动时触发操作。除非绑定设置了交互规则，否则直通操作不会使用"已启动"或"已取消"状态。直通模式最适合需要从任意数量控件获取输入，且无需操作端进行复杂处理、仅需透传所有输入的场景。

```C#
// An action that triggers every time any button on the gamepad is
// pressed or released.
var action = new InputAction(
    type: InputActionType.PassThrough,
    binding: "<Gamepad>/<Button>");

action.performed += ctx =>
{
    var button = (ButtonControl)ctx.control;
    if (button.wasPressedThisFrame)
    Debug.Log($"Button  was pressed");
    else if (button.wasReleasedThisFrame)
    Debug.Log($"Button  was released");
    // NOTE: We may get calls here in which neither the if nor the else
    //       clause are true here. A button like the gamepad left and right
    //       triggers, for example, do not just have a binary on/off state
    //       but rather a [0..1] value range.
};
action.Enable();
```

请注意，直通操作不会对输入进行任何消歧处理——这使得它们非常适合单纯转发所有连接控件的输入信号，但在需要从多个连接控件中生成单一输入时则不是理想选择。

另外两种行为类型分别是按钮(Button)和数值(Value)。

数值型操作会在输入值偏离默认值时立即启动(started)，随后即刻执行(performed)。此后只要输入值发生变化就会重复执行，除非输入值回归默认值——此时操作将取消(canceled)。

与按钮型和直通型操作不同，数值型操作在启用后的首次输入更新时会执行"初始状态检查"：检测所有绑定控件是否已处于激活状态(即非默认值)。若满足条件，操作将立即启动并执行。实际应用中，比如当数值操作绑定到游戏手柄左摇杆且摇杆已偏离静止位置时，操作会立即触发，而无需等待摇杆微调。

相比之下，按钮型和直通型操作不执行此类初始状态检查。以按钮为例，如果在操作启用时按钮已处于按下状态，则必须先将按钮释放后再次按下才能触发操作。

```C#
// An action that starts when the left stick on the gamepad is actuated
// and stops when the stick is released.
var action = new InputAction(
    type: InputActionType.Value,
    binding: "<Gamepad>/leftStick");
action.started += ctx =>
{
    Debug.Log("--- Stick Starts ---");
};

action.performed += ctx =>
{
    Debug.Log("Stick Value: " + ctx.ReadValue<Vector2D>();
};
action.canceled += ctx =>
{
    Debug.Log("# Stick Released");
};
action.Enable();
```

按钮型操作本质上与数值型操作运行机制相同，只是不执行初始状态检查。

按钮型和数值型与直通型最后一个关键区别在于：当多个操作绑定到同一控件时，前两者会执行"输入消歧"处理。直通型则完全不关心绑定控件的数量——无论输入源有多少，它都会原样透传所有输入信号。

相比之下，当按钮型和数值型操作同时接收到多个输入源时，其处理方式会有所不同。请注意，这种情况仅发生在以下两种绑定场景：

- 单个绑定解析出多个控件（如"*/"通配符）；
- 多个绑定同时指向同一操作且处于激活状态。若操作仅绑定单个控件，则会自动跳过消歧流程。
消歧处理的具体逻辑如下：

当操作尚未启动时，会响应首个非默认值的输入信号，并开始追踪该信号源；

在操作执行过程中，若接收到来自当前追踪控件之外的输入，系统会比较新输入与当前输入的强度值（参见EvaluateMagnitude()）；
若新输入强度更高，操作将切换追踪至该信号源。

值得注意的是，该流程具有双向性：当当前追踪控件的输入强度低于其他已激活的绑定控件时，操作会自动切换至强度更高的信号源。
简而言之，绑定多个控件的按钮型或数值型操作，始终会追踪输入强度最高的控件。

- Button

  作为触发器 trigger 的 action。

  按钮型操作设有明确的触发点（对应Performed状态）。触发完成后，操作将返回等待状态，准备响应下一次触发。

  需注意：按钮型操作仍可能使用Started状态，且不一定会立即响应输入。例如当采用HoldInteraction时，绑定按钮一旦超过按压阈值就会启动操作，但必须持续按压达到设定时长（duration）才会真正触发。

  无论操作设置为何种类型，皆可通过IsPressed()、WasPressedThisFrame()和WasReleasedThisFrame()方法检测其当前/当帧的按压或释放状态。

  ```C#
  action.IsPressed(); // 是否处于持续按下的状态
  action.WasPressedThisFrame(); // 是否是本帧按下
  action.WasPressedThisFrame(); // 是否是本帧释放
  ```

- PassThrough

  一种无特定行为类型的操作，仅作为绑定控件数值变化的简单透传通道。实际上，这类操作将动作从单一数值生成器转变为纯粹的输入"接收器"。

  该机制与数值型操作有相似之处，但存在两个关键差异：

  其一，当同时绑定多个控件时，该操作不会执行任何消歧处理。例如，若操作同时绑定游戏手柄的左摇杆(0.5,0.5)和右摇杆(0.25,0.25)，则会先后执行两次操作——先输出(0.5,0.5)再输出(0.25,0.25)。这与数值型操作不同：后者在左摇杆触发(0.5,0.5)后，右摇杆的输入若未超过左摇杆的强度值就会被忽略。

  其二，该操作仅使用Performed状态，任何数值变化都会触发该状态（无论具体数值如何）。而数值型操作会在偏离默认值时触发Started状态，并在回归默认值时触发Canceled状态。

  需注意：直通操作仍可能因非设备输入因素被取消（此时会调用canceled）。典型场景包括：操作被禁用（参见Disable()）、失去焦点（参见backgroundBehavior）或设备连接重置（参见ResetDevice(InputDevice, bool)）等情况。

  另外，对直通操作调用ReadValue()通常效果有限，因其仅返回最后传入控件的数值。建议通过监听performed回调来获取所有数值变化通知。若无需此功能，通常直接使用数值型操作更为合适。

- Value

  一种从连接源读取单一数值的操作。当多个绑定同时激活时，会执行消歧处理（参见../manual/ActionBindings.html#conflicting-inputs）以实时检测当前贡献值最高的输入源。

  数值型操作的工作流程如下：

  - 当绑定控件的数值变为非默认值时，操作立即启动（Started）并执行（Performed）。例如，若操作绑定左摇杆且摇杆从(0,0)移动到(0.5,0.5)，则触发启动和执行。

  启动后，只要数值变化为非默认值就会持续执行。延续上述例子：

  - 摇杆移至(0.75,0.75)时执行一次
  - 继续移至(1,1)时再次执行
  - 当控件数值恢复默认值时，操作取消（Canceled）。即若摇杆归位至(0,0)，将触发取消状态。