尝试将 C# 作为主要语言。尽量将一种语言作为主要语言，熟悉它的方方面面，这样可以快速实现一个事情。

熟练使用一个编程语言，最重要的是熟悉它的生态系统，它的各种标准库和框架，语法不是很重要的东西。熟悉一个语言的生态系统本身就是很花费时间和精力的事情，因此要熟练使用两种语言（不仅仅是熟悉语法）是很困难的，而且同一件事情学会两种实现方法是没有意义的。

使用 C# 代替 python 有很多优点：

- C# 各种语法糖已经非常便捷，不比 python 逊色多少
- python 只适合短小程序的快速实现，一旦要实现复杂一点的任务，编辑器的代码提示、补全、类型检查都是必须的，快速实现快速运行在此场景没有任何优势，必须要使用静态强类型的语言，否则动态类型带来的问题远远大于它提供的优势
- 游戏相关的功能都使用 C# 实现，可以避免两种语言的切换，而且可以直接在 Unity 编辑器中提供程序启动入口（菜单、Inspector 按钮），不需要单独使用一个命令行窗口
- 统一使用一种语言实现，无论是游戏本身还是工具，可以快速实现，而且强化对 C# 本身的熟练程度
- 工具和游戏功能可以共享逻辑，否则就要用 C# 和 Python 两种语言实现相同的功能
- C# 的静态语言特性（静态类型检查、调试、代码提示等等）提供了更强大的功能，而且和 Visual Studio 配合，构成强大的 IDE 环境
- 将工具在 Unity Editor 中用 C# 实现，还可以联合使用其他 Unity 插件和强大功能（例如异步编程，LINQ 等等），形成强大的协同效应（C# 的功能 + Unity 的功能）。就像只有把不同的物质强行放在一个容器里不断混合搅拌，才能产生化学发应，产生新的物质）
