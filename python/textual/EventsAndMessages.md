# Events and Messages

## Messages

Events 是被 Textual 发送的一种特殊类型的 message，以响应 input 和其他状态变化。

Events 是被 Textual 保留内部使用的 message，但是可以创建自定义 messages 来在 app 中的 widgets 之间协作。

总之 Event 也是 message，对 message 成立的事情，对 events 也一样成立。

## Message Queue

每个 App 和 Widget 都包含一个 message queue，处理各自的 message。

消息是在一个 asyncio Task 中处理的，这个 Task 在 widget mount 时开始，它监视 queue 中新的 message，并将它们分发到合适的 handler。

## Default behaviors

Python 中的 super 可以调用基类定义的函数。Textual 中不必显式调用 widget 基类中定义的 event handlers，Textual 会自动调用它。

假设 Paddle 扩展 Static，而 Static 扩展自 Widget。如果在 Paddle 按下 key，Textual 会先调用 Paddle.on_key，然后调用 Static.on_key，最后调用 Widget.on_key。

基类定义的 event handler 就是 default behavior。

### Preventing default behaviors

调用 event.prevent_default() 告诉 Textual 不会继续调用基类上的 handlers。

## Bubbling

Message.bubble 属性如果为 True，event 会在处理之后被发送给 widget 的 parent。

上面的 Default behavior 是关于是否调用 widget class 基类的 handler（仍然是在一个 widget 上的），而 bubbling 是关于是否将消息传递到 widget 的 parent widget 的（另一个 widget）。另外 default behavior 是关于 event 的，它需要在 event 对象上调用 prevent_default()，而 bubbling 是关于 message 的。

Input events 通常 bubble，这样一个 widget 将会有机会响应 input events（如果它们的 children 不处理事件的话）。

App 总是 DOM 的 root，它总是能在最后接收消息，但是不会再向上 bubbling。

### Stop bubbling

与 event 可以阻止继续调用 widget 基类的 handler 一样，message 也可以通过调用 event.stop() 或 message.stop() 方法停止向上 bubble。

## Custom messages

可以创建自定义 message，它们可以想 events 一样被使用（event 就是 Textual 保留的 message 而已）。

这通常用于 child widget parent 通知状态变化（child 不应该直接引用 parent，以促进可重用性）。

- 定义消息

  ```py
  class Selected(Message):
      """Color selected message."""
  
      def __init__(self, color: Color) -> None:
          self.color = color
          super().__init__()
  ```

- 发送消息

  ```py
  def on_click(self) -> None:
      # The post_message method sends an event to be handled in the DOM
      self.post_message(Selected(self.color))
  ```

- 接收消息

  ```py
  def on_color_button_selected(self, message: Selected) -> None:
      self.screen.styles.animate("background", message.color, duration=0.5)
  ```

自定义消息扩展 Message。它通常定义在 widget 内部。这不是必须的，但是建议如此，因为消息是和 widget 紧密相关的，而紧密相关的东西应该放在一起，并且还为 Message 创建了名字空间，避免了命名冲突。

### Sending messages

每个 widget 都有一个 post_message 方法，它将消息放在 widget 的消息队列中，然后由 widget 处理消息的 asyncio Task 处理，并运行各种 message handlers（向上 bubble）。

注意 Textual event 是由 Textual 将 event 放在 widget 的 message queue 的，而自定义消息是由 widget 自己将消息放在 queue 的。

通常，widget 也会为它们自己发送消息，并允许它们 bubble。这样 widget 的基类就有机会处理 message（default handler），这需要 widget 或它的基类自己定义好 handler。

## Prevent messages

可以调用 widget.prevent() 临时禁止发送特定类型的消息。它以一个消息类型为参数，返回一个 context manager，用在 python with 语句中。这通常用于更新 child widget 的数据时不想收到状态发生改变的消息。

## Message handlers

Textual app 大部分逻辑写在 message handlers 中。

### Handler naming

Textual 使用下面的约定来确定 message 的 handler 方法：

- 以 on_ 开始
- 以驼峰式命名添加 message 的 namespace 和 _
- 以驼峰式命名添加 message 类名

on_{namespace}_{classname}

如果不确定消息 handler 名字，message 类的 handler_name 包含 handler 名字字符串。

### On decorator

除了使用上面的命名约定，还可以使用 on 描述符来定义一个消息的 handler。

```py
@on(Button.Pressed)
def handle_button_pressed(self):
    ...

def on_button_pressed(self):
    ...
```

使用 on 描述符的优势：

- handler 方法可以是任何名字
- 可以指定想要为哪些 widget 处理消息

这通常发生在 container widget 上。如果一个 container 的多个 child widget 会发送相同的消息，container 必须想办法区分消息的发送者，这通常通过 event.widget.id 来实现的。

但是 on 描述符可以传递一个 css 选择器，这可以让 container 指定一个 handler 只为这些 widgets 处理某个类型的消息：

```py
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button


class OnDecoratorApp(App):
    CSS_PATH = "on_decorator.tcss"

    def compose(self) -> ComposeResult:
        """Three buttons."""
        yield Button("Bell", id="bell")
        yield Button("Toggle dark", classes="toggle dark")
        yield Button("Quit", id="quit")

    @on(Button.Pressed, "#bell")  
    def play_bell(self):
        """Called when the bell button is pressed."""
        self.bell()

    @on(Button.Pressed, ".toggle.dark")  
    def toggle_dark(self):
        """Called when the 'toggle dark' button is pressed."""
        self.dark = not self.dark

    @on(Button.Pressed, "#quit")  
    def quit(self):
        """Called when the quit button is pressed."""
        self.exit()


if __name__ == "__main__":
    app = OnDecoratorApp()
    app.run()
```

注意 on decorator 需要 message class 有一个 control 属性，它应该返回和 message 关联的 widget（发送消息的 widget）。内置的 widget 的消息都有这个属性，但对于自定义消息，需要添加 control 属性。

如果有多个 decorated handlers 匹配消息，它们将会按照定义的顺序依次调用。

如果同时存在 on decorated handler 和命名约定的 handler，前者先运行，后者后运行。

#### Apply CSS selectors to arbitrary attributes

on decorated handle 还可以以关键字参数接受一个 selector，用来匹配 message 的其他属性，这些属性定义在 Message.ALLOW_SELECTOR_MATCH 中。

下面的示例中，只有 tab 的 id 属性等于 home 时，才匹配这个 message。

```py
@on(TabbedContent.TabActivated, pane="#home")
def home_tab(self) -> None:
    self.log("Switched back to home tab.")
    ...
```

### Handler arguments

Message handler 方法可以包含一个位置参数，也可以没有。如果包含，Textual 将为这个参数传递 event object。

```py
def on_color_button_selected(self) -> None:
        self.app.bell()

def on_color_button_selected(self, message: ColorButton.Selected) -> None:
    self.screen.styles.animate("background", message.color, duration=0.5)

@on(ColorButton.Selected)
def animate_background_color(self, message: ColorButton.Selected) -> None:
    self.screen.styles.animate("background", message.color, duration=0.5)
```

### Async handlers

Message handlers 可以是 coroutines。如果 handler 带有 async 关键字，Textual 将会 await 它。这可以让 handler 使用 await 关键字使用 异步 API。

如果 event handlers 是 coroutines 的，这可以允许多个 events 并行处理。但是一个单独的 widget 或 app 在 handler（无论是同步还是异步）返回之前不能从 queue 取出下一个消息。之前说的多个 events 并行处理指的是 app 中多个 widgets 可以并行处理它们各自的 message，否则如果任何一个 widget 的 message handler 是同步的话，整个 app 都会停下来等等这个 handler 执行完毕。因为 Textual 是基于 asyncio 的，app 是单线程的。但是具体到单个 widget 或 app，handler 无论是同步还是异步，都只能处理完一个消息才处理下一个。

但是因为 Textual 是基于 asyncio 的，可以自己在 event loop 中异步地执行 handler 中的逻辑，而让 handler 即时返回，这样 widget 或 app message queue Task 就不用等待 handler 逻辑执行完再去处理下一个消息了。

例如 Network access 是一个场景的 slow handlers。如果尝试从 internet 获取一个文件，message handler 可能要花费好几秒才返回，这将阻止 widget 或 app 在此期间更新。解决方案就是创建一个新的 asyncio Task 在后台执行网络任务，让 handler 立即返回去处理其他消息。

```py
async def on_input_changed(self, message: Input.Changed) -> None:
    asyncio.create_task(self.network_task(message.value))
```

