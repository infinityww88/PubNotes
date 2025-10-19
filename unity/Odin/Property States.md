# Property States

在 3.0 版本，Odin 引入了 property state 系统，它是一个用于 drawers（以及其他挂载到 properties 的东西，例如 resolvers 和 processors）创建和暴露 named states 的方法，named states 可以在外面被查询。3.0 还添加 property query syntax 到 attribute expressions，这与 state system 是一个强大的协同作用。Property states 被包含在一个 InspectorProperty instance 的 State member 中，它是一个 PropertyState 类型。 

所有 properties 默认有 3 个硬编码的 states，因为它们被频繁地使用。它们是：

- Visible state
- Enabled state
- Expanded state。

Property 就是 Odin 修饰的可序列化对象。

Visible state 控制查询的属性的可见性。简短地说，如果 Visible state 是 false，则调用 InspectorProperty.Draw() 会几乎立即返回而不绘制任何东西。所有 groups 属性具有和 visible state 相关的默认行为：如果以 group 包含的 properties（group 在一起的 Inspector 字段）具有 false 的 visible states，则这个 group 将会切换它自己的 visible state 也是 false，这样当它所有的 children 被隐藏时，它自己也自动隐藏。

Enabled state 默认控制 property 的 GUI 是 enabled 还是 disabled。注意，单个 drawers 可以覆盖它，并且还要注意 Enabled state 从不会导致 GUI 从 disabled 切换到 enabled，只能从 enabled 切换到 disabled。很多其他的因素，例如称为 ReadOnly，可能导致一个属性的 GUI 以 Enabled state 不能影响的方式成为 disabled。当 Enabled state 是 false，在 property 的 drawer chain 绘制时调用 InspectorProperty.Draw() 将会设置 GUI.enabled 为 false。

Expanded state 控制 property 是否在 UI 展开，使 property drawer 在它们的实现中使用这个状态。所有内置的 Odin drawers 使用这个 state 来控制一个 property 是否展开，而且建议你在编写自己的 drawers 时也使用这个 state，而不是使用一个 local drawer 字段来控制它。不想 Visible 和 Enabled state，Expanded state 是持久化的。如果被修改，新的 value 将会通过 PersistentContext cache 在 reloads 之间持久化。

不是所有 properties 都使用所有这些 states！

例如一个简单的 string property，将会有一个 Expanded state，但是因为它的 drawers 都不使用这个 state，改变这个 state 对 string 如何绘制没有影响。

现在来看一个简单使用 state system 的属性声明的例子：一个 enum 控制一个 list 的 Expanded state，基于它是否具有一个特定 flag。这个例子使用 Odin attribute expressions 特性 的 property query syntax，#(exampleList)，来方便地使用 list 成员的 InspectorProperty instance 并修改它的 state。

```C#
// It is generally recommended to use the OnStateUpdate attribute to control the state of properties
[OnStateUpdate("@#(exampleList).State.Expanded = $value.HasFlag(ExampleEnum.UseStringList)")]
public ExampleEnum exampleEnum;

public List<string> exampleList;

[Flags]
public enum ExampleEnum
{
    None,
    UseStringList = 1 << 0,
    // ...
}
```

![state-system-example-1](../Image/state-system-example-1.gif)

还可以创建自定义 states。任何想要创建一个 custom state 的 drawer，processor 或 resolver 需要调用一次 InspectorProperty.State.Create() 来创建 custom state。之后，custom state 可以通过 InspectorProperty.State.Get() and InspectorProperty.State.Set() 访问和修改。

例如，TabGroup 属性的 drawer 暴露 3 个自定义 states：CurrentTabName, CurrentTabIndex and TabCount，允许当前选择的 Tab 查询和修改，就像下面的例子：

```C#
// All groups silently have "#" prepended to their path identifier to avoid naming conflicts with members.
// Thus, the "Tabs" group is accessed via the "#(#Tabs)" syntax.
[OnStateUpdate("@#(#Tabs).State.Set<int>(\"CurrentTabIndex\", $value + 1)")]
[PropertyRange(1, "@#(#Tabs).State.Get<int>(\"TabCount\")")]
public int selectedTab = 1;

[TabGroup("Tabs", "Tab 1")]
public string exampleString1;

[TabGroup("Tabs", "Tab 2")]
public string exampleString2;

[TabGroup("Tabs", "Tab 3")]
public string exampleString3;
```

![state-system-example-2](../Image/state-system-example-2.gif)
