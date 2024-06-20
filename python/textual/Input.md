# Input

## Keyboard input

接收 input 的最基础方式是 Key events。当用户按下按键时，Key events 被发送到 app 中。

```py
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog


class InputApp(App):
    """App to display key events."""

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)


if __name__ == "__main__":
    app = InputApp()
    app.run()
```

### Key Event

key event 包含以下属性：

- key

  key 属性是一个字符串，指示哪个按键被按下。对单个字母、数字按键，是一个字符的 string，对控制键是一个描述控制键的 string。

  按下 shift 时，字母键的 key 变成大写字母。对于非打印 keys，key 属性将会加上 shift+ 前缀。例如 Shift + Home 组合键，event.key 将是 "shift+home".

  按下 ctrl 时，event.key = "ctrl+{key}".

  不是所有的 key 组合在 Terminal 都支持，一些 keys 可能被 OS 截获。

- character

  如果 key 有一个可打印字符，character 包含一个 Unicode character 的 string。否则 character 为 None。

- name

  name 类似 key，但是它可以保证是一个有效的 Python 函数名。例如按下 ctrl + p，name 将会是 ctrl_p. 如果字母是大写的，name 将加上前缀 upper_. 例如按下 shift + p，name = upper_p. 这可以直接用于映射到一个 Python 函数。

- is_printable

  is_printable 属性是一个 boolean，只是 key 是否可以产生一个可打印字符。

- aliases

  一些键或键的组合可以产生相同的 event。例如，在终端中，Tab key 和 ctrl + I 是一样的。对于这样的键，Textual events 将会包含可能产生这个 event 的所有 key 组合列表。前面这种情况，aliases 将会包含 ["tab", "ctrl+i"].

### Key methods

Textual 提供了一种简便方法来处理特定 keys。如果方法名为 key_{name}，name 等于 event 的 name 属性的值，则这个方法会被 Textual 调用来响应相应的 key 事件。

```py
def on_key(self, event: events.Key) -> None:
    self.query_one(RichLog).write(event)

def key_space(self) -> None:
    self.bell()
```

key_space 就会被 Textual 自动调用来处理 Space 按键事件。

将 key methods 视为体验 Textual 特性的便捷方法。几乎在所有情况下，key bindings 和 actions 更合适。

## Input focus

同一时间只有一个 widget 接收 key。当前正在接收 key events 的 widget 被称为具有 input focus。

key event 只会发送到具有 input focus 的 widget。

:focus 伪类可以用来给 focused widget 添加样式。

可以通过按 Tab 键将 focus 移动到下一个 widget。Shift+Tab 向相反方向移动 focus。

### Controlling focus

Textual 会自动处理 keyboard focus。但是可以通过调用 widget.focus() 告诉 Textual focus 一个 widget，此后这个 widget 称为唯一接收 key event 的 widget。

### Focus events

如果一个 widget 收到 focus，Textual 将会向它发送一个 Focus event。当 widget 失去 focus，Textual 向它发送一个 Blur event。

## Bindings

Keys 可以为给定的 widget 关联 actions。这称为 key binding。

要创建 bindings，为 App 或 widget 添加一个 BINDING 类变量。它是一个 (string, string, string) 的 tuple 的 list。Tuple 的第一个值是 key，第二个是 action，第三个是简短的可读描述。

```py
class BindingApp(App):
    BINDINGS = [
        ("r", "add_bar('red')", "Add Red"),
        ("g", "add_bar('green')", "Add Green"),
        ("b", "add_bar('blue')", "Add Blue"),
    ]

    def compose(self) -> ComposeResult:
        yield Footer()

    def action_add_bar(self, color: str) -> None:
        bar = Bar(color)
        bar.styles.background = Color.parse(color).with_alpha(0.5)
        self.mount(bar)
        self.call_after_refresh(self.screen.scroll_end, animate=False)
```

Footer 中会显示 bindings，并使它们变成可点击的，点击它效果等价于按下按键。

### Binding class

对于简单的 bindings，3-string 足够了。但是还可以使用 Binding 实例来替换 tuple，它提供了更多的选项来控制 binding。

### Priority bindings

单个 bindings 可以被标记为 priority，这意味着它们在 focused widget 的 bindings 之前被检查。这个特性通常用于在 app 或 screen 上创建 hot-keys。这样的绑定不可以一个 widget 上相同的 key binding 关闭。

要创建 priority key bindings，要使用 Binding 实例，并设置 priority=True 参数。Textual 使用这个属性为 ctrl+c 添加一个 default binding，使得总能退出应用程序。下面是 App 基类的 bindings：

```py
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("tab", "focus_next", "Focus Next", show=False),
        Binding("shift+tab", "focus_previous", "Focus Previous", show=False),
    ]
```

### Show bindings

Footer widget 可以显式可用的 key bindings。如果不想在 Footer 上显示 key bindings，设置 show=False.

## Mouse Input

Textual 会为鼠标移动和点击发送事件。这些事件包含鼠标光标相对于 Terminal 或 widget 的坐标。

Terminal 坐标的 x 是 screen/widget 从左到右的 offset，y 是 screen/widget 从上到下的 offset。

坐标可以相对于 screen，也可以相对于 widget。

### Mouse movements

当在一个 widget 上移动鼠标时，widget 将会接收到 MouseMove events，它包含鼠标的坐标，和哪些 modifier keys（ctrl、shift 等）按下的信息。

### Mouse capture

Textual 会向 cursor 下面的 widget 发送 mouse event events。但是可以通过调用 widget.capture_mouse() 将所有 mouse events 发送给这个 widget，而不管 mouse cursor 的位置。

这类似 key events 的 focus() 方法，显式将一个 widget 作为当前 key events 或 mouse events 的发送目标。

调用 widget.release_mouse() 来恢复 default behavior。

注意，当 widget capture mouse 时，可能收到负数的鼠标坐标。

当 mouse 被 captured 时，Textual 会向 widget 发送 MouseCapture event，release capture 时会发送 MouseRelease event。

### Enter and Leave events

当鼠标首次进入 widget 时，Textual 向 widget 发送 Enter event。当鼠标离开 widget 时，发送 Leave event。

### Click events

当用鼠标点击 widget 时，Textual 会向 widget 发送 3 个事件。初始按下时，发送 MouseDown event。鼠标释放时，发送 MouseUp event。最后发送一个最终的 Click event。

如果想要 app 响应鼠标点击，最好使用 Click event（而不是 MouseDown 或 MouseUp）。

### Scroll events

绝大多鼠标都有一个滚动轮，可以用于滚动鼠标下面的 widget。Textual 中 Scrollable 容器将会自动处理这些，但是如果想构建自己的滚动功能，可以处理 MouseScrollDown 和 MouseScrollUp。

