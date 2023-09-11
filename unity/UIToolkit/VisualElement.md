# Visual Element

当前没有 z-index 支持，但是可以通过 hierarchy 控制渲染顺序：

- parent 先于 child 渲染，child 在 parent 上面
- 前面的 sibling 先于后面的 sibling 渲染，后面的 sibling 在前面的 sibling 上面

当前没有办法复制 VisualElement，更不用说 VisualElement Tree。因为这不仅涉及元素样式，还包含元素很多内部属性，以及元素上注册的回调函数。

通常复制一个 VisualElement 主要是复制它的外观，而 UITK 的外观完全通过样式定义。因此简单复一个元素的方法就是创建一个相同类型的 VisualElement，然后指定相同的样式。但是在 C# 中 VisualElement.style 是只读的，不能直接全部复制样式。唯一能赋值的是 stylesheet，而它引用的是外部 USS 资源。

因此重用 VisualElement 和 VisualElement Tree 的唯一方法就是使用外部的 UXML 和 StyleSheet。

UGUI 可以很方便地重用、赋值一个元素和 tree。但是 UGUI 不能方便地改变整体 UI 外观，实现样式主题功能，而 UITK 通过样式表则可以很方便地实现。
