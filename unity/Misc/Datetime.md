# Datetime

C# 有两个日期对象 DateTime/DateTimeOffset，都用来表示日期（年月日时分秒时区）。DateTime 应该是比较旧的实现，只使用一个 DateTimeKind 枚举表示时区，而且只能表示 UTC 和 Local 两个时区。而 DateTimeOffset 是更新的实现，可以用任意的 TimeSpan 作为 Offset 表示时区。因此应该只需要使用 DateTimeOffset 即可。

DateTimeOffset 等价于 python 的 datetime，用来表示一个具体的时间戳日期，TimeSpan 等价于 python 的 timedelta，用来表示两个时间戳的差（时间偏移量）。

两个 DateTimeOffset 相减得到一个 TimeSpan，一个 DateTimeOffset 加上 TimeSpan 得到另一个 DateTimeOffset。

DateTimeOffset 使用 年月日时分秒毫秒+TimeSpan（而不是 DateTimeKind） 表示一个时间，TimeSpan 用 days，hours，minutes，seconds 表示一个时间偏移量。

DateTimeOffset 上面有各种 AddDays，AddHours 等方法修改时间。DateTimeOffset 是结构体，Add 方法不操作结构体本身，而是返回一个新的结构体。

DateTimeOffset 构造时的年月日时分秒不被 TimeSpan 修改，而是对应这个 TimeSpan 的 年月日时分秒，它减去 TimeSpan 才得到 UTC 时间。

DateTimeOffset.Now 返回 TimeSpan = Local 时区的当前时间，DateTimeOffset.UtcNow 返回 TimeSpan=TimeSpan.zero 的当前时间。

DateTimeOffset 的 ToUnixTimeSeconds FromUnixTimeSeconds 可以在 Unix 时间戳之间进行转化。

DateTimeOffset 的 ToString() 返回的 YYYY-MM-DD HH:mm:SS.SSS +XX:XX 格式可以直接被 DateTimeOffset.Parse 解析。

