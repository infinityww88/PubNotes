# UltEvent

UltEvents 是一个 Unity 插件，允许你容易地在 Inspector 中设置和配置持久化 event callbacks 。它用于内置的 UnityEvents 相同的目的，但是有一些超级特性并且很少的限制，以及一个改进的 Inspector 接口，只需要很少的点击来执行独立的 tasks

## Example

它使用 TriggerEvents3D 脚本，后者具有一些 UltEvents，用于响应 Unity 物理 trigger 消息。特别地，它使用 OnTriggerEnter：

![trigger-event](../Image/trigger-event.png)

## Parameter Types

UnityEvents 可以只调用带有一些参数类型的方法：bool，int，float，string，或者任何派生自 UnityEvent.Object.

UltEvents 支持所有这些类型，包含 Enum，Vector2/3/4，Quaternion，Rect，Color，Color32.

## Parameter Count

UnityEvents 只支持调用 0 或 1个参数。

UltEvents 支持任何类型的参数。

## Access Modifiers

UnityEvents 只调用 public 方法。

UltEvents 允许任何 access modifiers，包括 private 和 static。

## Return Values

UnityEvents 只能调用空返回值的方法。

UltEvents 允许任何返回类型的方法，并且允许返回值可以被用于 list 后面方法的一个参数。如果返回值没有被使用，则它简单地被忽略。

## Inspector Layout

UltEvents also have a much better Inspector interface than UnityEvents:

UltEvents 还有一个比 UnityEvents 更好的 Inspector 接口

- 收拢 event 到单一行以占据更少的屏幕空间
- 无参数函数只使用一行
- 函数参数名被显示出来。你可以看见全部方法签名而不是只有名字
- 当在 target object 上有多于一个相同类型的 component，选择一个特定 component 上的 listener
- 拖放 listeners 来重新排列它们
- keyboard shortcuts 和 context menu 允许你容易地 Copy，Paste，Add，Delete，甚至 Invoke events
- 更好地组织方法选择菜单，它可以被定制以满足你的需求
- 如果 target missing，可以快速查找一个相似名字方法的按钮
- 在 footer 显示动态 listeners（通过 code 添加的那些）

使用 UltEvents，独立的 tasks 也趋向于更少的点击：

- 相比于拖放一个 target 并添加一个新的 listener，你只需要拖放 target 到 event header 上
- 相比于选择一个 listener 然后在 footer 点击 remove button，每一个 listerner 有它自己的 remove button
- 如果将一个特定组件作为 target，它将会立即打开 method selection menu，让你直接选择 component 中的方法，而不是每次通过一个 sub-menu

