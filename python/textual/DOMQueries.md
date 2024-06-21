# DOM Queries

## Query one

query_one 方法查找匹配一个 selector 或 type 的 widget。

```py
send_button = self.query_one("#send")
```

如果没有匹配的 widgets，Textual 会抛出 NoMatches 异常。如果有多个匹配，Textual 会抛出 TooManyMatches 异常。

可以提供第二个参数，指示期望的 type，确保得到想要的类型：

```py
send_button = self.query_one("#send", Button)
```

如果 matched widget 不是 Button，即 isinstance(widget, Button) == False，Textual 会抛出 WrongType 异常。

第二个参数允许诸如 MyPy 的类型检查器知道返回的类型。否则 MyPy 只会知道 query_one 的结果是一个 Widget。

还可以用一个 widget type 替换 selector，这将会返回那个类型的 widget。

```py
my_button = self.query_one(Button)
```

## Making queries

Apps 和 widgets 还有一个 query 方法来查找 widgets。它返回一个 DOMQuery 对象，这是一个 list-like 的 widgets container。

类似 jQuery，每个 query 返回的都是匹配的 widget 的集合。

如果不用参数调用 query，会得到一个包含所有 widgets 的 DOMQuery。这个方法是递归的，它还会返回 child widgets。

```py
# 遍历所有 widgets
for widget in self.query():
    print(widget)
```

在 app 上调用 query()，它会返回 app 的所有 widgets。在 widget 上调用 query()，它返回 widget 的所有 children。

所有 query 和相关方法同时可以用于 App 和 Widget。

### Query selectors

可以使用 selector 调用 query。query 与 query_one 的区别是，query() 返回所有查到的组件的集合 DOMQuery，query_one 只返回一个组件，但是这个组件对查询必须是唯一的，否则会抛出异常。

```py
# 查找所有 Button
for button in self.query("Button"):
    print(button)
```

任何用于 CSS 的 selector 都可以用于 query 方法：

```py
for button in self.query("Dialog Button.disabled"):
    print(button)
```

### Results

Query objects 有一个 results 方法，是遍历 widgets 的另一种方法。如果提供一个 type，这个方法只会产生那个类型的 widgets。

下面的例子查询所有 disabled 的 widgets，然后遍历其中所有的 Button objects。

```py
for button in self.query(".disabled").results(Button):
    print(button)
```

This method allows type-checkers like MyPy to know the exact type of the object in the loop. Without it, MyPy would only know that button is a Widget (the base class).

## Query objects

query 方法返回一个 DOMQuery object，可以一个循环中遍历。DOMQuery 就像一个 Python list，并支持所有 list 相关操作，例如 query[0], len(query), reverse(query) 等等。

还有很多其他简化获取和修改 widgets 的方法。

## First and last

first 和 last 方法返回 selector 匹配的 widgets 的第一个和最后一个。

如果没有匹配，Textual 会抛出 NoMatches 异常。

first() 和 last() 接受一个 expect_type 参数，检查和提示最后一个 widget 的类型：

```py
# 查找所有 disabled widget，返回最后一个 widget，并检查它是否是 Button，如果不是，Textual 抛出 WrongType 异常
disabled_button = self.query(".disabled").last(Button)
```

这允许 MyPy 这样的类型检查器检查类型。

## Filter

Query object 有一个 filter 方法，可以进一步调整 query 的结果。它返回一个新的 query object，其中的 widgets 匹配 filter 指定的 selector。

```py
# Get all the Buttons
buttons_query = self.query("Button")
# Buttons with 'disabled' CSS class
disabled_buttons = buttons_query.filter(".disabled")
```

## Exclude

Query objects 有一个 exclude 方法，它是 filter 的取反逻辑。exclude 从 query object 中移除匹配新 selector 的 widgets。

```py
# Get all the Buttons
buttons_query = self.query("Button")
# Remove all the Buttons with the 'disabled' CSS class
enabled_buttons = buttons_query.exclude(".disabled")
```

## Loop-free operations

一旦得到一个 query object，可以迭代它，在匹配的 widgets 上调用方法。

Query 还可以像 jQuery 一样，直接在整个集合上执行一个方法，而不用显式循环。

```py
# disable 所有 Button
self.query("Button").add_class("disabled")
```

等价于

```py
for widget in self.query("Button"):
    widget.add_class("disabled")
```

可以在 Query Object 上执行的其他 loop-free 方法：

- add_class
- blur（remove focus）
- focus
- refresh
- remove_class
- remove：从 DOM 移除匹配的 widgets
- set_class
- set：在 widget 上设置常见属性
- toggle_class

