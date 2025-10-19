# Actions

Input Actions 被设计用来分离输入的逻辑意义和物理方式（输入设备上的活动，enter 键按下，鼠标左键按下等）。

相比于编写：

```C#
var look = new Vector2();

var gamepad = Gamepad.current;
if (gamepad != null)
    look = gamepad.rightStick.ReadValue();

var mouse = Mouse.current;
if (mouse != null)
    look = mouse.delta.ReadValue();
```

你可以编写输入源不可知的 code：

```C#
myControls.gameplay.look.performed +=
        context => look = context.ReadValue<Vector2>();
```

然后你可以使用 visual editor 来完成映射：

![LookActionBinding](../../../Image/LookActionBinding.png)

这可以很容易让 player 在运行时自定义绑定。

注意：Actions 是一个 game-time only code。你不能在 EditorWindow 代码中使用它们。

## Overview

API 中有3个关键的类用于 Actions。

- InputActionAsset

  一个 Asset，包含一个或多个 Action Maps，可选的，一个 Control Schemes 序列。

- InputActionMap

  一个命名的 Actions 集合。

- InputAction

  一个命名的 Action，作为 input 触发的响应

Actions 使用 InputBinding 来引用它们收集的 inputs。

每个 Action 有一个名字（InputAction.name）和一个 Id（InputAction.id）。

每个 ActionMap 有一个名字 和 Id。

## Creating Actions

- 使用 .inputactions 的专用 editor
- 嵌入到 MonoBehavior 组件，使用 MonoBehavior 的 inspector
- 从 JSON 手工 load
- 直接在 code 中创建

### Using the Action Editor

![MyGameActions](../../../Image/MyGameActions.png)

### Embedding Actions in MonoBehaviours

```C#
public MyBehavior : MonoBehaviour
{
    public InputAction fireAction;
    public InputAction lookAction;

    public InputActionMap gameplayActions;
}
```

![MyBehaviorInspector](../../../Image/MyBehaviorInspector.png)

可视化编辑器和 Action Asset editor 工作类似：

- 点击 Add（+）或 Remove（-）icon 添加或移除 Actions 或 Binding
- 要编辑 Binding，双击它们

  ![InputBindingInspector](../../../Image/InputBindingInspector.png)

- 要编辑 Actions，在一个 ActionMap 中双击它们，或点击单个 Action 属性上的齿轮 icon

  ![InputActionInspector](../../../Image/InputActionInspector.png)

- 可以右键点击 entries 打开 context menu，并且你可以拖拽它们。按住 Alt key
 并且拖拽一个 entry 来复制它

你必须手动 enable 和 disable 嵌入到 MonoBehavior 组件中的 Actions 和 Action Maps：

```C#
public class MyBehavior : MonoBehaviour
{
    // ...

    void Awake()
    {
        fireAction.performed += OnFire;
        lookAction.performed += OnLook;

        gameplayActions["fire"].performed += OnFire;
    }

    void OnEnable()
    {
        fireAction.Enable();
        lookAction.Enable();

        gameplayActions.Enable();
    }

    void OnDisable()
    {
        fireAction.Disable();
        lookAction.Disable();

        gameplayActions.Disable();
    }
}
```

Action 记录一个 输入-响应 的绑定，ActionMap 记录一组 输入-响应 绑定。

### Loading Actions from JSON

你可以从一个 Action Maps 或一个全量 InputActionAsset 格式的 Json 加载 Actions。这在运行时工作。

```C#
// Load a set of action maps from JSON.
var maps = InputActionMap.FromJson(json);

// Load an entire InputActionAsset from JSON.
var asset = InputActionAsset.FromJson(json);
```

### Creating Actions in code

可以在运行时手动创建和配置 Actions。

```C#
// Create free-standing Actions.
var lookAction = new InputAction("look", binding: "<Gamepad>/leftStick");
var moveAction = new InputAction("move", binding: "<Gamepad>/rightStick");

lookAction.AddBinding("<Mouse>/delta");
moveAction.AddCompositeBinding("Dpad")
    .With("Up", "<Keyboard>/w")
    .With("Down", "<Keyboard>/s")
    .With("Left", "<Keyboard>/a")
    .With("Right", "<Keyboard>/d");

// Create an Action Map with Actions.
var map = new InputActionMap("Gameplay");
var lookAction = map.AddAction("look");
lookAction.AddBinding("<Gamepad>/leftStick");

// Create an Action Asset.
var asset = ScriptableObject.CreateInstance<InputActionAsset>();
var gameplayMap = new InputActionMap("gameplay");
asset.AddActionMap(gameplayMap);
var lookAction = gameplayMap.AddAction("look", "<Gamepad>/leftStick");
```

## Using Actions

要是 Action 做一些事情，你必须 enable 它。或者独立的 enable Actions，或者通过 Action Maps 批量 enable 它们。在所有的场景中，第二种方法更高效。

```C#
// Enable a single action.
lookAction.Enable();

// Enable an en entire action map.
gameplayActions.Enable();
```

当你 enable 一个 Action 时，Input System 解析它的 binding。

当一个 Action 被 enable 后，你不能改变配置的特定方面，例如 Action Binding。要停止 Actions 或者 Action Maps 响应输入，调用 Disable。

当开启时，一个 Action 积极监控它绑定到的 Controls。如果绑定的 Control 改变了状态，Action 将处理这个变化。如果 Control 的变化代表了一个交互变化（Interaction Change），Action 创建一个响应。所有这些发生在 InputSystem update 逻辑中。依赖于 input setting 中选择的 update mode，这发生在每一帧发送，在 fixed update 中发生，或者手动更新，如果设置为 manual。

### Responding to Actions

一个 Action 自己不代表一个实际的对 input 的响应。相反，一个 Action 通知你一个特定类型的 input 发生了。然后你的 code 响应这个信息。

有几种方式来完成此事：

- 每个 Action 有一个 started，performed，和 canceled 回调函数
- 每个 Action Map 有一个 actionTriggered 回调函数
- Input System 有一个 InputSystem.onActionChange 回调函数
- 你可以 poll 一个 Action 的当前状态，使用 InputAction.ReadValue<>()
- InputActionTrace 可以记录发生在 Actions 上的变化

还有两个高级 high-level，更加流线化的方式来从 Actions 获取输入：使用 PlayerInput 或者 generate script code，其包装 Input Actions。

#### Action 回调

每个 Action 有一组它经历的不同的阶段来响应接收到的 Input。

- Disabled：Action 被 disable，不能再接受输入了
- Waiting：Action 被 enable，并积极等待输入
- Started：对一个 Action 的 Interaction 已经开始
- Performed：对一个 Action 的 Interaction 已经完成
- Canceled：对一个 Action 的 Interaction 已经取消

可以使用 InputAction.phase 读取一个 action 的当前阶段 phase。

Started，Performed，Canceled 阶段具有响应的回调函数

```C#
var action = new InputAction();

action.started += ctx => /* Action was started */;
action.performed += ctx => /* Action was performed */;
action.canceled += ctx => /* Action was canceled */;
```

每个 callback 接收一个 InputAction.CallbackContext 结构，它保存 context 信息，你可以用来查询 Action 的当前状态，以及读取触发这个 Action 的 Controls 的数值（InputAction.CallbackContext.ReadValue）。

这个结构体中的内容只在 callback 期间有效。尤其是，存储 context 并在 callback 之外访问它的属性是不安全的。

Callbacks 何时以及如何触发依赖于相应 Binding 上的 Interactions。如果 Binding 没有应用到它们上的 Interactions，使用 default Interaction。

#### InputActionMap.actionTriggered 回调

相比于监听独立的 actions，你可以在整个 Action Map 监听其中任何 Action 的状态变化。

```C#
var actionMap = new InputActionMap();
actionMap.AddAction("action1", "<Gamepad>/buttonSouth");
actionMap.AddAction("action2", "<Gamepad>/buttonNorth");

actionMap.actionTriggered +=
    context => { ... };
```

接收的参数和 InputAction.CallbackContext 结构相同。

Input System 为 Actions 上全部3个 callbacks 调用 InputActionMap.actionTriggered。即，你在一个 callback 中得到 started，performed，canceled。

#### InputSystem.onActionChange 回调

和 InputSystem.onDeviceChange 类似，你的 app 可以全局监听任何 action 相关的变化。

```C#
InputSystem.onActionChange +=
    (obj, change) =>
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

#### Polling Actions

相比使用 callbacks，有时候轮询一个 Action 的值可能更简单。 InputAction.ReadValue<>()：

```C#
public InputAction moveAction;
public float moveSpeed = 10.0f;
public Vector2 position;

void Start()
{
    moveAction.Enable();
}

void Update()
{
    var moveDirection = moveAction.ReadValue<Vector2>();
    position += moveDirection * moveSpeed * Time.deltaTime;
}
```

对于 button-type actions，你还可以使用 InputAction.triggered，如果这个 action 在当前 frame performed，则为 true

```C#
private InputAction buttonAction;

void Start()
{
    // Set up an action that triggers when the A button on
    // the gamepad is released.
    buttonAction = new InputAction(
        type: InputActionType.Button,
        binding: "<Gamepad>/buttonSouth",
        interactions: "press(behavior=1)");

    buttonAction.Enable();
}

void Update()
{
    if (buttonAction.triggered)
        Debug.Log("A button on gamepad was released this frame");
}
```

InputAction.triggered 绝大多数情况用于 button-type actions，但是也可以被任何 action 使用。

#### InputActionTrace

你可以追踪 Actions 来生成发生在一个特定 Actions 集合上的所有 activity 的 log。使用 InputActionTrace。它的行为和 Event 的 InputEventTrace 类似。

### Action Types

每个 Actions 是 3 个不同 Action types 中的一种。它影响 Input System 如何处理 Actions 的状态改变。默认 Action Type 是 Value。

- Value

  这是默认的 Action type。任何应该连续追踪 Control 状态变化的输入应该使用这个类型。

  Value type actions 连续监控绑定在 Action 上的所有 Controls，并选择最开发的（最受操控的）actuated 作为驱动 Action 的 Control，并在 callback 中报告那个 Control 的数值。如果一个不同的绑定 Control 变得更加显著 actuated，则这个 Control 变成驱动这个 Action 的 Control，并且 Action 开始包括来自那个 Control 的数值。这个过程称为 disambiguation（消除模棱两可）。这可以用于你想允许不同的 Controls 操控同一个 action 的情景，但同一时刻只采用一个 control 的数据。

  当 Action 初始 enable 时，它对所有绑定的 Controls 执行一个初始状态检查。如果它们中任何一个是 actuated 的，则 Action 使用当前 value 触发一个回调。

- Button

  Button 类型的 Action 和 Value 相似，但是只能绑定到 ButtonControl Controls，并且不能想 Value Action 一样执行初始状态检查。对于每次按下触发一次 Action 的 inputs 使用这个类型。初始状态检查此时没有什么用，因为当 Action enable 时，如果 button 仍然保持按下，它就可以触发一个 actions。

- Pass-Through

  绕开 Value actions 的 disambiguation 过程，并且不使用一个特定 Control 驱动 Action 的概念。相反，对任何 Control 的任何改变使用 control 的 value 触发一个 callback。这可以用于你想处理来自一个 Controls 集合的所有输入。

### Debugging Actions

使用 Input Debugger 查看当前 enabled Actions 和她们的绑定 Controls。还可以使用 InputActionVisualizer 组件（Visualizers sample）获得一个 on-screen 的实时 Action value 和 interaction state 的 visualization。

### Using Actions with multiple players

你可以使用相同的 Action definitions 用于 multiple local players 游戏。

## Terms and concepts

- Action

  一个逻辑输入，例如 Jump 或 Fire。即一个 input action，player 可以通过一个或多个 devices 触发，并运行游戏逻辑的一部分作为响应。

- Binding

  一个 Action 和 一个或多个通过 control path 表示的 Controls("<Gamepad>/leftStick") 之间的连接。在运行时，Bingding 被解析以产生 0 或 多个 Controls，然后 Input System 连接 Controls 到 Action

- Interaction

  可以在一个 Control 上被识别的一个明确的输入模式。只有当 Input System 识别这个模式时，Interaction 才会触发一个 Action。

  例如，一个 hold Interaction 需要一个 Control to be actuated，并且在触发相关 Action 之前 held 特定时间

- Processor

  Input System 应用到一个 input value 的操作。例如，一个 invert Processor invert 一个 float 值。

- Phase

  一个描述 Interaction 当前状态的枚举值。Interaction 的输入模式有一组阶段组成。

- Control Scheme

  允许你定义 Binding 的映射到不同的 Control Schemes，以及在不同的 Control Schemes 之间 switch 你的 Action Maps，来为你的 Actions 开启不同的 Binding 子集。

  Control Schemes 可以关联一个 Devcie types，使得 game 可以在发现那个设备的 Device 时自动为 player 开启绑定映射。

- Action Map

  一个命名的 Actions 集合。你可以同时 enable 或 disable 一个 action map 中的所有 Actions，因此用它可以按照所在的相关上下文将 Actions 收集到一组，一起控制

- Action Asset

  包含一个或多个 Action Maps，以及可选地，一个 Control Schemes 序列（Gamepad，keyboard&mouse，touch 等）。每个 Control Schemes 一个 Action Maps。
