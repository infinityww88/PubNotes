# Editor Memory Issue

Unity Editor 运行时占用 2-3G 左右的内存，Visual Studio 运行时占用 1G，WSL 的 vmmem.exe 占用接近 1G 内存。8G 内存的机器内存占用几乎 96%，这是导致 Editor 每次修改需要执行非常长时间的 script compiling、reloading domain、import assets 的主要原因。与此同时，CPU 占用倒不是非常高。因此要尽可能流畅运行 Editor，最优先解决的是内存问题，而不是 CPU 的问题。

在内存受限的情况下，有几种方法可以很大程度缓解问题：

- 不使用 Visual Studio，使用 Unity ScriptInspector3 插件作为 IDE

  ScriptInspector3 支持语法高亮、代码提示、跳转、引用查找，基本功能够用，而且它还有一个优势，就是改完代码后不会立即编译，可以让你继续查看 Project 其他信息，两次保存才触发代码编译。

- 关闭 WSL，退出 Vmmem.exe，在 cmd 窗口中执行 wsl --shutdown。注意打开任何 wsl 终端都会启动 wsl，不论是 Cmder 还是 Visual Studio Code。

- 关闭其他非必需的应用，包括 Visual Studio Code、Google Chrome。临时 note 可以先保存到 Sticky Notes 中。

- 使用 Windows 版本的程序，gvim.exe 编辑文件，git.exe(git bash) 版本控制。gvim.exe 和 git.exe 各自只占用 30M 作用的内存。git bash 还可以用来模拟 bash shell 环境，包含大多数标准 unix 命令。

  Windows10 安装 git 客户端之后，安装文件夹下有 git-bash.exe 和 git-cmd.exe 两个执行文件。

  Git CMD 就像带有 git 命令的常规 Windows 命令提示符。它允许通过命令行使用所有 Git 功能。如果熟悉 Windows cmd 并且只在 Windows 上工作，则很有用。

  Git Bash 在 Windows 上模拟 bash 环境。它允许在命令行中使用所有 git 功能以及大多数标准 unix 命令。如果习惯了 Linux 并希望保持相同的习惯，则很有用。

  其他类似软件还有 MSYS2，MinGW64，Cygwin 等。MSYS2 包含一个命令行终端 mintty，bash，版本控制系统 git 等等，它主要目的是提供最小版本的 Cygwin。

  MSYS2 中安装软件使用命令 pacman -S ... 例如 pacman -S openssl。

