# Styles

- Align

  align style 在 container 内对齐 children widget。注意它是对齐 widget，而不是 text 或 renderable 的。

  ```css
  align: <horizontal> <vertical>;
  align-horizontal: <horizontal>;
  align-vertical: <vertical>;
  ```

  horizontal: center/left/right, 默认 left

  vertical: middle/top/bottom, 默认 top

- Background

  ```css
  background: <color> [<percentage>]
  ```

  如果指定后面的百分比，它指定了颜色的透明度。

  ```css
  /* Blue background */
  background: blue;
  
  /* 20% red background */
  background: red 20%;
  
  /* RGB color */
  background: rgb(100, 120, 200);
  
  /* HSL color */
  background: hsl(290, 70%, 80%);
  ```

- Border

  ```css
  border: [<border_style>] [<color>] [<percentage>];
  border-top: [<border_style>] [<color>] [<percentage>];
  border-right: [<border_style>] [<color> [<percentage>]];
  border-bottom: [<border_style>] [<color> [<percentage>]];
  border-left: [<border_style>] [<color> [<percentage>]];
  ```

  border_style: ascii/blank/dashed/double/heavy/hidden/hkey/none/outer/panel/round/solid/tall/vkey/wide

  ```css
  #container {
    border: heavy red;
  }
  
  #heading {
      border-bottom: solid blue;
  }
  ```

  ```py
  widget.styles.border = ("heavy", "red")
  widget.styles.border_bottom = ("solid", "blue")
  ```

- Border-subtitle-align

  ```css
  border-subtitle-align: <horizontal>;
  ```

- Border-subtitle-background
- Border-subtitle-color
- Border-subtitle-style
- Border-title-align
- Border-title-background
- Border-title-color
- Border-title-style

- Box-sizing

  border-box / content-box

- Color

  ```css
  /* Blue text */
  color: blue;
  
  /* 20% red text */
  color: red 20%;
  
  /* RGB color */
  color: rgb(100, 120, 200);
  
  /* Automatically choose color with suitable contrast for readability */
  color: auto;
  ```

- Content-align

  content-align style 在 widget 内对齐 content，而不是 child widget。

  ```css
  content-align: <horizontal> <vertical>;
  content-align-horizontal: <horizontal>;
  content-align-vertical: <vertical>;
  ```

- Display

  定义 widget 是否显示。block 显示，none 隐藏，并且不会为它保留空间。

- Dock

  ```css
  dock: bottom | left | right | top;
  ```

- Grid

  - column-span：cell 跨越的 columns 数量
  - grid-columns：grid columns 的宽度（字符数量）
  - grid-gutter：grid cells 之间的空间
  - grid-rows：grid rows 的高度（字符数量）
  - grid-size：grid layout 包含的 columns 和 rows 的数量
  - row-span：cell 跨越的 rows 数量

- Hatch

  hatch（影线）使用重复的 character 填充 widget 的 background，产生纹理效果。

  hatch: cross/horizontal/left/right/vertical

  ```css
  /* Red cross hatch */
  hatch: cross red;
  /* Right diagonals, 50% transparent green. */
  hatch: right green 50%;
  /* T custom character in 80% blue. **/
  hatch: "T" blue 80%;
  ```

  ```py
  widget.styles.hatch = ("cross", "red")
  widget.styles.hatch = ("right", "rgba(0,255,0,128)")
  widget.styles.hatch = ("T", "blue")
  ```

- Height

  决定 widget 的高度（字符数量）。

- Keyline

  keyline style 应用到 container，可以在 child widgets 周围绘制 lines。

  keyline 看起来就像 border，而是 border 绘制在 widget 内部，keyline 绘制在 widget 的外面（绘制在 margin 里，不算在 widget 的 size 之内）。此外，keylines 还可以重叠和交叉，来在 widgets 之间创建分割线。

  因为 keyline 绘制在 widget 的 margin 中，因此需要应用 margin 或 grid-gutter 来看到效果。总之它们不会占据 widget 空间。

- Layer
  
  定义 widget 所在的 layer。

- Layers

  定义这个 widget 下面的 layers 集合。

- Layout

  layout 定义 widget 如何摆放 children。

  horizontal、vertical(default)、grid

- Links

  Textual 支持嵌套在 text 中的 inline links, 当点击它时可以触发一个 action。有很多样式可以定义 links 的外观。

  正常样式（background，color，style）

  - link-background：link text 的背景色
  - link-color：link text 的颜色
  - link-style：link text 的样式（underline italic bold 等等）

  Hover 样式（background，color，style）

  - link-background-hover：cursor hover link text 时的背景色
  - link-color-horver：cursor hover link text 时的 text 颜色
  - link-style-hover：cursor hover link text 时的 text 样式

- Margin

  定义 widget 周围的空间。

  ```css
  /* Set margin of 1 around all edges */
  margin: 1;

  /* Set margin of 2 on the top and bottom edges, and 4 on the left and right */
  margin: 2 4;

  /* Set margin of 1 on the top, 2 on the right, 3 on the bottom, and 4 on the left */
  margin: 1 2 3 4;
  
  margin-top: 1;
  margin-right: 2;
  margin-bottom: 3;
  margin-left: 4;
  ```

  ```py
  # Set margin of 1 around all edges
  widget.styles.margin = 1
  # Set margin of 2 on the top and bottom edges, and 4 on the left and right
  widget.styles.margin = (2, 4)
  # Set margin of 1 on top, 2 on the right, 3 on the bottom, and 4 on the left
  widget.styles.margin = (1, 2, 3, 4)
  ```

- Max-height

  限制 widget 的最大高度（字符数量）。Widget 的高度绝不会超过这个高度。

  ```css
  /* Set the maximum height to 10 rows */
  max-height: 10;
  
  /* Set the maximum height to 25% of the viewport height */
  max-height: 25vh;
  ```

  ```py
  # Set the maximum height to 10 rows
  widget.styles.max_height = 10
  
  # Set the maximum height to 25% of the viewport height
  widget.styles.max_height = "25vh"
  ```

- Max-width
- Min-height

  Widget 的高度绝不会小于这个高度。

- Min-width

- Offset

  widget 相对于正常布局位置的偏移。不会再影响布局，只是简单从原来的位置移动。

- Opacity

  ```css
  /* Move the widget 8 cells in the x direction and 2 in the y direction */
  offset: 8 2;
  
  /* Move the widget 4 cells in the x direction
  offset-x: 4;
  /* Move the widget -3 cells in the y direction
  offset-y: -3;
  ```

  ```py
  widget.styles.offset = (2, 4)
  ```

- Outline

  outline 在 content 的周围绘制一个 box，它绘制在 content area 的上面，不占据 widget 的 size。

  border 和 outline 不能再 widget 的一个 edge 上同时存在。

  ```css
  /* Set a heavy white outline */
  outline:heavy white;

  /* set a red outline on the left */
  outline-left:outer red;
  ```

  ```py
  # Set a heavy white outline
  widget.outline = ("heavy", "white")

  # Set a red outline on the left
  widget.outline_left = ("outer", "red")
  ```

  和 border 不一样，outline 的 frame 绘制在 content 之上，而不是绘制在 content 之外。这可用于为 widget 添加边框，临时强调 widget 的内容。

  因为 outline 绘制在 content 上面，因此它会覆盖掉 content 最外面一圈的内容。但因为 outline 通常是为 widget 临时添加的，来吸引用户注意力的，因此这没什么问题。

- Overflow

  overflow 指定 scrollbars 是否以及何时显示。

  默认值是 overflow: auto auto. 但是一些内置 containers 像 Horizontal 和 VerticalScroll 覆盖这些值。

  ```css
  /* Automatic scrollbars on both axes (the default) */
  overflow: auto auto;
  
  /* Hide the vertical scrollbar */
  overflow-y: hidden;
  
  /* Always show the horizontal scrollbar */
  overflow-x: scroll;
  ```

- Padding

  Padding 在 content 和 border 之间添加空白。

  ```css
  /* Set padding of 1 around all edges */
  padding: 1;
  /* Set padding of 2 on the top and bottom edges, and 4 on the left and right */
  padding: 2 4;
  /* Set padding of 1 on the top, 2 on the right,
                   3 on the bottom, and 4 on the left */
  padding: 1 2 3 4;
  
  padding-top: 1;
  padding-right: 2;
  padding-bottom: 3;
  padding-left: 4;
  ```

  ```py
  # Set padding of 1 around all edges
  widget.styles.padding = 1
  # Set padding of 2 on the top and bottom edges, and 4 on the left and right
  widget.styles.padding = (2, 4)
  # Set padding of 1 on top, 2 on the right, 3 on the bottom, and 4 on the left
  widget.styles.padding = (1, 2, 3, 4)
  ```

- Scrollbar-colors

  设置 scrollbar 的各种颜色。通常不需要修改它们，Textual 仔细选择了 scrollbar 颜色。但是如果想修改是能够修改的。

  - scrollbar-background：scrollbar 背景色
  - scrollbar-background-active：thumb 被拖拽时 scrollbar 的背景色
  - scrollbar-background-hover：mouse hover scrollbar 时 scrollbar 的背景色
  - scrollbar-color	Scrollbar：thumb 拖放块的颜色
  - scrollbar-color-active：thumb 被拖放时的颜色
  - scrollbar-color-hover：mouse hover thumb 时 thumb 的颜色
  - scrollbar-corner-color：Horizontal 和 Vertical scrollbars 之间的空隙

- Scrollbar-gutter

  scroller-gutter 允许为 vertical scrollbar 预留空间（即使当前不需要显示滚动条，仍然留出空间）。

  ```css
  scrollbar-gutter: auto;    /* Don't reserve space for a vertical scrollbar. */
  scrollbar-gutter: stable;  /* Reserve space for a vertical scrollbar. */
  ```

- Scrollbar-size

  定义 scrollbars 的 widget。

  ```css
  /* Set horizontal scrollbar to 10, and vertical scrollbar to 4 */
  scrollbar-size: 10 4;
  
  /* Set horizontal scrollbar to 10 */
  scrollbar-size-horizontal: 10;
  
  /* Set vertical scrollbar to 4 */
  scrollbar-size-vertical: 4;
  ```

- Text-align

  text-align 设置 widget 中的 text 的对齐。注意 content-align 也是对齐 widget 的内容，但是它将 content（renderable）作为一个整体，而 text-align 只对齐 widget 的 text。如果 content 是 renderable 而不是 text，

- Text-opacity

  text-opacity 样式混合 text 的颜色和背景色：text-opacity: 50%.

- Text-style

  bold/italic/reverse/strike/underline

- Tint

  tint 将 widgt 的颜色和一个颜色进行混合。这个颜色应该有一个 alpha 分量（直接在颜色中指定，或者通过一个可选的百分比），否则结果颜色
将遮蔽 widget 的 content。

- Visibility

  ```css
  /* Widget is invisible */
  visibility: hidden;
  
  /* Widget is visible */
  visibility: visible;
  ```

  ```py
  # Widget is invisible
  self.styles.visibility = "hidden"
  
  # Widget is visible
  self.styles.visibility = "visible"

  # Make a widget invisible
  widget.visible = False
  
  # Make the widget visible again
  widget.visible = True
  ```

  visibility 只控制 widget 是否可见，不影响 layout，它占据的空间还会在那里。要将 widget 从 layout 移除，直接用 unmount 将 widget 解除挂载就可以。

  默认，children 继承 parent 的 visibility。如果 container 被设置为 invisible，children widgets 默认也会 invisible。但是如果 child widgets 显式设置了 visibility: visible，child widget 仍然会显示。

- Width

  默认 width 扩展到 container 的宽度。

