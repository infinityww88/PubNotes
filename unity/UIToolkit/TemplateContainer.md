# 加载其他 UXML 到当前 UXML

VisuallTreeAsset.Instainte() 返回 TemplateContainer 容器，包含 UXML 里所有元素在它下面。

VisualElement 自动创建一个 TemplateContainer 元素，TemplateContainer 就是个普通的 VE 元素，只是自动创建的而已，但是它的 style 无法在 UIBuilder 中设置，因为 UIBuilder 里面之后 UXML 声明的元素。可以在 C# 脚本里面设置它的样式。

它的默认 position 是 relative。而 absolute 是相对父元素定位，而不是相对 screen。如果 UXML 的 root 想创建一个相对于 screen 的对话框，脱离 flex 流，那还需要将加载后自动创建的 TemplateContainer 设置为 absolute，否则 TemplateContainer 是 relative 的，直接添加到 UIDocument.root 会加载到 root UXML 的下面。

UIDocument ------

Template Container 就是普通的 VE，只是自动创建，但是就是 style 无法在 UIBuilder 指定样式
默认 position 时 relative
包括 UIDocument root 也是 Container，UXML root 也是在 container 之下
因此默认将 子 UXML 插入 UIDocument root 之下，是以 relative 插入了以元素，而元素 的 position absolute 是相对于 父元素进行定位，而不是 screen，因此插入总是在 main root 所有元素之下
可直接 style container，甚至 style root container，还可以将 container 的子元素添加到 root container 之下，类似于 clonetree
VE.Children 返回 IEnumerable，使用 LINQ 的 First() 得到它唯一的 child 元素