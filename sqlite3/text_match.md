# Text Match

LIKE 运算符进行一个模式匹配比较。LIKE 右边的操作数是一个 pattern，左边是一个 string value。% 匹配 0 或多个字符，_ 匹配单个字符，其他字符匹配自己（大小写不敏感）。注意，sqlite 默认只对 ascii 立即大小写，对 > ascii 的 unicode 字符 LIKE 是大小写敏感的。

如果有可选的 ESCAPE 子句，则 ESCAPE 后面的表达式必须求值为一个字符的字符串。这个字符用来在 LIKE pattern 中包含 % \_ 字面量。ESCAPE 字符后面的 % \_ 或它自身各自匹配 % \_ 它自身。

LIKE 可以通过 case_sensitive_like pragma 选项设置为大小写敏感：

```sql
PRAGMA case_sensitive_like = boolean;
```

GLOB 运算符类似 LIKE，但是使用 UNIX file globbing 语法的通配符。与 LIKE 不同，GLOB 是大小写敏感的。GLOB 和 LIKE 前面都可以有 NOT 关键字，来反转测试。

REGEXP 运算符是 regexp() 函数的特殊语法。

MATCH 运算符是 match() 函数的特殊语法。

## Like 优化

Where 子句的 LIKE 或 GLOB 运算符有时可能使用 index 来做一个范围搜索，几乎就像 LIKE 或 GLOB 是一个 Between 运算符。这种优化出现的条件是：

- LIKE 或 GLOB 右边必须是一个字符串字面量或绑定到字符串字面量的参数，它不以一个通配符开头
- 如果左边是数字，LIKE 和 GLOB 不会返回 true，这意味着：

  - 左边操作数是一个 TEXT affinity 的 indexed column
  - 右边 pattern 不以 \- 或数字开头

  这是因为数字不以字符顺序排序，例如 9 < 10 但是 '9' > '10'

- 对于 GLOB 运算符，column 必须使用内置的 BINARY collating sequence indexed
- 对于 LIKE 运算符，如果 case_sensitive_like 模式开启，column 必须使用 BINARY collating sequence indexed，否则必须使用内置的 NOCASE collating sequence indexed
- 如果使用 ESCAPE 选项，ESCAPE 字符必须是 ASCII，或一个字节的 UTF-8

如果 x = "hello", 则 y = "hellp"。p 是 o 的下一个字符。

The LIKE and GLOB optimizations consist of adding two virtual terms like this: column >= x AND column < y。

绝大多数情况下，LIKE 或 GLOB 会扫描 x-y 之间的每条 row 进行测试，因为无法知道 x 右边还有什么其他的通配符。但是如果 x 的右边只有一个通配符的话，则不会扫描，直接返回 x-y 之间的所有结果，因为它们都会通过测试。

普通表的 text 没有前缀索引，如果有 index，会按全部字符序列进行排序和比较。FTS5 表有前缀索引。
