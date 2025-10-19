# Cython In Depth

## 使用cdef声明静态类型

Cython中，untyped dynamic variables就像Python变量一样

cdef int i, j = 0
cdef float k

使用静态类型变量就像Python或C code一样

cdef block

cdef:
    int i
    float dx = 1.0

可以声明任何C支持的类型的变量

- 指针

  cdef int *p
  
  cdef void **buf

- 在栈上分配的C数组

  cdef int arr\[10]

  cdef double points\[20]\[30]

- 类型别名

  cdef size_t len

- 复合类型

  cdef tm time_struct

  cdef int_short_union_t hi_lo_bytes

- 函数指针

  cdef void (*f)(int, double)

Cython支持所有C的类型声明，例如cdef int *signal(int (*f)(int))(int)。这对于包装外部C库非常重要

### Cython自动类型推断（TODO）

cdef不是Cython中唯一声明静态类型的方法。Cython还对函数和方法中的untyped variables执行自动类型推断。默认Cython只在不会改变code语义的情形下推断类型

@cytyon.infer_types(True)

### Cython中的C指针

Cython中的指针解引用和C不同。因为Python已经使用*args和**kwargs。因此在Cython通过索引指针位置上第0个元素解引用指针

cython.operator.dereference函数可以解引用C指针。通过cimport导入。这种方式不常使用

```python
from cython cimport operator
cdef double *p_double
print(operator.dereference(p_double))
```

对于结构体指针引用成员，Cython使用.而不是->。在Cython中，任何使用->的地方都变成.

### 混合静态类型和动态类型变量

Cython允许在对应的静态类型和动态类型变量之间赋值。这种在静态类型和动态类型之间的流畅混合是非常强大的属性

这允许我们使用动态的python objects作为code base的主体，然后在性能关键的区域可以很容易地将它们转换成快速、静态的对应体

```python
cdef int a, b, c
tuple_of_ints = (a, b, c)
```

这段代码平淡无奇甚至很无聊，强调的点是a, b, c 都是静态类型整数，而Cython可以用它们直接创建动态类型的Python tuple字面量。这种简洁性就是Cython的power和beauty：我们使用C int就可以创建Python tuple，直观明了。而使用Python/C API则非常繁琐，需要大量代码

下面是C types和Python types的对应关系，它们之间可以自动转换

| Python types | C types |
| --- | --- |
| bool | bint |
| int/long | \[unsigened] char/short/int/long/long long |
| float | float/double/long double |
| complex | float/double complex |
| bytes/str/unicode | char */std::string |
| dict | struct |

### 静态声明一个Python类型变量

cdef 不仅可以声明C语言的静态类型变量，还可以声明Python的静态类型。这样后面就不必动态地决定变量的类型了。Python内置类型诸如list，tuple，dict，扩展类型诸如NumPy数组等等都可以静态声明类型

不是所有Python类型都可以静态声明，它们必须以C实现，而且Cython必须能够访问它们。内置类型已经满足这些条件

cdef list particles, modified_particles

cdef dict names_from_particles

cdef str pname

cdef set unique_particles

Cython在幕后将它们声明为指向内置Python struct的指针。它们可以像正常的Python变量一样使用，但是只用用于它们声明的类型，相当于Cython对Python执行了像C语言一样的类型检查

动态类型可以通过静态类型声明初始化

但是Python的一些类型名字和C语言的类型名相同，例如int，float等，在静态声明类型的时候优先使用C类型

对有符号操作数的求余在Python和C具有不同的行为。C rounds toward zero，Python rounds toward infinity。例如-1 % 5在Python中求值为4，而在C中求值为-1。此外对于整数除法，Python总是检查除零错误并抛出ZeroDivisionError，而C语言则不检查

遵循最少惊讶原则，Cython对division和modulus默认使用Python语义，即使它们声明为C类型。要得到C语言的语义，可以使用cdivision编译器指示符：

- 在全局模块level或者在指示注释中

```python
# cython: cdivision=True
```

- funciton level的decorator

```python
cimport cython

@cython.cdivision(True)
def divides(int a, int b):
    return a / b
```

- context block

```python
cimport cython

def remainder(int a, int b):
    with cython.cdivision(True)
        return a % b
```

### Static Typing for Speed

越多声明静态类型，Cython越能更好地优化结果

Cython当前支持的可以静态声明的Python类型

- 具有和C语言对应的类型（int long float）
- type, object
- bool
- complex
- basestring, str, unicode, bytes, bytearray
- list, tuple, dict, set, frozenset
- array
- slice
- date, time, datetime, timedelta, tzinfo
- 以后可能支持更多类型

### 引用计数和静态字符串类型

Cython不再C变量和Python变量之间维持引用计数，如果C指针指向一个Python对象的数据，必须保证Python对象的有效

## Cython的3种类型函数

Python函数可以在import时创建，或者运行时动态创建，也可以在其他函数或其他嵌套作用域（class）中创建

Cython支持Python函数和C函数相互自然直接地调用，全部在同一个source文件

可以使用IPython %timeit magic测量函数执行的时间

当cdef关键字用于创建一个函数时，它创建一个C调用语义的函数。cdef 函数的参数和返回值是静态声明类型的

将cdef 函数想象成在Cython中以Python语法定义的C函数。参数和返回值类型都不使用Python objects。调用cdef 函数就像纯C函数一样快。可以在cdef函数中声明和使用Python objects和动态变量，或者接受它们为参数。但是cdef函数通常用于我们像尽可能接近C code

Cython允许cdef函数和Python的def函数在同一个Cython source file中定义。cdef函数可选的返回类型可以是任何静态类型，包括pointers，structs，C arrays，静态Python类型例如list或dict。还可以是void。如果返回类型被忽略，默认是object

```python
cdef long c_f(long n):
    return n * n
```

cdef函数可以在同一个source file的任何def/cdef函数中调用。但是Cython不允许cdef函数在外部的Python code中调用。因为这个限制，cdef函数通常用作帮助def完成工作的快速辅助函数。如果想在外部的Python code调用cdef函数，则需要一个最小的def函数调用这个cdef作为它的Python wrapper

```python
def wrap_c_f(n):
    return c_f(n)
```

Python基础类型和C基础类型并不是完美匹配，尤其是类型range，必须注意C语言的类型限制

还有第3种类型的函数，使用cpdef关键字声明，这是一个def和cdef的混合体。cpdef函数联合了两种类型函数的features并且解决了很多限制。使用cpdef定义的函数自动生成cdef函数和对应的def wrapper函数，它们具有相同的名字。当在Cython中调用它时，执行C函数，当在外部Python中调用它时，执行wrapper函数。这样它在一个地方提供了C的运行速度和Python的可访问性

```python
cpdef long cp_f(long n):
    return n * n
```

inline传递给C++编译器处理

```python
cdef inline long c_f(long n):
    return n * n
```

因为cpdef函数同时完成了cdef函数和def函数的功能，因此它的参数和返回值必须同时和Python、C兼容。任何Python object都可以在C level被表示（PyObject Python/C API），但是不是所有的C类型都可以表示成Python类型。因此不要任意使用void、指针、C数组作为函数的参数和返回值

### 函数和异常处理

def函数总是返回C level上的某种PyObject。这种不变性允许Cython正确地传播def函数中的异常。而cdef、cpdef可能返回一个non-Python类型，这使得其他异常指示机制成为必须

Python在发生异常的地方生成一个异常对象，作为返回值传递给它的caller，caller检查如果返回值为异常，就如此一样继续向上传播。但是cdef、cpdef函数可能不返回Python对象，使得Python可以检查到异常并生成异常对象，但是不能想caller传播异常

Cython提供except clause，允许cdef或cpdef函数和它的caller通信，告诉它发生了一个Python异常

```python
cpdef int divide_ints(int i, int j) except? -1:
    return i / j
```

except? -1 clause允许返回值-1作为可能的哨兵指示异常可能发生。一旦divide_ints返回-1，Cython检查全局异常状态是否被设置，如果是，开始unwinding stack。我们不需要在异常发生时自己设置异常状态，Cython自动完成它。值-1是任意的，我们也可以使用一个不同的整数，它属于函数返回值类型的范围

返回except后面的问号表示只有在返回-1的时候检查全局异常状态。因为-1也可能是函数的正常返回值，而此时全局异常状态没有设置。当返回-1时，无论有没有异常，Cython都会检查，有则传播异常，否则什么也不发生。如果-1不是正常的返回值，则可以使用它总是指示发生了异常，此时可以忽略问号。或者可以使用except * clause，它总是检查异常，而不管返回值是什么，这需要额外的消耗

### 函数和嵌入签名编译器指示符

embedsignature编译器指示符指示Cython注入编译的Python签名到docstring中，使得可以在IPython中查看函数的信息（参数名、顺序、默认值等等）

## 类型强制转换

Python和C都有良好定义的强制类型转换。C的强制转换规则也应用在Cython中

Cython中的显式类型转换和C一样，但是使用\<>而不是\()包围类型

cdef int \*ptr_i = \<int *>v

可以和Python扩展类型，或者built-in或者我们自己定义的，一起使用casting

```python
def cast_to_list(a):
  cdef list cast_list = <list>a
  print(type(a))
  print(type(cast_list))
  cast_list.append(1)
```

这种转换只可用在我们确认a是list兼容类型的情形下，否则可以使用带检查的casting

```python
cdef list cast_list = <list?>a
```

如果a不是list或其子类，则抛出一个TypeError

Casting也可以工作于基类和派生类

## 声明和使用struct，union，enum

Cython还可以声明、创建、操作C语言的structs、unions、enums

```C
struct mycpx {
  int a;
  float b
};

union uu {
  int a;
  short b, c;
};
```

等价的Cython声明是

```python

cdef struct mycpx:
  float real
  float imag

cdef union uu:
  int a
  short b, c

```

Python使用缩紧block定义C-level的概念

可以使用ctypedef声明struct和union，它创建struct/union的同时还为它们创建了一个类型名

```python

ctypedef struct mycpx:
  float real
  float imag

ctypedef union uu:
  int a
  short b, c

cdef mycpx zz
```

有3中方式可以初始化struct：

- 使用struct字面量

```python

cdef mycpx a = mycpx(3.1415, -1.0)
cdef mycpx b = mycpx(real=2.718, imag=1.618034)

```

- 独立为struct自动赋值

```python

cdef mycpx zz
zz.real = 3.1415
zz.imag = -1.0

```

- 从一个Python dict进行赋值

```python

cdef mycpz zz = {'real': 3.1415, 'imag': 1.0}

```

不支持嵌套和匿名内部 struct/union 声明

初始化嵌套结构的struct时，可以逐字段赋值，或者赋予一个和struct结构匹配的嵌套dict

要声明enum，在每一行声明一个成员，或者在一行声明所有成员并使用逗号隔开

```python

cdef enum PRIMARIES:
  RED = 1
  YELLOW = 3
  BLUE = 5

cdef enum SECONDARIES:
  ORIANGE, GREEN, PURPLE

```

与struct/union一样，可以使用cdef或ctypedef声明enum

匿名enum可以用来声明全局整数常量

```python

cdef enum:
  GLOBAL_SEED = 37

```

Structs, unions, enums经常用于暴露外部C code在Python的接口

## Type Aliasing with ctypedcdf

Cython使用ctypedef支持C语言的变量别名，就像C语言的typedef一样

```python

ctypedef double real # 这允许只需要修改一行就可以改变浮点数的精度
ctypedef long integral

def f(real r, integral i):
  pass

```

ctypedef语句只能出现在file scope，不能在function或其他local scope中声明一个local type

### Fused Types（Templates模板）

Cython有一个新奇的typing feature——fused types，允许我们在一个类型定义里面引用几种相关的类型，进而编写一个static-typed cython算法但可以用于多种类型。Fused types允许在Cython中进行范型编程

Fused types当前不支持作为extension types的属性（范型类）。只有变量和function/method参数可以声明为fused types（范型函数和范型方法）

```python

ctypedef fused char_or_float: # 类型声明
  char
  float

cpdef char_or_float plus_one(char_or_float var):
  return var + 1

def show_me():
  cdef:
    char a = 127
    float b = 127
  print('char', plus_one(a))
  print('float ', plus_one(b))

```

#### 声明Fused Types

```python

cimport cython
ctypedef fused my_fused_type:
  cython.int
  cython.double

```

或者

```python

my_fused_type = cython.fused_type(cython.int, cython.float)

```

类型名可以是任何类型，包括typedef/ctypedef定义的类型别名

#### 使用Fused Types

Fused types可以被用于声明函数或方法的参数/返回值类型

如果在参数列表中（或返回值）多次使用同一个Fused Types，则它们必须是相同类型

只声明范型数值类型

Cython提供了3个built-in fused types，可以直接使用：integral，floating，numeric。所有都通过cython命名空间访问，它必须通过cimported导入

只具化数值类型可能并不是很有用，Fused types可以用于数组、指针、typed view of memory类型

Cross Product of All combinations（TODO）：同一个类型被使用多次，它们必须具化成相同的类型，如果希望具化成不同的类型，使用相同的fused类型声明创建一个新的类型

可以使用两种方法选择具化类型

- Indexing

  ```python
  cfunc[cython.p_double](p1, p2)
  func[float, double](myfloat, mydouble) # From Cython space
  func[cython.float, cython.double](myfloat mydouble) # From Python space
  ```

- Calling

  直接调用，自动推断具化类型。对于cdef/cpdef，这意味着具化类型在编译时推断。对于def函数，参数在运行时检查，如果不能推断类型，则抛出TypeError。cddef如果不能知道funciton的类型，则当作def处理

有一些内置的Fused types可以直接使用

cython.integral fused type groups together C short，int，和long scalar types
cython.floating fused type groups together float和double C types
cython.numeric（最通用的类型）groups 所有integral和floating类型，以及float complex和double complex

Fused cdef和cpdef函数可以转换或赋值给C函数指针

```python

cdef myfunc(cython.floating, cython.integral):
  ...

cdef object (*funcp)(float, int)

funcp = myfunc
funcp(f, i)

(<object (*)(float, int)> myfunc)(f, i)

funcp = myfunc[float, int]
funcp(f, i)

```

带类型检查的具化，可以对具化类型进行判断，以执行不同的代码。可以使用is, is not, ==, !=检查一个fused type是否是某个其他的(non-fused)类型，或者使用in，not in检查具化类型是否属于某个类型集合(通过一个fused type指定)

```python

ctypedef fused bunch_of_types:
  ...

ctypedef fused string_t:
  cython.p_char
  bytes
  unicode

if cython.integral is int:
   ...

if bunch_of_types in string_t:

```

## Cython的for循环和while循环

```python

cdef unsigned int i, n = 100

for i in range(n):
  ...

```

将生成C code

```C

int i, n = 0;
for (i = 0; i < n; i++) {
  /*...*/
}

```

Guidelines for efficient loops

- 如果是range循环，将range参数和迭代参数声明为C int
- 对于容器迭代（list，tuple，dict等），声明索引为静态类型反而增加overhead。要有效地迭代容器，使用memoryviews
- 对于while循环，保证loop condition表达式高效（包括使用静态类型变量和cdef函数）

## Cython预处理器

DEF -> #define

定义编译时常量，使得它的值在多个地方使用，但是只在一个地方更新

DEF常量必须在编译时确定，并在只限制使用简单类型

预定义常量、函数、类型（TODO）

支持条件编译 #IF-#ELIF-#ELSE 判断条件不仅限于DEF常量，它们根据python语义解析为bool
