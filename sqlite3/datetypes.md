# Datetypes

绝大多数数据库引擎（几乎除了 sqlite 的所有数据库）都使用静态、固定的类型。静态类型的数据，一个 value 的类型取决于它的容器，即它所在 column 声明的类型。

Sqlite 使用动态类型系统（就像脚本语言一样，隐式地可以把 string 当 int/float，把 int/float 当 string，把 int 当 float 等等）。Sqlite 中 datatype 关联到 value 本身，而不是 column。动态类型的 sqlite 不仅完全兼容静态类型数据库的功能，还可以做到静态类型数据库中不可能的做到的事情。Flexible Typing is a feature，not bug。

Sqlite 3.37.0 开始，Sqlite 为更偏好静态类型数据库的开发者，提供了 STRICT table 来强制静态类型。

## Storage class 和 Datatypes

## Flexible Typing
