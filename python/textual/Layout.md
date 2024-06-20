# Layout

Layout 定义 Widgets 在容器中如何摆放。

Textual 支持很多 layouts，它们皆可以在 code 中用 widget.styles 设置，也可以在 CSS 中设置。

Layouts 既可以用于 Screen 上 high-level 的 widgets 定位，也可以用于嵌套 widgets 的定位。

## Vertical

vertical layout 将 child widgets 垂直排列，从上到下，无论 child 的 width 是否占据 container 的全部 width。类似 web css 中 block level 布局，不管 child 元素的 width，总是自上向下排列。

Screen 是最顶层的 widget，是 App 最基础的容器，是 App.compose yield 的 widgets 的容器，可以被视为 Terminal 窗口自己。在 CSS 中用 Screen 为它添加样式。Screen 默认就是 vertical layoiut 的。

widget 默认 width 是扩展到容器的 width 的。

在 code 中设置 layout:

```py
widget.styles.layout = "vertical"
```

使用 fr 单位可以保证 children 可以填充 parent 的可用高度。如果所有 children 的高度超过可用空间，对于 Screen 会自动添加滚动条，但是对 widget，则默认会剪裁掉超出的部分。

## Horizontal

从左到右摆放 child widgets。

尽管默认 widget 会扩展 width 到 container 的 width，除非显式设置 width，但是默认 widget 不会扩展 height 到 container 的 height，height 只会扩展到适应 content 的高度，如果没有内容，就是 0. 要扩展 height 到 container，需要显式指定 height: 100%.

注意因为 widget 默认会扩展 width 到 container，因此如果不显式设置 width，每个 widget 的宽度都会变成和 container 一样宽。假设有 3 哥 widget，第一个 widget 就会占据整个 screen，剩下的 widget 都会被挤出到 screen 之外。只有为三个 widget 显式设置 1fr，则每个 widget 会占据 screen 的 1/3.

Textual 的布局系统不是 Flex 布局的。

对于 Screen 的垂直布局，child widgets 超出 screen height 时会自动添加滚动条，但是对于 Screen 的水平布局，不会自动添加滚动条。

要开启水平滚动，必须声明 overflow-x: auto，声明后，如果 children 超出 parent container（不仅是 Screen）的 size，Textual 会自动添加滚动条。

## Unitylity containers

Textual 包含一些 container widgets。其中，Vertical、Horizontal 和 Grid 具有相应的 layout。它们就是一些实用类，使得不必手动创建 container 然后为 layout 赋值，仅此而已。

```py
def compose(self) -> ComposeResult:
    yield Horizontal(
        Vertical(
            Static("One"),
            Static("Two"),
            classes="column",
        ),
        Vertical(
            Static("Three"),
            Static("Four"),
            classes="column",
        ),
    )
```

## Composing with context managers

上面的例子使用位置参数为 container 添加 children，但是 Textual 使用 context managers 提供了一个简化的语法。

```py
 def compose(self) -> ComposeResult:
    with Horizontal():
        with Vertical(classes="column"):
            yield Static("One")
            yield Static("Two")
        with Vertical(classes="column"):
            yield Static("Three")
            yield Static("Four")
```

这与上面的结果一样。

## Grid

Grid layout 在一个 grid 中摆放 widgets。Widgets 可以横跨多行或多列，可以创建复杂的 layouts。它可以作为 App 布局设计的基础。

注意这与 web css 的 Grid 布局不是一个东西，它是 Textual 提供的布局。

要使用 grid layout，在 CSS 中设置 layout 为 grid，并用 grid-size 设置 grid 的行数和列数。Widgets 按照从左到右，从上到下插入 cells。

如果 yield 超过 grid size 的 widget，它将不可见，因为 grid 没有足够的空间容纳它。

如果忽略 grid-size 的 rows 参数，Textual 将会根据 widgets 的数量添加新的 rows。

### Row and column sizes

默认 grid cell 的宽度和高度是从 grid dimensions 等分的，但是可以使用 grid-columns 和 grid-rows 调整 grid 中 columns 的宽度和 rows 高度。这些属性可以接收多个值，让你按照逐行或逐列指定 dimensions。

```css
Screen {
    layout: grid;
    grid-size: 3;
    grid-columns: 2fr 1fr 1fr;
}
```

因为 grid-size = 3，则 grid-columns 声明有三个空白分隔的数值。这些值的每一个设置对应 column 的宽度。

同样的方法可以用于设置不同 row 的高度。

如果没有为 grid-columns 或 grid-rows 声明指定足够的 values，提供的 values 将会被重复。例如，如果设置 grid-size: 4，grid-columns: 2 4 等价于 grid-columns: 2 4 2 4. 如果 grid-size: 3，grid-columns: 2 4 将等价于 grid-columns: 2 4 2.

#### Auto rows / columns

grid-columns 和 grid-rows rules 都可以在任何 dimension 接受 auto 关键字，告诉 Textual 根据 内容自动计算最优 size。

fr 单位占用的空间是其他显式单位指定占据的空间后剩余的可用空间。

### Cell spans

Cells 可以跨越多行或多列，来创建更有趣的 grid 布局。

每个 cell 只会添加一个 widget，如果要在一个 cell 添加更多更复杂的 widgets，只需要将 cell 下面的 widget 作为 root 容器，创建嵌套布局即可。

因为每个 cell 下面只有一个 widget，因此要调整 cell 跨越多行或多列，只需要在 cell 对应的 widget 上指定跨越多少行多少列即可。

要使一个 cell 跨越多行或多列，为 widget 添加一个 ID，然后在 CSS 中用 column-span 和 row-span 指定跨越多少行列。还可以再 widget 上使用 tint: magenta 40% 来添加一个轻微的 slight tint，来吸引注意力。

当一个 widget 占据多个 cell 之后，后续 widget 顺延向后移动。

注意 row-span 和 column-span 设置到超过 grid size 之后，widget 的 size 将会被 clamp 到 grid size 大小。

我们可以简单调整

### Gutter

grid-gutter 可以调整 grid 中 cells 之间的空白。默认 cells 之间是没有 gutter 的，即它们的 edges 彼此挨着。grid-gutter 必须用在具有 layout: grid 的 widget 上，而不是 cell widget 上。

gutter 只会在 cells 直接添加空白，不会在 cell 和 parent container edge 之间添加空白。

可以为 grid-gutter 属性提供两个 value，分别设置垂直和水平 gutter。因为 Terminal cells 通常高度是宽度的两倍，因此通常将水平 gutter 设置为垂直 gutter 的两倍。

## Docking

Widgets 可以停靠。停靠的组件会从 layout stream 中移除，并在固定它的位置，它可以被停靠在容器的 top，right，bottom，left。停靠的组件不会滚动，因此它们非常适合 sticky headers，footers，和 sidebars。

要停靠一个 widget 到 edge，只需要在 css 声明 dock: \<EDGE\>。Edge 可以是 top, right, bottom, left。这类似于将 position 声明为 Absolute 或 Fixed，将 widget 从 layout 中移除。

停靠多个 widgets 到同一个 edge，会导致重叠。后面 yield widget 在上面。

可以停靠多个 widgets 到不同的 edges 上。停靠的 widget 尽管从 layout 移除，但是它会占据 container 的空间，而不是浮动在 container 上面，因此其他的 widgets 只能在剩余的空间布局。要创建浮动的停靠 widget，在原本的 container 上添加一个相同大小的 container，然后内容放在第一个 container 中，停靠的 widget 放在第二个 container 中。

内置的 Header 就是停靠在 top 的 widget。但是只需要直接在 App.compose 中直接 yield 它，不需要显式设置 Dock 属性，因为它内置的 default css 包含了 Dock 的设置。

只有停靠在相同的 edge 的 widgets 会重叠，停靠在不同 edge 的 widget 会按照 yield 顺序分别占据 container 空间，后面停靠的 widget 只能占据前面停靠的 widget 剩下的空间。

要调整那个停靠 widget 占据更大的空间，只需要调整它们 yield 的顺序。

## Layers

Textual 有一个 layer 的概念，它可以更精细地控制 widgets 放置的顺序。

当绘制 widgets 时，Textual 按照 layers 自底向上的顺序绘制 widgets。这样更高层的 widgets 将绘制低层的 widgets 上面。注意 widgets 在计算它们的 layout rect 时是没有 layer 概念的，就像它们在一个 layer 一样，只是计算后，按照 layer 自底向上的顺序绘制 widgets 而已。

Container widget 上用 layers 属性定义一组 layer 名字。然后它下面的 widget 可以使用 layer 属性选择其中一个 layer。

layers 属性使用一个空白分隔的 layer name 列表。最左边的 layer 是最低的，最右边的 layer 是最高的。

## Offsets

Widgets 有一个 relative offset，它相对于 widget 正常布局的位置进行偏移。这发生在 layout 完成之后，因此对 widget 偏移不会再影响其他 widget 的布局。这类似 web css 的相对定位。Widget 默认的 Offset 是 (0, 0)。

