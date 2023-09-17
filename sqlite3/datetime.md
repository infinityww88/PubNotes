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

strftime 可以代替其他所有的日期函数。尽量使用 strftime，因为它和 python 的 strftime 和 unix date 命令的格式相同。可移植性才是最重要的。

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

2-10 后面可以跟着一个时区指示符，格式为 [+-]HH:MM 或就是一个 Z。日期时间函数内部使用 UTC，因此 Z 后缀没有什么作用。任何非零的 HH:MM 后缀都从指示的时间内减去以获得 UTC 时间。下面的时间值是等价的：

```plain
2013-10-07 08:23:19.120
2013-10-07T08:23:19.120Z
2013-10-07 04:23:19.120-04:00
2456572.84952685    #   儒略日，sqlite3 自动识别浮点数，并以儒略日解析
```

4,7,10 格式中的带小数的 seconds 值 SS.SSS 可以有一个或多个小数数字。上面的例子中只显示 3 个数字是因为只有前 3 个数字是显著的，但是输入字符串（time value）可以有更少或更多的数字，而 date/time 函数仍然可以正确操作。

12 格式中 DDDDDDDDDD 可以是整数也可以是浮点数，它默认解释为儒略日（公元-4713年开始，小数表示一天中的时间）。但是如果它后面跟着 "auto" 或 "unixepoch" modifier，则解释为 unix 时间戳。

以数字指定日期有两种方式：

- 整数 integer：表示 Unix 时间戳，从 1970-01-01 00:00:00 UTC 算起的秒数（需要加 auto 或 unixepoch modifier）
- 实数 real：表示儒略日，即从公元前 4714 年 11 月 24 日格林尼治时间的正午开始算起的天数

## Modifiers

每个日期时间函数（除了 timediff），time value 都可以跟着一个或多个 modifers，可以修改这个 time value。类似 gnu date 的 -d 中的 time modifier，python 中的 timedelta，以及等价 timediff 函数。每个 modifier 应用到左边的 time value，从左到右以此应用。

1. NNN days
2. NNN hours
3. NNN minutes
4. NNN seconds
5. NNN months
6. NNN years
7. ±HH:MM
8. ±HH:MM:SS
9. ±HH:MM:SS.SSS
10. ±YYYY-MM-DD
11. ±YYYY-MM-DD HH:MM
12. ±YYYY-MM-DD HH:MM:SS
13. ±YYYY-MM-DD HH:MM:SS.SSS
14. start of month
15. start of year
16. start of day
17. weekday N
18. unixepoch
19. julianday
20. auto
21. localtime
22. utc
23. subsec
24. subsecond

1-13 添加指定的 time delta 到左边的 time value。

1-6 结尾的 s 是可选的。

NNN 可以是整数或实数，可选前面跟着一个 +/- 前缀。

7-9 从左到右依次调整 Year，Month，Day，Hour，Minute，Second。

14-16 start of modifiers 偏移日期到指定 month，year 或 day 的开始。

weekday modifier 如果可能向前修改 date，到下一个 weekday number 是 N 的那天。Sunday 是 0，Monday 是 1，以此类推。

localtime modifier 假设它左边的 time value 是 UTC，并且调整那个 time value 为 local time。如果不是 UTC 时间，行为未定义。utc modifier 是 localtime 的逆操作。

unixepoch modifier 只在它跟随的 time value 是 DDDDDDDDDD 格式的数值时才有效。这导致数值解释为 unix 时间戳，而不是儒略日。

julianday modifier 与 unixepoch 一样，必须紧随这 DDDDDDDDDDD 格式的数值，它强制将数值解释为儒略日。

auto modifier 自动解释 DDDDDDDDDDD time value 为 unix 时间戳或儒略日：

- 如果数值在 0.0 到 5373484.499999 之间，则解释为儒略日（-4713-11-24 12:00:00 and 9999-12-31 23:59:59, inclusive）
- 否则，解释为 unix 时间戳，但是范围必须在 -210866760000 to 253402300799 之间

## strftime 格式化指示符

%d        day of month: 00
%f        fractional seconds: SS.SSS
%H        hour: 00-24
%j        day of year: 001-366
%J        Julian day number (fractional)
%m        month: 01-12
%M        minute: 00-59
%s        seconds since 1970-01-01
%S        seconds: 00-59
%w        day of week 0-6 with Sunday==0
%W        week of year: 00-53
%Y        year: 0000-9999
%%        %

The format string supports the most common substitutions found in the strftime() function from the standard C library plus two new substitutions, %f and %J.

## 儒略日

儒略周期内以连续的日数计算时间的计时法，主要是天文学家在使用。儒略日数（英语：Julian Day Number，JDN）的计算是从格林威治标准时间的中午开始，包含一个整天的时间，起点的时间（0日）回溯至儒略历的公元前4713年1月1日中午12点（曾在格里历是公元前4714年11月24日）[1]，这个日期是三种多年周期的共同起点，且是历史上最接近现代的一个起点。
