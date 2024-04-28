# Auto Layout

Rect Transform layout 足够灵活来处理很多类型不同的布局，并且允许完全自由地放置 UI 元素。如果需要更结构化的布局，使用 Auto Layout。

Auto Layout 系统提供一嵌套 layout groups 放置元素的方法，例如 Horizontal Groups，Vertical Groups，以及 Grids。还允许允许根据包含的内容自动调整大小。

Auto Layout 时基于基本的 Rect Transform layout system 构建的，它可以可选地应用到一些或所有元素上面。

## 理解 Layout Elements

Auto layout 系统是基于 layout elements 和 layout controller 概念的。

layout elements 是一个具有 Rect Transform 的 GameObject。layout element 知道它应该具有的大小。layout elements 不直接设置它们自己的大小，但是其他作为 layout controllers 的组件可以使用 layout elements 提供的信息来为它们计算大小

Auto Layout 大体也对应 Web CSS 布局系统的设计，很多属性和布局功能都可以对比 CSS 布局，这样可以更好的理解和使用 Auto Layout 布局。

layout element 拥有它自己的属性：

- Minimum width - CSS Min Width
- Minimum height - CSS Min Height
- Preferred Width - CSS Width
- Preferred Height - CSS Height
- Flexible Width - CSS Flex 布局的 Grow 因子
- Flexible Height - CSS Flex 布局的 Grow 因子

Min Width/Height 是元素需要具有的最小大小，元素最小具有这个大小，无论 Layout Controller 有多大，如果容器大，就将多余空间分配给每个元素，否则元素将具有最小size，无视容器大小，容器可以选择 overflow 或者 hide 多出来的部分。

Preferred Width/Height 就是 CSS 中的 Width Height。

Flexible Width/Height 相当于 CSS Flex 布局中的 Grow 因子，当 controller 有多余空间时，按照比例分配给每个元素，但是有两个区别：

- grow 同时应用到 widht/height 上，而 AutoLayout 则对 Width 和 Height 分别提供了两个因子
- 多余的空间，AutoLayout 分配到元素本身的大小上，而 Flex 则是分配给每个元素的周围空白空间

CSS Flex 中 width/height 和 min/max 相互之间没有关系，min 和 max 只是为正常 width、height 提供一个 clamp 范围，就像 Unity 中的 Mathf.Clamp(value, minValue, maxValue) 一样。wdith/height 时在空间足够的情况下，元素期望的正常大小。然后根据各种因素，设置 min 和 max 范围对 width/height 进行 clamp，保证它不小于某个阈值，不大于某个阈值。

AutoLayout 也是一样，只是 layout element 没有 Max Width/Height 属性，只提供了 Minimum Size 属性。

Minimum Size 是元素必须具有的最小大小，Preferred Width 是元素期望具有的大小，即当空间足够时应该给元素分配的空间。当空间还有多余的空间时，多余的空间将按照 Flexible Width/Height 的比例再次分配到每个元素的 size 上，注意是增加到元素本身的大小，而不是增加到元素的空白区域，因此元素的大小可能超过 Preferred Size。

Preferred Size 和 Flexible Size 的区别是，前者按照固定大小分配给元素，后者是将容器多余空间按照比例再次分配到元素 size 上。

布局属性只是数据，是否发挥作用以及如何发挥作用需要看 controller 是否使用以及如何使用它们。例如各种 Layout Group 中包含 Control Child Size 选项。不勾选时，child 元素自己控制自己的 RectTransform size，此时就不会考虑这些布局属性。只有勾选了 Control Child Size 后，child 元素 size 才会按照上面的被 parent 计算和设置。

布局属性只负责元素 size 的计算，并不涉及元素的位置。元素的位置被 child alignment 控制，这相当于 Flex 的对齐属性。Layout Controller 先根据自己的空间大小划分出虚拟的分区用于分配给每个 child（size allocate），然后每个子元素在自己的分区（虚拟空间）中，按照分区大小被设置 size，按照特定的对齐属性来对齐 position。

注意 AutoLayout 中 pending 和 space 是不能自动分配的，只能明确指定，多余空间只分配到元素自身大小上。但是可以用一个空白的 parent 容器来实现相似的效果，这样空白 parent 分配的大小本身就作为空白使用。

Content Size Fiter 和各种 Layout Group 组件使用 layout elements 提供的信息。layout group 布局 layout element 的基本原则是：

- 首先分配最小 size，无论容器是否有这么大，元素总有这么大
- 如果容器还有足够的空间，则分配 preferred size
- 如果还有足够的空间，则分配 flexible size

任何具有 Rect Transform 的元素都是一个 layout element。它们默认的 minimum preferred flexible size = 0。特定组件在添加到 GameObject 上时会改变这些布局属性，例如 Image 和 Text 组件，它们改变 preferred width 和 height 来匹配 sprite 或 text content。

就像使用 CSS Flex 布局一样使用 AutoLayout，然后 flex 的每个功能找到 AutoLayout 的对应功能。

## Layout Element Component

添加 Layout Element Component 组件可以显式覆盖 layout 布局属性。

# 理解 Layout Controllers

Layout Controllers 是控制一个或多个 layout elements（带有 RectTransform 的 GameObject） 的大小或位置的组件。

Layout Controller 可能控制它自己的 layout element（自己的 Rect Transform），或者它的 child layout elements。

一个 layout controller 自己也可以是另一个 layout controller 的 layout element。

## Content Size Fitter

Content Size Filter 控制它自己的 Rect Transform。

## Aspect Ratio Filter

Content Size Filter 控制它自己的 Rect Transform。它通过 width 控制 height，或反之，来填充到 parent 或包裹 parent。Aspect Ratio Fitter 不考虑 minimum size 和 preferred size。各种 layout 属性只是数据，具体起不起作用，如何起作用要看 controller 如何使用它们。

## Layout Groups

Layout Groups 不控制自己的 Rect Transform，它的 Rect Transform 或者被 Anchor Layout 控制，或者它作为 layout element 被其他 controller 控制。

## Driven Rect Transform 属性

因为 layout controller 会自动控制 child layout element 的大小和位置，这些被控制的属性不可以通过 Inspector 或 Scene View 或者运行时修改，它们将在下一个 layout calculation 中被重置为计算的结果。

## 技术细节

接口（自定义）：

- ILayoutElement
- ILayoutGroup
- ILayoutSelfController

布局计算：

- 在 ILayoutElement 组件上调用 CalculateLayoutInputHorizontal 得到 layout element 的 minimum、preferred、flexible width 属性

  这是一个自底向上的过程，children 先于 parent 计算，这样 parent 可以将 children 的 layout 信息算到自己的 layout 信息内。这个过程只是根据 child layout 属性计算自己的 layout 属性，不涉及空间分配，元素的空间是被 parent 元素分配的。然后元素根据自己被分配的空间和它的 child 元素的布局属性为每个子元素分配空间。

- 在 ILayout Controller 组件上调用 SetLayoutHorizontal 来计算和设置 effective widths。这是个自顶向下的过程，先分配 parent 的 size，然后分配 children 的 size。这个过程结束时，RectTransform 将具有新的 width

- 按照相同的过程在 Vertical 上计算 height。

按照这个过程，height 的计算可能依赖 width，但是 width 的计算永远不依赖 height。

## 触发 Layout 重建

当 layout 属性改变时，可能导致当前 layout 不再有效，需要重新计算 layout。可以使用调用 LayoutRebuilder.MarkLayoutForRebuild(transform as RectTransform) 触发重建。

Rebuild 不会立即发生，而是在当前帧的结束时，渲染开始前执行。这是因为一帧中可能有很多处属性的修改，每个都重建 layout 会导致性能严重下降。

建议触发重建的时机是：

- 改变 layout 属性的 setter
- 在以下 callbacks 中：
  - OnEnable
  - OnDisable
  - OnRectTransformDimensionsChange
  - OnValidate (only needed in the editor, not at runtime)
  - OnDidApplyAnimationProperties

Layout Controller 自定向下分配空间时，可以认为它在自己的空间中为每个子元素划分出一个个虚拟的空间，然后将每个虚拟空间的大小设置为相应子元素 RectTransform 的 size，最后每个子元素按照自己的对齐属性在这个虚拟空间中设置自己的 position。注意布局属性（Minimum Size，Preferred Size，Flexible Size）只用在第一个自底向上计算的阶段。

## Reference

### Content Size Fitter

属性：

- Horizontal Fit：如何控制元素自身的 width

  - Unconstrained：不基于 layout element drive 元素的 width
  - Min Size：基于 layout element drive 元素的 width
  - Preferred Size：基于 layout element drive 元素的 width

- Vertical Fit：类似 Horizontal Fit

Layout Element 的布局属性只是为布局过程的第一阶段报告数据而已。布局第二阶段才真实为元素分配空间，真实元素 size 只有 width 和 height，不再有 Minimum Size 和 Preferred Size。

Content Size Fitter 就是将 Layout Element 的 Minimum Size 或 Preferred Size 设置到元素的 Size 上而已，非常简单。真正的魔法在于元素的 Layout Element 如何报告自己的 Minimum Size 或 Preferred Size，例如 Image 和 Text 都有自己的 Layout Element 的实现。

Content Size Fitter 是一个控制自己 RectTransform size 的 layout controller。最终 RectTransform Size 基于 GameObject 上的 layout element 组件提供的 Minimum Size 或 Preferred Size 决定。这样的 Layout Elements 可以是 Image 或 Text 组件，layout groups，或者 Layout Element 组件。

值得注意的是，当 Rect Transform 被 resized 时，无论是被 Content Size Fitter 还是其他的，resizing 绕着 pivot 进行。这意味着 resizing 的方向可以通过 pivot 控制。

例如当 pivot 位于 center，Content Size Fitter 在所有方向上平均地扩展 Rect Transform。当 pivot 位于 upper left corner，Content Size Fitter 像右下方扩展 Rect Transform。

### Aspect Ratio Fitter

属性：

- Aspect Mode：如何 resize rectangle 来保证 aspect ratio

  - None：不保持 aspect ratio
  - Width Controls Height：width 控制 height 来保持 aspect ratio
  - Height Controls Width：height 控制 width 来保持 aspect ratio
  - Fit In Parent：自动调整 width，height，position，和 anchors 是 rect 填充到 parent rect 中，不超过 parent rect 同时保持 aspect ratio，这可能在 parent rect 中留下一些空白空间。
  - Envelope：自动调整 width，height，position，和 anchors 是 rect 包裹 parent rect，不小于 parent rect 同时保持 aspect ratio，rect 可能有超出 parent rect 的空间。

- Aspect Ratio：要保持的 aspect ratio，= width / height

Aspect Ratio Fitter 不计算 Minimum Size 和 Preferred Size。

当 Rect Transform 被 resized 时，无论是被 Content Size Fitter 还是其他的，resizing 绕着 pivot 进行。这意味着 resizing 的方向可以通过 pivot 控制。


### Vertical Layout Group

- Minimum Height = 所有 child layout elements 的 Minimum Height + 所有它们之间所有的 spacing
- Preferred Height = 所有 child layout elements 的 Preferred Height + 所有它们之间所有的 spacing
- 如果 Vertical Layout Group 的 Height（被它自己控制，或者被其他的 Layout Controller 控制）小于等于它自己的 Minimum Height，所有 child layout elements 的大小都变成它们的 Minimum Height。
- 如果 Vertical Layout Group 的 Height 大于它的 Minimum Height 而小于它的 Preferred Height，超出 Minimum Height 的空间平等分配每个 child 元素的 height 上。Group 的 Height 越接近它的 Preferred Height，每个子元素越接近它们的 Preferred Height
- 如果 Vertical Layout Group 的 Height 超过它的 Preferred Height，它将根据 child 元素的 Flexible height 按照比例分配多余的 height 到每个元素的 height 上

属性：

- Padding：layout group 边缘的 padding
- Spacing：layout elements 之间的空间
- Child Alignment：如果 child layout elements 不能填充
- Control Child Size：layout group 是否控制子元素的 size。开启后，子元素的 Width/Height 被容器控制。若关闭，子元素的 Width/Height 可以手动设置
- Child Force Expand：是否容器将全部空间都分配给子元素。注意这不意味着子元素都扩展到划分的虚拟区域大小，后者需要启动 Control Child Size。如果子元素大小被显式设置，而且小于划分给它的虚拟空间，就可以按照 Chld Alignment 在虚拟空间中定位。
- Use Child Scale：当 sizing 或 laying out elements 时，是否考虑子元素的 scale。Width 和 Height 分别对应每个子元素 Rect Transform 组件的 Scale.X 和 Scale.Y 的值。

如果关闭 Child Force Expand 而且容器空间大于所有子元素的大小总和，则所有子元素整体排列在一起（除了 spacing 没有多余的间隔），然后按照 Child Alignment 在整个容器中对齐定位（例如在整个容器的左上角开始对齐，或在整个容器的右下角开始对齐）。

Child Force Expand 开启时将容器空间全部被用来划分虚拟区域给子元素，但不一定让子元素的大小等于虚拟区域（这需要启动 Control Child Size）。这样当虚拟区域大于子元素的大小时，可以按照 Child Alignment 在虚拟区域中对齐子元素。

Child Alignment 要起作用必须子元素大小比容器划分给子元素的虚拟空间小，这需要关闭 Control Child Size（手动设置 size）同时启动 Child Force Expand，将全部空间都划分给子元素。

Vertical Layout Group 因为通常只用来在垂直方向上分配 height，因此使用它一般只关注 Height，Width 要么被控制设置为扩展到容器 width，要么手动设置 width。Horizontal Layout Group 类似，只关注 Width。

Layout Group 使用子元素的布局属性数值，控制子元素 RectTransform 的 size 和位置。Content Size Fitter 使用自身布局属性数值，控制自身 Rect Transform 的 size。因此将 Content Size Fitter 作为 Layout Group 的子元素在逻辑上时冲突的。子元素应该只被其中之一控制。在 Layout Group 上使用 Content Size Fitter 时合理的，这意味着 Layout Group 自身的大小希望根据子元素的大小计算出来，然后再按照这个大小分配子元素的空间，这可以实现容器动态适应子元素的效果。

### Horizontal Layout Group

和 Vertical Layout Group 类似。

### Grid Layout Group

Grid Layout Group 在网格中放置 layout elements。

和 flex 布局类似，它可以指定 main axis 和 cross axis（主轴和辅轴），即沿着哪个方向排列。还可以指定从主轴的哪一段开始排列。

它完全控制每个 cell 的 size，cell 不能手动指定 size。所有 cell 一个挨着一个的排列（除了两者之间的 spacing），因此不存在子元素在虚拟空间中对齐的问题。它的 Child Alignment 是所有 cell 排列在一起作为整体在整个 Grid 空间中的对齐。

Grid Layout Group 显式定义和控制每个 cell 的 size。如果 cell 自己内部需要特定的布局，可以自己内部再使用 AutoLayout 或 AnchorLayout 布局自己的子元素。AutoLayout 和 Anchor Layout 可以混合使用。Layout Group 自身可以使用 AnchorLayout 在 parent 空间中显式定位，Layout Group 布局后的子元素内部可再以使用 Anchor Layout 布局自己的子元素。

Grid Layout Group 包括其他的 Layout Group 只是控制子元素的 RectTransform 的 position 和 size，并不关系其他的 UI 属性。Layout Group 完全可以是一个空的 RectTransform，没有任何可见元素或交互元素，空元素只为了得到 AutoLayout 布局结果，然后它的 Hierarchy 下面再使用 AutoLayout 或 AnchorLayout 进行进一步布局。

属性：

- Padding：Layout Group 边缘的空间
- Cell Size：显式指定 cell 的 size
- Spacing：cell 之间的空间
- StartCorner：第一个元素所在的 corner（从哪里开始排列）
- StartAxis：哪个轴作为排列的主轴（Horizontal 还是 Vertical）
- Child Alignment：如果排列好的 cells 整体大小小于容器可用空间，如果对齐它们
- Constraint：限制 grid 为固定的行数或列数

与其他 Layout Group 不同，Grid Layout Group 忽略子元素的 Minimum，Preferred，Flexible size 属性，相反为子元素指定一个固定的 size（Cell Size 属性）。

当把 Grid Layout Group 作为一个 auto layout 的一部分使用时（例如和Content Size Fitter 一起使用时），有一些问题需要注意。Auto Layout system 分别独立计算 horizontal 和 vertical size。这对 Grid Layout Group 可能有一些怪异，因为 grid 行数或列数彼此依赖。对更定数量的 cells，有很多 rows columns 组合。为了帮助 layout sytem，可以使用 Constraint 指定一个固定数量的 columns 或 rows。

即把 Grid Layout Grup 作为一个 auto layout 一部分使用时，应该显式固定 rows 数或 columns 数。

下面是和 Content Size Fitter 一起使用 Grid Layout System 的一些建议：

- flexible 的 width 和 fixed 的 height

  具有灵活 width 和固定 height 的 grid，grid 可以水平扩展添加尽可能多的元素，为此设置以下属性：

  - Grid Layout Group Constraint：Fixed Row Count
  - Content Size Fitter Horizontal Fit：Preferred Size，将元素 Layout Element 的 Preferred Size 设置为元素 Rect Transform 的 Size
  - Content Size Fitter Vertical Fit：Preferred Size 或 Unconstrained

  如果使用 unconstrained Vertical Fit，就需要显式为 grid 提供一个足够高的 height 来适应指定的 row 数量。

- fixed 的 width 和 flexible 的 height

  与上面类似，只不过翻转 Vertical 和 Horizontal。

- width 和 height 都是 flexible 的

  不需要控制有多少 rows 和 columns。grid 会尝试使 row 和 column 数量近似一样。

  - Grid Layout Group Constraint: Flexible
  - Content Size Fitter Horizontal Fit: Preferred Size
  - Content Size Fitter Vertical Fit: Preferred Size

### Layout Element

如果想覆盖一个 layout element 的 Minimum，Preferred，Flexible size，可以添加一个 Layout Element 组件到 GameObject 上。

Minimum 和 Preferred size 以常规 units 定义，flexible size 以相对 units 定义。如果任何一个 layout element 具有大于 0 的 flexible size，意味着容器的可用空间将被填满。 Siblings 元素的 relative flexible size 决定每个 sibling 填充的可用空间的比例。绝大多数情况下，flexible width 和 height 被设置为 0 或 1。

Flexible size 只在所有 Preferred size 被完全满足后才开始分配。

