# 加载其他 UXML 到当前 UXML

VisuallTreeAsset.Instainte() 返回 TemplateContainer 容器，包含 UXML 里所有元素在它下面。

它的默认 position 是 relative。而 absolute 是相对父元素定位，而不是相对 screen。如果 UXML 的 root 想创建一个相对于 screen 的对话框，脱离 flex 流，那还需要将加载后自动创建的 TemplateContainer 设置为 absolute，否则 TemplateContainer 是 relative 的，直接添加到 UIDocument.root 会加载到 root UXML 的下面。

Template Container 也是一个 VE，只是自动创建，默认样式 position=relative，shrink = 1， grow = 0。

UIDocument 的 root 也是 TemplateContainer。

因此默认将子 UXML 插入 UIDocument root 之下，是以 relative 插入了以元素，而元素的 position absolute 是相对于父元素进行定位，而不是 screen，因此插入总是在 main root 所有元素之下
可直接 style container，甚至 style root container，还可以将 container 的子元素添加到 root container 之下，类似于 clonetree

VE.Children 返回 IEnumerable，使用 LINQ 的 First() 得到它唯一的 child 元素。

```text
There are multiple options here. When instantiating from c#, VisualTreeAsset.Intantiate() will create a TemplateContainer for the elements coming from a UXML. If you don't want that container, you can use VisualTreeAsset.CloneTree(myParentElement) which will add elements from the uxml directly into the parent.

When reffering to templates from uxml, that TemplateContainer will always get created. There are 2 ways to control the style applied to that container:

1. From the parent uxml, as inline styles. In the UI Builder, select the container element and set with/height directly on it. Adding a custom class to the container and adding a css rule from uss will also work here.

2. From the instantiated template itself, from uss. For this to work, you must use a uss style sheet in your child uxml. In the ui builder, you can add it, or create a new one. From uss, add your custom styles to that container by using the :root selector. In UIToolkit, the root selector will match not the root element of the window, but the element on which the stylesheet was applied.
```

TempateContainer 与普通 VisualElement 的区别在于它上面携带了 UXML 引用的所有样式表。UITK 创建 TemplateContainer 元素时会自动查找 UXML 引用的样式表 StyleSheet，加载它们并应用到 TemplateContainer 元素上面。因此如果在 C# 中直接使用 VisualTreeAsset 创建的 TemplateContainer，是无需手工引用并应用样式表的。但是如果丢弃 TemplateContainer 不用，只使用里面的元素，将里面的元素添加到其他 tree 上，定义的样式表也随之丢弃了，除非在 C# 中手动引用样式表并应用。因此不能随意丢弃 TemplateContainer，而且在 UIBuilder 中有方法可以为它添加样式，即 :root 伪类选择器，伪类选择器选中它所在样式表应用到的根元素（不是整个 UIDocument 的根元素）。

VisualTreeAsset.CloneTree 不指定目标，返回 TemplateContainer。指定目标，则剥离 TemplateContainer，直接将里面的元素添加到目标 tree 下。
