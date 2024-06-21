# Command Palette

Textual app 有一个内置的 command palette，为 users 提供了一个快速方法访问 app 内的特定功能。

## Launching the command palette

按下 Ctrl + \ 来调出 command palette screen。它包含一个 input widget。Textual 会随着 user input 给出建议的 commands。用上下箭头在列表中选择命令，按 Enter 来调用它。

Commands 通过一个 fuzzy search 来查找，这意味着 Textual 会显示和你按下的 keys相同的顺序匹配的 commands，但匹配不必在 command 的开头。

例如，如果你按下 "to" 会建议 "Toggle light/dark mode" 命令，但是还可以按下 dm（匹配 dark mode）来匹配这个 command。这允许 user 可以用最少的按键快速得到一个命令。

## Default commands

Textual app 默认开启一下 commands：

- "Toggle light/dark mode"，这会在 light/dark mode 之间切换，通过设置 app.dark True or False
- "Quit the application"，退出这个程序，等价于 ctrl+c
- "Play the bell"，播放 terminal bell，调用 app.bell

## Command providers

要使命令出现在 command palette，必须将自己的命令添加到 command palette。定义一个 command.Provider 类，然后将它添加到 App 的类变量 COMMANDS。

Command Provider 有 4 个方法可以覆盖：startup，search，discover，shutdown。这些方法都应该是 coroutines。只有 search 是必须的，其他方法是可选的。

### startup method

这个方法在 Command Palette 打开时调用。可以用这个方法执行一些 searching 之前的准备工作。

### search method

这个方法负责提供匹配 user input 的 result（hits）。它对于任何匹配 query argument 的 command yield Hit 对象。

Matching 如何实现取决于 Command Provider 的作者。但是建议使用内置的 fuzzy matcher 对象，可以调用 marcher 得到它。它有一个 match() 方法比较 user search term 和潜在的 command，并返回一个 score。score = 0 意味着没有 hit，大于 0 意味着 result 有一定程度匹配，1 意味着完全匹配，

Hit 包含关于 score 的信息（用于建议排序），hit 应该如何展示，以及一个可选的 string。它还包含一个 callback，当用户选择这个命令时将会运行它。

不像 Textual 的其他地方，command provider 的 errors 不会导致退出 app。这是故意设计的，防止一个有问题的 Provider 导致 command paletter 不可用。Command Provider 的 Errors 会被打印到 Console。

### discover method

discover 方法负责提供 results（或者 discovery hits），它在 user input 为空的时候显示给用户。这可以帮助 user 发现 command。

因为 discover hits 在 Command Palette 打开时即显示，它应该快速生成。需要花费一定时间生成的 commands 更适合留给 search。discover 是为了提示用户有这个功能相关的命令而已，然后当用户输入时为用户提供更多的命令提示。

discover 类似 search，但是有一些不同：

- discover 不接受参数，search 接受一个 value
- discover yield DiscoveryHit 的实例，search yield Hit 的实例
- discovery hits 以 asc 顺序排序，因为它没有 score

DiscoveryHit 包含关于 hit 应该如何显示的信息，一个可选的 string，以及一个用户选择 command 时执行的命令。

### shutdown method

shutdown 方法在 command palette 关闭时执行。它可以关闭一些 startup 创建的对象，例如文件。

## Screen commands

可以通过添加一个 COMMANDS 类变量到 Screen class 来为 screen 关联 commans。Screen 独占 terminal，通常代表一个独立的功能。可以使用它实现特定于一个特定 Screen 的 commands，而不是在 app 每个地方都可以应用的 commands。Command Palette 包含 App 提供的 Command 和当前 active screen 提供的 command。

## Disabling the command palette

Command Palette 默认是开启的。如果不想使用 command palette，可以在 App class 设置 ENABLE_COMMAND_PALETTE = False.

