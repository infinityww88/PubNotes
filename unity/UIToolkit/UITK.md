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


UITK 支持运行时动态图集，UGUI 只支持静态图集。图集是将一组小的 textures 合并到一张大 texture，使得使用这些 textures UI 在一个 drawcall 中被绘制，提高渲染效率。类似 dynamic mesh 合并，也类似 UITK 的动态文本字体图集。可以设置一组过滤规则，指定参与合并到图集的 textures。

UITK 支持抗击锯齿， UGUI 不支持。

UITK 支持全局样式修改，UGUI 如果没有 Prefab，需要单独修改界面中的每个 UI 元素。

UITK 支持矢量图，在任何分辨率上都能保证高清晰度。

UITK 支持圆角、边框、颜色，不必创建 texture，减少内存。

UITK 支持 CSS 过渡动画，UGUI 则需要使用 DoTween 之类的插件做过渡动画。

每个 PanelSetting 实例不会 batch 到一起，但是多个 Visual Elements 和多个 UI Documents 可以，只要它们属于同一个 PanelSettings。

UITK 主要的渲染策略目标是最小化绘制 UI 的 batch drawcall。相比 UGUI 提供定制 UI shader 的灵活性，UITK 有一个 uber-shader 用于整个 UI。通过集成 Text Mesh Pro（TextCore），相同的 shader 还可以绘制 text，因此文本和图片可以在一个 draw call 被绘制（图文混排）。

UIToolkit 同时支持 Static Sprite Atlas 和 Dynamic Atlas（每个 PanelSettings 一个大的 texture）。Dynamic Atlas 随着 elements 添加而被填充，它的一些属性可以在 Panel 的 Dynamic Atlas Settings 中设置。

UITK shader 有 8 个 slots，其可以动态绑定（例如一个 dynamic atlas，一个 sprite atlas，多个 single textures）。在 2022.1 之后，font atlas textures 也可以是 dynamic slots 的一部分，而之前只有一个 font textures slot。

UITK 不需要合并 geometries 来开启 batching。相反，vertices/indices 的 pages 预先分配，并且这些 pages 的 ranges 按照每个元素的需要进行分配。这允许 geometry 在 GPU 中是连续的，以允许一次绘制多个元素。当一个元素变化时，我们只需要更新那个元素的 range，因此我们不需要重新合并 geometry。

Additionally one can use the UsageHints on specific elements to enable some transformations be done on the GPU directly (like moving vertices).

We know all of this information isn't properly documented, I expect our documentation be updated before end of year about this.

In pratice though, any non-trivial UI will actually incur more than 1 draw calls, because:
- the geometry extends the maximum size for a specific page
- using UsageHints presents a tradeoff between CPU cost and batch breaks
- usage of masks changes the stencil buffer which leads to batch breaks

But in practice what we observe is that keeping the same material and just drawing a different range with a few different settings is less expensive that reconfiguring the whole GPU state.

## UsageHints

Offers a set of values that describe the intended usage patterns of a specific VisualElement.

- None

  No particular hints applicable.

- DynamicTransform

  Marks a VisualElement that changes its transformation often (i.e. position, rotation or scale). When specified, this flag hints the system to optimize rendering of the VisualElement for recurring transformation changes. The VisualElement's vertex transformation will be done by the GPU when possible on the target platform. Please note that the number of VisualElements to which this hint effectively applies can be limited by target platform capabilities. For such platforms, it is recommended to prioritize use of this hint to only the VisualElements with the highest frequency of transformation changes.

- GroupTransform

  Marks a VisualElement that hosts many children with DynamicTransform applied on them. A common use-case of this hint is a VisualElement that represents a "viewport" within which there are many DynamicTransform VisualElements that can move individually in addition to the "viewport" element also often changing its transformation. However, if the contents of the aforementioned "viewport" element are mostly static (not moving) then it is enough to use the DynamicTransform hint on that element instead of GroupTransform. Internally, an element hinted with GroupTransform will force a separate draw batch with its world transformation value, but in the same time it will avoid changing the transforms of all its descendants whenever a transformation change occurs on the GroupTransform element.

- MaskContainer

  Marks a VisualElement that hosts non-rectangular descendants using the "overflow: hidden;" style. Non-rectangular masks are implemented with the stencil. If applicable, the renderer breaks the batch to preemptively set the stencil state, before and after drawing the descendants, so that the descendants won't have to set them at the next masking level. When using this flag, consecutive stencil push/pop operations are cheap and don't require modifying the stencil reference. As a result, the batch doesn't need to be broken for each push/pop operation. Consecutive push/push or pop/pop operations are still expensive. Avoid cases that involve many subtrees, where each subtree uses 2 or more levels of masking, to avoid consecutive push/push or pop/pop operations.

- DynamicColor

  Marks a VisualElement that changes its color often (background-color, border-color, etc.). This will store the element's colors in an optimized storage suitable for frequent changes, such as animation.

