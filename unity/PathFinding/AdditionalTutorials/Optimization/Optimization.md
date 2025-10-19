# Optimization

一些关于如何提升性能的提示。

有很多不同的方法可以提升系统的性能。

- Profile！在试图优化任何事情之前，使用一个 profiler 来支持 code 中的那个部分拖累游戏。注意如果多线程被使用，则 pathfinding 将不会显示在 Unity profiler 中，因为它并没有运行在 主线程中
- 目前为止，最简单的方式是开启多线程（A* Inspector > Settings）。这将会使 pathfinding 运行在一个单独的线程中，而不是 Unity 线程，这将会很大程度提升性能，因为现在几乎所有计算机甚至智能手机都有多个核芯
- 确保 “Show Graphs”（A* Inspector 的底部）被关闭。对于很大的 graphs，每一帧绘制的消耗会非常严重地使游戏缓慢（这只应用于 editor，而不是 standalone 游戏）
- 打印 path 结果对性能有相当程度的影响。通常会降低 50% 的 pathfinding 吞吐量。你应该关闭 path logging，如果你不需要它。设置 A* Inspector > Settings > Path Log Mode 为 None
- 另一件要考虑的事情是你要使用什么 graph。Grid graphs 是开始的最简单的类型，但是它不能处理非常大的 worlds（千米或更大的尺寸）。Recast graph 可以处理大世界，并且在更小的 sizes 上也比 grid graph 快得多，因为包含少得多的 nodes。缺点是它扫描的时间更长，并且对于运行时更新没有 grid graph 灵活。但是如果你有一个静态的 level，你几乎绝对应该使用 recast graph
- 不同的内置移动脚本有不同的性能特征。AILerp 脚本是最快的，但是移动不是非常真实，根据你的游戏类型，这可能可以接受或不能接受
- 如果你有很多 units，要尽量避免使用 CharacterController 组件。移除它而使用一个简单的 raycast 来检测 ground 通常快得多（如果使用 AIPath 和 RichAI 移动脚本，这可以开箱即用）
- 减少新 paths 计算的频率。这是被移动脚本的 repathRate 字段控制的
  - 你可以甚至关闭自动 path 重新计算，并且只在 character 开始移动时重新计算 path
  - 你可以定制自动重新计算 path，当角色距离目标很远时减少 path 重新计算的次数，而距离较近时提高重新计算的次数
- 在 modifiers 上使用更低的质量设置。尤其是你可以降低 SimpleSmoothModifier 细分路径的线段数，如果你使用它的话。AIPath 移动脚本以及可以很好地平滑跟随 path 了，即使 path 自身不是非常平滑
- 如果你使用 AIPath 或 RichAI 脚本：
  - 如果你有很多 AIs，则打开 AIBase.cs 脚本，然后根据你是否对移动 character 使用 rigidbodies 移除 Update 或 FixedUpdate 方法（如果不使用 rigidbodies，移除 FixedUpdate）。否则 Unity 仍然必须调用另一个方法，当有很多 AIs 时，这将显著增加性能消耗
