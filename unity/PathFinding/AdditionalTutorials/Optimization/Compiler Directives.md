# Compiler Directives

使用编译器指示符来优化 package。

A* Inspector 中有一个 Optimization tab。

![optimization](../../../Image/optimization.png)

这个 tab 搜索 project 中列出的编译器指示符。一个编译器指示符是一块代码，控制另一块代码是否应该被编译。

```C#
#define DEBUG

public void Start () {
#if DEBUG
    Debug.Log ("The DEBUG compiler directive is defined");
#else
    Debug.Log ("The DEBUG directive is not defined");
#endif
}
```

A* Pathfinding Project 有一些可以被定制的方面。它正常需要手动编辑 code，但是 compolier directives 解决了这个问题。

指示符应用各种优化或者开启 debugging 消息。

指示符是否被开启 被存储在 player settings 中的 Scripting Define Symbols，这意味着这个 settings 被被 Unity project 中所有的 scenes 共享。

如果你目标平台时 mobile，你可能想要尽可能减少 built player 的文件大小。如果这样，你可以使用 ASTAR_NO_ZIP 选项来移除 DotNetZip 库的依赖。在 Optimizations 面板开启这个选项后，你可以移除 Assets/AstarPathfindingProject/Plugins/DotNetZip dll 文件，这应该会减少几百 kb。但是在使用 cache startup 时，这会使 cache 花费更长时间。

