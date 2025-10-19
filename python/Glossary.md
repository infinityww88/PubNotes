# Glossary

## type hint

一个annotation，指定一个variable，一个class属性，一个函数参数或者返回值的期望类型
Type hint是可选的并且不是强制的，但是它们可以被用于静态分析工具以及IDEs的代码完成和重构

annotation是与一个variable，class属性，函数参数或返回值关联的标签，用作type hint
局部变量的annotations不可以在运行时访问，但是全局变量，类属性，函数参数和返回值的annotation被存储在模块（全局变量），类（属性），函数（参数和返回值）的__annotations__属性中，或者通过typing.get_type_hints()访问
typing.get_type_hints(obj)通常就是__annotations__，返回一个dict

## named tuple

既可以通过下标索引又可以通过名称索引的tuple。
collections.namedtuple()可以创建这种类型的对象

## parameter

Python函数有5中参数：

- positional-or-keyword

    既可以通过位置传递，也可以通过关键字传递的参数，这是参数的默认类型

    def func(foo, bar=None): ...

    foo，bar既可以通过位置传递，也可以通过关键字传递

- positional-only

    只能通过位置传递的参数

    Python没有定义positional-only参数的语法，但是一些built-in函数只能通过位置传递参数

- keyword-only

    只能通过关键字传递参数

    关键字参数通过将一个var-positional参数或者一个*放在关键字参数之前来定义，即\*parameter之后的参数能通过关键字传递

    def func(arg, *, kw_only1, kw_only2): ...

    def func(arg, *args, kw_only1, kw_only2): ...

    kw_only1, kw_only2只能通过关键字传递参数

  - var-positional

    指示可以提供任意的positional arguments序列，这些参数将被指定的参数名接收为list

    def func(*args, **kwargs): ...

    所有的位置参数都被args接收为list

  - var-keyword

    指示可以提供任意多个keyword arguments，这些参数将被指定的参数名接收为dict

    def func(*args, **kwargs): ...

    所有args之后的关键字参数都被kwargs接收为dict

Parameters可以指定可选和必须参数，以及对一些可选参数指定默认值

## argument

Python有2中argument，关键字参数和位置参数。位置参数必须出现在关键字参数之前。

- 关键字参数

    指定名字传递值的参数，或者前缀以**的dict，dict中的每个key-value都作为关键字参数传递

    complex(real=3, imag=5)
    complex(**{'real': 3, 'imag': 5})

- 位置参数

    不是keyword的参数。位置参数可以出现在参数列表的开始，或者被传递为一个前缀以*的iterable对象

    complex(3, 5)
    complex(*(3, 5))
