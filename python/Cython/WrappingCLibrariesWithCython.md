# Wrapping C Libraries with Cython

控制复杂性是计算机编程的本质    —— B.Kernighan

Cython尽管不能想一些工具一样自动将外部C库暴露在Python中，但是它提供了简单明了的wrap 外部库的能力。Cython还可以使Cython定义的C-level construct在外部C库中可用，这在将Python嵌入一个C application非常有用

因为Cython同时理解Python和C语言，它允许interfacing的全部控制

## 在Cython中声明外部C code

要包装一个C库，必须先声明C组件的接口。Cython提供extern block语句完成这个工作

```python

cdef extern from "header_name":
    indented declearations from header file

```

这个声明块用于告诉Cython我们希望从指定的C头文件中使用什么C construct

头文件包含在单引号或双引号之间

包含extern block有以下效果：

- cython编译器在生成的source file产生一个#include "header_name"
- 块中声明的types，funcitons，和其他声明在Cython code可用
- Cython在运行时检查C声明被type-correct-manner方式使用，否则产生一个编译错误

extern block中的声明有一个直观的C-like语法（for variables和functions）。它们使用Cython特定语法声明structs和unions

Cython使用cdef extern添加任何C声明，在生成文件中放置带有extern modifier的声明。Cython的extern声明必须匹配C声明。单行的extern声明有一些缺陷，因此建议使用extern block

如果只需要在生成的文件中添加#include "header.h"，则可以

```python

cdef extern from "header.h":    # Cython本身是用Python编写
    pass

```

同样，如果头文件不需要时（例如它已经被其他头文件包含），但是我们想要与external code交互interface，可以

```python

cdef extern from *:
    declarations

```

Cython不会自动Wrapping（不像pybind11，cppyy）

Cython中，extern blocks的存在用于保证我们以type-correct manner方式调用和使用C functions，variables，和structs。extern block不自动生成相应的python wrapper。整个extern block生成的唯一的C code是一个简单的#include "header.h"。我们仍然需要写def和cpdef（或者cdef）函数来调用extern block中声明的C函数。否则外部C函数不能在Python中被调用。Cython不解析C文件并自动wrapping C libraries（尽管可以自己编写一个这样的处理器）

Cython处于自身定位和一些特定考虑不提供自动python wrapper（pybind11，cppyy），但是已经有一些项目基于Cython正在实现这一点。

## 声明外部C functions和typedefs

放在extern block中最常见的声明就是C funcitons和typedefs。这些声明几乎就是从C等价概念直接翻译过来的，通常仅有的需要的改变是：

- 将typedef改为ctypedef
- 移除不需要和不支持的关键字例如restrict和volatile
- 确保函数返回值和函数名在一行声明
- 移除行结尾的分号

对于很长的函数声明，可以在左括号之后将行打断成多行

header.h

```C

#define M_PI 3.1415926
#define MAX(a, b) ((a) >= (b) ? (a) : (b))

double hypot(double, double);

typedef int integral;
typedef double real;

void func(integral, integral, real);

real *func_array(integral[], integral[][10], real **);

```

Cython的声明，除了macros，几乎复制粘贴过来

```python

cdef extern from "header.h":
    double M_PI
    float MAX(float a, float b) # 宏被声明为函数
    double hypot(double x, double y)

    ctypedef int integral
    ctypedef double real

    void func(integral a, integral b, real c)

    real *func_array(integral[] i, integral[][10] j, real **k)

```

声明宏常量时，我们声明它就像一个全局double类型变量

声明function-like macro时，就像声明一个常规的C函数

声明中的函数添加来参数名，这不是必须的，但是这允许使用关键字方式调用C函数，并且帮助document函数

Cython支持全部的C声明

可以在extern block声明一些临时typedef，辅助更好地声明其他声明

## 声明和wrapping C structs，unions，enums

使用Cython C-level定义语法声明structs，unions，enums

```cdef extern from "header_name":

    [ctypedef] struct struct_name:
        struct_members

    [ctypedef] union union_name:
        union_members

    [ctypedef] enum enum_name:
        enum_members

```

struct声明前加ctypedef相当于C语言中加typeddef，定义struct同时还声明了一个类型别名可以直接使用

struct，union，enum中只需要声明真正需要使用的字段。如果不使用任何字段，只需要struct作为不透明类型，struct body应该是pass语句

## Wrapping C funcitons

在声明了external functions之后，就可以在Cython访问C函数了，但是要在Python中（Cython外部代码）访问C函数，还需要像wrap普通Cython C函数一样使用def/cpdef为其创建Python wrapper函数

## Wrapping C structs with Extension Types

当Cython访问外部C函数只需要opaque struct类型时，则只需要声明opaque struct类型，不必声明任何字段

## Constants，其他修饰符modifiers，控制Cython生成什么（TODO）

可以在extern block中为C functioss、struct、unions、enums起一个不同的名字，这可以更好地控制C库函数的导入

```python

cdef extern from "printer.h":
    void _print "print"(fmt_str, arg)

```

这个函数在Cython名为_print，但是在C中名为print。因为print在Python已经是函数了。这对struct、union、enum、typedef也是一样

### Exposing Cython Code to C（TODO）

## 错误检查和抛出异常

外部C函数通过返回码和错误标记通知错误状态是很常见的。要正确wrap这些函数，必须在wrapper函数中测试这些情景，当error发生时，显式抛出一个Python异常。

这里不能使用except clause，因为except clause是真正发生了异常，而这里不是发生异常，而是向调用者报告错误状态

## 回调

Cython支持C函数指针。使用这个功能，我们可以wrap使用回调函数指针的C 函数。回调函数可以是不调用Python/C API的纯C函数，或者可以调用任何Python code。这个强大的特性允许我们传递一个运行时创建的Python函数来控制底层C函数的行为

跨语言边界使用回调函数可能会变得复杂，尤其是当需要正确处理异常的时候

一切Python都是对象object，object是python关键字。Python函数也是object。\__call__是object协议。一切定义__call__函数的object都是callable的。Cython可以同时立即Python和C语言代码。合法的Python代码本身也是合法的Cython代码

```python

def f(n):
    return n * n

cdef object o = f
o(10)

```

### Callbacks和异常传播

使用except \*检查和传播函数异常。except \*是函数声明的一部分，在每个函数声明的地方添加except \*到声明的最后

```python

cdef extern from "stdlib.h":
    void qsort(void *array, size_t count, size_t size, int (*compare)(const void *, const void *) except *)

ctypedef int (*qsort_cmp)(const void *, const void *) except *

cdef int int_compare(const void *a, const void *b) except *:
    # ...

```

使用except *，Cython将在每次回调函数调用时检查异常，并在发生异常时正确unwinds call stack和传播异常。这需要消耗一定overhead，但是和改进的error handling相比，少量的性能消耗是值得的

带有cdef callback的异常传播为纯C函数提供了Pythonic的接口
