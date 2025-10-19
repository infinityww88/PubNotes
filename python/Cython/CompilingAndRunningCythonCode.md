# Compiling and Running Cython Code

Python和C/C++最大的区别就是Python是解释运行，而C/C++是编译运行的。编译大量C/C++代码base可能需要花费数小时甚至数天。Python则允许快速原型开发，引起显著开发效率的提升

Cython也需要一个编译步骤，可以是显式的或者隐式的。两种模式都有它们的用处。自动编译Cython的一个好处是它工作起来像是纯python。无论显式还是隐式，因为Cython只被选择用于Python code中的一小块code，Cython的编译需求可以被最小化

本章介绍各种编译Cython code的方式，使得它可以被Python运行

- Cython code可以被编译，然后再IPython解释器中交互式运行
- 它可以再import时自动编译
- 它可以被类似Python distutils之类的build tools单独编译（TODO）
- 它可以整合进标准build system，诸如make，cmake等（TODO）

不需要知道所有的编译Cython code 方法才能使用Cython，因此只选择需要方式阅读即可

再每种情形下，每个方法将Cython code传递到2个编译阶段，以生成一个Python可以使用的编译模块

Cython Compilation Pipeline

Pipeline的工作是将Cython code转换成Python可以使用的扩展模块。Pipeline可以自动运行（使得Cython用起来像Python），或者显式被终端用户调用以施加更多控制

Pipeline包含两个阶段。第一个阶段被cython编译器处理，将Cython code转换成优化的平台独立的C/C++ code。第二个阶段使用C/C++编译器将生成的C/C++ code编译成共享库。生成的共享库是平台相关的。再Linux/Max OS X上是一个.so扩展库对象，再Windows中是一个.pyd动态链接库扩展。传递给C/C++编译器的flags保证共享库是完成标准的Python模块。我们称这些编译后的模块为扩展模块，它们可以被当作纯Python模块被import和使用

cython编译器是一个source-to-source编译器(cython->c/c++)

按照C/C++编译器和cython

python -m pip cython
pip install cython

## 标准方式：Using distutils with cythonize

Python标准库包含distutils package用于building，packaging，distributing Python projects

distutils包有很多功能，我们感兴趣的是它编译c程序到扩展模块的功能，pipeline的第二个阶段。它为我们管理所有平台，架构，和Python-version细节，因此我们可以使用一个distutils脚本，在任何地方运行它来生成我们自己的扩展模块

cythonize命令处理pipeline第一个阶段，其包含在Cython中。它使用一个Cython source file（以及任何必须的选项），并且将它编译到C/C++ source file，之后distutils得到source

通过联合使用Python distutils模块和Cython的cythonize命令，我们可以显式控制编译管线。这种方式需要我们编写一个小的python脚本并且显式运行它。这是将Python projects编译并分发Cython code到终端用户的最常用的方式

通过一个Python脚本控制distutils的行为，来创建一个扩展模块(.so/.pyd)，通常命名为setup.py

最小的setup.py脚本：

```python
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('fib.pyx'))
```

脚本的核心是setup(cythonize(...))。cythonize是将调用cython编译器将Cython source编译成C source最简单的方式。可以传递给它一个文件，一组文件，或者一个glob pattern匹配的任何Cython文件

cythonize命令返回一个distutils Extension objects的列表，setup函数知道如何将它转换成扩展模块。它被设计用来使distutils更容易和Cython projects联合使用

这两个函数的连续调用展示了pipeline的两个stages：cythonize调用cython编译器将.pyx source编译成C source，setup将C source编译成python扩展模块

在控制台执行setup.py：python setup.py build_ext --inplace

build_ext参数指示distutils去构建cythonize调用创建的Extension objects。可选的--inplace flag指示distutils将每个扩展模块与它们对应的Cython .pyx source放在一起

要查看build_ext所有子命令，执行python setup.py build_ext --help。其他选项包括控制预处理器，include目录，link目录，link库

一旦编译了扩展模块，就可以启动Python或IPython解释器来import和使用它们，就像正常的python模块一样

import fib

可以使用IPython的内省功能显式扩展模块的细节

In [2]: fib?
Type: module
String Form:\<module 'fib' from 'fib.so'>
File: /Users/ksmith/fib.so Docstring: \<no docstring>

函数显式为builtin_function_or_method表示函数是通过编译代码而不是直接python source实现的

当使用Cython wrap C/C++ source时，我们必须在编译阶段包含其他source files

setup_wrap.py

```python
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="wrap_lib", sources=["cfib.c", "wrap_fib.pyx"])
setup(ext_modules=cythonize(ext))
```

如果我们提供了一个预编译的动态链接库libfib.so，而不是source code，我们可以指示distutils在链接时连接libfib.so

```python
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name = "wrap_fib", sources=["wrap_fib.pyx"], library_dirs=["/path/to/libfib.so"], libraries=["fib"])
setup(ext_modules=cythonize(ext))
```

## 交互式Cython和IPython %%cython魔法

使用IPython和Cython可以方便地在解释器中交互式地试验Cython

这些额外的命令是被成为magic commands的IPython-specific命令，它们使用%或者%%开头。它们提供普通Python解释器支持之外的功能。IPython具有一些magic commands允许动态编译Cython code

在使用这些magic Cython命令之前，我们首先需要告诉IPython加载它们。在IPythn中使用%load_ext meta-magic命令：

%load_ext Cython
%%cython
  def f(int n):
    cdef r = n * 2
    return r

%%cython magic命令允许我们在IPython中直接编写一块Cython代码。当使用两个return退出block时，IPython将使用我们编写的Cython code，将它粘贴到一个临时Cython source file中，然后将它编译成一个扩展模块。如果编译成功，IPython将会从模块import任何东西使得f函数在IPython中可用，整个过程是自动化的。之后就可以在IPython中调用f函数了。在输入完code block之后IPython会出现短暂的暂停，这是因为它在背后编译加载code

可以给%%cython传递可选参数

第一阶段参数

- \-n \--name：指示生成的.pyx文件名
- \--cplus：生成C++代码
- \-f \--force：强制cython重新生成C/C++代码

第二阶段参数

- \-I \--include：添加额外目录来搜索文件包含和cimports
- \-c \--compile-args：指定额外的C compiler参数
- \--link-args：指定额外的链接参数
- \-L：指定额外的库搜索目录
- \-l：指定额外的链接库

在IPython中使用%%cython交互式使用Cython，必须使用def和cpdef来定义函数，函数才能在%%cython结束后可用，因为每次%%cython创建一个临时Cython source并编译，而cdef只能在Cython内部可用，外部无法访问。而def和cpdef则可以在外部访问

## pyximport on-the-fly 编译

Cython是以Python为中心的，它天然地倾向像正常的，动态的，可导入的Python模块一样使用Cython source files

pyximport改进了import语句以识别.pyx扩展模块，将它们自动送入pipeline，然后import编译后的扩展模块

只需要两行代码：

```python
import pyximport
pyximport.install() # 在import任何Cython扩展模块之前调用install
```

也可以在IPython中使用pyximport

可以将.pyx文件视为常规的Python模块。如果.pyx文件修改了，在下次它被import的时候自动重新编译

如果Cython source file依赖其他的C/C++ source/header文件，或者其他的Cython source文件，pyximport需要在这些依赖发生变化时重新编译.pyx，而不仅是.pyx本身变化。

创建一个和.pyx同名的.pyxdeps文件在同一目录。它应该包含.pyx依赖的文件列表，每个一行。这些文件可以在.pyxdeps目录的其他相对位置。每一项可以使用glob patterns来匹配多个文件

.pyxbld文件告诉pyximport将多个source files编译链接成一个扩展模块。它也是和.pyx具有相同的名字和位置

.pyxbld内部可以又一个或两个python函数，每个都是可选的：

- make_ext(modname, pyxfilename)

  如果定义，make_ext在编译前执行。第一个参数是模块名，第二个参数是要编译的.pyx。make_ext返回一个distutils.extension.Extension实例，或者它可以返回Cython.Build.cythonize的结果。这允许定制被使用的Extension。通过在创建Extension实例时，添加文件到sources参数，它可以在创建扩展模块时引导pyximpor将外部source files和.pyx file一起编译和链接

- make_setup_args()

  如果定义，pyximport调用这个函数得到传递给distutils.core.setup的额外参数map。这允许控制传递到setup的参数，提供了对distutils的完全控制

## 手动编译

最底层全面的方式

第一阶段：

cython fib.pyx

产生fib.c。cython可以接受一些编译器flags。直接输入cython查看它可以接受的参数。最常用的参数是

- \--cplus产生C++ source
- \-2 or \-3控制Python语言版本

第二阶段：

将fib.c编译为fib.o，然后将fib.o链接到一个动态链接库fib.so。Python提供了python-config命令来给出正确的编译和链接选项

- python-config \--cflags：产生正确的gcc编译选项
- python-config \--ldflags：产生正确的gcc链接选项

在mac平台，需要指定-shared来创建共享库。python-config给出编译Python时的编译和链接选项

## 与其他Build Systems一起使用Cython（TODO）
