# Datetypes

绝大多数数据库引擎（几乎除了 sqlite 的所有数据库）都使用静态、固定的类型。静态类型的数据，一个 value 的类型取决于它的容器，即它所在 column 声明的类型。

Sqlite 使用动态类型系统（就像脚本语言一样，隐式地可以把 string 当 int/float，把 int/float 当 string，把 int 当 float 等等）。Sqlite 中 datatype 关联到 value 本身，而不是 column。动态类型的 sqlite 不仅完全兼容静态类型数据库的功能，还可以做到静态类型数据库中不可能的做到的事情。Flexible Typing is a feature，not bug。

Sqlite 3.37.0 开始，Sqlite 为更偏好静态类型数据库的开发者，提供了 STRICT table 来强制静态类型。

## Storage class 和 Datatypes

Sqlite 数据库中存储的每个 value（而不是 column），都有且仅有以下之一的 storage class：

- NULL
- INTEGER
- REAL
- TEXT
- BLOB

storage class 比 datatype 更具一般性。INTEGER 存储类包含 7 个不同 size 的 integer datatypes。

datatypes 是更具体的类型，也是存储到磁盘上的类型，例如 byte 占用一个字节，int32 占用 4 个自己，double 占用 8 个字节。storage class 是 sqlite 中声明的通用类型，一旦磁盘上存储的各种整数读取到内存中，它们就被转化为 storage class。

这与 sqlite 动态类型的设计是一样，尽可能模糊类型，由程序去具化类型。在 sqlite 只使用这 5 种类型声明 type，在应用程序中转化为所需的具体类型。如 .NET 中：

| .NET|SQLite|Remarks|
| --- | --- | --- |
| Boolean|INTEGER|0 or 1|
| Byte|INTEGER||
| Byte[]|BLOB||
| Char|TEXT|UTF-8|
| DateOnly|TEXT|yyyy-MM-dd|
| DateTime|TEXT|yyyy-MM-dd HH:mm:ss.FFFFFFF|
| DateTimeOffset|TEXT|yyyy-MM-dd HH:mm:ss.FFFFFFFzzz|
| Decimal|TEXT|0.0########################### format. REAL would be lossy.|
| Double|REAL||
| Guid|TEXT|00000000-0000-0000-0000-000000000000|
| Int16|INTEGER||
| Int32|INTEGER||
| Int64|INTEGER||
| SByte|INTEGER||
| Single|REAL||
| String|TEXT|UTF-8|
| TimeOnly|TEXT|HH:mm:ss.fffffff|
| TimeSpan|TEXT|d.hh:mm:ss.fffffff|
| UInt16|INTEGER||
| UInt32|INTEGER||
| UInt64|INTEGER|Large values overflow|
||||

## Boolean Datatype

Sqlite 没有单独的 boolean storage class，boolean 被存储为整数 0 和 1.

Sqlite 识别关键字 TRUE 和 FALSE，但是它们只是 0 和 1 的符号。

## Date and Time Datatype

Sqlite 没有单独的 date 和 time 类型，而是使用 Text，Real，Integer 存储日期时间值，然后提供了一组 date time 函数来操作这些类型的日期时间值。

应用程序可以选择这 3 种类型的任何一种来存储日期、时间，并使用时间函数在它们之间进行转换。

## Type Affinity

Sqlite 最大程度兼容其他类型的数据库引擎的 sql 语句，这其中也包括了 column 类型的声明。即在 Sqlite 中可以用 Mysql 的数据类型声明 column，但是 Sqlite 会将这些类型转换为相应的 storage class，这称为 type affinity。

|Example Typenames From The CREATE TABLE Statement or CAST Expression|Resulting Affinity|Rule Used To Determine Affinity INT|
| --- | --- | --- |
INTEGER TINYINT SMALLINT MEDIUMINT BIGINT UNSIGNED BIG INT INT2 INT8|INTEGER|1||
CHARACTER(20) VARCHAR(255) VARYING CHARACTER(255) NCHAR(55) NATIVE CHARACTER(70) NVARCHAR(100) TEXT CLOB|TEXT|2|
BLOB no datatype specified|BLOB|3|
REAL DOUBLE DOUBLE PRECISION FLOAT|REAL|4|
NUMERIC DECIMAL(10,5) BOOLEAN DATE DATETIME|NUMERIC|5|
||||
