# App Basics

构建一个 Textual App 第一步就是 import App 类，然后创建一个子类。

```py
from textual.app import App

class MyApp(App):
    pass

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

当 App.run() 运行时，Textual 将 terminal 置于一个特殊状态，称为 application mode。

Application mode 下，terminal 不会再回显你的按键。Textual 负责响应你的输入（键盘和鼠标），并且更新 terminal 的可见部分。

按下 Ctrl+C 将会退出 application mode，并且返回命令行提示。


进入 application mode 的一个副作用是，不能够再想往常那样选择和复制文本了。终端通常会提供一种方法，使用一个 key modifier 来解决这个问题。在 iTerm 上，可以按下 Option 键来选择和复制文本，在 Windows 上是 shift 键。


## Run inline

还可以以 inline 模式运行 app，这会导致 app 出现在 prompt 下面，并且不会进入 application 模式。Inline apps 非常适合于终端紧密集成的工作流。

要以 inline 模式运行 app，App.run(inline=True)。

Inline 模式当前不支持 Windows。


## 事件 Events

Textual 有一个事件系统可以响应按键、鼠标、内部状态变化。每个 Event handler 方法都一个 on_ 开头，后面跟着事件的名字。

一个 event 是 mount，当程序进入 application mode 之后，被发送给 app，可以定义 on_mount 来响应这个事件。

on_key 处理按键事件，事件参数 events.Key，它的 key 属性包含按下的按键信息。

## 异步事件

Textual 是基于 Python asyncio 框架的。

如果 event handler 方法是 coroutine 的，Textual 会 await 它。

## Widgets

Widgets 是自包含组件，负责生成 Screen 上一块区域的 output。Widgets 使用于 App 相同的方式响应事件。大多数 App 都会包含至少一个（可能很多个）widgets，它们一起构成了 User Interface。

Widgets 可以简单如 text，button，或者复杂如 text editor 或 file browser（它们可以包含自己的 widgets）。

## Composing

为 app 添加 widgets，使用 compose() 方法，它应该返回一个 widget 实例的 iterable。可以是一个 list，但是 yield widgets 更方便（它使方法变成 generator）。

## Mounting

Compose 用于在程序初始启动时添加 widgets，还可以使用 mount() 在运行时动态添加 widget 到 UI。

当 mount 一个 widget，Textual 会 mount 这个 widget composes 的每个组件。Textual 保证 mounting 在下一个 message handler 之前完成，但是不会再 mount() 结束之后立即完成。因此 mount() 会后立即 query 新添加的 widget 会查询不到。

为此，可以选择 await mount()，这需要将方法本身声明为 async 的，例如 event handler 方法。wait mount() 之后，就可以保证所有子组件已经 mount 好了。

## 退出

App 会持续运行，直到你调用 App.exit()，它退出 application mode（但不一定退出程序本身，只是终端退出 application mode），app.run() 方法会返回，后面的程序就想一个普通的 python 程序了。

App.exit() 可以接收一个可选的位置参数作为 run() 的返回值。

Subclass App 时，可以加上 type hints 声明返回值的类型：

```py
class QuestionApp(App[str]):
    def compose(self) -> ComposeResult:
        yield Label("Do you love Textual?")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id) 
```

## 挂起

可以挂起 Textual app（就像 ctrl + z 挂起 vim 一样），使得你可以离开 application mode 一段时间，之后再恢复。这通常可以用来使用其他的 terminal applicaiton（例如 vim）临时替换 Textual app。

例如可以使用 text editor 来允许用户编辑内容。

### Suspend context manager

可以使用 App.suspend context manager 来挂起程序：

```py
from os import system

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button


class SuspendingApp(App[None]):

    def compose(self) -> ComposeResult:
        yield Button("Open the editor", id="edit")

    @on(Button.Pressed, "#edit")
    def run_external_editor(self) -> None:
        with self.suspend():  
            system("vim")


if __name__ == "__main__":
    SuspendingApp().run()
```

### 前台挂起

在 Unit 或 Unix-like 系统上（GNU/Linux, macOS），Textual 支持用组合键将进程作为前台挂起。终端中原始挂起组合键 Ctrl+Z 在 Textual app 中默认是关闭的，但是提供乐意 action_suspend_process 来支持这种常规挂起：

```py
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Label


class SuspendKeysApp(App[None]):

    BINDINGS = [Binding("ctrl+z", "suspend_process")]

    def compose(self) -> ComposeResult:
        yield Label("Press Ctrl+Z to suspend!")


if __name__ == "__main__":
    SuspendKeysApp().run()
```

但是这在 Windows 上不支持。

## CSS

Textual app 可以引用 CSS 文件来定义 app 和 widgets 的外观。而让 Python code 只定义逻辑。

Textual 是几种炫酷的技术集成：Terminal + LightWidget UI + Python + asyncio + CSS。

Textual CSS 文件名通常以 tcss 结尾，以区分于 web 的 css 文件。t 代表 Textual。

CSS_PATH 类变量应用一个外部的 css 文件对 App 进行样式化。注意它是 App 类的类变量，即一个 App 引用一个 css 文件。css 文件路径可以是相对的，也可以是绝对的。

建议对大多数程序使用外部的 CSS 文件，它可以开启一些很酷的特性，例如 live editing。但是还可以直接在 code 中指定 CSS 样式。

在 App 类定义类变量 CSS 来定义内置的 CSS 样式。

## Title and subtitle

App 有一个 title 属性（通常是 app 的名字），和一个可选的 sub_title 属性（提供额外信息，例如正在操作的文件名）。

默认 title 是 App class 的名字，sub_title 是空的。

可以使用 App 类变量 CSS_PATH/SUB_TITLE 定义它们，也可以使用 app.title/app.sub_title 在 code 中动态定义它们。

