# USS supported properties

和 CSS 语法相同

基本分为这几类属性：

- Box Model 属性
- Flex Layout 属性
- 外观绘制属性
- 文本属性
- 光标属性

## Box Model

![style-box-model](../../Image/style-box-model.png)

### Dimensions

- width: \<length> | auto
- height: \<length> | auto
- min-width: \<length> | auto
- min-height: \<length> | auto
- max-width: \<length> | auto
- max-height: \<length> | auto

如果 width 不指定，width 基于元素内容设置。如果 height 不指定，height 基于元素内容高度设置。

### Margins

- margin-left: \<length> | auto
- margin-top: \<length> | auto
- margin-right: \<length> | auto
- margin-bottom: \<length> | auto
- margin: [\<length> | auto]{1, 4}

简写 margin：

- 1 个：应用到所有 margins
- 2 个：(margin-top & margin-bottom), (margin-left & margin-right)
- 3 个：margin-top, (margin-left & margin-right), margin-bottom
- 4 个：margin-top, margin-left, margin-right, margin-bottom

### Borders

- border-left-width: \<length>
- border-top-width: \<length>
- border-right-width: \<length>
- border-bottom-width: \<length>
- border-width: \<length>{1, 4}

### Padding

- padding-left: \<length>
- padding-top: \<length>
- padding-right: \<length>
- padding-bottom: \<length>
- padding: [\<length>]{1, 4}

## Flex Layout

默认所有 items 垂直放置在容器中

### Items

- flex-grow: \<number>
- flex-shrink: \<number>
- flex-basis: \<length> | auto
- flex: none | [\<'flex-grow'> \<'flex-shrink'>? || \<'flex-basis'>]

### Containers

- flex-direciton: row | row-reverse | column | column-reverse
- flex-wrap: nowrap | wrap | wrap-reverse 
- algin-content: flex-start | flex-end | center | stretch
- align-items: flex-start | flex-end | center | stretch
- justify-content: flex-start | flex-end | center | space-between | space-around

## Relative and absoute positioning

### Positioning

- position: absolute | relative

  默认 relative，position 基于 parent。如果设置为 absolute，元素离开 parent layout，元素位置和维度基于 parent bounds 指定。

### Position

- left: \<length> | auto
- top: \<length> | auto
- right: \<length> | auto
- bottom: \<length> | auto

相对 parent edge 或元素原始 position 的距离

## Drawing properties

绘制属性设置 background，borders，以及 visual element 的外观

### Background

- background-color: \<color>
- background-image: \<resource> | \<url> | none
- -unity-background-scale-mode: stretch-to-fill | scale-and-crop | scale-to-fit
- -unity-background-image-tint-color: \<color>

### Slicing

当赋予一个 background image，它可以绘制为 9-slice

- -unity-slice-left: \<integer>
- -unity-slice-top: \<integer>
- -unity-slice-right: \<integer>
- -unity-slice-bottom: \<integer>

### Borders

- border-color: \<color>
- border-top-left-radius: \<length>
- border-top-right-radius: \<length>
- border-bottom-left-radius: \<length>
- border-bottom-right-radius: \<length>
- border-radius: \<length>{1,4}

### Appearance

- overflow: hidden | visible
- -unity-overflow-clip-box: padding-box | content-box
- opacity: \<number>
- visibility: visible | hidden
- display: flex | none

display 默认为 flex。设置 display 为 none 移除这个元素。这个 visibility 为 hidden 隐藏这个元素，但是允许仍然占据 layout 中的空间。

-unity-overflow-clip-box 定义元素内容的 cliping rectangle。默认是 padding-box，padding area 外边缘的 rectangle；content-box 表示 padding area 內边缘的 rectangle。

## Text properties

Text 属性设置 font 的 color，font，font size，Unity 特定 font 资源属性，font style，alignment，word wrap，clipping。

- color: \<color>
- -unity-font: \<resource> | \<url>
- font-size: \<number>
- -unity-font-style: normal | italic | bold | bold-and-italic
- -unity-text-align: upper-left | middle-left | lower-left | upper-center | middle-center | lower-center | upper-right | middle-right | lower-right
- white-space: normal | nowrap

## Cursor property

光标纹理

- cursor: [ [ \<resource> | \<url> ] [ \<integer> \<integer>]? , ] [ arrow | text | resize-vertical | resize-horizontal | link | slide-arrow | resize-up-right | resize-up-left | move-arrow | rotate-arrow | scale-arrow | arrow-plus | arrow-minus | pan | orbit | zoom | fps | split-resize-up-down | split-resize-left-right ]
