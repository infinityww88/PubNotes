# Actions

Actions 是可以使用 string 语法嵌套在 links 或绑定到 keys 的允许函数列表。

## Action methods

Action 方法是 app 或 widget 的以 action_ 为前缀的方法。Action 方法可以是 coroutines（async）。

Actions 的意图是在一个 action string 中被解析，例如 "set_background('red')" 是一个 action string，它会调用 widget.action_set_background('red').

可以显式用 action string 调用 action：

```py
async def on_key(self, event: events.Key) -> None:
    if event.key == "r":
        await self.run_action("set_background('red')")
```

注意 run_action 是一个 coroutine 方法。

实际中不需要显式调用 action，因为 Textual 会在 links 或 key bindings 中运行 actions。

## Syntax

Action strings 有一个简单语法，几乎就是 Python 函数调用语法的重复。但是 Textual 不会调用 Python 的 eval 函数来编译 action strings.

Action strings 格式如下：

- 只有 action name 的 string 将会以无参数的形式调用 action 方法。例如 "bell" 调用 action_bell()
- action name 后面可以跟着括号，包含 Python objects。"set_background('red')" 会调用 action_set_background("red")
- action string 可以以一个 namespace 和 dot 为前缀

### parameters

如果 action string 包含参数，参数必须是有效的 python 字面量，这意味它们可以是 numbers，strings，dicts，lists 等等，但是不可以包含变量或其他 Python 符号。

## Links

Actions 可以嵌套在 Console Markup 的 links 中。可以使用 @click 创建这样的 links。

```py
from textual.app import App, ComposeResult
from textual.widgets import Static

TEXT = """
[b]Set your background[/b]
[@click=set_background('red')]Red[/]
[@click=set_background('green')]Green[/]
[@click=set_background('blue')]Blue[/]
"""

class MyLabel(Static):

    def action_set_background(self, color: str) -> None:
        self.screen.styles.background = color

class ActionsApp(App):

    BINDINGS = [
        ("r", "set_background('red')", "Red"),
        ("g", "set_background('green')", "Green"),
        ("b", "set_background('blue')", "Blue"),
    ]

    def compose(self) -> ComposeResult:
        yield MyLabel(TEXT)

    def action_set_background(self, color: str) -> None:
        self.screen.styles.background = color


if __name__ == "__main__":
    app = ActionsApp()
    app.run()
```

注意 action string 调用的 action 必须在它嵌入的 widget 上，否则会找不到 action 方法。

点击 link 就会执行相应的 action。

## Bindings

Textual 可以为 App 绑定 key 到 action 上（只对 App 有效，对 Widget 无效）。

action 方法必须在 App 中。

Actions string 对 Console Markup links 更有用，因为这免去了实现可点击 link 的一大堆逻辑。但是对 Key binding 并不是太有用，因为用普通 key event 很容易实现调用 key 对应的逻辑。

## Namespaces

Textual 在 action string 所在的 App/Widget 中查找 action methods。

可以为 action 添加一个 namespace，告诉 Textual 在一个不同的 object 上运行 action 方法：

- app 在 App 实例上调用 action 方法
- screen 在 screen 上调用 action 方法
- focused 在当前 focused widget（如果有的话）调用 action 方法

## Dynamic actions

有时由于一些 App 内部状态的原因，action 临时不可用。例如，考虑一个 app 具有固定数量 pages 和用于导航到上一页或下一页的 actions。如果当前位于第一页，则 Previous Page action 没有意义，同样在最后一页，Next Page action 没有意义。 

很容易添加逻辑到 action 方法处理这些边界条件，但是 footer 总是会显示这些 actions，不管它们是否有意义。

要解决这个问题，可以在 app，screen，或 widget 上实现 check_action。Textual 在运行 actions 或属性 footer 之前，会用 action 的名字和任何参数调用这个方法。它的返回值：

- True：正常显示 key 并运行 action
- False：隐藏 key 并阻止 action 运行
- None：disable key（显式为灰色），组织 action 运行

```py
class PagesApp(App):
    BINDINGS = [
        ("n", "next", "Next"),
        ("p", "previous", "Previous"),
    ]

    CSS_PATH = "actions06.tcss"

    page_no = reactive(0)

    def compose(self) -> ComposeResult:
        with HorizontalScroll(id="page-container"):
            for page_no in range(PAGES_COUNT):
                yield Placeholder(f"Page {page_no}", id=f"page-{page_no}")
        yield Footer()

    def action_next(self) -> None:
        self.page_no += 1
        self.refresh_bindings()  
        self.query_one(f"#page-{self.page_no}").scroll_visible()

    def action_previous(self) -> None:
        self.page_no -= 1
        self.refresh_bindings()  
        self.query_one(f"#page-{self.page_no}").scroll_visible()

    def check_action(
        self, action: str, parameters: tuple[object, ...]
    ) -> bool | None:  
        """Check if an action may run."""
        if action == "next" and self.page_no == PAGES_COUNT - 1:
            return False
        if action == "previous" and self.page_no == 0:
            return False
        return True
```

widget.refresh_bindings() 告诉 Textual 刷新 Footer（以防 bindings 有变化）。另一种实现这个目的的方式是在 reactive 上手动设置 bindings=True，如果 reactive 发生改变，这将会刷新 bindings。

如果将 check_acition 中的 return False 替换为 return None，则当 action 没有意义的时候，binding 将会置灰不可点击，而不是隐藏。

## Builtin actions

Textual 支持很多内置的 actions，可以在 action string 中直接使用：

- action_add_class
- action_back
- action_bell
- action_check_binding
- action_focus
- action_focus_next
- action_focus_previous
- action_pop_screen
- action_push_screen
- action_quit
- action_remove_class
- action_screenshot
- action_switch_screen
- action_suspend_process
- action_toggle_class
- action_toggle_dark

