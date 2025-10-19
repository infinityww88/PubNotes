# UltEvent

## Quick Start

```C#
[SerializeField]
private UltEvents.UltEvent _MyEvent;
```

1. 在脚本中声明一个 SerializeField 字段来创建 UltEvent
2. 一旦你声明了 event，它将会在 Inspector 中显示，你可以配置它
3. 要触发 event 的执行，只需调用 _MyEvent.Invoke()

存在很多预制 Event 脚本，它暴露 MonoBehavior events，例如 Awake，Update，等等

### Serializable Event System Feature Comparison	

| Features | UnityEvent | UltEvent |
| --- | --- | --- |
| Persistent listeners (serialized) | * | * |
| Dynamic listeners (non-serialized) | * | * |
| Parameter types: bool, int, float, string, UnityEngine.Object | * | * |
| Parameter types: Enum (regular and flags), Vector (2, 3, 4), Quaternion, Rect, Color, Color32 | | * |
| Unlimited parameter count | | * |
| Allows methods with non-void return types | | * |
| Use values returned from earlier calls as parameters | | * |
| Public methods | * | * |
| Non-public methods | | * |
| Static methods | | * |
| Source code included | | * |
| Disable specific listeners entirely or just in Edit Mode | * | |
||||

UnityEvents 只支持 0 或 1 个参数，而 UltEvents 可以调用任何数量参数的方法。

UnityEvents 对每个持久化监听器有一个 dropdown 菜单来选择

### Performance

- UltEvents 和 UnityEvents 相比常规 C# Delegates 例如 System.Action 对性能有明显的负面影响。如果你只想要一个 event 在 code 中使用，而不想在 Inspector 中设置它，或者保存为 scene/prefab 的一部分，则你应该简单地使用常规的 delegates。
- 当不带参数调用，UltEvents 比 UnityEvents 略快一些
- 当使用一个参数调用，UnityEvents UnityEvents 比 UltEvents 略快
- UnityEvents 不能调用超过一个参数的方法

## Creating and Triggering

你可以在自己的脚本中声明并调用一个 UltEvent，或者使用一个预制的 Event 脚本组件。

### Declaring an Event in a Script

你可以像任何其他 serialized field 一样声明一个 UltEvent，并显示在 inspector 中：

```C#
// Public field:
public UltEvents.UltEvent myEvent;

// Private field with the [SerializeField] attribute:
[SerializeField]
private UltEvents.UltEvent _MyEvent;
```

你需要调用 myEvent.Invoke() 在你想要时间触发事件：

### Invocation Exceptions

- 正常 UltEvent.Invoke 方法不包含异常处理。任何异常都会想正常那样被从调用者传递出
- UltEvent.InvokeSafe 方法将会自动捕获异常并打印任何异常
- 如果在脚本顶部包含 using UltEvents，可以 UltEventUtils.InvokeX 扩展方法，如果 event 是 null 它不做任何事，以避免抛出 NullReferenceException。这在运行时调用 AddComponent 很有用因为 event 字段将会是 null，不想当你在 Unity Editor 中添加组件时一样，后者将会自动创建一个新的 event object。

### Premade Event Scripts

这个插件包含依稀包含 UltEvents 的脚本，可以被各种 MonoBehavior event message 触发：

![PremadeEventScripts](../Image/PremadeEventScripts.png)

- CollisionEvents2D
  - OnCollisionEnter2D
  - OnCollisionStay2D
  - OnCollisionExit2D
- CollisionEvents3D
  - OnCollisionEnter
  - OnCollisionStay
  - OnCollisionExit
- LifeCycleEvents
  - Awake
  - Start
  - OnEnable
  - OnDisable
  - OnDestroy
- TriggerEvents2D
  - OnTriggerEnter2D
  - OnTriggerStay2D
  - OnTriggerExit2D
- TriggerEvents3D
  - OnTriggerEnter
  - OnTriggerStay
  - OnTriggerExit
- UpdateEvents
  - Update
  - LateUpdate
  - FixedUpdate

### UltEventHolder

UltEventHolder 脚本和预置的 Event Scripts 类似，除了它只有一个不被任何东西触发的 event。这个脚本的一个用途是接收一个来自 UI element 的重定向的 UnityEvent，使得你可以使用 UltEvents 的改进特性。

DelayedUltEventHolder 脚本可以被类似地使用，来强制一个事件执行的延迟。

![button-click-redirect](../Image/button-click-redirect.png)

## Inspector Configuration

一个 UltEvent 有两个 listeners 集合：

- 在 Inspector 中配置的持久化监听器
- 使用 code 在运行时添加的动态监听器

你可以使用 [+] 按钮添加一个持久化监听器，或者从 Hierarchy window 或 Project window 拖放一个 object 到 event 上。

如果一个 event 有多个 calls，你可以拖放改变它们的执行顺序。执行从 top 开始向下遍历整个 list。

### Configuring a Function Call

![labelled-inspector](../Image/labelled-inspector.png)


每个持久化监听器有一个 target object（对于实例方法）或者一个类型引用（对于静态方法），以及一个 target method

如果一个参数一个 event 的参数，或者一个更早 listener 的返回类型，它将会显式一个 [∞] 按钮，将会连接 parameter 以使用那个 value，而不是使你在常规的 field 输入一个 value。

### Context Menus

右键单击 event hander 以打开一个 context menu：

![event-context-menu](../Image/event-context-menu.png)

| Function | Description |
| --- | --- |
| Invoke Event | 调用 UltEventBase.Invoke 来执行事件 |
| Copy Event | 复制 event 到剪贴板 |
| Paste Event (Overwrite) | 使用剪贴板上次复制的 event 覆盖当前 event |
| Paste Listener (New)	| 将剪贴板中复制的 event 添加到末尾。Ctrl + Shift + V |
| Clear Event | 调用 UltEventBase.Clear 移除 event 上的所有监听器 |
| Log Description | 在 Console 中打印事件和它的监听器的描述 |
| Display Options | 一个 sub-menu，包含各种设置 |
|||

可以右键点击一个 persistent 监听器来打开一个 context menu：

![listener-context-menu](../Image/listener-context-menu.png)

| Function | Description |
| --- | --- |
| Duplicate Array Element | 添加一个相同的 listener 在这个 listener 后面. Ctrl + C 然后 Ctrl + Shift + V |
| Delete Array Element | 从 event 移除选择的 listener。Delete key |
| Copy Listener | 复制选择 listener。Ctrl + C | 
| Paste Listener (Overwrite) | 粘贴复制的 listener。Ctrl + V |
| Display Options | 包含各种设置的 sub-menu |
|||

当你选择了一个持久化 listener，还可以使用 + key 添加一个新的 listener 在它后面。

## Advanced

## Event Parameters

标准的 UltEvent 类允许你使用预定义的 values 注册方法，但是不能让你在事件被调用时传递自定义参数。例如，你可以有一个 event，当它被调用时，在一个你在 event Inspector 设置的特定位置实例化一个 prefab。但是你不能使用来自一个 OnCollisionEnter 消息的信息使你的 event 在 collision 发生的位置实例化这个 prefab。要完成这件事，你需要使用通用版本的 UltEvent。

要使用一个 generic event type，你必须首先创建一个 serializable class，它继承自期望的 event type。例如，如果你想要一个 event 使用一个 Vector3 参数：

```C#
[Serializable]
public sealed class Vector3Event : UltEvents.UltEvent<Vector3> { }
```
然后在声明 event field 时，使用那个 event type 而不是通常的 UltEvent

```C#
[SerializeField]
private Vector3Event _MyEvent;
```

然后当你想要调用这个 event，你需要传递需要的参数：

```C#
_MyEvent.Invoke(transform.position);
_MyEvent.Invoke(Vector3.zero);
_MyEvent.Invoke(new Vector3(...));
// Etc.
```

当使用 Inspector 配置一个 event 的参数时，任何具有合适类型的方法参数将会显式一个 [∞] 按钮，它在 linked（因此它可以接收你传递进 Invoke call 的值）和 unlinked（因此你可以正常地使用 Inspector 来指定它的 value）之间切换那个参数。

如果你指定一个通常不被 UltEvents 支持的参数类型，例如 UltEvent\<Collision> 或 UltEvent\<SomeCustomClass>，你将能够选择那个参数类型的方法，而它通常不出现在 list 中。这样的参数被自动 linked，并且不能 unlinked（即手工在 Inspector 中指定参数值）。

Event 有一组 listeners，在事件发生时被依次调用，但是 UltEvent Listener list 的一个 feature 是前一个 listener 的 type 可以被作为后面 listener 的参数。

![collision-redirect](../Image/collision-redirect.png)

### Linked Return Values

如果你注册一个非空返回类型的方法，你可以使用它返回的 value 作为后面方法的参数。然和匹配之前方法返回值类型的参数将会显式一个 [∞] 用来 link event 参数。

![linked-return-value](../Image/linked-return-value.png)

### Configuring Events Using Code

你可以很容易地使用 += 运算符注册 delegates 到一个 event，就像标准的 C# delegate 一样：

```C#
_MyEvent += SomeMethod; // Existing Method.
_MyEvent += () => ...; // Lambda Expression.
```

通常这会注册 delegate 作为一个动态 listener（非序列化），然而如果你当前在 Edit Mode，它将会被注册为一个持久化 listener。

要特别指定添加一个 dynamic listener（指明不序列化），可以直接访问 dynamicCalls 字段，或者使用 static AddDynamicCall 方法，后者将会自动对 event 进行 null-check：

```C#
_MyEvent.dynamicCalls += SomeMethod;
UltEvent.AddDynamicCall(ref _MyEvent, SomeMethod);
```

### Configuring Persistent Listeners Using Code

要特别指明添加一个持久化 listener，可以创建一个新的 PersistentCall，并添加它到 UltEventBase.PersistentCalls list 中，或者调用 UltEventBase.AddPersistentCall，它返回一个 PersistentCall。

```C#
// Make the call yourself:
var call = new PersistentCall((Action<float>)SomeMethod);
_MyEvent.PersistentCalls.Add(call);

// Or let it be created for you:
var call = _MyEvent.AddPersistentCall((Action<float>)SomeMethod);
```

然后你可以配置这个 call 使用 SetArguments 或者通过直接访问 persistentArguments 数组。

```C#
call.SetArguments(2);
call.PersistentArguments[0].Float = 2;
```

所有这些 + 操作符和 Add 方法有一个相应的 - 操作符来移除 方法。
