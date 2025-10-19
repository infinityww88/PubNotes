# 常用string操作

## Format String Syntax

str.format方法和Formatter类共享相同的字符串格式化语法。这个语法与f-string相关，但是有不同之处

格式化字符串包含{}包围的replacement fields。任何不包含在{}中的字面量，不作改变地复制到输出。如果需要输出{和}，双写它们，{{和}}

    replacement_field: "{" [field_name] ["!" conversion] [":" format_spec] "}"
    field_name: arg_name("." attribute_name | "[" element_index "]")
    arg_name: [identifier | digit+]
    attribute_name: identifier
    element_index: digit+ | index_string
    index_string: <any source character except "]">+ #key
    conversion: "r" | "s" | "a"
    format_spec: <Format Specification Mini-Language>

field_name忽略时，自动按照0，1，2，...应用位置参数(不能应用关键字参数），'{} {}'.format(a, b)等价与'{0}, {1}'.format(a, b)。自动位置参数与手动位置参数不能混合使用，要么使用自动位置参数要么使用手动位置参数，但是它们都是位置参数，都可以和关键字参数混合使用

因为arg_name没有引号分割，因此不能指定某些属性/键字符串，例如'10'或者':-]'

conversion字段使参数格式化之前进行转换。默认一个value的格式化使通过调用value自己的\_\_foramt__完成，例如datetime.\_\_format__(fmt)使用strftime语法进行格式化。但是有时我们希望value以字符串形式参与格式化而不是调用它自己的format定义。通过在调用\_\_format__之前将value转换成string来跳过正常的formatting逻辑

有3个conversion flags

    !s calls str on value
    !r calls repr on value
    !a calls ascii on value

repr返回一个可以生成value的字符串字面量

ascii与repr类似，但是对于non-ASCII字符使用\x, \u, \U进行转义

format_spec字段包含value应该如何表示的指示，包括诸如field width，alignment，padding，decimal precision之类的细节。每种value类型可以定义它自己的FormatingMiniLanguage或者对format_spec的解释，例如datetime

绝大多数built-in类型支持一个通用的formatting mini-language

format_spec字段可以包含嵌套的replacement fields在其中，这些嵌套字段可以包含field_name（指定哪个参数），conversion flag（!s/r/a），以及format specification，但是更深层次的嵌套是不允许的。format_spec中的replacement fields在format_spec被解释之前进行替换。这允许动态指定一个value的格式化

### Format Specification Mini-Language

格式化指示符format specifications被用于format string中的replacement fields，来定义value如何被表示。它们也可以被直接传递给built-in format函数。每个formattable（具有\_\_format__方法）类型可以定义format specifications如何解释

每个类型都有自己的\_\_format__，接收一个spec字符串（格式化指示符），用于格式化value自己，因此spec也是value自己独特的指示符，例如datetime

format(value, spec)调用value.\_\_format__(spec)

str.format使用format string格式化一组value。每个replace_field的format_spec传递给相应被格式value的\_\_format__，用于替换这个field

"abc {0:spec0} {1:spec1}".format(a, b) == "abc %s %s" % (a.format(spec0), b.format(spec1))

绝大多数built-in类型实现下面的格式化指示符，尽管一些格式化指示符只能用于特定数值类型

一个通用的转换是empty format string("")产生str(value)相同的结果

### 标准格式化指示符

    format_spec: [[fill]align] [sign] [#] [0] [width] [grouping_option] [.precision] [type]
    fill: <any character>
    align: "<" | ">" | "+" | "^"
    sign: "+" | "-" | " "
    width: dight+
    grouping_option: "_" | ","
    precision: digit+
    type: "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%" |

- align

    如果指定一个有效的align值，它前面可以有一个fill字符，可以是任何字符，如果忽略默认是空格。在f-string和str.format中，fill无法设置成{和}，因为它们格式化多个value，{}用于指定replace field。但是value自己的format函数可以，因为不需要{}指定replace field

    | Option | Meaning |
    | --- | --- |
    | < | 使字段在可用空间中左对齐，默认 |
    | > | 使字段在可用空间中右对齐 |
    | ^ | 使字段在可用空间中居中对齐 |
    | = | 右对齐，但是填充字符在在sign之后（如果存在），digits之前。只用于数值类型，如果field width前面是0，将是默认行为 |

    除非指定最小field width，否则field width将总是和填充的data相同长度，此时align将没有意义

- sign

    只能用于数值类型

    | Option | Meaning |
    | --- | --- |
    | + | 正负数都有符号 |
    | - | 只有负数有符号 |
    | space | 负数有符号，正数前有一个前导空格 |

- '#'

    '#'选项将导致"alternate form"用于转换。不同类型的alternate form有不同的定义。

    只用于integer，float，complex和Decimal

    integer：当使用二进制、八进制、十六进制时，这个选项添加相应的前缀'0b', '0o', '0x'

    float/complex/Decimal：这个选项总是添加小数点，即使后面没有数字。通常小数点只在后面有数字时才出现。此外对于g/G转换，结果中托尾的0将不会被移除

- ','

    ','选项使用comma作为千位分隔符。要使用locale相关分隔符，使用'n'作为正数转换选项

- '_'

    _选项对浮点表示类型和'd'选项正数表示使用_作为千分位分隔符。对于'b', 'o', 'x', 'X'选项，'_'将每4个字符插入一个

- width

    width是一个十进制整数表示最小字段宽度。如果不指定，field width总是content的长度，因此没有align发生。当指定width时，如果content长度小于widht发生对齐，否则field width仍然是content长度

- precision

    对于'f'和'F'格式化的浮点数指定小数点后应该显示多少个数字

    对于'g'和'G'格式化的浮点数小数点前后共显示多少个数字

    对于非数值类型，指定maximum field size，最多使用content中的多少个字符（最左边的字符）。不可用于整数类型

- type

    对于字符串类型

    | Type | Meaning |
    | --- | --- |
    | s | 字符串格式化，对于字符串是默认类型，可以忽略 |
    | None | 与s相同 |

    对于整数类型

    | Type | Meaning |
    | --- | --- |
    | b | 二进制类型 |
    | c | 字符，将整数转换为对应的unicode字符 |
    | d | 十进制整数 |
    | o | 八进制整数 |
    | x | 十六进制整数，小写 |
    | X | 十六进制整数，大写 |
    | n | 与d相同，除了它使用locale setting插入正确的分隔符 |
    | None | 与d相同，除了它使用locale setting插入正确的分隔符 |

    整数也可以被用于浮点数转换类型，除了浮点数的'n'和None选项

    对于浮点数类型

    | Type | Meaning |
    | --- | --- |
    | e | 科学计数法指数表示，使用e指示exponent，默认precision=6 |
    | E | 科学计数法指数表示，使用E指示exponent，默认precision=6 |
    | f | 定点数表示，默认precision=6 |
    | F | 与f相同，但是将nan转换成NAN，inf转换成INF |
    | g | 通用格式 |
    | G | 与g相同，除了e、nan、inf都变成大写 |
    | n | 与g相同，除了使用locale setting插入正确的分隔符 |
    | % | 百分数，将浮点数乘以100，并以'f'选项格式化显示，跟随一个% |
    | None | 与g相同，除了对于fixed-point表示，小数点后至少有一个数字，默认精度尽可能高来显示特定数值。总体效果是匹配str()的输出并被其他format modifiers修改

    浮点数只有两种表示：fixed-point(123.456)和科学计数法(1.23456e2)

    浮点数'g'通用格式

        对于给定precision p >= 1，四舍五入number到p个有效数字，然后根据它的magnitude以fixed-point或者科学计数法格式化结果

        正负无穷，正负0，nan被格式化为inf，-inf，0，-0，nan，无视精度

        精度=0等价于精度=1，默认精度=6

绝大多数情况下，Format语法与printf-format语法相似，除了使用{}而不是位置确定格式化的参数，以及使用前导:而不是后缀%指定指示符。例如'%03.2f'可以转换为{:03.2f}

这些指示符基本上用于所有built-in类型，但是一些类型可以有自己特定的指示符，例如datetime

'{:%Y-%m-%d %H:%M:%S}'.format(datetime)

str.format和f-string只是把format-spec传递给value类型的\_\_format__方法，只不过大多数built-in类型共享上面的format-spec语法，除了datetime等具有自己spec的类型

## Template strings
