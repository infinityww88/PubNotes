# Organizing Cython Code

Python提供了modules和packages来组织project。这允许我们将functions，classes，和variables组织成逻辑单元，使一个project更容易理解和navigate。Modules和packages还使得code更容易重用。在Python中使用import访问其他模块和包中的functions、objects、classes

Cython也允许我们将project break up成多个模块。它全面支持import语句，与python具有相同的意义。这允许我们在运行时访问定义在外部纯python模块或者扩展模块的Python objects

但是这无法使两个Cython模块相互访问另一方的cdef或cpdef函数，ctypedefs，structs，还有它不允许在C-level访问其他扩展类型

Cython提供来3个文件类型帮助组织Cython和C-level的project部分

- .pyx是Cython的implementation files
- .pxd是Cython的definition files
- .pxi是Cython的include files

Cython还提供了cimport语句来支持编译时访问C-level constructs，它在.pxd文件中查找这些constructs

Cython尽管看起来像Python语法，但是它本质和C一样是编译时语言，它要编译成动态链接库的

使用.pyx .pdx .pxi和cimport，就可以组织大型的Cython项目了

## Cython Implementation(.pyx) and Declaration(.pxd) Files

可以将纯Python文件.py也视为Cython的implementation files

如果只有一个很小的Cython项目，不需要访问C-level概念construct的code，则一个小的实现文件就足够了。但是一旦我们需要share它的C-level construct（cdef函数、cdef变量、structs、ctypedefs），我们就需要创建一个定义文件。Cython本质上是编译语言，就像C语言一样。定义文件就是C语言头文件.h的Cython对应体。它只定义类型和声明，没有实现。

```python

ctypedef double real_t

cdef struct State:
    unsigned int n_particles
    real_t *x
    real_t *vx

cpdef run(State st)

cpdef int step(State st, real_t timestep)

```

定义文件就是C语言的头文件，它只在编译时被访问，只存放C-level的声明，不允许Python-only的声明（例如def函数），否则产生一个编译错误

具有定义文件的实现文件也需要修改。具有相同名字的定义文件和实现文件被认为是Cython的一个命名空间。我们不能在实现文件中重复定义文件中的声明

.pyx -> .c
.pxd -> .h

在编译.pyx时，cython编译器自动检测对应的.pxd并使用它的声明

定义文件中应存放所有意图被其他Cython模块访问的C-level声明：

- C类型声明——ctypedef，struct，union，enum
- 外部C/C++库声明（cdef extern）
- cdef和cpdef声明的模块级函数
- cdef class扩展类型声明（TODO）
- 扩展类型的cdef属性和方法（C++的头文件.hpp)（TODO）
- C-level的inline函数和方法

定义文件不可以包含：

- Python或non-inline-C函数或方法
- Python类定义
- IF或DEF宏之外的可执行Python代码

实现文件被其他Cython通过cimport导入。cimport就是C语言的include

## cimport statement

```python
from simulator cimport State, step, real_t
from simulator import setup as sim_setup
```

cimport是编译时语句，import是运行时语句。cimport查找simulator.pxd文件，并导入其声明的C-level的概念constructs，import是常规的python语句，在运行执行，查找simulator.pyx文件，并导入其中声明的python概念constructs

但是cimport和import具有相同的语法

- cimport simulator作为一个命名空间
- cimport simulator as sim
- from simulator cimport State as sim_state, step as sim_step

使用cimport导入一个Python-level object或者使用import导入一个C-level的声明都产生一个编译错误。import只产生Python level的访问，cimport产生C-level的访问

定义文件可以包含cdef extern blocks。这可以用来将这些声明组织到它们自己的.pxd文件并在其他地方使用。这提供了一个有用的命名空间来帮助解决函数声明的歧义

Cython提供了一些预定义的定义文件用来访问常用的C/C++和Python的header files。它们组织成定义文件packages，并位于Cython source主目录的Includes目录。有一个为C标准库libc提供的package，包含了stdlib, stdio, math, string, stdint等头文件的.pxd文件。还有一个libcpp声明package的.pxd文件，包含常用的C++标准模板库STL的容器包括string，vector，list，map，pair，和set。还提供了cpython声明package的.pxd文件，可以方便访问Python/C API。还有NumPy/C API（TODO）

```python

from libc cimport math
math.sin(3.14)

from libc.math cimport sin
sin(3.14)

from libc.stdlib cimport rand, srand, qsort, malloc, free
cdef int *a = <int *>malloc(10 * sizeof(int))

from libc.string cimport memcpy as c_memcpy

from libcpp.vector cimport vector   # Cython支持从C++ STL中cimport C++ classes
cdef vector[int] *vi = new vector[int](10)

```

如果使用cimport和import使用相同名字导入不同的函数，将产生一个编译错误。简单的办法是为cimport和import导入的函数起不同的别名

cimport就是C/C++的include，但是更高级，自动处理重复import，并且提供了命名空间和别名的功能

## Include Files and the include Statement

.pxi则是C/C++的Include的完全对应体。它只是简单的source-level的替换

## Organizing and Compiling Cython Modules Inside Python Packages（TODO）
