# 词法分析

## 行结构（line structure）

## 字面量（Literals）

### 格式化字符串字面量（Formatted string literals）

    f_string: (literal_char | "{{" | "}}" | replacement_field)*
    replacement_field: "{" f_expression [ "!" conversion ] [":" format_spec ]}"
    f_expression: (conditional_expression | "*" or_expr)
                    ("," conditional_expression | "," "*" or_expr)* [","] | yield expression
    conversion: "s" | "r" | "a"
    format_spec: (literal_char | NULL | replacement_field)*
    literal_char: <any char except "{", "}" or NULL>

Formatted string literals称为f-string，是以f或F为前缀的字符串。这些字符串可以包含替换字段，它们是被{}包围的表达式。其他字符串总是编译常量，f-string则是运行时真正求值的表达式

转义序列就像其他普通字符串一样标记（除非字面量还被标记为raw string，所有字符都不转义）

{}之外的字符串被当作普通的字面量对待，除了双花括号{{}}，它对{}的转义。单个{}标记一个替换字段，其中包含一个Python表达式。表达式之后，可以有一个!转换字段，后面可以有一个:格式化指示符

替换表达式被当作常规的python表达式求值，除了

    不允许空表达式
    lambda和赋值表达式:=必须被()包围

替换表达式可以包含断行（例如triple-quote字符串），但是它们不能包含注释。每个表达式在f-string出现的上下文中求值，按照从左到右的顺序。如果指定了转换，表达式求值的结果在格式化之前被转换。!s调用str(), !r调用repr(), !a调用ascii()

之后结果会使用format协议被格式化。格式化指示符被传递给表达式结果对象的\_\_format__函数。如果忽略格式化指示符，将传递一个空字符串给\_\_format__。format的结果被包含进最终的字符串

不同类型有自己的\_\_format__，因而可以有自己独特的格式化指示符，例如datetime。因此对于不同类型的对象，可能会指定不同的格式化参数

顶层的格式化指示符可以包含嵌套的替换字段，因此可以使用当前上下文中的变量生成不同的格式化指示符。这些嵌套字段可以包含它们自己的转换指示符和格式化指示符，但是不能包含更深层次的嵌套替换字段。格式化指示符mini语言与format方法相同

如果替换表达式包含字符串，则只能使用和f-string不同的quote符号

反斜线不可以用在表达式中。要在字符串中包含一个需要转义的字符，创建一个临时变量，并在表达式中对它求值

f-string不可用于docstring，即使它不包含任何表达式。因为f-string本质是运行时表达式，而不是运行时常量
