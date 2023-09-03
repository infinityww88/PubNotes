# Structured Logging with slog

log/slog 标准库提供结构化日志输出。

结构化日志使用 key-value pairs，因此日志本身可以被解析，过滤，搜索，分析。

对于服务器，logging 是开发者观察系统详细行为的重要方式，也是调试时最先开始的地方。因此日志总是冗长浩繁的，而快速搜索和过滤它们的能力就变得非常重要。

Log records 包含一个 message, 一个 severity level, 和各种以 key-value pairs 表示的属性。

它定义一个类型，Logger，其提供了一些方法（例如 Logger.Info 和 Logger.Error），来报告感兴趣的事件。

每个 Logger 关联一个 Handler。一个 Logger 输出方法使用方法参数创建一个 Record，并将 Record 传递给 Handler，Handler 决定如何处理它。有一个默认可用的 Logger，可以通过顶层 Log 方法来访问（例如 slog.Info 或 slog.Error），顶层方法会调用响应的 Logger 方法。

一个 log record 包含 time，message，一组 key-value pairs，其中 keys 是 strings，values 可以是任何类型。例如，

```go
slog.Info("hello", "count", 3)
```

创建一个 Record，包含调用的 time，level of Info，消息 "hello"，和一个 key-value pair: count=3。


顶层 Log 方法：Debug，Info，Warn，Error。除了这些便捷方法，还有 Log 方法可以接受一个 level 作为参数。

默认 handler 将 log record 的 message，time，level 和属性格式化为一个字符串，并传递给 log 包。

```plain
2022/11/08 15:28:26 INFO hello count=3
```

要更多地控制输出格式，使用不同的 handler 创建一个 logger。下面的语句使用 New 创建一个新的 logger，关联一个 TextHandler，后者将结构化 records 以 text 写入 standard error。

```go
logger := slog.New(slog.NewTextHandler(os.Stderr, nil))
```

TextHandler 输出是一个 key=value pairs 的序列，很容易被机器解析。

```go
logger.Info("hello", "count", 3)
```

产生以下输出：

```plain
time=2022-11-08T15:28:26.000-05:00 level=INFO msg=hello count=3
```

slog 包还提供 JSONHandler，输出是 line-delimited JSON：

```json
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
logger.Info("hello", "count", 3)
```

产生以下输出：

```plain
{"time":"2022-11-08T15:28:26.000000000-05:00","level":"INFO","msg":"hello","count":3}
```

TextHandler 和 JSONHandler 都可以使用 HandlerOptions 配置，可以设置 minimum level，显示 log call 的 source file 和 line，以及在 logged 之前对属性进行修改。

将一个 logger 设置为默认 logger：

```go
slog.SetDefault(logger)
```

使得顶层方法例如 Info 来使用它。SetDefault 还更新 log 包使用的默认 default logger，因此使用 log.Printf 和相关方法的现有程序将会发送 log records 到 logger 的 handler，而无需重写。

一些属性对很多 log calls 是通用的。例如你可能想将一个 server request 的 URL 或 trace identifier 包含到这个 request 发出的所有 log events 中。相比在每个 log call 中重复属性，可以使用 Logger.With 来构造一个新的包含这些属性的 logger：

```go
logger2 := logger.With("url", r.URL)
```

With 参数和 Logger.Info 使用的 key-value pairs 相同。结果是一个新的 Logger，与原来的 logger 有相同的 handler，但是额外的属性会出现在每一个 call 的输出中。

## Levels

Level 是一个整数，表示一个 log event 的 servertity 重要性。更高的 level，event 的 server 更重要。这个包定义了绝大多数常见的 levels，但是任何 int 都可以用作 level。

在应用程序中，你可能想要 >= 特定 level 的 log messages。一个常见的配置是 log INFO 或更高 level 的 messages，抑制 DEBUG logging。内置 handlers 可以配置一个输出的 minimum level，通过设置 HandlerOptions.Level。通常由程序的 main 函数来设置 logger 的 level（例如通过命令行参数）。默认值是 LevelInfo。

设置 HandlerOptions.Level 字段为一个 level 值，将在 handler 的整个声明周期中固定它的 的 minimum level。而将它设置为一个 LevelVar 则允许 level 被动态改变。LevelVar 保存一个 Level 值，并且可以被多个 goroutine 安全的读写。要为整个程序动态改变 level，首先初始化一个全局 LevelVar：

```go
var programLevel = new(slog.LevelVar) // Info by default
```

然后使用 LevelVar 构建一个 handler，并将它设置为 default：

```go
h := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: programLevel})
slog.SetDefault(slog.New(h))
```

现在程序可以使用一个语句改变它的 logging level：

```go
programLevel.Set(slog.LevelDebug)
```

## Groups

Attributes 可以被收集到 groups 中。Group 有一个名字，用来 qualify 它的属性的名字。Qualification 如何显示取决于 handler。Texthandler 使用点号 . 分割 group 和属性名。JSONHandler 则将每个 group 作为一个单独的 JSON object，并使用 group name 作为 key。

使用 Group 用一个名字和 key-value list 创建一个 Group 属性：

```go
slog.Group("request", "method", r.Method, "url", r.URL)
```

TextHandler 将这个 group 显示为：

```plain
request.method=GET request.url=http://example.com
```

JSONHandler 将这个 group 显示为：

```json
"request":{"method":"GET","url":"http://example.com"}
```

使用 Logger.WithGroup 以一个 group name 来 qualify 一个 Logger 的所有 output。在一个 Logger 上调用 WithGroup 产生一个新的 Logger，使用和原来的 Logger 相同的 Handler，但是它的所有属性都被 group name qualified。

在大的系统中，这可以防止属性 keys 冲突。为每个 subsystem 传递一个带有自己 group name 的不同的 Logger：

```go
logger := slog.Default().With("id", systemID)
parserLogger := logger.WithGroup("parser")
parseInput(input, parserLogger)
```

当 parseInput 使用 parserLogger 打印日志时，它的 keys 使用 parser qualify。因此即使它使用常见的 key id，这个 log line 也会有不同的 keys。

## Contexts

Logger.Log 和 Logger.LogAttrs 方法使用一个 context 作为第一个参数，它们对应的 top-level 函数（slog.Log, slog.LogAttrs）也是一样。

尽管诸如 Debug, Info, Warn, Error 这些函数和它们对应的顶层函数，不使用 context，但是它们对应的以 Context 为结尾的版本则使用 context。

```go
slog.InfoContext(ctx, "message")
```

如果 context 可用，建议传递它给 output method。

## Attrs and Values

一个 Attr 是一个 key-value pair。Logger output 方法可以接受 Attrs，也可以接受 keys 和 values。

```go
slog.Info("hello", slog.Int("count", 3))
slog.Info("hello", "count", 3)
```

两者是等价的。

有一些用于 Attr 的便捷构造器，例如 Int，String，和 Bool，用于常见类型，还有 Any 函数用于构造任何类型的 Attr。

Attr 的 value 部分的类型是 Value。就像一个 any，一个 Value 可以保存任何 Go value，but it can represent typical values, including all numbers and strings, without an allocation.

最高效地输出 log 是使用 Logger.LogAttrs。它和 Logger.Log。它和 Logger.Log 类似，但是只接受 Attrs，不能直接指定 keys 和 values，这可以让它避免 allocation。

```go
slog.Info("hello", "count", 3)
logger.LogAttrs(ctx, slog.LevelInfo, "hello", slog.Int("count", 3))
```

两者输出相同的 log，第二种方式是最高效的方式。

## Customizing a type's logging behavior

如果一个 type 实现了 LogValuer 接口，它的 LogValue 方法返回的 Value 被用于 logging。你可以使用它控制 type 的 values 如何出现在 logs 中。例如，你可以编辑诸如 passwords 的机密信息，或者收集一个 struct 的 fields 到 Group 中。

log 使用 LogValuer 的 LogValue 输出 log 信息，而不是 stringer 的 String 方法。

LogValue 方法可以返回一个实现 LogValuer 接口的 Value。Value.Resolve 方法会小心处理这些情景，避免无限循环和递归。自定义 Handler 以及其他场景应该使用 Value.Resolve 而不是直接调用 LogValue。

## Wrapping output methods

logger 方法在调用堆栈上使用反射查找 logging call 的 file name 和 line number。对于包装 slog 的 function，这可能产生不正确的源代码信息。例如，如果你在 mylog.go 文件中定义这个函数：

```go
func Infof(format string, args ...any) {
    slog.Default().Info(fmt.Sprintf(format, args...))
}
```

然后再 main.go 中调用这个方法：

```go
Infof(slog.Default(), "hello, %s", "world")
```

则 slog 将报告源文件是 mylog.go 而不是 main.go。

一个正确的 Infof 实现会获取 source location 并将它传递到 NewRecord。Package-level 中的 wrapping example 中的 Infof 函数展示了如何做到这一点。

## Working with Records

有时一个 Handler 会需要在将它传递到另一个 Handler 或 backend 之前修改 Record。一个 Record 包含简单 public fields（例如 Time，Level，Message）和间接引用 state（例如 attributes）的 hidden fields 的混合。这意味着修改一个简单的 Record 的 copy（例如调用 Record.Add 或 Record.AddAttr 来添加属性）可能导致原来的 Record 上意料之外的效果。在修改一个 Record 之前，使用 Record.Clone 来创建一个和原始 Record 不共享任何 state 的 copy，或者使用 NewRecord 创建一个新的 Record，并且使用 Record.Attrs 遍历旧的 Record 的属性来构建新 Record 的属性。
