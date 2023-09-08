# Template UXML

当前 UIBuilder 只支持导出 Template，还不支持导入 Template。

使用 Template 还必须显式编辑 UXML 文件。

另一种将 UXML 作为模板使用的方式是，在 C# 中引用 UXML 资源为 VisualTreeAsset。然后在代码中需要创建新实例的地方，调用 visualTreeAsset.CloneTree()。

CloneTree 创建 UXML 文件描述的 visual tree 的副本。如果不指定 target visual element，则创建的是独立的副本，否则添加到 target visual element 中。

注意 VisualTreeAsset.CloneTree 创建的子树包装在一个 TemplateContainer 中。TemplateContainer 也是一个普通的 VisualElement 元素，但是是自动创建的，无法在 UIBuilder 指定它的样式。通常不需要担心它，但是有时需要考虑这个 container 元素：

- 它的 position 是 relative 的，如果我们原本是在里面创建了一个 position=absolute 的 visual tree（例如对话框）准备添加到 UIDocument 的 root 中使用，那这就会导致 Template Container 以 relative 的方式添加的 root 中，而里面的元素相对于 Container absolute 定位。
- 如果我们需要引用里面的 root 元素，例如放在 pool 中管理

对这些场景，可以创建独立的 TemplateContainer（off-screen），从 TemplateContainer 中取出元素，显式添加到 target 上。

注意只有 VisualTreeAsset 有 CloneTree 方法，VisualElement 没有任何 Clone 方法。

另外这样使用的 VisualTreeAsset 不会自动加载它里面的样式表。当把 VisualTreeAsset 作为 UIDocument 的 source asset 加载时，UIDocument 会加载 VisualTreeAsset 里面的样式表。为此，需要显式为 VisualTreeAsset 加载样式表。有两种方式：

- 在 C# 中引用样式表为 StyleSheet 资源，然后将它添加到克隆出的 VisualTreeAsset 上：

  ```C#
  visualTree.styleSheets.Add(styleSheet)
  ```

- 在使用 UXML 的 root UXML 中添加引用的 USS 样式表。一个 UXML 可以引用多个 USS 样式表
