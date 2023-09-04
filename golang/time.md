# Time Package

操作系统提供两种时间：

- wall clock：用于与其他人协作，对表的时间，例如 "2013-10-07: 08-23-19 19.120"，在时间同步时会被更新
- monotonic clock：CPU 节拍器产生的单调时间 tick，只用于测量，例如测量一个函数的执行时间

相比于分别提供这两种时间的 API（例如 C 或 Python），这个包中 time.Now() 返回 Time 同时包含 wall clock reading 和 monotonic reading。后续的 time-telling 操作使用 wall clock reading，但是后续的 time-measuring operations，特别是比较和减法，使用 monotonic clock reading。

例如，下面的代码总是计算一个差不多 20 毫秒的时间差，即使在期间 wall clock 因为同步已经发生了变化（因此用 wall clock 测量时间差就可能不准确）：

```go
start := time.Now()
//... operation that takes 20 milliseconds ...
t := time.Now()
elapsed := t.Sub(start)
```

其他类似操作，例如 time.Since(start), time.Until(deadline), time.Now().Before(deadline) 都类似的免疫于 wall clock reset。

time.Now 返回 Time 包含一个 monotonic clock reading。如果 Time t 有一个 monotonic clock reading，t.Add 添加同一个的 duration 到 wall clock 和 monotonic clock reading 来计算 result。因为 t.AddDate(y, m, d), t.Round(d) 和 t.Truncate(d) 是 wall time 计算，它们总是从它们的结果中去除任何 monotonic clock reading。因为 t.In, t.Local, t.UTC 用于解释 wall time，它们也会从结果中去除 monotonic clock reading。去除 monotonic clock reading 的标准方法是 t = t.Round(0)。

如果 Times t 和 u 都包含 monotonic clock reading，t.After(u), t.Before(u), t.Equal(u), t.Compare(u), t.Sub(u) 都只使用 monotonic clock reading 计算，忽略 wall clock reading。

Time 结构体中包含两个值，一个 wall clock 的读取结果，一个 monotonic clock 的读取结果。而时间差也有两种，wall clock 即日历上的时间差，比如计算 "2013-10-07: 08-23-19 19.120"  和 "2013-10-07: 08-23-19 20.120" 的时间差，以及 cpu 时钟周期的时间差。Time 同时包含了这两个 reading，不同目的的 API 使用不同的 reading。

对于 Python 中的就分别是 time.monotonic() 和 time.time()。

Python time.monotonic() Return the value (in fractional seconds) of a monotonic clock, i.e. a clock that cannot go backwards. The clock is not affected by system clock updates.

在一些系统上，如果计算机进入休眠状态，monotonic clock 将会停止。在这样的系统上，t.Sub(u) 可能不能精确反应真实流逝的时间。

因为 monotonic clock reading 在当前进场之外没有意义，t.GobEncode, t.MarshalBinary, t.MarshalJSON 和 t.MarshalText 在序列化时，忽略 monotonic clock reading，t.Format 也没有提供 format 给它。类似的，time.Date, time.Parse, time.ParseInLocation, 和 time.Unix 以及反序列化器 t.GobDecode, t.UnmarshalBinary, t.UnmarshalJSON 和 t.UnmarshalText 总是创建没有 monotonic clock reading 的 times。

```go
struct Time {
    WallTime int64
    MonotonicTime int64
}

func Now() Time {
    t := Time()
    t.WallTime = readWallTime()
    t.MonotonicTime = readMonotonicTime()
}
```

monotonic clock reading 仅存在于 Time values。它不是 t.Unix 和其他类似函数返回的 Unix times 或 Duration values 的一部分。

Go == 运算符不仅仅比较 time instant 还比较 Location 和 monotoni clock reading。

出于调试目的，t.String 的结果包含 monotonic clock reading，如果它存在的话。如果 t 和 u 因为 monotonic clock reading 不同而不相等，则这个不同可以通过打印 t.String() 和 u.String() 发现。

## 常量

### 常用 Layout

- Layout      = "01/02 03:04:05PM '06 -0700" // The reference time, in numerical order.
- ANSIC       = "Mon Jan _2 15:04:05 2006"
- UnixDate    = "Mon Jan _2 15:04:05 MST 2006"
- RubyDate    = "Mon Jan 02 15:04:05 -0700 2006"
- RFC822      = "02 Jan 06 15:04 MST"
- RFC822Z     = "02 Jan 06 15:04 -0700" // RFC822 with numeric zone
- RFC850      = "Monday, 02-Jan-06 15:04:05 MST"
- RFC1123     = "Mon, 02 Jan 2006 15:04:05 MST"
- RFC1123Z    = "Mon, 02 Jan 2006 15:04:05 -0700" // RFC1123 with numeric zone
- RFC3339     = "2006-01-02T15:04:05Z07:00"
- RFC3339Nano = "2006-01-02T15:04:05.999999999Z07:00"
- Kitchen     = "3:04PM"

Handy time stamps.

- Stamp      = "Jan _2 15:04:05"
- StampMilli = "Jan _2 15:04:05.000"
- StampMicro = "Jan _2 15:04:05.000000"
- StampNano  = "Jan _2 15:04:05.000000000"
- DateTime   = "2006-01-02 15:04:05"
- DateOnly   = "2006-01-02"
- TimeOnly   = "15:04:05"

基于 Layout 定义各种标准和便捷的日期时间格式

Go 不使用 C/Python 的 strftime 格式化时间，而是用一个特殊的 layout parameter。

```plain
Mon Jan 2 15:04:05 MST 2006
```

指示时间如何格式化。

This date is easier to remember when written as 01/02 03:04:05PM '06 -0700，即：

1 2 3 4 5 6 7

1 月 2 日 3 点 4 分 5 秒 06 年 西 7 区，此外 Mon 显示 weekday，PM 显示 AM/PM。

layout 中的各个分量是固定的，不可改变，这样 Go 就知道 04 表示要格式化分钟，01 表示要格式化月份。如果随意使用数字，Go 就不知道要格式化哪个分量了。

Layout options
|Type|Options|
| --- | --- |
|Year|06   2006|
|Month|01   1   Jan   January|
|Day|02   2   _2   (width two, right justified)|
|Weekday|Mon   Monday|
|Hours|03   3   15|
|Minutes|04   4|
|Seconds|05   5|
|ms μs ns|.000   .000000   .000000000|
|ms μs ns|.999   .999999   .999999999   (trailing zeros removed)|
|am/pm|PM   pm|
|Timezone|MST|
|Offset|-0700   -07   -07:00   Z0700   Z07:00|
|||

### 常用 duration

- Nanosecond  Duration = 1
- Microsecond          = 1000 * Nanosecond
- Millisecond          = 1000 * Microsecond
- Second               = 1000 * Millisecond
- Minute               = 60 * Second
- Hour                 = 60 * Minute

duration 都以纳秒为单位，要计算其他单位的 duration，除以相应的单位常量，例如 second / time.Millisecond 返回毫秒数。类似的，将一个单位转换为 Duration，简单乘以相应的单位常量：

```go
seconds := 10
fmt.Print(time.Duration(seconds)*time.Second) // prints 10s
```

## 定时器

- func After(d Duration) <-chan Time

  立即返回一个 <- 管道，然后等待 Duration 时间，向管道发送当前时间值。它等价于 NewTimer(d).C，后者高效。

- func Sleep(d Duration)

  暂停当前 goroutine 指定的 duration，负数和 0 立即返回。

- func Tick(d Duration) <-chan Time

  NewTimer 的便捷包装函数。但是它没有方法关闭底层的 Ticker，底层 Ticker 不能被 GC 回收，因此它是泄露的，这是故意涉及的，它用于不需要关闭 Ticker 的 client。与 NewTicker 不同，如果 d <= 0, Tick 总是返回 nil。

## Duration

表示一个 int64 纳秒数的流逝时间。

提供各种计算 Duration 的方法。

- func ParseDuration(s string) (Duration, error)

  解析一个 duration string。
  
  "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".

- func Since(t Time) Duration

  返回自 t 到当前时间的 Duration，等于 time.Now().Sub(t).

- func Until(t Time) Duration

  返回当前时间到 t 的 Duration，等于 t.Sub(time.Now())

- func (d Duration) Abs() Duration

  Abs 返回 d 的绝对值，负 Duration 变正 Duration。math.MinInt64 转换为 math.MaxInt64。

以浮点数返回 duration 的各种时间单位的数量：

- func (d Duration) Hours() Duration
- func (d Duration) Microseconds() Duration
- func (d Duration) Milliseconds() Duration
- func (d Duration) Minutes() Duration
- func (d Duration) Nanoseconds() Duration
- func (d Duration) Seconds() Duration

- func (d Duration) Round(m Duration) Duration

  Round 返回 d round 到 m 的最近整数倍的值。例如取证到小时、分钟、秒，甚至 1 小时 25 分钟的整数倍。Halfway 值四舍五入。

- func (d Duration) String() string

  返回 duration 的字符串表示，例如 72h3m0.5s，可以被 ParseDuration 解析。作为一个特殊情形，小于 1s 的 duration 使用一个更小的 unit (milli-, micro-, or nanoseconds) 来确保 leading digit 是非零的。0 duration 格式化为 0s。

- func (d Duration) Truncate(m Duration) Duration

  Truncate 返回将 d 向下取整到 m 的整数倍的值，类似 Round，只是 Halfway 的值向下取整。

## Location

Location 映射 time instants 到这个时区的相同时间，并且考虑夏令时。

```go
var Local *Location = &LocalLoc
```

Local 表示系统 local time zone。在 Unix 系统上，Local 使用 TZ 环境变量得到要使用的 time zone。没有 TZ 意味着使用系统默认的 /etc/localtime。TZ = "" 意味着使用 UTC。TZ = "foo" 意味着使用系统 timezone 目录的 foo 文件。

```go
var UTC *Location = &utcLoc
```

UTC 表示 Universal Coordinated Time (UTC)。

- func FixedZone(name string, offset int) *Location

  FixedZone 返回一个 Location，它总是使用给定的 zone 名字和 offset（seconds east of UTC）。

  loc := time.FixedZone("UTC-8", -8*60*60)

- func LoadLocation(name string) (*Location, error)

  LoadLocation 返回给定名字的 Location，使用名字得到 Location，FixedZone 使用秒数得到 Location。

  如果名字是 "" 或 "UTC"，LoadLocation 返回 UTC。如果名字是 "Local"，返回 Local。

  否则，name 必须是一个对应 IANA Time Zone database 的 location 名字，例如 "America/New_York"。

  LoadLocation 在以下 locations 按顺序查找 IANA Time Zone database。

  - ZONEINFO 环境变量命名的目录
  - 在 Unix 系统中，系统的标准安装位置
  - $GOROOT/lib/time/zoneinfo.zip
  - time/tzdata package，如果 imported

- func LoadLocationFromTZData(name string, data []byte) (*Location, error)

- func (l *Location) String() string

  返回 time zone 信息的描述名字，对应 LoadLocation 或 FixedZone 的 name 参数

## Month

type Month int

枚举月份值。

```go
const (
  January Month = 1 + iota
  February
  March
  April
  May
  June
  July
  August
  September
  October
  November
  December
)
```

- func (m Month) String() string

## ParserError

解析 layout 错误。

## Ticker

```go
type Ticker struct {
  C <-chan Time
}
```

一个 Ticker 保存一个 channel，以一定时间间隔发送 ticks。

- func NewTicker(d Duration) *Ticker

  返回一个新的 Ticker，按 d 时间间隔发生 current time。Ticker 会调整 time interval 或丢弃 ticks 来弥补慢接受者。

  duration d 必须大于 0，否则 NewTicker panic。Stop ticker 来释放关联的资源。

  ```go
  ticker := time.NewTicker(time.Second)
  defer ticker.Stop()
  done := make(chan bool)
  go func() {
    time.Sleep(10 * time.Second)
    done <- true
  }()
  for {
    select {
    case <-done:
      fmt.Println("Done!")
      return
    case t := <-ticker.C:
      fmt.Println("Current time: ", t)
    }
  }
  ```

- func (t *Ticker) Reset(d Duration)

  Reset 停止一个 ticker，重置它的 peroid 为指定的 duration，即调整定时器时间间隔。下一个 tick 会在新的 peroid 之后到达。duration d 必须大于 0，否则 Reset 将会 panic。

- func (t *Ticker) Stop()

  关闭 Ticker。Stop 后，不会发送更多的 ticks。Stop 不关闭 channel，来防止一个读取 channel 的并行的 goroutine 看到一个错误的 tick。

## Time

Time 以纳秒精度表示一个 instant。

使用时间的 Programs 通常应该以值的方式存储和传递它们，而不是指针。即 Time 类型的变量或结构体字段，应该是 Time 类型，而不是 *Time 类型。

一个 Time value 可以被多个 goroutines 同时使用，除了 GobDecode，UnmarshalBinary，UnmarshalJSON 和 UnmarshalText，因为它们向 Time struct 写入，而且不是 goroutine 安全的。

Time instants 可以使用 Before，After，或 Equal 方法比较。Sub 方法在连个 instants 之间做差，得到一个 Duration。Add 方法相加一个 Time 和一个 Duration，得到一个 Time。

Time 的零值是公元 0001:01:01 00:00:00.000000000 UTC。因为这个时间在实际中不太可能出现，IsZero 方法提供一个简单方法来检测一个 time 是否被显示初始化。

每个 Time 关联一个 Location，在计算 Time 的表示时被使用，例如 Format，Hour，Year 方法。Local，UTC，In 方法返回一个指定 location 的 Time。改变 Loation 只改变时间的表示，不改变绝对时间。

GobEncode, MarshalBinary, MarshalJSON, and MarshalText 这些序列化方法保存 Time.Location 的 offset，而不是 location 的 name，因此它们丢失了关于夏令时的信息。

除了读取 wall clock 的需求，Time 还可以包含一个可选的当前进程的 monotonic clock 的读取，来提供比较和相减的额外的精度。

注意 Go == 不仅比较 time instant，还比较 Localtion 和 monotonic clock reading。因此如果不保证相同的 Location 设置到所有的 values 上（可以通过 UTC 或 Local 方法做到）以及去除 monotonic clock reading（通过 t=t.Round(0) 做到），Time value 不应该被用作 map 或数据库 keys，而前者可以通过 UTC 或 Local 方法做到。通常应该使用 t.Equal(u) 而不是 t == u，因为 t.Equal 使用最精确的比较，并且正确处理一个参数包含 monotonic clock reading 的情景。

### 构造 Time

- func Date(year int, month Month, day, hour, min, sec, nsec int, loc *Location) Time

  构造一个 Time

- func Now() Time

  返回当前 Local time

### 从字符串解析 Time

- func Parse(layout, value string) (Time, error)

  解析一个字符串，返回它表示的 time。

  当解析时，input 可能在 seconds 部分包含小数，即使 layout 没有指定它。小数部分被截断为纳秒精度。

  layout 忽略的字段被假设为 0，如果 0 是不可能的值，则指定为 1。day-week 用来做语法检查，但是被完全忽略，因为年月日就已经确定日期了。

  如果用 NN 指定年份，NN >= 69 解释为 19NN，NN < 69 解释为 20NN。

  如果没指定 Location，返回 UTC 的 time。

- func ParseInLocation(layout, value string, loc *Location) (Time, error)

  类似 Parse，区别：

  - 缺省 time zone 信息时，Parse 将时间解释为 UTC 时间，ParseInLocation 将时间解释为函数参数给定的 Location 的时间
  - 如果给定 zone offset 或简写，Parse 尝试将它解释为 Local Location 的时间，而 ParseInLoation 就按照给定的 location 解释。

### 用自 January 1, 1970 UTC 以来的秒数，毫秒数，微妙数，纳秒数构建 Time

- func UnixMicro(usec int64) Time
- func UnixMilli(msec int64) Time
- func Unix(sec int64, nsec int64) Time

### Time + Duration = Time

- func (t Time) Add(d Duration) Time
- func (t Time) AddDate(years int, months int, days int) Time

### Time 比较

- func (t Time) After(u Time) bool
- func (t Time) Before(u Time) bool
- func (t Time) Compare(u Time) int

- func (t Time) Equal(u Time) bool

  两个 time 即使在不同的 Location 也可能相等，例如 6:00 +0200 and 4:00 UTC are Equal。绝大多数判断 time 是否相等应该使用 Equal。


  t < u 返回 -1；t > u 返回 1；t == u 返回 0

### 格式化

- func (t Time) AppendFormat(b []byte, layout string) []byte

  类似 Foramt，但是将时间的 textual 表示添加到 b 中，返回扩展的 buffer。

- func (t Time) Format(layout string) string

- func (t Time) GoString() string

  GoString implements fmt.GoStringer and formats t to be printed in Go source code.

### 返回分量

- func (t Time) Clock() (hour, min, sec int)

  返回时间在一天中的小时，分钟，和秒数。

- func (t Time) Date() (year int, month Month, day int)

  返回时间对应的 year，month，day

- func (t Time) Day() (year int, month Month, day int)

  类似 Date，仅返回 day

### Gob 接口

- func (t *Time) GobDecode(data []byte) error

  GobDecode 实现 gob.GobDecoder 接口

- func (t *Time) GobEncode(data []byte) error

  GobDecode 实现 gob.GobEncoder 接口

### 返回各种时间分量

- func (t Time) Hour() int

  一天中的小时数。

- func (t Time) Minute() int

  小时内的分钟数。

- func (t Time) Month() int
- func (t Time) Nanosecond() int

  秒内的纳秒数。

- func (t Time) Second() int

  分钟内的秒数。

- func (t Time) ISOWeek() (year, week int)

- func (t Time) Year() int

- func (t Time) Weekday() int

- func (t Time) Yearday() int

### 向不同时区的 Time 转换

- func (t Time) In(loc *Location) Time

  返回 loc 中的同一个时间的 time 副本。

- func (t Time) Local() Time

  返回 t 在 Local 时区的 Time 副本，即 t.In(Local)。

- func (t Time) UTC() Time

  返回 t 在 UTC 时区的 Time 副本，即 t.In(UTC)。

### 获取时区信息

- func (t Time) Location() *Location

  返回 time 关联的 time zone。

- func (t Time) Zone() (name string, offset int)

  返回 t 所在时区的字符串信息和秒数偏移。

- func (t Time) ZoneBounds() (start, end Time)

  ZoneBounds 返回 t 所在 time zone 的边界。Zone 在 start 开始，在 end 结束。

### 判断

- func (t Time) IsDST() bool

- func (t Time) IsZero() bool

  判断 t 是否代表 January 1, year 1, 00:00:00 UTC。判断 time 是否显式初始化。

### 序列化与反序列化

- func (t Time) MarshalBinary() ([]byte, error)
- func (t *Time) UnmarshalBinary([]byte) error

  实现 encoding.BinaryMarshaler 接口，将 time 序列化为二进制数据。

- func (t Time) MarshalJSON() ([]byte, error)
- func (t *Time) UnmarshalJSON([]byte) error

  实现 json.Marshaler 接口，将 time 序列化为 JSON。

- func (t Time) MarshalText() ([]byte, error)
- func (t Time) UnmarshalText([]byte) error

  实现 encoding.TextMarshaler 接口，将 time 序列化为文本。

### 取整

- func (t Time) Round(d Duration) Time

  将 t 四舍五入取整到 d 的整数倍。

- func (t Time) String() string

  返回 time 的字符串表示，格式为 "2006-01-02 15:04:05.999999999 -0700 MST"。如果 Time 中还包括 monotonic clock reading，返回的 string 还包含 "m=+/-\<value>"，value monotonic clock 秒数。

  返回的 string 用于调式，对于稳定的序列化，使用 t.MarshalText, t.MarshalBinary, 或 t.Format 显示格式化。

- func (t Time) Sub(u Time) Duration

- func (t Time) Truncate(d Duration) Time

  类似 Round，但是向下取整到 d 的整数倍。

返回自 1970.1.1 开始的时间戳：

- func (t Time) Unix() int64
- func (t Time) UnixMicro() int64
- func (t Time) UnixMilli() int64
- func (t Time) UnixNano() int64

## Timer

Ticker 是定时器（固定时间间隔发送 ticks），Timer 是计时器（指定时间之后发送信号）。

```go
type Timer struct {
  C <-chan Time
}
```

Timer 类型表示一个事件。当 Timer 过期，当前 Time 将会发送到 C 上，除非 Timer 是通过 AfterFunc 创建的。Timer 必须使用 NewTimer 或 AfterFunc 创建。

- func AfterFunc(d Duration, f func()) *Timer

  AfterFunc 等待 duration 过期，然后在单独的 goroutine 中调用函数 f。它返回一个 Timer，可以在上面调用 Stop 方法来 cancel 调用函数 f。

- func NewTimer(d Duration) *Timer

  NewTimer 创建一个 Timer，在 d 过期后向 C 上发送 current time。

- func (t *Timer) Reset(d Duration) bool

  Reset 改变 timer 的过期时间。返回 true 表示 timer 仍然有效，fasle 表示 timer 已经过期，或者被 stop 了。

  对于 NewTimer 创建的 Timer，Reset 应该仅在被 stop 或过期的 timer 上调用，让 timer 重新可用。

  如果程序已经从 t.C 上接收了一个 value 了，timer 被视为已经过期，channel 已经 drained 了，因此 t.Reset 可以直接使用。但是如果程序还没有从 t.C 上接收一个 value，timer 必须被 stop 并且显式清空 channel（如果 Stop() 方法报告 timer 在 stop 之前已经过期了）：

  ```go
  //注意不应该与其他从 Timer channel 接收 value 的 goroutine 并行去做。
  if !t.Stop() {
    <-t.C
  }
  t.Reset(d)
  ```

  注意不可能正确使用 Reset 的返回值，因为在清空 channel 和新 timer 过期之间有一个竞争条件，即 Reset 返回时指示 timer 已经重设，程序准备在 channel 上等待之前 channel 被其他 receiver 清空了。Reset 应该总是在 stopped 或 expired channel 上调用。Reset 的返回值是为了保持和现有程序兼容。

  对于 AfterFunc(d, f) 创建的 Timer，Reset 或者在 f 运行之前重设，此时 Reset 返回 True，或者 f 已经运行完毕，Reset 重新调度 f 再次运行，此时返回 false。当 Reset 返回 false，Reset 既不在返回之前等待 f 完成，也不保证接下来运行 f 的 goroutine 不会和之前的 f 并行执行。如果调用者需要知道 f 的上次执行是否完成，它必须显式和 f 协作。

- func (t *Timer) Stop() bool

  停止 Timer 发送信号。如果 Stop 真的停止了 timer 则返回 true，如果 timer 已经过期或被 stopped 了，返回 false。Stop 不关闭 channel。

  要确保在调用 Stop 后 channel 是空的，检查返回值并清空 channel。

  ```go
  //不可以和其他从 Timer channel 上读取的 receiver 或其他调用 Stop 方法的 receiver 并行执行，只能用于 stop 自己使用的 Timer
  if !t.Stop() {
    <-t.C
  }
  ```

  对于 AfterFunc(d, f) 创建的 timer，如果 t.Stop() 返回 false，则 timer 已经过期，并且函数 f 已经在单独的 goroutine 开始调用。Stop 不等待 t 完成。如果调用者需要知道 f 是否已经完成，必须显式和 f 协作。

## Weekday

```go

type Weekday int

const (
  Sunday Weekday = iota
  Monday
  Tuesday
  Wednesday
  Thursday
  Friday
  Saturday
)

func (d Weekday) String() string
```
