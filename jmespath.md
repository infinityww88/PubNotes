# JMESPATH Specification

```plain
search(<jmespath expr>, <JSON document>) -> <return value>
```

将 JMESPath 表达式应用到一个 JSON 文档上总是返回一个有效的 JSON，在求值期间没有错误。Structured data in，structured data out。

JSON 支持的类型：

- number（整数和双精度浮点数）
- string
- boolean（true 或 false）
- array
- object
- null

## Grammer(ABNF 格式)

ABNF 语法格式中

```bnf
ruleset     =   alt1 / alt2
ruleset     =/  alt3
ruleset     =/  alt4 / alt5
```

is the same as specifying

```bnf
ruleset     =  alt1 / alt2 / alt3 / alt4 / alt5
```

JMESPath 语法

```bnf
expression  = sub-expression / index-expression / comparator-expression
expression  =/ or-expression / identifier
expression  =/ and-expression / not-expression / paren-expression
expression  =/ "*" / multi-select-list / multi-select-hash / literal
expression  =/ function-expression / pipe-expression / raw-string
expression  =/ current-node
sub-expression  =   expression "." (identifier  /
                                    multi-select-list /
                                    multi-select-hash /
                                    function-expression /
                                    "*")
pipe-expression     =   expression "|" expression
or-expression       =   expression "||" expression
and-expression      =   expression "&&" expression
not-expression      =   "!" expression
paren-expression    =   "(" expression ")"
index-expression    =   expression bracket-specifier / bracket-specifier
bracket-specifier   =   "[" (number / "*" / slice-expression) "]" / "[]"
bracket-specifier   =/  "[?" expression "]"
multi-select-list   =   "[" ( expression *( "," expression) ) "]"
multi-select-hash   =   "{" ( keyval-expr *( "," keyval-expr ) ) "}"
keyval-expr         =   identifier ":" expression
comparator-expression   =   expression comparator expression
comparator          =   "<" / "<=" / "==" / ">" / ">=" / "!="
slice-expression    =   [number] ":" [number] [ ":" [number] ]
function-expression =   unquoted-string ( no-args / one-or-more-args )
no-args             =   "(" ")"
one-or-more-args    =   "(" ( function-arg *( "," function-arg ) ) ")"
function-arg        =   expression / expression-type
expression-type     =   "&" expression
current-node        =   "@"
literal             =   "`" json-value "`"
jsonvalue           =   false / null / true / json-object / json-array / json-number / json-quoted-string
```

优先级（由低到高）：

- pipe: |
- or: ||
- and: &&
- unary not: !
- rbracket: \]
