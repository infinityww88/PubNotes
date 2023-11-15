# pyquery

pyquery 可以在 xml 文档上进行 jquery 查询，API 非常类似 jquery。

pyquery 使用 lxml 进行 xml 和 html 操作。

## 快速开始

```py
from pyquery import PyQuery as pq
from lxml import etree

import urllib
```

- 从字符串解析

  ```py
  d = pq("<html></html>")
  ```

- 从 etree 解析

  ```py
  d = pq(etree.fromstrinmg("<html></html>")

  ```

- 从 url 解析


  ```py
  d = pq(url="https://google.com")
  d = pq(url="...", opener=lambda url, **kw: urlopen(url).read())
  ```

- 从文件解析


  ```py
  d = pq(filename="file_path")
  ```

d 就像 jquery 的 $。一个 jquery 元素是一组 html 元素的包装，而不止是一个，尽管很多时候只是一个元素的包装。例如 css 查询的结果是所有匹配选择器的元素的集合。

在 d(...) 传入 css 选择器字符串就可以选择 d 文档中包含的子元素。


```py
>>> d("#hello")
[<p#hello.hello>]
>>> p = d("#hello")
>>> print(p.html())
Hello world !
>>> p.html("you know <a href='http://python.org/'>Python</a> rocks")
[<p#hello.hello>]
>>> print(p.html())
you know <a href="http://python.org/">Python</a> rocks
>>> print(p.text())
you know Python rocks
```

可以在 d 中使用一些 jQuery 中的伪类，例如 :first :last :even :odd :eq :lt :gt :checked :selected :file 。

## 属性

使用 css 属性选择器 选择特定 tag：

```py
d = pq("<option value='1'><option value='2'>")
d('option[value="1"]')
```

操作元素属性：

```py
p = pq('<p id="hello" class="hello"></p>')('p')
print(p.attr("id"))
p.attr("id", "hello")
```

或者 pythonic 方式：

```py
p.attr.id = "hello"
print(p.attr.id)
p.attr["id"] = "world"
p.attr(id="hello", class_="hello2") # 自定义属性
print(p.attr.class_)
p.attr.class_ = "world"
```

## 操作 css

操作 css 类

```py
p.addClass("toto")
p.toggleClass("titi")
p.removeClass("titi")
```

操作 css 样式

```py
p.css("font-size", "15px")
print(p.attr("style"))
p.css({"font-size": "17px"})
```

或者 pythonic 方式：

```py
p.css.font_size = "16px"
print(p.attr.style)
p.css["font-size"] = "15px"
p.css(font_size="16px")
p.css = {"font-size": "17px"}
```

## 使用 css 伪类

- :button

- :checkbox

- :checked

- :child

- :contains("text")

  匹配所有包含指定文本的元素

- :descendant

  right is a child, grand-child or further descendant of left

- :disabled

- :empty

  不包含其他元素的元素

- :enabled

- :eq(index)

- :even

- :file

- :first

- :gt(index)

- :has(selector)

- :header

- :hidden

- :image

- :input

- :last

- :lt(index)

- :odd

- :parent

- :password

- :pseudo

- :radio

- :reset

- :selected

- :submit

- :text

## 元素操作

- 在元素末尾追加内容

  ```py
  d("selector").append(html_string)
  ```

- 在元素开头插入内容

  ```py
  d("selector").prepend(html_string)
  ```

- prepend 或 append 元素到另一个元素前后

  ```py
  p.prependTo(d("selector"))
  p.insertAfter(d("selector"))
  p.insertBefore(d("selector"))
  ```

- 对每个元素执行操作

  ```py
  p.each(lambda i, e: pq(e).addClass("hello2"))
  ```

- 移除一个元素

  ```py
  d.remove("selector")
  ```

- 移除一个元素的内部

  ```py
  d("selector").empty()
  ```

- 返回操作后的 html
 
  ```py
  print(d)
  ```

- 生成 html

  ```
  >>> from pyquery import PyQuery as pq
  >>> print(pq('<div>Yeah !</div>').addClass('myclass') + pq('<b>cool</b>'))
  <div class="myclass">Yeah !</div><b>cool</b>
  ```

- 移除所有名字空间

  ```
  >>> d = pq('<foo xmlns="http://example.com/foo"></foo>')
  >>> d
  [<{http://example.com/foo}foo>]
  >>> d.remove_namespaces()
  [<foo>]
  ```

## 遍历

使用 string selector 过滤 selection list

```
>>> d = pq('<p id="hello" class="hello"><a/></p><p id="test"><a/></p>')
>>> d('p').filter('.hello')
[<p#hello.hello>]
```

选择单个元素

```
>>> d('p').eq(0)
[<p#hello.hello>]
```

查找嵌套元素

```
>>> d('p').find('a')
[<a>, <a>]
>>> d('p').eq(1).find('a')
[<a>]
```

终止一个遍历层级（不再向下遍历）

```
>>> d('p').find('a').end()
[<p#hello.hello>, <p#test>]
>>> d('p').eq(0).end()
[<p#hello.hello>, <p#test>]
>>> d('p').filter(lambda i: i == 1).end()
[<p#hello.hello>, <p#test>]
```

如果元素 id 包含 dot，需要转义 dot

```
>>> d = pq('<p id="hello.you"><a/></p><p id="test"><a/></p>')
>>> d(r'#hello\.you')
[<p#hello.you>]
```

## 完整 api

- pyquery.PyQuery(*args, **kwargs)

  main class

- addClass(value) 为每个元素添加 css 类
- after(value) 在每个 node 后面添加 value
- append(value) 追加 value 到每个 node
- appendTo(value) 追加 nodes 到 value
- base_url
- before(value) 在每个 node 前面 insert value
- children(selector=None) 使用可选的 selector 过滤 self 的 direct children
- clone()
- closest(selector=None) 上下游最近的元素
- contents() 返回所有元素 list，包含 text nodes
- each(func) 对每个元素操作
- empty()
- encoding
- end() Break out of a level of traversal and return to the parent level.
- eq(index) 返回指定 index 元素的 PyQuery
- extend(other) 使用另一个 PyQuery object（一组文档元素的集合）扩展这个 PyQuery object（一组文档元素的集合）
- filter(selector) 使用 string 或 function 过滤 self 自身元素
  ```
  >>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p>')
  >>> d('p')
  [<p.hello>, <p>]
  >>> d('p').filter('.hello')
  [<p.hello>]
  >>> d('p').filter(lambda i: i == 1)
  [<p>]
  >>> d('p').filter(lambda i: PyQuery(this).text() == 'Hi')
  [<p.hello>]
  >>> d('p').filter(lambda i, this: PyQuery(this).text() == 'Hi')
  [<p.hello>]
  ```
- find(selector) 使用 selector 从 self 向下遍历查找元素

  一个 PyQuery 是一组文档元素的集合。filter 只遍历 self PyQuery 对象包含的元素列表，而 find 是递归向下遍历每个元素的元素树

- hasClass(name)

- height(value)

- hide() 添加 display:none 到元素的 style

- html(value=<NoDefault>, **kwargs)

  获取或设置 sub nodes 的 html 表示

  ```
  >>> d = PyQuery('<div><span>toto</span></div>')
  >>> print(d.html())
  <span>toto</span>
  ```

  额外的参数传递给 lxml.etree.tostring.

  设置 text value

  ```
  >>> d.html('<span>Youhou !</span>')
  [<div>]
  >>> print(d)
  <div><span>Youhou !</span></div>
  ```

- insertAfter(value) 插入 self nodes 到 value 后面
- insertBefore(value) 插入 self nodes 到 value 前面
- is_(selector) 如果 selector 至少匹配 PyQuery 中的一个元素，返回 true
- items(selector=None)

  在 sellf 元素上迭代，返回包装每个元素的 PyQuery objects：

  ```
  >>> d = PyQuery('<div><span>foo</span><span>bar</span></div>')
  >>> [i.text() for i in d.items('span')]
  ['foo', 'bar']
  >>> [i.text() for i in d('span').items()]
  ['foo', 'bar']
  >>> list(d.items('a')) == list(d('a').items())
  True
  ```

- make_links_absolute(base_url=None)
- map(func) 使用 func 转换当前 items 后返回新的 PyQuery。func 参数是 index 和 element。在 func 内部，元素还可以通过 this 引用。

- nextAll(selector=None) 返回元素后面的所有内容
- nextUntil(selector, filter_=None)
- not_(selector) 参见 is_(selector)
- outerHtml(method="html") 返回第一个选择的元素的 html 表示
- parents(selector=None) 向上查找祖先元素
- prepend(value) 
- prevAll(selector=None) 子元素树下面的指定 selector 元素前面的所有元素
- remove(expr=<NoDefault>) 从 PyQuery 所在的元素树中移除其元素
- removeAttr(name)
- removeClass(value)
- remove_namespaces() 移除所有命名空间
- replaceAll(expr) 在文档中使用 expr 替换 PyQuery 内容
- replaceWith(expr) 
- root 返回 xml root 根元素
- serialize()
- show()
- siblings(selector=None) 返回元素的兄弟元素，可选使用 selector 过滤结果
- text(value) 返回或设置 sub nodes 的所有 text 表示。doc.text(squash_space=False) 可移除所有 newlines
- toggleClass(value)
- val(value) 返回或设置 input 属性值
- width(value)
- wrap(value) 使用一个 html string（例如<div></div>） 包装 self 每个元素
- wrapAll(value) 类似 wrap，但是将 self 所有元素包装在一个标签下，而不是包装每个元素
- xhtml_to_html() 移除 xhtml 命名空间
  
