# Cython Essentials

Cython是一个混合Python和C/C++的编程语言

cython是一个编译器，将Cython源代码翻译为高效的C/C++源代码。这个源代码可以被编译为一个Python扩展模块或者一个standalone可执行程序

Cythons的power来自它联合了Python和C：它看起来像Python同时提供了访问C的便捷方式。Cython位于high-level Python和low-level C之间

Cythons的优美之处在于它联合了Python的表达能力和动态性，以及C语言的bare-metal性能，同时仍然看起来像Python

除了一少部分例外，Python代码已经是合法的Cython代码了

Cython提供了少量的关键字到Python语言中以融入C的类型系统，允许cython编译器产生高效的c代码。如果你已经熟悉python以及对C/C++的基础理解，你可以很快的学习Cython。你不需要学习另一种接口语言

可以将Cython想象成两个project合成一个。如果编译python到c是Cython的yin，将C/C++暴露接口给python则是Cython的yang。我们可以从需要性能的python代码开始，也可以从那些需要更好的python接口的C/C++代码开始。要加速Python代码，Cython编译Python源代码以及可选的静态类型声明以得到大量的性能提升。

Cython主要提供了两个功能

- 编译Python到C代码
- 暴露C/C++代码的Python接口

要将Python的动态类型转换成Cython的静态类型，使用cdef（c def）语句声明静态类型的c语言变量

Cython可以达到C-level的性能，更多的，它比手写C扩展模块做得更好。Cython生成高度优化的code，通常比等价的手写C扩展模块更快

更进一步，还可以使用Cython创建Python-like的C函数，但是没有Python的overhead。这些函数不能直接在Python中调用，只用于Cython代码。这允许我们移除核心计算的昂贵的call overhead

Cython只对CPU密集的计算可以大量提升性能，对于内存密集、IO/网络密集的程序不能期望有太大提升。

根据80/20定律，80%的程序运行时花费在20%的代码上。因此优化之前应该先profile，找到程序瓶颈，在确认是否可以使用Cython优化。Cython是强大的工具，但必须以正确的方式使用

Cython的另一个应用，为C/C++代码提供Python wrapper接口

对于一个C接口(cfib.h)

```C
double cfib(int n);
```

Cython wrapper code不超过10行

```c
cdef extern from "cfib.h":
  double cfib(int n)

def fib(n):
  return cfib(n)
```

在cdef extern块中提供cfib.h头文件(from cfib.h)，在块body中（缩进）声明cfib的C函数签名。在cdef extern block之后，定义一个python wrapper函数，调用cfib，并返回它的结果

将前面的Cython code编译成一个名为wrap_fib扩展模块之后，就可以在Python中使用它了

```python
from wrap_fib import fib
help(90)
```

手写Python扩展模块需要大量C code，以及Python/C API的细节知识。Cython无论是从编码的简便性还是代码的性能都比手写扩展要好

Cython可以帮助我们wrap任意复杂的数据结构、类、函数、方法。Cython是全面成熟的语言，而不是领域特定的语言，因此可以用它整合C/C++代码之后可以做任何事情，使用所有的Python标准库、Python的Power和灵活性

前面的示例中C code和Cython code是分开的，但它们甚至可以写在一个文件里

Cython本质上是把Python使用Python/C API编译成使用PyObject的C语言代码，对那些使用cdef定义的construct就直接复制到C code里面，这就是Cython所做的magic，这也是为什么它能够任意地混合Python和C代码。C的代码保持原样，Python代码转换成PyObject的C code。
