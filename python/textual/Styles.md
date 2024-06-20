# Styles

## Styles object

每个 Textual widget class 提供一个 styles 对象，它包含大量属性。这些属性告诉 Textual widget 应该如何显示。设置任何属性都会立即相应更新 screen。

Screen 是一个特殊 widget，表示整个 Terminal。

App.screen 引用整个屏幕。App.screen.styles 引用 screen 的样式。

每个组件 widget.styles 可以设置 widget 的样式。

widgets 会占据它所在容器的全部 width，以及在垂直方向上足够多的填充内容的行。

border 会单独占据一行或一列，除非移除 border。

Widgets 默认会 wrap text，向下扩展 widget 的高度来适应内容。

## Colors

很多属性可以接收颜色。最常用的是 color，它设置 widget 的默认文本颜色，以及 background 设置 widget 或 screen 的背景色。

颜色值可以设置为一个预定义颜色常量，例如 crimson, lime, palegreen：

```py
self.screen.styles.background = "lime"
```

除了颜色名字，还可以使用一下方式表达颜色：

- #F00, #9932CC
- rgb(255, 0, 0)
- hsl(280, 60%, 49%)

在 code 中，color style 对象还可以接受 Color 对象，显式创建颜色：

```py
self.widget1.styles.background = "#9932CC"
self.widget2.styles.background = "hsl(150,42.9%,49.4%)"
self.widget2.styles.color = "blue"
self.widget3.styles.background = Color(191, 78, 96)
```

### Alpha

Textual 内部使用 rgb 三个分量的 tuple 表示颜色。

Textual 支持第四个分量 alpha，可以使颜色透明。如果在一个 background color 上设置 alpha，Textual 会 blend 背景色和它下面的颜色。如果在 text color 上设置 alpha，Textual 会 blend text 和 background 的颜色。

有几种方法设置颜色的 alpha：

- ##9932CC7F
- rgba(192, 78, 96, 0.5)
- Color 对象：Color(192, 78, 96, a=0.5)

## Dimensions

Widgets 占据 screen 上的一块矩形区域，最小可以是一个字符，最大可以是整个 screen（如果开启 scrolling 甚至可以更大）。

### Box Model

以下样式影响 widget 的 dimensions：

- width 和 height 定义 widget 的 size
- padding 在 content area 周围添加可选 space
- border 在 content area 和 padding 周围绘制一个可选的矩形边框
- margin 在 border 外添加空间，技术上 margin 不是 widget 的一部分，但是在 widgets 之间提供了视觉分隔

这些样式一起构成了 widget 的 box 模型

### Width and Height

设置 width 限制 widget 使用的 columns 数量，height 限制使用的 rows 的数量。

widget 的内容显示在矩形 content area 内部，如果内容超出 area 大小，多余的部分会被剪裁掉。如果显示的是 text，text 默认会自动 wrap。

#### Auto dimensions

实践中，通常会想要 size 调整到适应它的内容，我们可以通过设置 auto 到 dimession 上。例如限制了 width 后，将 height 设置为 auto，widget 的高度会自动增长来适应内容的大小。

### Units

Textual 提供了不同的 units，这允许你相对于 screen 或 container 指定 dimessions。相对 units 可以更好地利用可用空间，如果用户调整 Terminal 大小的话。

- 百分比单位，50%，将 widget dimension 设置为 widget 的 parent size 的相对大小
- View 单位类似百分比单位，但是显式引用一个 dimension。vw unit 设置相对于 Terminal width 的 1% 的数量，vh 设置相对于 Terminal height 的 1% 的数量。注意这里引用的是 Terminal，即 Viewport，而不是 parent 容器
- 与 wv 和 vh 类似，w 和 h 单位相对于 parent 容器，而不是相对于 Viewport

#### FR units

对一些相对比例，百分比单位可能会有问题。例如如果想将 screen 划分为 3 份，必须将 dimension 设置为 33.333333%，比较奇怪。Textual 支持 fr 单位，对这种情况下，比百分比更适合。

当为给定 dimension(width/height) 指定 fr 单位，Textual 会将可用空间在那个 dimension 上划分为 fr 单位的总数个 cell。然后每个 fr 对应一个 cell，将可用空间按照 cell 单元分配个每个指定了 fr 的 widget。

### Maximum and minimums

同样的单位可以用于设置一个 dimession 的限制。min-width，max-width，min-height，max-height 可以接收和 width 和 height 一样的单位。

### Padding

Padding 在 border 和 content 之间添加空间，以提高可读性。

```py
self.widget.styles.padding = 2
self.widget.styles.padding = (2, 4)
self.widget.styles.padding = (2, 4, 2, 4)
```

### Border

border 在 widget 周围绘制一个矩形框。

```py
 self.widget.styles.border = ("heavy", "yellow")
```

border 是一个 tuple，第一个值是 border type，第二个值是 border 颜色。

border type 是一个字符串，可以使用 textual-devs 的 textual borders 查看不同的 border 类型。

#### Title alignment

Widget 的 border_title 显示在 top border 上，border_subtitle 显示在 bottom border 上。

有两个属性可以设置 title 在 border 上的对齐：

- border-title-align，默认 left
- border-subtitle-align，默认 right

### Outline

Outline 类似 border，并且以相同方式设置。不同的是，outline 不会改变 widget 的 size，并且会覆盖 content area。

### Box sizing

width、height 默认设置包括 border，padding，content area 在内的矩形区域的大小。因此当设置 border 或 padding 时，会减少 widget 的 content area。换句话说，设置 border 或 padding 不会改变 widget 的 size。

这通常是想要的，因为添加 border 或 padding 不会影响 widget 布局。但是有时会希望保持 content area 不变，而是增加 widget 的大小来适应 padding 或 border。box-sizing 样式允许你在两种模式间切换。

如果将 box-sizing 设置为 "content-box"，则 padding 和 border 需要的空间不算在 width 或 height 上，而是被添加到它上面。box-sizing 默认是 border-box。

### Margin

Margin 类似 padding，但是它在 border 外部添加空间，并且不算在 widget 的大小中，无论 box-sizing 是什么。padding 用来在 border 和 content 之间添加空白，margin 用来在 widgets 之间添加空白。

注意如果两个 margin 在之间同时设置了 margin，margin 会重叠，即最终 maring 是两个 margin 最大的那个。

## Style Reference

- align
- background
- border
- border-subtitle-align
- border-subtitle-background
- border-subtitle-color
- border-subtitle-style
- border-title-align
- border-title-background
- border-title-color
- border-title-style
- box-sizing
- color
- content-align
- display
- dock
- grid
- hatch
- height
- keyline
- layer
- layers
- layout
- links
- margin
- max-height
- max-width
- min-height
- min-width
- offset
- opacity
- outline
- overflow
- padding
- scrollbar colors
- scrollbar-gutter
- text-align
- text-opacity
- text-style
- tint
- visibility
- width
