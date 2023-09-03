# Date

显示、设置系统时间。通常不会用到设置，只用于显示当前或指定时间的表示。

```sh
date -d "时间" [+Format]
```

-d 提供一个时间值 time-value，默认是 now，就是当前时间，也可以显示指定 -d now

The -d, --date=STRING is a mostly free format human readable date string such as "Sun, 29 Feb 2004 16:21:42 -0800" or "2004-02-29 16:21:42" or even "next Thursday".  A date string may contain items indicating calendar date, time of day, time zone, day of week, relative time, relative date, and numbers.  An empty string indicates the beginning of the day.  The date string format is more complex than is easily documented here but is fully described in the info documentation.

-d 指定时间的格式：

- 不指定：now
- -d now
- -d @2147483647
- -d '2023-09-01 10:10:10'
- -d '任意时间值 +1 day'

date 以一个默认格式显示日期时间值，可以可选地提供显示格式，以一个 + 作为前缀，格式指示符和 c/python 的指示符相同，其中 +%s 表示显示为时间戳。

date -d now +%s 显示当前日期的时间戳。

