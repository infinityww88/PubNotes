# 时间访问与转换

time模块提供各种时间相关函数，大部分是C语言库函数的封装

## 术语和约定

- epoch

    时间的开始，时间戳为0的时间

    1970-01-01 00:00:00 UTC

    time.gmtime(0)

- seconds

    自epoch经过的秒数，包含闰秒

- 这个模块的函数可能无法处理epoch之前或现在之后的时间。可处理时间范围依赖C函数库和系统。对于32位系统和对应的C库，最远处理到2038年

- UTC

    统一协作时间，格林尼治标准时间，GMT

- DST

    政策相关的夏令时时区调整时间，通常是1hour

- 实时时间精度可能比能表达的值小，time提供微妙的精度，但是通常Unix系统只提供每秒50/100个clock，即5～20毫秒的精度

- time()和sleep()比对应的unix函数更好，都尽可能以cpu clock精度执行

    time()返回尽可能精确的时间，unix.gettimeofday

    sleep()接收float，使用select来定时

- 转换

    | From | To | Use |
    | --- | --- | --- |
    | seconds since the epoch | struct_time in UTC | gmtime() |
    | seconds since the epoch | struct_time in local time | localtime() |
    | struct_time in UTC | seconds since the epoch | calendar.timegm() |
    | struct time in local time | seconds since the epoch | mktime() |

## struct_time

gmtime()，localtime()，strptime()返回的时间值序列

namedtuple对象

    0=tm_year
    1=tm_mon（1～12）
    2=tm_mday
    3=tm_hour
    4=tm_min
    5=tm_sec
    6=tm_wday
    7=tm_yday
    8=tm_isdst(0, 1, -1)
    N/A=tm_zone（时区缩写名称）
    N/A=tm_gmtoff（UTC东部偏移seconds）

调用mktime时，如果DST有效则tm_isdst=1，DST无限则tm_isdst=0。-1表示不确定，通常结果会被正确设置

## 函数列表

- asctime([t])

    将struct_time表示的时间转换为"Sun Jun 20 23:21:05 1993"格式。t=None，则使用localtime()的返回值

- ctime([secs])

    将自epoch经过的secs表示为local time。secs=None则转换time()

    ctime(secs) == asctime(localtime(secs))

    asctime接收的是struct_time，ctime接收的是seconds

- gmtime([secs])

    将时间戳转换为UTC struct_time。secs=None则转换time()

    gm表示格林尼治

    dst=0

- localtime([secs])

    类似gmtime，但转换到本地时区。dst根据指定时间夏令时是否生效设置

- mktime(t)

    localtime的逆函数。参数为本地时区struct_time（dst如果不确定设置为-1）。返回与time()意义相同的浮点数

- monotonic()

    单调递增时钟的time()。不受系统时钟更新的影响。时钟上的时间点没有明确意义，但是时间差表示真实流逝的时间

- perf_counter()

    返回性能计数器的计数（float seconds）。使用可用的最高分辨率时钟测量一小段时间。它是系统范围的，包含sleep时流逝的时间。时钟时间差没有意义，只有时间差有意义

- process_time()

    返回当前处理器系统和用户CPU时间的总和（float seconds）。不包括sleep时流逝的时间

- sleep(secs)

    挂起调用线程指定时间。secs可以是一个float来指定更加精确的sleep时间

- strftime(format[, t])

    将一个struct_time格式化。t=None则格式化localtime()

- strptime(string[, format])

    将日期字符串解析为struct_time。format默认为"%a %b %d %H:%M:%S %Y"，匹配ctime/asctime的格式。当格式化指示符对应的属性缺失时None，默认填充值为(1900, 1, 1, 0, 0, 0, 0, 1, -1)

- time()

    返回自epoch以来经过的seconds。性能计数器本身的返回没有意义，它的时间差才有意义。time返回的时间戳本身是有意义的

    时间戳可以被gmtime/localtime转换为struct_time
