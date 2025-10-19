# Subprocess management

subprocess模块允许你生成新的进程，连接它们的input/output/error管道，获得它们的返回码

## 使用subprocess模块

建议为任何可能case使用run方法，对于更高级的用法，可以使用popen接口

call、check_call、check_out都是过时函数，Python3.6之后都应该用run/Popen运行子进程

run基于Popen实现，只有Popen才是最底层的函数

- run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, env=None)

    允许args描述的命令，等待完成，返回一个CompletedProcess实例

    上面列出的只是常用的参数，全部可用的参数与Popen一样多

    默认不捕获stdout和stderr，因此子进程的输出直接到控制台。传递PIPE给stdout和stderr参数，在返回的CompletedProcess的stdout/stderr中就可以捕获子进程的输出

    input参数传递输入给子进程的stdin。它可以是byte sequence，或者string（如果指定encoding或errors；或者universal_newline=true）。如果指定input，内部Popen对象自动以stdin=PIPE创建

    如果check=true，并且子进程以non-zero exit code退出，CalledProcessError异常将被发出。异常属性包括参数，退出码，stdout/stderr（如果设置为PIPE）

    如果encoding或errors被指定，或者universal_newlines=true，为stdin、stdout和stderr打开的file objects将是text模式，并使用指定的encoding和errors，或者默认使用io.TextIOWrapper，否则将以二进制形式打开

    如果env不为None，它必须是一个为新进程定义环境变量的map

- CompletedProcess

    run的返回结果，代表一个运行完成的进程

  - args

    用于启动进程的参数，list or string

  - returncode

    子进程退出码，0表示正常退出，+N表示进程失败原因，-N表示进程被信号N中断

  - stdout/stderr

    捕获的子进程输出。bytes sequence或者string（run指定encoding或errors）。如果不捕获（stdout=None），其为None

    指定stderr=subprocess.STDOUT，可以将stderr重定向到stdout

  - check_returncode()

    如果returncode不为0，调用这个函数发出CalledProcessError异常

- DEVNULL

    对应/dev/null设备，可以用于stdin，stdout，stderr

- PIPE

    用于stdin，stdout，stderr，指示连接管道到stdin，stdout，stderr，在Popen中可以使用Popen.communicate()与子进程通信。input将输入给子进程，stdout/stderr将捕获子进程输出

- STDOUT

    用于stderr，可以将stderr重定向到stdout

- SubprocessError

    subprocess模块所有异常的基类

- TimeoutExpired

  - cmd（args，list or string）
  - timeout（timeout seconds）
  - output
  - stdout（=output）
  - stderr

- CalledProcessError

  - returncode（退出码）
  - cmd
  - output
  - stdout
  - stderr

- 常用参数

    为支持广泛的use case，Popen（run）接收大量的可选参数。对于绝大多数典型应用，许多参数都可以安全的忽略（使用默认值）

  - args

    启动子进程的参数，string或者list。使用list通常是更理想的方式，因为它允许模块处理参数的转义和引用（例如允许文件名中包含空格）。如果传递string，或者shell=True，或者string本身就是子进程的名字，不带任何参数执行

  - stdin，stdout，stderr
  
    指定子进程的标准输入，标准输出，标准错误文件handles。有效值包括PIPE，DEVNULL，一个存在的文件描述符（正整数），一个存在的file object，以及None。

  - 如果指定encoding或errors，或者universal_newlines为true时，stdin，stdout，stderr将以text模式以encoding、errors打开，或者默认为io.TextIOWrapper

  - 对于stdin，line ending characters '\n'将被转换为os.linesep。对于stdout和stderr，所有的line ending被转换为'\n'

  - 如果不使用text模式，stdin，stdout，stderr都以二进制形式打开，没有执行encoding或line ending转换

  - 如果shell=True，指定的命令将通过shell执行。这对于将Python主要用于增强它系统shell的控制流，并仍然想要方便的访问其他shell特性（如shell管道，文件名匹配，环境变量扩展，以及～到用户home目录扩展）时非常有用。但是Python提供了许多shell-like的特性（glob，fnmatch，os.walk，os.path.expandvars，os.path.expanduser，和shutil）

