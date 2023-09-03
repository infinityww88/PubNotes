# Date and Time

Sqlite 支持 7 个 date 和 time 函数：

- date(time-value, modifier, modifier, ...)
- time(time-value, modifier, modifier, ...)
- datetime(time-value, modifier, modifier, ...)
- julianday(time-value, modifier, modifier, ...)
- unixepoch(time-value, modifier, modifier, ...)
- strftime(format, time-value, modifier, modifier, ...)
- timediff(time-value, time-value)

除了 strftime，都使用一个 time-value 作为第一个参数，而 strftime 第一个参数是 format，第二个参数才是 time-value。

前 6 个函数的 time-value 是可选的，如果不提供，默认是 "now"，即以当前日期时间为 time-value。

尽量使用 strftime，因为它和 python 的 strftime 和 unix date 命令的格式相同。可移植性才是最重要的。

date(), time()，datetime() 和它们的对应的 strftime 都返回 text，即日期时间的字符串表示。

julianday 和 unixepoch 返回 numeric values，它们的对应的 strftime（分别是 %J, %s）返回 text，表示相应的数字。

提供除 strftime 之外的函数主要为了便捷性。

unixepoch 直到 sqlite 3.38.0 才开始支持。查询 sqlite 版本号：

- shell 中 sqlite3 --version
- sqlite 中 select sqlite_version()

## Timediff

timediff 函数提供两个时间值 time-value，返回一个字符串描述的时间差，格式为人可读的：

```plain
(+|-)YYYY-MM-DD HH:MM:SS.SSS
```

而这个 diff 字符串可以用于其他时间函数的 modifier。这意味着下面的等式是成立的：

```plain
datetime(A) = datetime(B, timediff(A,B))
```

timediff 直到 3.43.0 (2023-08-24) 才提供。timediff 考虑每个月天数的不同，以及闰年的问题。

## Time Values

时间值可以以一下任意一种方式提供（这些表示或者是 Integer/Real，或者是 Text，就是 sqlite 数据库中保存的某个 value）：

- YYYY-MM-DD
- YYYY-MM-DD HH:MM
- YYYY-MM-DD HH:MM:SS
- YYYY-MM-DD HH:MM:SS.SSS
- YYYY-MM-DDTHH:MM
- YYYY-MM-DDTHH:MM:SS
- YYYY-MM-DDTHH:MM:SS.SSS
- HH:MM
- HH:MM:SS
- HH:MM:SS.SSS
- now
- DDDDDDDDDD

最后一种方式，value 值是一个 integer 或 float，其他的 value 值是字符串。

5-7 方式中的 T 是个字符串字面量，用来分隔日期和时间，它是 Time 的简写，表示后面的是时间，这是 ISO-8601 格式要求的。

8-10 仅指定 time，日期假设为 2000-01-01。如果只指定 time，即 db 中的 value 只保存 time 字符串，说明不关心 date。但是计算 timediff 需要完整的 datetime，因此假设了一个日期足够了。
