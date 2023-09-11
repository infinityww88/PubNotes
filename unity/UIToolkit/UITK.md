# UI Toolkit

Unity 倾向于 UITK 框架，UGUI 只用于向后兼容，主要资源都投入到 UITK 中。除了自定义 shader 和 world GUI，其他方面 UITK 都可以完全替换 UGUI 甚至提供更多的功能。因此除非要自定义 shader 或使用 world GUI，否则都使用 UITK。

visualelement.resolvestyle 存放 ui 元素最终解析的样式值，类似 web 中的 computed style，在这里读取最终的样式值。样式不再是 VisualElement.style 中的 StyleLength，StyleColor，StyleEnum 这样的类型，而是 float，color 这样的具体类型。StyleLength 这样的类型不仅可以表示数字，还可以表示关键字，它用于存储解析前为样式设定的 value。

为 VisualElement.style 设定 style 时，可以直接赋值，不必先转换为 StyleXXX 类型，如果那个 StyleXXX 可以包含要设定的值的类型，它应该具有那个类型的隐私转换运算符。

用 visualelement.resolvestyle.height，visualelement.resolvestyle.top 读取最终元素的样式属性，它们都是 float。

```text
But yes, most of these won't be computed on the first frame after creating an element so you have to wait until it has already computed its size and position by registering for the GeometryChangeEvent (on the element you want to read the size from).
```

混合使用时，UITK 和 UGUI 的元素可能相互覆盖，影响事件分发。设置 Canvas.order 和 UIElement.order 设置渲染顺序，order 更大的后渲染，并遮挡下面的元素（事件）。

RectTransform 是 Transform 的子类。Transform 表示一个点，RectTransform 表示一个矩形，因此它在 position 基础上，添加了 size 相关的属性（表示矩形）。

Canvas 坐标系，从左到右，从下到上。

在 Canvas 中，RectTransform.position 不再像普通 Scene 3D GameObject 那样表示 GameObject 的 world position。它表示的是 UI 元素在 Canvas 坐标系中的绝对坐标，不相对任何父元素，就是相对 Canvas 坐标系。它的 1 个单位就是 Canvas 一个左边单位的意义，真实意义取决于 Canvas 的设置：

- 对于 Screen Overlay，如果 Canvas 没有缩放，一个 Canvas 单位就对应屏幕的一个像素，则 RectTransform UI 元素的 position 就是屏幕坐标。如果 Canvas 缩放，坐标单位也随之缩放（一个坐标单位对应相应的像素数）
- 对于 Screen Camera 或 World Canvas，因为 Canvas 不是相对于屏幕的，因此需要手动设置 Canvas 的分辨率：

  - Screen Camera：提供一个参考分辨率，然后映射到真实屏幕上，最终还是一个坐标单位对应特定数量的像素。RectTransform.position 的单位就是这个
  - World Canvas：使用 world 坐标，此时就和 3D GameObject 坐标单位大小一样了。

RectTransform 中的相对坐标，例如 anchorPosition 的单位和 position 的单位意义一样，只是它是相对于 anchor 矩形的。

另外，RectTransform.position 定义的是元素的 pivot 的位置，而不是左上角或左下角。

RectTransform.position 是元素相对于 Canvas 的绝对左边值，不相对任何其他元素，类似 UITK 中的绝对定位（但是 UITK 中的绝对定位也是相对于 Parent，只是从布局流中移除）。因此可以用它实现一些绝对定位的效果，类似实现自己的布局系统。例如可以混用 UITK 和 UGUI，使用一个 VisualElement placeholder 元素在 UITK 的布局系统，获得定位和布局信息，然后将 UGUI 的元素手工对齐到 VisualElement 的位置，这需要 UITK 和 UGUI 之间的坐标转换。或者在 UGUI 中实现 UI 元素对齐，不管两个元素各自嵌套在哪些元素中，只要让它们的 RectTransform.position 相等，就能将它们对齐到一起。

UITK VisualElement.LocalToWorld 中的 world 指的是 panel，不是 3D world。如果 UIDocument 没有缩放，就是屏幕坐标，否则坐标也随之相应缩放。LocalToWorld 将元素局部坐标系中的位置转换为 panel 坐标。

UITK 和 UGUI 之间的坐标转换通过屏幕坐标系进行：

```text
UITK 坐标 <-> UITK scale <-> screen position <-> Canvas scale <-> Canvas 坐标
```

注意，UITK panel 坐标系的 Y 轴和 Canvas 坐标系的 Y 轴是相反的，前者从左上角向下，后者从左下角向上。
