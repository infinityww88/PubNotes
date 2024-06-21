# Workers

## Concurrency

Textual 的很多有趣应用需要从 internet service 读取数据。

如果一个 app 需要从 network 请求数据，让网络请求不要阻止 UI 更新非常重要。换句话说，网络请求必须是并行的，这对那些需要一定时间完成的任务也是一样，必须要独立 UI updating 进行。

## Workers

所有 message/event 都是在一个 Message Queue Task 中 handle 的。Task 从 queue 取出一个 message 进行分发，执行所有的 handler，直到这个 message 处理完之后，才去处理下一个。如果 handler 就是简单的函数，那么它会阻塞整个 app 的运行。如果 handler 是 coroutines，虽然不会阻止整个 app 的运行，但是会阻塞 Message Queue Task 的运行，因为 Task 会 await 它的结果，因此仍然会阻塞这个 widget 的 UI 更新。要解决这问题 handler 必须在一个新的 asyncio task 中执行，让 handler 立即返回。这个新的 task 就是 Worker。

Textual 的 app/widget 提供了 run_worker 方法，来在一个新的 asyncio task 运行一个 async handler，让 message handler 立即返回：

```py
async def on_input_changed(self, message: Input.Changed) -> None:
    """Called when the input changes"""
    self.run_worker(self.update_weather(message.value), exclusive=True)

async def update_weather(self, city: str) -> None:
    pass
```

run_worker 方法返回一个 Worker object。exclusive=True 可以让 Textual 在开始一个新的 worker 之前先 cancel 这个 task 之前的 worker。因为所有的 worker 都是并行执行的，如果同时发送了多个网络请求，有可能更早发送的请求更晚返回，导致一些逻辑上的问题。

### Work decorator

除了手动调用 run_worker，另一种创建 worker 的方法是 work decorator，它自动将装饰的方法变成 worker。

```py
async def on_input_changed(self, message: Input.Changed) -> None:
    """Called when the input changes"""
    self.update_weather(message.value)

@work(exclusive=True)
async def update_weather(self, city: str) -> None:
    pass
```

### Worker return values

worker.result 属性记录 worker 函数的返回值。它初始时是 None，但是在 function 完成后会替换为 function 的返回值。

如果需要返回值，调用 worker.wait。它将会等待 worker 完成。但是如果在 message handler await 它仍然会向之前那样阻塞 widget 的 updating，直到 worker 返回。更好的方式是处理 worker events，它在 worker 完成时通知 app。

### Cancelling workers

Worker.cancel 可以在任何时候 cancel 一个 worker。这会在 coroutine 内部 raise 一个 CancelledError 异常，让 worker function 提前退出。

### Worker errors

当 worker 遇到异常时，默认行为是退出 app，并在 terminal 中显示 traceback。如果不想在异常时立即退出，可以用 exit_on_error=False 创建 worker。

### Worker lifetime

Workers 被一个 WorkerManager 实例管理，可以通过 app.workers 访问。这是一个 container-like object，可以 iterate 来查看 active workers。

Workers 被绑定到创建它们的 DOM node（widget，screen，app）。这意味着如果移除 widget，或 pop screen，它们关联的 worker 会自动清理。类似的，如果退出 app，任何运行的 tasks 都会被 cancelled。

Worker objects 有一个 state 属性，它会包含一个 WorkerState 枚举，它指示 worker 的当前状态：

- PENDING：worker 被创建，但是还没开始
- RUNNING：worker 正在运行
- CANCELLED：worker 被 cancelled，不再运行
- ERROR：worker 遇到异常，worker.error 包含异常
- SUCCESS：worker 成功运行完毕，worker.result 包含函数返回值

### Worker events

当 worker 改变状态，它发生 Worker.StatgeChanged event 到创建它的 widget。可以通过定义 on_worker_state_changed event hander 来处理它。

### Thread workers

对于 asyncio API 可以使用 worker 来并行运行。但是对于同步的 API，只能使用 threads 来并行运行。

可以在 run_worker 方法或 work 装饰器中传递 thread=True 来创建 Thread 运行的 worker。Thread workers API 和 async workers 的 API 是相同的，但是有一些需要注意的地方：

- 避免在 thread worker 中调用 UI 相关方法，或设置 reactive variables。可以使用 app.call_from_thread 方法在 main thread 调度一个 task 来绕过这个问题 
- 不能像 coroutine 一样 cancel threads，但是可以手动检测 worker 是否被 cancelled

对于网络访问，Python 的标准库 urllib.request 是同步网络 API，httpx 库是异步网络 API。

```py
async def on_input_changed(self, message: Input.Changed) -> None:
    """Called when the input changes"""
    self.update_weather(message.value)

@work(exclusive=True, thread=True)
def update_weather(self, city: str) -> None:
    """Update the weather for the given city."""
    weather_widget = self.query_one("#weather", Static)
    worker = get_current_worker()
    if city:
        # Query the network API
        url = f"https://wttr.in/{quote(city)}"
        request = Request(url)
        request.add_header("User-agent", "CURL")
        response_text = urlopen(request).read().decode("utf-8")
        weather = Text.from_ansi(response_text)
        if not worker.is_cancelled:
            self.call_from_thread(weather_widget.update, weather)
    else:
        # No city, so just blank out the weather
        if not worker.is_cancelled:
            self.call_from_thread(weather_widget.update, "")
```

这里 update_weather 是同步常规函数。@work 装饰器的 thread=True 使它变成了一个 thread worker。

注意，在 worker function 内，get_current_worker 用来获取当前 worker，可以检查它是否被 cancel。类似 Thread API 的 GetCurrentThreadId。

如果为一个常规函数添加 work 装饰器，Textual 会抛出异常。

#### Posting messages

绝大多 Textual 函数都是非线程安全的，这意味着需要使用 call_from_thread 来运行 Textual 相关的 code。一个例外时 post_message，它是线程安全的。如果 worker 需要多次更新 UI，发送自定义消息并让 message handler 更新 UI 的状态是更好的方法。

