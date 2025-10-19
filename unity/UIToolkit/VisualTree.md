# The Visual Tree

Visual Tree 保存一个 window 中所有 visual elements。它是一个 object graph，有称为 visual elements 的轻量 nodes 组成。

这些 nodes 在 C# heap 上分配，或者手动或者从 UXML template file 加载 UXML assets。

每个 node 包含 layout 信息，它的 drawing 和 redrawing 选项，node 如何响应事件。

## Visual Element

VisualElement 是 visual tree 中所有 node 的基类。VisualElement 基类包含 styles，layout data，local transformations，event handlers 等等属性。

VisualElement 具有一些子类，定义了更多的行为和功能，即具体的控件。VisualElement 实例可以有 child elements。

你不需要从 VisualElement 基类派生来使用 elements。你可以通过 stylesheets 和 event callbacks 定制一个 VisualElement 的外观和行为。

## Connectivity

Visual Tree 的 root object 被认为是 panel。一个新的 element 是被忽略的，直到它连接到 panel。你可以添加 elements 到现有 element 来挂载你的 UI 到 panel。

要验证一个 VisualElement 是否连接到一个 panel，你可以检测 element 的 panel。如果 visual element 没有连接，它返回 null。

## Drawing order

Visual Tree 中的元素以下列 order 的绘制：

- parent 在 children 之前绘制
- children 按照它们的 sibling list 中的顺序绘制

改变它们 drawing order 的唯一的方式是 reorder 它们 parents 的 VisualElement objects。

## Position，transforms，and coordinate systems

不同的坐标系定义如下：

- World：坐标相对于 panel space（root element）。Panel 是 visual tree 中的最高 element。
- Local：坐标相对于 element 自身

Layout system 为每个 element 计算 VisualElement.layout 属性（Rect）

layout.position 被解释为相对于它 parent 的坐标空间的 pixels。尽管你可以直接为 layout.position 直接赋值，建议使用 style sheets 和 layout system 来放置 position elements。

每个 VisualElement 还有一个 layout.transform 属性（ITransform），它相对于它的 parent 定位 element。默认地，transform 是 identity。

VisualElement.layout.position 和 VisualElement.layout.transform 属性定义如何在 local 坐标系和 parent parent 坐标系转换。

VisualElementExtensions 静态类提供了以下扩展方法，它们在坐标系之间变换 points 和 rectangles：

- WorldToLocal：变换 panel space 中的 Vector2 或 Rect 到 element space
- LocalToWorld：变换 element space 中的 Vector2 或 Rect 到 Panel space
- ChangeCoordinatesTo：从一个 element 的 local space 变换 Vector2 或 Rect 到另一个 element 的 local space

元素的原点位于左上角，x 向右，y 向下。

使用 worldBound 属性来获取 VisualElement 的 window space 坐标，考虑它的祖先元素的 transforms 和 positions。
