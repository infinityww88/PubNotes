# Screens

## What is a screen

Screen 是 widgets 的容器，占据整个 terminal。一个 app 可能有很多 screens，但是同一时间只能有一个 screen 活动。

Textual 需要至少一个 screen object，并且在 App 中会默认创建一个。

如果不改变 screen，用 mount() 或 compose() 添加的任何 widgets 都会添加到这个默认 screen 上。

## Creating a screen

可以通过扩展 Screen class 来创建 screen。Screen 可以使用和其他 widget 一样的方式添加样式，除了不能改变它的 dimension（它们总是具有 terminal 的大小）。

```py
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

ERROR_TEXT = """
An error has occurred. To continue:

Press Enter to return to Windows, or

Press CTRL+ALT+DEL to restart your computer. If you do this,
you will lose any unsaved information in all open applications.

Error: 0E : 016F : BFF9B3D4
"""

class BSOD(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Static(" Windows ", id="title")
        yield Static(ERROR_TEXT)
        yield Static("Press any key to continue [blink]_[/]", id="any-key")


class BSODApp(App):
    CSS_PATH = "screen01.tcss"
    SCREENS = {"bsod": BSOD()}
    BINDINGS = [("b", "push_screen('bsod')", "BSOD")]


if __name__ == "__main__":
    app = BSODApp()
    app.run()
```

Screen 和 App 一样，可以定义 Key Action Binding，但是 Widget 不能定义 Key Action Bindings。

BSOD 类定义了一个 screen，具有 key binding 和 compose 方法。它和 app 一样工作。

Screen 可以堆叠，push_screen 和 pop_screen。

App 类的有一个类变量 SCREENS，Textual 用这个类变量定义 name 和 screen object 的映射，后续各种 screen api 都直接使用 screen name。

## Named screens

App.SCREENS（dict） 类变量可以为 screen 关联一个 name。在绝大多数 screen API 中，name 和 screen object 是可以互换的。

和 compose 一样，SCREENS 定义 App 初始时的可用的 Screen。和 mount() 可以动态添加 widget 一样，app.install_screen 可以在运行时动态添加 screen。

```py
self.install_screen(BSOD(), name="bsod")
```

尽管二者都能完成相同的事情，但是建议将 SCREENS 用于在整个 App 生命周期都存在的 screen。

### Uninstalling screens

定义在 Screens 中或者通过 install_screen 的 Screen 成为 installed screens。Textual 会在 app 的生命周期中将它们保存在内存中。如果想移除一个 Screen，调用 app.uninstall_screen.

## Screen stack

Textual apps 保持 screen 的堆栈 stack。可以将 screen stack 想象为一堆纸，只有最上面的可见。如果移除顶层 screen，下面的 screen 就变得可见。

还可以使 top screen 的部分透明，让下层 screen 可见。

Active screen（顶层 stack）渲染屏幕，并接受 input events。下面的 APP 方法可以操作这个 stack，让你决定用户与哪个 screen 交互。

### Push screen

push_screen 方法将一个 screen 放置在 stack 的顶层，并使它变成 active screen。可以用 installed screen 的 name 调用它，也可以用一个 screen object。

注意，要使用 name 来操作 screen，screen 必须是 installed 的（SCREENS 中定义的，或 install_screen 安装的）。如果使用 screen object，screen object 可以是普通的 object，不需要有 name。

#### Action

可以使用 "app.push_screen" action 来 push screens，这需要一个 installed screen 的 name。

### Pop screen

pop_screen 从 stack 移除顶层 screen，并使下面的 screen 变成 active 的。

注意无论是 new 的 screen object，还是 installed 的 screen，都只是保存在内存中对象，不会出现在 App 中。只有 push_screen 后才被 App 显示。pop_screen 将 screen 从 app 中移除。对于 installed screen，screen 仍然会保留在内存中。对于 non-installed screen，screen object 还会被 deleted。

只有 installed 的 screen 才被总是保留。

screen stack 必须至少有一个 screen，否则 pop 会抛出异常。

#### Action

可以用 "app.pop_screen" action pop screens。

### Switch screen

Switch screen 方法用一个新 screen 替换 stack 顶层的 screen。和 pop_screen 一样，被替换的 non-installed 的 screen 会被 removed 和 deleted。

Switch screen = pop + push

#### Action

"app.switch_screen"

## Screen opacity

如果 screen 有一个带 alpha 分量的背景色，background color 将会与下面的 screen 的颜色混合。例如，如果顶层 screen 又给 rgba(0, 0, 255, 0.5) 的 background，则 screen 上没有被 widget 占据的部分将会显示它下面的 screen，tinted with 50% blue.

background alpha 的一个用途是样式化 modal dialogs。

## Modal screens

Screens 可以用于创建 model dialogs。

因为 non-installed screen 在 pop 或 replace 后，会自动销毁，因此非常适合这种临时的 dialog。push 或 switch 时，直接构造一个 Screen 对象即可。

Textual 的 alpha 只在 Screen-Screen，Widget-Screen 之间创建透明混合。

Textual 为这种应用提供一个专门的类 textual.screen.ModalScreen。扩展它实现自定义 screen 的子类。它自动包含透明，只需要在其中添加 widgets，并 install 并 push 即可。

## Returning data from screens

Screen 一个常见的需求是返回 data。例如，可能想要一个 screen 显示一个 dialog，并在 screen 被 pop 后处理 dialog 的结果。

要从 screen 返回 data，使用要返回的 data 调用 screen.dismiss()。这会 pop screen，并调用 screen push 时设置的一个 callback。

```py
# In Screen

def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "quit":
        self.dismiss(True)
    else:
        self.dismiss(False)

# In App

def check_quit(quit: bool) -> None:
    """Called when QuitScreen is dismissed."""
    if quit:
        self.exit()

self.push_screen(QuitScreen(), check_quit)
```

Returning data 的 Screen 可以让 code 更具管理行，让清理逻辑放在调用者一侧，而不需要 Dialog 执行自己工作之外的任务，可以让 Dialog 更好地重用。

### Typing screen results

对于返回 data 的 Screen，可以添加 type hints，例如 ModalScreen\[bool\]

### Waiting for screens

可以 await screen 被 dismissed，可以让逻辑表达更自然，而不必使用一个 callback。app.push_screen_wait() push 一个 screen 并 await 它的结果（screen.dismiss 设置 value）。但是这只可以在一个 worker 中完成，这样 await screen 不会阻止 app 的更新。

```py
@work  
async def on_mount(self) -> None:
    if await self.push_screen_wait(QuestionScreen("Do you like Textual?")):
        self.notify("Good answer!")
    else:
        self.notify(":-(", severity="error")
```

@work 使得 on_mount 在一个 worker（background task）中运行，使 app 的 message queue Task 立即返回，去处理下一个 message。

## Modes

一些 apps 会从 multiple screen stacks 而不是 single screen stack 受益。尤其是具有多种独立功能的 app，每个功能使用一个单独的 screen 是很正常的。但是当这样的 screen 具有 modal dialog 时，我们不希望阻止用户在独立的功能之间进行切换。这样我们希望每个独立的 screen 有一个单独的 navigation stack，可以在其中 push 和 pop screens。

在 Textual 中可以用 modes 管理这种功能。

mode 简而言之就是一个命名的 screen stack，我们可以在 screen stack 之间切换，而不仅仅是在一个 stack 中的 screen 之间切换。当切换 modes 时，新 mode 的最顶层 screen 就变成 active visible screen。 

和其他 App 的类变量一样，要为 app 添加 modes，在 App class 中定义一个类变量 MODES，它是一个 dict，映射 mode name 到一个 screen object，一个返回 screen 的 callable，或者 installed screen 的 name。指定的这些 screen 设置了每个 mode screen stack 的 base screen。

可以在任何时候调用 app.switch_mode 来切换这些 mode screen stack。app.push_screen 或 app.pop_screen 只会应用在当前 active mode 的 stack 上。

注意 MODES 只是被 Textual 用来初始化所有 mode statck 的参数，它本身不是 mode stacks，Textual 在自身内部创建和维护 mode stack。

## Screen events

在 screen 由于其他 screen 被 push 或切换 mode 而变得不可见时，Textual 会向 screen 发送 ScreenSuspend event。

当 screen 变成 active 时，Textual 会向新 active screen 发送一个 ScreenResume event。

