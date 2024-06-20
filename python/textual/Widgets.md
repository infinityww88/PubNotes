# Widgets

Widget 是一个 UI 组件，负责管理 screen 上的一块矩形区域。Widgets 可以和 App 一样的方式响应事件。很多方面，widgets 就像 mini-apps，或者说 App 就像一个大号的 widget。

每个 widget 运行在它自己的 asyncio task 中。

## 自定义 widgets

Textual 有很多内置 widgets，还可以以相同的方式完全构建自定义 widgets。

构建 widget 的第一步是 import widget 并扩展一个 widget 的子类。它可以是 Widget，也可以是另一个 Widget 子类。

```py
from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget


class Hello(Widget):
    """Display a greeting."""

    def render(self) -> RenderResult:
        return "Hello, [b]World[/b]!"


class CustomApp(App):
    def compose(self) -> ComposeResult:
        yield Hello()


if __name__ == "__main__":
    app = CustomApp()
    app.run()
```

自定义 widget 最简单只需要定义一个 render() 方法。Textual 会在 widget 的内容区域显示 render() 返回的任何东西。可以返回一个简单的 string，也可以返回 Rich renderable。

## Static widget

当开始扩展 Widget 时，最好从一个 subclass 开始。Static 是 widget 最简单的一个子类，相比于 widget，它提供一个 update() 方法来更新 content area 内容。每次要更新 widget 内容时，只需要调用 update() 方法，然后传递要渲染的内容。然后 update() 的内容被 widget 就被缓存，之后总是显示这个内容（Static render 总是返回缓存的内容，仅此而已)，直到下次调用 update 更新缓存的内容。

```py
class Hello(Static):
    """Display a greeting."""

    def on_mount(self) -> None:
        self.next_word()

    def on_click(self) -> None:
        self.next_word()

    def next_word(self) -> None:
        """Get a new hello and update the content area."""
        hello = next(hellos)
        self.update(f"{hello}, [b]World[/b]!")
```

### Default CSS

当构建应用程序 时，最好将 CSS 保存到外部文件。这可以让你在一个地方查看所有 CSS，并开启 live editing。然而，如果你想要分发 widget（例如 PyPI），最后将 code 和 CSS 打包在一起。这可以通过为 widget class 添加一个类变量 DFFAULT_CSS 来实现。

Textual 内置组件就是使用这种方法打包 CSS 的。

注意和 CSS_PATH、CSS 不一样，DEDAULT_CSS 是 Widget 的类变量。

#### Scoped CSS

Default CSS 默认是 scoped 的。这意味着 DEFAULT_CSS 定义的 CSS 只会影响 widget 和它的 children。这可以防止意外干扰不相关的组件。例如 .myclass 只会查找这个 widget 下面的带有 myclass 的组件，但不会影响 app 中其他带有 myclass 的组件。但是可以设置类变量 SCOPED_CSS = False 来关闭 scoped CSS。

#### Default specificity

DEFAULT_CSS 定义的 CSS 具有最低的 CSS 优先级，APP CSS 和 CSS_PATH 样式优先级高于 DEFAULT_CSS。

## Text links

Widget 中的 Text 可以标记为 links，当点击它时可以执行一个操作。Console Markup 中标记 links：

```
"Click [@click='app.bell']]Me[/]"
```

它可以作为 renderable 显示为任何组件的内容。

```py
class Hello(Static):
    """Display a greeting."""

    def on_mount(self) -> None:
        self.action_next_word()

    def action_next_word(self) -> None:
        """Get a new hello and update the content area."""
        hello = next(hellos)
        self.update(f"[@click='next_word']{hello}[/], [b]World[/b]!")
```

@click tag 引入一个 click handler，它运行 app.bell action。

## Border titles

和 app 的 title/sub_title 一样，每个 widget 也具有 border_title 和 border_subtitle 属性。设置 border_title 会在 top border 中显示 text，设置 border_subtitle 会在 bottom border 中显示 text。

类似，可以通过 Widget 类变量 BORDER_TITLE/BORDER_SUBTITLE，也可以通过 Widget 实例的 border_title/border_subtitle 设置标题和子标题。

注意，title 限制为单行 text。如果提供的 text 太长，超过了 widget，它将会被剪裁，并在结尾显示省略号。

有很多样式可以影响 title 的显示。

## Rich renderables

Widget 的内容不仅可以显式普通的 text，还可以显式 renderables。可以使用 Rich 和第三方库定义的 renderable。

## Content Size

如果 widget 的 width 和 height 设置为 auto，Textual 会从 rich renderables 自动检测内容区域的维度。还可以通过实现 get_content_width() 或 get_content_height() 覆盖 auto dimensions（注意这覆盖的是 auto 检测的长度，如果 CSS 显示指定了 widget 的维度，这个两个方法没有作用。

```py
def get_content_width(self, container: Size, viewport: Size) -> int:
    """Force content width size."""
    return 50
```

构建 rich.Table 时，如果传递 expand=True，Table 将会扩展到最大可能区域，而不是它自己计算的最优宽度。

## Tooltips

Widgets 可以有 tooltips，当鼠标滑过 widget 时，会显示 tooltips。

要添加 tooltip，为 tooltip 属性指定文本。你可以为它设置 text，或任何 Rich renderable。

### Customizing the tooltip

如果不喜欢默认的 tooltips 外观，可以使用 CSS 定义其外观。

```
Tooltip {
    padding: 2 4;
    background: $primary;
    color: auto 90%;
}
```

## Loading indicator

Widgets 有一个 loading reactive 属性，如果设置为 True，将会使用 LoadingIndicator 临时替换 widget。

可以使用它来指示用户，app 当前正在获取数据，当数据可用时将会显示内容。

```py
def on_mount(self) -> None:
    for data_table in self.query(DataTable):
        data_table.loading = True  
        self.load_data(data_table)

@work
async def load_data(self, data_table: DataTable) -> None:
    await sleep(randint(2, 10))  
    data_table.add_columns(*ROWS[0])
    data_table.add_rows(ROWS[1:])
    data_table.loading = False  
```

## Line API

返回 Rich renderables 的 widgets 的一个缺点是当 widget 的状态更新或改变 size 时，Textual 会重绘整个 widget。如果 widget 足够大需要 scrolling，或者 widget 更新频繁的时候，这样的重绘会使 app 响应变慢。

Textual 提供了另一个 API，可以减少重绘一个组件需要的工作，并可以更新 widget 的一部分区域（最小到单个字符），而不需要完全重绘。这称为 line API。line 指的是 Terminal 的一行。

使用 Line API 需要比直接返回 Rich renderables 更多的工作，但是可以产生更强大的 widgets，例如内置的 DataTable，可以处理成千上万，甚至上百万行的 rows。

### Render Line method

要使用 line API 构建一个 widget，实现 render_line 方法而不是 render 方法。render_line 方法使用一个整数参数 y，y 是从 widget top 开始的一个偏移（line API 是一行一行渲染 Widget 的）。注意 Textual 的坐标 x、y 是以 Terminal 中的字符 cell 单位（两个 cell 的宽度等于一个 cell 的高度）。render_line 返回一个 Strip object（strip：纸带，纸条），它包含 widget 一行的内容。Textual 会按需调用这个方法得到 widget 中每行的字符内容。

#### Segment and Style Strips

Segment 是 Rich 中的一个类。它是一个很小的对象（实际上就是一个 named tuple），它将要显式的 string 和 Style 实例打包在一起，告诉 Textual text 的外观（color，bold，italic 等等）。它就是 Rich 显示的基本单位，有点类似 Unity GUI 的 GUIContent（内容和样式的打包类）。

```py
greeting = Segment("Hello, World!", Style(bold=True))
```

Rich 和 Textual 都使用 segments 生成内容。Textual app 就是组合成百上千的 segments 的结果。

#### Strips

Strip 是一组 segments 的容器，它们一起显示 Widget 的一行。一个 Strip 至少包含一个 segment，但通常很多。

一个 Strip 对象从一个 Segment 对象列表构造。

```py
segments = [
    Segment("Hello, "),
    Segment("World", Style(bold=True)),
    Segment("!")
]
strip = Strip(segments)
```

Strip 构造函数有一个可选的第二参数，它是 strip 的 cell length：

```py
strip = Strip(segments, 13)
```

注意 cell length 参数不是 string 的字符数量总数，而是 Terminal 中 cells 的数量。终端上两个 cell 的宽度等于一个 cell 的高度。

注意一个中文字符或表情符号占据两个西方字母的空间。如果不能提前知道 segments 能占据的 cells 数量，最后忽略 length 参数，让 Textual 自动计算长度。

### Component classes

当对 widgets 应用样式，可以用 CSS 选择 child widgets。但是使用 line API 渲染的 widgets 没有 children，就像最简单的用 render 渲染的 widget。然而还是可以通过定义 component classes 来使用 CSS 为 widget 的部分添加样式。

Line API 渲染的 widget 和 render() 渲染的 widget 都是最基础的 widget，它们直接提供渲染的内容（text 或 renderables），没有 child 组件。另一种组件是自己不渲染，而是组合 widget 的复合组件（compose）。

CSS 是以组件为单位应用样式的，它定义的样式直接应用到整个组件。

对于普通 widget，只能使用 Rich renderables 的 Console Markup 来定义内容的样式，无法使用 CSS 样式。

对于 Line API Widget，虽然不能将 CSS 样式应用到整个组件，但是可以用 CSS 的方式定义样式，然后在 code 中将其解析为 Style 对象，然后手动为一行的内容中的部分应用这个 Style。因为一行就是一个 Strip 对象，一个 Strip 对象是一组 Segments，一个 Segments 是一个 text 加上一个 Style。Component class 就是用 CSS 的方法定义样式，然后应用到 Segment 上。

COMPONENT_CLASSES 是 widget 的类变量，它是一个 set(), 集合中是一组 css class 的名字，每个 class 的具体样式在使用普通方法定义（App 的 CSS/CSS_PATH 或 Widget 的 DEFAULT_CSS）。然后再 code 中使用 widget.get_component_rich_style("className") 获得指定 class 的具体样式，返回 Style 对象，之后将 Style 应用到 Segment 上就可以了。

Style 就是一组样式在 code 中的表示对象。每个属性对应一个 css 样式。

```py
class CheckerBoard(Widget):
    """Render an 8x8 checkerboard."""

    COMPONENT_CLASSES = {
        "checkerboard--white-square",
        "checkerboard--black-square",
    }

    DEFAULT_CSS = """
    CheckerBoard .checkerboard--white-square {
        background: #A5BAC9;
    }
    CheckerBoard .checkerboard--black-square {
        background: #004578;
    }
    """

    def render_line(self, y: int) -> Strip:
        """Render a line of the widget. y is relative to the top of the widget."""

        row_index = y // 4  # four lines per row

        if row_index >= 8:
            return Strip.blank(self.size.width)

        is_odd = row_index % 2

        white = self.get_component_rich_style("checkerboard--white-square")
        black = self.get_component_rich_style("checkerboard--black-square")

        segments = [
            Segment(" " * 8, black if (column + is_odd) % 2 else white)
            for column in range(8)
        ]
        strip = Strip(segments, 8 * 8)
        return strip
```

Component Classes 的类名通常以组件名开头，跟着两个短线，然后描述性的 class 名字。这可以避免名字冲突。

### Scrolling

Line API widget 可以通过扩展 ScrollView 类（而不是 Widget）来进行滚动。

ScrollView class 完成绝大部分工作，但是我们需要管理一下细节：

- ScrollView 类需要一个 visual size，它是 scrollable content 的 size，可以通过 virtual_size 属性设置。如果它比 widget（ScrollView）的 size 大，Textual 将会添加滚动条。virtual size 描述被滚动内容的虚拟完全大小。
- 实现 render_line 方法来为 widget 的可见区域生成 strips。

ScrollView 组件有一个 scroll_offset 属性，它是一个 tuple，指示 scroll 的 Offset 位置。

Strip 有一个 crop 方法，类似 string.substr(start, end)，截取一行的内容，start 可以设置为 scroll_offset.x，end 设置为 scroll_offset.x + size.width。size 是 Widget 的属性，指示 widget 的大小。

可以动态按需更新 virtual_size 属性。

Strip 对象是 immutable，如果有更新，返回新的 Strip，而不是修改原有的 Strip。

### Region updates

Line API 使得刷新 widget 的一部分称为可能，最小可以是单个字符。刷新更小区域使得更新更高效，保持 widget 的响应。

events.MouseMove 包含 offset，指示鼠标的位置。

```py
from textual.geometry import Offset, Region, Size
```

textual.geometry 包含各种向量计算相关类，可以像 Unity 的 Vector，Rect 一样计算。

```py
def watch_cursor_square(self, previous_square: Offset, cursor_square: Offset) -> None:

    def get_square_region(square_offset: Offset) -> Region:
        x, y = square_offset
        region = Region(x * 8, y * 4, 8, 4)
        # Move the region in to the widgets frame of reference
        region = region.translate(-self.scroll_offset)
        return region

    self.refresh(get_square_region(previous_square))
    self.refresh(get_square_region(cursor_square))
```

Widget.refresh(Region) 告诉 Textual 只更新指定区域，而不是整个 widget。

Textual 可以只能执行更新。如果刷新多个区域，Textual 会将它们合并成尽可能少的 non-overlapping regions。

on_mouse_move handler 处理鼠标移动事件，MouseMove 对象中可以获取鼠标的当前位置。

默认 widget 更新整个 widget 的内容。Line API（render_line）被 Textual 调用按行生成整个 widget 的内容。它是 widget 的全部大小，可能是内容的部分大小。但是 refresh(Region) 可以只更新 Widget 的部分区域。生成 widget 内容（逐行 Strips）仍然是全部生成，即 Textual 会调用 render_line 依次为 widget 的每一行生成内容，最终得到 widget 的全部内容，但是不会将全部内容都刷新到 Screen 上，而是只将指定 Region 的内容更新到 Screen 上。通常生成内容是非常快的，但是对于很大的 Widget，每次都刷新全部区域（尤其是只有部分区域有变化时）可能会导致屏幕闪烁。这与 GUI 中的脏区绘制技术一样。计算是省不了的，但是计算结果只会更新部分区域到 screen 缓冲区中。

## Compound widgets

提供 render 和 render_line 的都是直接渲染组件的内容，没有 child 组件，是最基本的组件。还可以将组件组合来创建新的组件。这类似 Unity 中的 Text/Image 和 Layout Controller 一样。

组合的 widgets 称为 compound widgets。复合组件可以像其他 widget 一样使用。复合组件和基本组件的唯一区别是，基本组件提供 render 方法，复合组件提供 compose 方法。

复合组件将一堆组件打包在一起，是它可以在其他地方重用。

## Coordinating widgets

Widgets 很小会单独存在，通常需要与 app 其他的组件彼此通信或交换数据。

如果组件之间相互依赖，就会组件很难重用。

为了确保组件的可重用性，要遵循 "attributes down, messages up" 的原则。widget 可以直接访问操作 child 的属性，或调用它的方法，但是 widgets 只能通过发送消息与它的 parent 通信。如果想与 sibling 通信，可以将消息发送给 parent，然后由 parent 协调两个 child 之间的通信。

这个与软件架构组织是一样的原则，即树形组织。parent 直接访问 child，child 不能直接引用 parent，而是通过 message 向外发送消息。Sibling 之间由 parent 协调通信。

这会比直接访问更费事一点，但是遵循明确的设计原则，会产生清晰简单的结构，大大减少扩展和维护的代价。

### Messages up

自定义消息：

```py
from textual.message import Message
from textual.reactive import reactive

# 自定义消息
class BitChanged(Message):
    """Sent when the 'bit' changes."""

    def __init__(self, bit: int, value: bool) -> None:
        super().__init__()
        self.bit = bit
        self.value = value
```

发送消息：

```py
widget.post_message(BitChanged(bit, value))
```

消息发送后，从这个组件一路向上查找处理函数，处理函数的名称为 on_class_name_message_name。


