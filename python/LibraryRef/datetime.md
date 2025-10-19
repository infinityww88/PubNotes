# 基本date和time类型

datetime模块提供了访问dates和times的类

尽管支持date/time计算，这个模块的实现关注于输出格式和操作的高效的属性导出

## Aware/Naive Object

Date/Time对象可以分为Aware和Naive的

Aware带有时区信息，因此是确定的日期和时间。Naive没有时区信息，它表示UTC时间，本地时间，还是其他时区时间完全依赖于程序的解释。Naive对象易于理解和操作，但是忽略了一些真实的时间特性

对于需要Aware对象的应用，datetime/time对具有一个可选的time zone信息属性，tzinfo，可以被设置为抽象类tzinfo类的子类的一个实例。tzinfo对象捕获从UTC时间的偏移信息，时区的名字以及daylight saving time是否有效

只有一个tzinfo类的具体子类，datetime.timezone

## Constants

- MINYEAR(1)

  date/datetime可表示的最小年份，==1，因此date/datetime不能表示公元前的时间

- MAXYEAR(9999)

## Available Types

这些类型都是不可修改的，immutable

- date

    naive date对象

    属性：year，month，day

- time

    naive time对象

    属性：hour，minute，second，microsecond，tzinfo

- datetime

    date和time的合体

    属性：year，month，day，hour，minute，second，microsecond，tzinfo

- timedelta

    两个date，time，或datetime实例的差值连续时间，毫秒分辨率

- tzinfo

    时区信息对象，被datetime和time类使用，提供时间调整信息

- timezone

    tzinfo的唯一具体子类

### Common Properties

date、datetime、time、timezone类型共享一些共同特性

    不可修改Immutable
    Hashable，可以用于dict key
    支持pickle

### Determining if an Object is Aware or Naive

date总是naive的

time/datetime可以是naive或者aware的

time/datetime是aware的，如果它满足两个条件，否则是naive的

    o.tzinfo不是None
    o.tzinfo.utcoffset(d)不返回None

aware和naive对象不可计算差值timedelta

## timedelta

timedelta表示一段连续时间，两个date、time、datetime的差值

timedelta可以用于date、time、datetime的计算，它以day，second和microsecond表示时间长度

- timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    所有参数都是可选的，默认为0。参数可以是整数或者浮点数，可以是整数或负数

    在内部只有days，seconds，和microseconds被存储，所有参数都转换为这些unit

        millisecond转换为1000microseconds
        minute转换为60seconds
        hour转换为3600seconds
        week转换为7days

    days，seconds，microseconds被规范化，以产生统一的表示

        0 <= microseconds < 1000000(1s)
        0 <= seconds < 3600*24(1d)
        -999999999 <= days <= 999999999

    参数可以是float。如果有多个参数包含小数部分的microseconds，所有这些小数部分会合并在一起并取整

    对于负数的timedelta，只有days是负的。seconds、microseconds总是正的

- min

    最负的timedelta。timedelta(-999999999)

- max

    最正的timedelta。timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)

- resolution

    两个不同的timedelta最小可能的差值，timedelta(microseconds=1)

### 属性（只读）

| Attribute | Value |
| --- | --- |
| days | [-999999999, 999999999] |
| seconds | [0, 86399] |
| microseconds | [0, 999999] |

### 操作

- t1 = t2 +/- t3

- t1 = t2 * int(float)

- float = t2 / t3

- t1 = t2 / float(int)

- t1 = t2 // i or t1 = t2 // t3

- t1 = t2 % t3

- q, r = divmod(t1, t2)

- +t1 or -t1

- abs(t)

- str(t), [D day[s], ][H]H:MM:SS[.UUUUUU]

- repr(t)

- 比较大小与相等

- 与datetime，time的加减操作

- t.total_seconds()，以seconds表示的时间长度，等价于t / timedelta(seconds=1)

## date

date表示一个理想化日历的日期（year，month，day），公历向两个方向无限延伸。第一天是公元1年1月1日

- date(year, month, day)

    所有参数都是必须的，所有参数都是整数

        MINYEAR <= year <= MAXYEAR
        1 <= month <= 12
        1 <= day <= 指定年份的月份的天数

- 类方法

  - today()
  
    本地日期，等价于date.fromtimestamp(time.time())

  - frometimestamp(timestamp)

    返回对应POSIX时间戳对应的本地日期，C.localtime()

  - fromordinal(ordinal)

    返回公历第n天对应的日期，ordinal=1对应公元1年1月1日

    ordinal <- [1, data.max.toordinal()]

  - fromisoformat(date_string)

    返回ISO日期格式'YYYY-MM-DD'指定的日期

    date.isoformat()的逆函数

  - fromisocalendar(year, week, day)

    返回ISO日历指定year，week，day对应的日期

    date.isocalendar的逆函数

  - date2 = date1 +/- timedelta

  - timedelta = date1 - date2

  - date1 < date2

    当且仅当date1.toordinal() < date2.toordinal()

- 类属性

  - min

    可表示的最早日期，date(MINYEAR, 1, 1)

  - max

    可表示的最晚日期，date(MAXYEAR, 12, 31)

  - resolution

    两个不同date的最小差值，timedelta(days=1)

- 实例属性（只读）

  - year([MINYEAR, MAXYEAR])
  - month([1, 12])
  - day([1, day_in_month])

- 实例方法

  - replace(year=self.year, month=self.month, day=self.day)

  - timetuple()

    返回time.struct_time对象，就像time.localtime()返回的一样

    time.struct_time((d.year, d.month, 0, 0, 0, d.weekday(), yday, -1))

    yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1

  - toordinal()

    返回公历日期的天序数，0001-01-01的序数为1

  - weekday()

    返回日期是星期几，Monday=0，Sunday=6

  - isoweekday()

    返回日期是星期几，Monday=1，Sunday=7

  - isocalendar()

    返回3-tuple (ISO Year, ISO week number, ISO weekday)

  - isoformat()

    返回ISO'YYYY-MM-DD'格式日期

  - str=isoformat

  - ctime

    返回表示日期的描述字符串，C.ctime()，time.ctime(time.mktime(d.timetuple()))

  - strftime(format)

    格式化日期，但是格式化字符串中的hours，minutes，seconds总是0

  - \_\_format__(format)

    与strftime相同。它是的date对象可以用于formatted string literals以及str.format

## time

time对象表示一天中的时间，与具体哪一天无关，并且是tzinfo可调整的对象

time对象支持time到time到比较。两个aware time对象比较，将考虑时区的offset。

- 构造函数

  - time(hour = 0, minute = 0, second=0, microsecond=0, tzinfo=None, fold=0)

    microsecond是微妙，10000000microseconds = 1000millisecond = 1s

    fold in [0, 1]

    tzinfo指定这个time对象表示的是哪个时区一天中的时间
  
  - fromisoformat(time_string)

    isoformat的逆函数

    HH[:MM[:SS[.fff[fff]]]]

- 类属性

  - min

    可表示的最小时间time(0, 0, 0, 0)

  - max

    可表示的最大时间time(23, 59, 59, 999999)

  - resolution

    两个不同time对象的最小差值，timedelta(microseconds=1)

- 实例属性（只读）

  - hour
  - minute
  - second
  - microsecond
  - tzinfo
  - fold

- 实例方法

  - replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, *, fold = 0)

    基于这个time对象返回一个新的time对象，并使用参数替换指定的字段

    tzinfo=None可以从aware time创建一个naive time
  
  - isoformat(timespec='auto')

    返回ISO格式的时间字符串表示

        HH:MM:SS.ffffff, if microsecond != 0
        HH:MM:SS, if microsecond = 0
        HH:MM:SS.ffffff+HH:MM[:SS[.ffffff]], if time.utcoffset() != None
        HH:MM:SS+HH:MM[:SS[.ffffff]], if microsecond = 0 and time.utcoffset() != None

    可选参数timespec指示time包含的额外组件的数量

        default：根据microsecond，time.utcoffset()选择不同的格式
        auto：same as seconds if microsecond = 0， microseconds otherwise
        hours：以HH包含hour组件
        minutes：以HH:MM包含hour，minute组件
        seconds：以HH:MM:SS包含hour，minute，second组件
        milliseconds：以HH:MM:SS.fff包含全部组件，但是移除小于毫秒的微秒数
        microseconds：以HH:MM:SS.ffffff包含全部组件

  - \_\_str__()

    == t.isoformat
  
  - strftime(format)

    通用格式化，与date.strftime一样，只是time的year=1900，month=01，day=01，weekday=Mon
  
  - \_\_format__(foramt)

    == strftime，使time对象可以用在f-string中
  
  - utcoffset/dst/tzname

    如果tzinfo=None，返回None；否则返回self.tzinfo.utcoffset/dst/tzname(None)
  
## datetime

datetime是date和time的联合

时间戳是日期和datetime的合体，因此只有datetime和time.time()可以获取当前时间，date/time对象只是表示日期和时间的组件

- 构造函数

  所有构造函数都带有指定的tz参数，如果tz=None，则以本地时区创建一个naive时间（即没有时区信息的时间对象），即year、month、day、hour、minute、second、microsecond都表示本地当前时间的数值，但是因为没有时区信息，datetime很多方法相应地将naive时间对象处理为本地时区aware时间。如果构造函数指定tz信息，则创建一个aware时间对象，year，month，day，hour，minute，second，microsecond都为指定时区当前时间的数值

  时间戳是绝对的，不依赖于任何时区的，它是utc时区自1970-01-01 00:00:00经过的描述。因此不同时区的时间转换都通过时间戳进行通信。

  - datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)

  - today()

      返回本地时间，tzinfo=None

      == datetime.fromtimestamp(time.time())

      == now(tz=None)
  
  - now(tz=None)

      返回本地时间

      如果tz!=None，当前日期和时间将转换为指定tz的日期和时间
  
  - utcnow()

      == now(tz=timezone.utc)，但是返回的是naive datetime，即没有tzinfo的datetime对象。很多datetime的方法将naive datetime当作本地时间而不是utc时间，因此最好传递带有时区信息的aware时间对象。因此建议的创建utc时间对象的方式是datetime.now(timezone.utc)
  
  - fromtimestamp(timestamp, tz=None)

      使用指定时间戳创建一个时间对象。如果tz==None，则一个本地时区创建一个naive时间对象，否则创建指定时区的aware时间对象
  
  - utcfromtimestamp(timestamp)

    == fromtimestamp(timestamp, tz=timezone.utc)，但是创建的是naive时间对象

    == datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=timestamp)
  
  - fromordinal(ordinal)

    使用公历天序数创建datetime，time信息都是0
  
  - combine(date, time, tzinfo=self.tzinfo)

    创建一个datetime对象，date组件等于date参数，time组件等于time参数。如果提供tzinfo，则datetime使用它作为tzinfo，否则使用time.tzinfo。只有time和datetime才有tzinfo，因为date最小只能表示天，而时区信息调整的是hour，minute，second，microsecond，可调整的最大值小于一天，因此在date上使用tzinfo没有意义

    date，time和tzinfo只是简单地把属性数值设置到datetime相应的属性上，不涉及任何时间转换计算，最终datetime的意义由赋值之后的date，time，tzinfo联合确定

  - strptime(date_string, format)

    == datetime(*(time.strptime(date_string, format)[0:6]))

    time.strptime从字符串中解析日期和时间的全部组件，返回time.struct_time，只有struct_time和datetime能表示完整的日期时间，date/time只是表示日期/时间的组件，因此只有datetime类具有strptime方法，而date和time类没有strptime。但是3个类都有strftime方法

- 类属性

  - min

    最小可表示的datetime，datetime(MINYEAR, 1, 1, tzinfo=None)

  - max

    datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=None)
  
  - resolution

    timedelta(microseconds=1)
  
- 实例属性（只读）

  - year
  - month
  - day
  - hour
  - minute
  - second
  - microsecond
  - tzinfo
  - fold

- 运算符

  - datetime2 = datetime1 +/- timedelta
  - timedelta = datetime1 - datetime2
  - datetime1 < datetime2

- 实例方法

  - date()

    返回相同year, month, day数值的date对象
  
  - time()

    返回相同hour，minute，second，microsecond，fold数值的time对象，tzinfo为None
  
  - timetz()

    返回相同hour，minute，second，microsecond，fold，tzinfo数值的time对象

  - replace(...)

    基于当前datetime对象返回一个新的datetime对象，并使用参数替换指定属性
  
  - astimezone(tz=None)

    as = adjust

    基于tzinfo参数返回一个新的datetime对象，并调整date和time数据使得UTC时间相等，但是表示为tz时区的时间

    如果self是naive时间，它被假设为系统本地时区aware时间

    如果tz=None，tz假设为系统本地时区

    如果tz=self.tzinfo，则self.astimezone(tz)与self相等，不调整任何date/time数据

    如果只想改变tzinfo，而不想相应调整日期和时间，使用replace(tzinfo=tz)

    == tz.fromutc((self - self.utcoffset()).replace(tzinfo=tz))

    先将date/time数据减去self.utcoffset()，变成utc时间，然后将tzinfo设置为tz，最后调用tz.fromutc，将date/time加上tz的utcoffset()，成为tz时区时间
  
  - utcoffset/dst/tzname

    代理tzinfo.utcoffset/dst/tzname
  
  - timetuple()

    返回time.struct_time，就像time.localtime()一样。d.timetuple() == time.struct_time((d.year, d.month, d.day, d.hour, d.minute, d.second, d.weekday(), yday, dst))，直接使用self的时间组件数值构造struct_time，没有utc转换
  
  - utctimetuple()

    如果self是naive的，返回与timetuple相同，直接赋值构造struct_time

    如果self是aware的，self被转换为utc时间（通过减去utcoffset），并返回相应的struct_time

  - toordinal()

    self.date().toordinal()
  
  - timestamp()

    返回绝对时间戳。naive对象假设为本地时区
  
    没有方法可以直接从一个naive datetime获取表示UTC时间的时间戳。如果本地时区不是UTC，需要自己转换

        dt.replace(tzinfo=timezone.utc).timestamp()
        (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
  
  - weekday()

    返回星期天数。Monday=0，Sunday=6。self.date().weekday()

  - isoweekday()

    Monday=1, Sunday=7
  
  - isoformat(sep='T', timespec='auto')

    self.date.isoformat() + sep + self.time.isoformat(timespec)
  
  - \_\_str__

    str(d) == d.isoformat(' ')
  
  - ctime()

    返回日期时间的描述性文本。Wed Dec 4 20:30:40 2020
  
  - strftime/\_\_format__

## tzinfo

表示时区的抽象类。需要继承它创建具体的子类。datetime模块提供了一个简单的具体子类timezone，可以表示基于UTC固定偏移的时区

tzinfo对象可以传递给datetime，time对象，因为它调整的是时间，不超过24小时，对date无意义。对于time对象，如果tzinfo=None，将参考本地时区

tzinfo时区信息不仅仅表示全球24个固定时区，而是可以表示相对于UTC的任何minutes级别的偏移。

tzinfo具体子类需要实现一些方法。时区表示的是地理位置上的固定偏移+dst，其中地理位置偏移和具体时间无关，但是dst（夏令时）与具体时间相关，因此utcoffset和dst都接收一个datetime参数，用来确定是否应用dst调整。tzname被设计为一个函数而不是一个属性，并且同样接收datetime参数，是因为一些tzinfo子类基于是否使用dst来返回不同的时区名字，例如相同时区名字的不同变体，表示是否应用夏令时，因此需要datetime参数确定这个时间是否在夏天

- utcoffset(dt)

  返回这个时区在datetime时间到utc的偏移timedelta。偏移不只是常用的1hour，可以是任何timedelta。它需要返回时区调整和dst调整的总和。如果到UTC的offset不能确定，返回None；否则返回timedelta([-1439, 1439] minutes).

  如果utcoffset不返回None，dst也应不返回None

- dst(dt)

  返回这个时区在datetime时间的日间节省时间（将时间提前以充足应用日间时间，夏令时），UTC东部（正offset）的minutes，或者None如果不能确定。如果dst不生效，返回timedelta(0)

  dst以及包含在utcoffset中，因此除非需要单独获取dst，否则不需要访问dst。例如datetime.timetuple()调用tzinfo.dst()来决定是否设置tm_isdst

  tz.utcoffset(dt) - tz.dst(dt)返回只与地理相关的时间偏移。dst是政策相关的，不同国家可以选择使用或不使用dst，使用时可以选择调整不同长度的dst

- tzname(dt)

  返回这个时区的名字。datetime模块没有定义任何名字相关的属性，而且时区名字不需要有任何特殊意义，即可以是任何名字，例如"GMT", "UTC", "-500", "-5:00", "EDT", "US/Eastern" "America/New York"。dt参数可以用于确定是否处于夏令时，并返回不同的时区名字，例如"+4:00"/"+4:00 DST"

这3个函数被datetime/time对象调用以响应它们自身的相同名字的方法。datetime将self传递给dt参数，time将None传递给dt参数

- fromutc(dt)

  被默认的datetime.astimezone()实现调用。astimezone允许为datetime设置不同的tzinfo，同时根据新的tzinfo调整date/time数据，来表示相同的utc时间。

  astimezone和fromutc将dt参数的date/time数据与tzinfo视为完全不相关的。date/time总是表示utc的时间，tzinfo表示某个特定的时区。astimezone通过指定tzinfo参数产生这样的datetime，fromutc基于这样的datetime，根据tzinfo调整date/time，使得date/time表示tzinfo时区中的时间，产生date/time和tzinfo相关的datetime

  astimezone简单将datetime的tzinfo设置为另一个tzinfo，然后调用tzinfo.fromutc将date/time调整到这个tzinfo

  fromutc名字的意思就是从utc时区的date/time转换到tzinfo时区的date/time

  fromutc具有默认实现，绝大多数tzinfo子类只需要直接继承。它是基于utcoffset/dst实现的

dateutil.tz标准库提供了固定UTC偏移的tzinfo子类

## timezone

tzinfo的子类，每个实例表示一个到UTC的固定偏移

timezone(timedelta_offset, name=None)

忽略dst，因而忽略dt参数

如果构造timezone时不指定tzname，则tzname(dt)返回"UTC+HH:MM"格式的名字。tzinfo最小只能以minute为偏移

dst(dt) == None

fromutc(dt) = dt + utcoffset(None)

utc = timezone(timedelta(0))

## strftime/strptime

date/datetime/time对象都支持strftime进行格式化。本质都是调用time模块的time.strftime(fmt, d.timetuple())。对于date，hour/minute/second/microsecond总是0；对于time，year=1900，month=1，day=1

datetime支持strptime。本质是调用time模块的time.strptime(date_string, fomat)产生struct_time，然后使用struct_time构造一个datetime

strftime/strptime是C语言对应函数的包装

就像printf的格式化一样，格式化字符串fmt可以同时包含plain text和指示符%X。如果只能包含指示符，就不需要%了。和printf的唯一区别就是，不需要在fmt之后传递指示符%X对应的参数，因为它们会默认使用datetime对应的属性

小写意味着简写，大写代表全写

- %%

  %转义

- Week相关

  - %a：缩写的weekday，Sun，Mon
  - %A：全写的weekday，Sunday，Monday
  - %u：weekday的数字，Monday=1，Sunday=7
  - %w：weekday的数字，Sunday=0，Saturday=6
  - %W：一年中的星期数，0～53，Monday为星期的第一天
  - %U：一年中的星期数，0～53，Sunday为星期的第一天

- Month相关

  - %b：缩写的month，Jan，Feb
  - %B：全写的month，January，Februrary
  - %d：DD格式的monthday，01，02，31
  - %m：MM格式的month，01，02，12

- Year相关

  - %j：DDD格式的yearday，001，002，366
  - %y：YY格式的year，00，01，99
  - %Y：YYYY格式的year，0000，0001，9999

- Hour相关

  - %H：HH格式的24小时hour，00，01，24
  - %I：HH格式的12小时hour，00，01，12
  - %p：AM or PM

- Minute相关

  - %M：MM格式的minute，00，01，59

- Second相关

  - %S：SS格式的second，00，01，59

- Microsecond相关

  - %f：ffffff格式的microsecond，000000，000001，999999

- 时区相关

  - %z：+HHMM/-HHMM格式的UTC offset，empty if naive，+0000，-0400，+1030
  - %Z：时区名字，empty if naive，UTC，EST，CST

- local字符串表示

  - %c：本地date+time表示
  - %x：本地date表示
  - %X：本地time表示
