# Tips and Tricks

## 使用 Terminal

当编写 Python scripts 时，有一个打开的 Terminal 很有用。它不是内置的 Python Console，而是用于打开 Blender 的 terminal application。

这个 terminal 有 3 个主要用途：

- 可以看见脚本中 print() 的输出，这对于查看调试信息非常有用
- error traceback 会打印在 terminal 中，而 Blender UI 的功能并不总能生成 report message
- 如果 script 运行时间太长，或者不小心进入死循环，可以通过 ctrl-c 结束执行的功能


## Interface Tricks

### Access Operator Commands

你可能会注意到 menu items 和 buttons 的 tooltip 包含 bpy.ops.[...] 命令来运行那个功能，这是一个很有用的特性，你可以在任何 menu item 或 button 按 ctrl-c 来复制这个命令到剪贴板。

### Access Data Path

要从一个 ID data-block 找到一个到它的 setting 的 path 不总是如此简单，因为它可能是一个嵌套数组。要快速得到 path，打开 setting 的 context menu，然后选择 Copy Data Path，如果不能生成，则只有 property name 被复制。



