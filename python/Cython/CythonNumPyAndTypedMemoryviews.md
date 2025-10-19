# Cython, Numpy, and Typed Memoryviews

所有Python容器从实现角度都有一个相同点：它们都存储到Python objects的引用。如果使用Python list存储100w个ints，每个元素在C-level都是一个boxed PyObject的指针，而不是int。将这个list转换成一个C ints数组是非常昂贵的。需要我们迭代整个list，并把每个PyObject转换成一个C int，同时执行正确的错误检查

大型的一致容器，例如全是floats的list，是非常常见的，不仅仅是在数值编程领域。更进一步，CPUs和现代内存层次hierarchies是对这种情形专门优化的（Local热点）。C语言有固定大小和heap-allocated arrays，C++有std:vector。我们想要的是一种在Python中表示和操作unboxed data 类型的一致连续数组，或者buffer的方法

Python buffers和new Python buffer protocol

Buffers允许我们表示连续大范围的简单数据类型的unboxed data。NumPy数组（Python中最广泛使用的array类型）支持buffer协议。可以将buffer想象成简化的NumPy数组

有效地使用buffers是在Cython code中获得C-level性能的关键，而Cython将它变得非常容易。它对new buffer protocol和NumPy数组有着第一级的支持

## The power of the New Buffer Protocol

New Buffer Protocol是一个C-level protocol。Python object可以实现这个protocol而不影响它们的Python level的接口。它定义了C-level struct，其具有一个data buffer（内存块）和描述buffer layout，data type，和读写权限的元数据（这是C语言编译时语法树中struct元数据的对应体）。Protocol定义了支持它的object必须实现的API

New Buffer Protocol最重要的特性是它以不同方式表示底层数据的能力。它允许NumPy arrays，一些Python built-in类型，和Cython-level array-like object共享相同的数据而不需要复制。使用Cython，我们能够很容易扩展buffer protocol以便和来自外部库的数据一起工作

Protocol细节在Python/C API中有详细描述，但幸运的是Cython允许我们不需要了解protocol细节就可以使用buffers。只要知道当使用buffers的时候，我们可以有效地访问它们的底层数据而不需要复制就足够了

实现了buffer protocol的类型：

- NumPy ndarray：NumPy包
- Built-in bytes和bytearray
- 标准库的array.array
- 标准库的ctypes arrays
- 各种第三方库：例如Python Imaging Library（PIL）

还有另外一种built-in Python类型，memoryview，它唯一的目的就是在Python level上表示一个C-level的buffer

通过传递给mmemoryview（callable）一个实现protocol的object来创建一个memoryview

```python
bb = b'hello, world'
memv = memoryview(bb)
```

memv和bb共享bytes中的数据。操作memoryview可以得到在C-level上操作buffer的感觉

```python
memv[0] == 'h'
```

Slicing返回另一个memoryview，它和原始memoryview共享底层bytes数据

```python
memv[:10]
memv[:10][0]
```

由于bytes object是immutable，使用bytes创建的memoryview也是只读的。memoryview的读写权限等于底层数据的读写权限。这就是为什么Prtotocol的元数据包含读写权限的原因

```python
memv.readonly == True
memv[0] = 'F' => TypeError: cannot modify read-only memory
```

如果使用bytearray创建memoryview，就可以共享并修改buffer中的数据

memoryview有一些可以查询底层buffer元数据的属性

Python标准库提供与外部C库交互的模块ctypes，但是它比较初级，基本被废弃了

memoryview的format来自struct标准库模块的指示符

## Typed Memoryviews

Cython有一个C-level类型，typed memoryview，它概念上和Python memory view重叠并且扩展了它，这样我们就不需要直接操作Python的memoryview了

typed memoryview用来使用特定类型从buffer中查看数据。但是它操作在C-level上，而不是想Python的memoryview操作在python level上，因此具有最小的python消耗并且非常高效

Typed Memoryview具有memoryview-like的接口（它们的主要区别在一个才C-level，一个在Python level，例如extend、insert、index等函数，一个用C-level实现，一个用Python level实现）

Typed Memoryview给设计用来和buffer protocol一起工作，因此它可以高效地支持buffer-producing object，允许共享data buffering而不copy

```python
def sum(double[:] mv):
    cdef double d, ss = 0.0
    for d in mv:
        ss += d
    return ss
```

double[:] mv声明mv为typed memoryview，double为底层数据类型，\[:]表示一个一维memoryview对象

当从python中调用sum时，传递一个Python Object（编译后的PyObject），它被assign给mv，mv将访问这个object的底层数据buffer。如果object不能提供一个buffer，即它不支持buffer protocol，将抛出一个ValueError异常。否则，它就提供另一个C-level buffer给memoryview使用。迭代mv就像一个常规Python object一样

这段代码中d和ss声明为c变量，避免了Python的overhead。但是for d in my仍然设计PyObject的调用，即Python level的调用

### C-level Access to Typed Memoryview data

```python
def sum(double[:] mv):
    cdef:
        double ss = 0.0
        int i, N
    N = mv.shape[0]
    for i in range(N):
        ss += mv[i]
    return ss
```

i, N被静态声明为C int变量，这样for i in range(N)被翻译为C语言的for(i = 0; i < N; i++)，ss和mv\[i]都被直接翻译为C level的代码，而略过生成Python/C API的code（PyObject），因此这段代码严格等价与C code

Python level调用指的是PyObject相关的调用，Cython将Python object编译为C code中的PyObject。C-level调用则指的就是严格的C语言层面语句

### Trading Safety for Performance

每次访问memoryview，Cython检查index是否在bounds内。如果超出bounds，就抛出IndexError。还有Cython允许使用负数index索引memoryviews，就像Python lists一样

如果我们自信确保index不会超出范围而且不使用负数索引（Cython也会检查index是否是负数以将其转化为相应的正数索引），可以让Cython关闭边界检查——boundscheck和wraparound

```python

from cython cimport boundscheck, wraparound

def sum(double[:] mv):
    with boundscheck(False), wraparound(False): # context manager，关闭边界检查和负数索引
        for i in range(N):
            ss += mv[i]

```

如果关闭边界检查之后index超出了边界或使用负数索引（仍然是超出边界），可能导致segment fault

要为整个函数关闭边界检查和负数索引

```python
from cython cimport boundscheck, wraparound

@boundscheck(False)
@wraparound(False)
def sum(double[:] mv):
    # ...
    for i in range(N):
        ss += mv[i]
    # etc.
```

要为整个扩展模块关闭边界检查和负数索引，在文件顶部特殊的Cython comment中使用编译器指示符

```python
# cython: boundscheck=False
# cython: wraparound=False

def sum(double[:] mv):
    # ...
    for i in range(N):
        ss += mv[i]
    # etc.
```

还可以使用--directive flag编译选项在全局范围开启这些指示符

### Declaring Typed Memoryviews

当声明一个typed memoryviews时，我们可以控制很多属性

- Element Type

    元素类型，例如int、float、double、complex等等。它可以是ctypedef别名，还可以是结构体类型，甚至范型类型

- Dimensionality

    维度。Typed memoryviews当前最多有7个维度，要声明一个3维typed memoryview，在类型后面的方括号中使用逗号分隔的冒号，每个冒号表示一个维度，double[:, :, :]

- Contiguous or strided data packing

    typed memoryview中带跨幅带维度和带跨幅的buffer兼容。这可以使typed memoryview访问底层带跨幅的底层数据

- C or Fortran contiguity

    C contiguity（C连续性）是列主序（那个维度连续在一起），即最后一个维度是连续的。Fortran contiguity是行主序，即第一个维度是连续的。如果可能，从性能角度来说将数组声明为C/Fortran连续性是有益的。因为这使得Cython产生更快的代码而不必采用strided。Strided（跨幅）的主要目的就是使用不同连续性访问buffer，例如以行主序的方式访问列主序的底层buffer

- Direct or indirect access

    直接访问是默认的，并且覆盖了几乎绝大部分使用情形。它指明dimension可以使用直接的index算数来访问底层数据。如果为一个dimension指明间接访问，底层buffer存储一个到另一个buffer array的指针。当访问这个维度的时候，访问的另一个buffer（即这个维度每个item都可能不再同一块连续的内存区域。

Typed memoryviews允许高效访问内存buffer，而不需要任何Python overhead（Cython最终是C code）。Memoryviews类似NumPy的array buffer，但是它有更多的功能和更干净的语法

Memory可以用于任何context（函数参数，module-level，cdef class属性等等），而且可以从任何实现buffer protocol的object得到

```python
from cython.view cimport array as cvarray
import numpy as np

# Memoryview on a NumPy array
narr = np.arange(27, dtype=np.dtype('i')).reshape((3, 3, 3))
cdef int [:, :, :] narr_view = narr

# Memoryview on a C array
cdef int carr[3][3][3]
cdef int [:, :, :] carr_view = carr

# Memoryview on a Cython array
cyarr = cvarray(shape=(3, 3, 3), itemsize=sizeof(int), format="i")
cdef int [:, :, :] cyarr_view = cyarr

# 从一个memoryview向另一个复制
carr_view[...] = narr_view
cyarr_view[:] = narr_view

# 将一个元素赋给memoryview中所有元素
narr_view[:, :, :] = 3

# 引用和赋值memoryview
carr_view[0, 0, 0] = 100

# 使用memoryview不需要GIL，只有设计PyObject的C code才会需要GIL

# 接受memoryview作为参数的函数同样能处理NumPy array，C array，Cython array，在参数赋值的时候，直接将它们转换成typed memoryview

```

## 语法

Memoryview使用和NumPy相似的**Python slicing**语法。一个:表示一个slice。一个slice可以是

- x：表示索引第x位置上第元素
- x:y：表示获取从x位置到y位置上到slice
- x:y:s：表示获取从x位置到y位置，step=s到slice

对于多维数组，每个slice索引一个维度，因此经常可以看见这样到语法：

    arr[:2, 1, 3:-1:2]
    这表示arr是一个3D memoryview。第一个维度索引0到2的slice，第二个维度索引第一个元素，第3个维度索引3到结尾（-1）且step=2的slice。这应该返回一个2D memory，因为第一个和第三个索引都是范围slice，第二个索引则引用单一元素

```python
cdef int[:] view1D = exporting_object

cdef int[:, :, :] view3D = exporting_object

def process_3d_buffer(int[:, :, :] view not None):  # not None的参数声明自动rejects None输入。默认是可以的，以便可以返回这个None参数
    pass
```

Cython自动reject不兼容的buffer，例如传递一个3D buffer给一个2D buffer参数，将抛出ValueError

## 索引

索引访问memoryview自动转换为memory地址

```python
cdef int[:, :] buf = exporting_object
print(buf[1, 2])
```

负数索引也可以，从相应维度的结尾开始，-1是最后一个元素

Indexing和slicing可以使用或不使用GIL完成。它基本上像NumPy一样工作。如果索引指定了每个维度的index，则得到基本类型（int，long，float，double），否则得到一个新view

省略号意味着为为每个未指定维度得到连续slices

```python
import numpy as np

exporting_object = np.arange(0, 15 * 10 * 20, dtype=np.intc).reshape((15, 10, 20))

cdef int[:, :, :] my_view = exporting_object

# 下面3个语句等价。得到位于第10个位置处的2D memoryview
my_view[10]
my_view[10, :, :]
my_view[10, ...]

```

## 复制

```python
cdef int[:, :, :] to_view, from_view
# 初始化

# 以下3中复制方法等价
to_view[...] = from_view
to_view[:] = from_view
to_view[:, :, :] = from_view
```

copy和copy_fortran() (C and Fortran contiguous copies)(TODO)

## 转置Transposing

memoryview可以以和NumPy slices相同的方式转置

```python
import numpy as np

array = np.arange(20, dtype=np.intc).reshape((2, 10))

cdef int[:, ::1] c_config = array
cdef int[::1, :] f_config = c_config.T
```

声明中::1表示这个维度是连续的（主序）

转置语法要求memoryview是直接内存访问的，而不是间接

## Newaxis（TODO）

## Read-only view

cdef const double[:] myslice

这只是显示mv的只读性，而不是改变底层buffer访问权限
