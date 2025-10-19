# Heuristic Optimization

如何使用启发式优化来获得显著的加速。

通常当开始一个 pathfinding 搜索时，将会使用一个启发函数 heuristic。A* 算法和 dijkstra 算法的区别就是 dijkstra 看的是当前 node 到邻近 node 的路径代价，而 A* 看的时当前 node 到 target 的估计代价。这个代价估计就是启发函数。启发函数是当前 node 到 target 的最小粗略估计代价。通常真实世界中，直接使用到 target 的欧几里得距离，因为它很快而且通常给出相对好的结果。问题是在不是很开放，四周散步很多小的 obstacles 的世界中，这样的估计不是非常好。这会导致搜索会比使用更好的启发函数时通过更多 nodes。

## Results

这个技术可以剧烈地降低找到 target 需要被搜索的 nodes 的数量。因此这可以显著提升性能。 

考虑下面两个图片。第一个图片中优化是关闭的，而第二个是开启的。在第二个图片中，搜索具有更多的信息，并且可以避免很多不会使它到达 target 的方向。

Heuristic optimization disabled

![heuristic_off](../../../Image/heuristic_off.png)

Heuristic optimization enabled

![heuristic_on](../../../Image/heuristic_on.png)

## Background

如果你的世界是静态的，或者更新非常少，有一种技术可以用于预计算两个 nodes 之间的距离，并获得更好的启发。这在很多情况下可以数量级地提升 pathfinding 性能（10x）。

当然优化的启发是当我们知道 graph 中每个 node 到每个其他 node 的距离，然而这有点不太实际，因为它将会花费很长时间来计算，并使用大量空间。

因此能做的是我们选择一些 nodes（此后称为 pivot points），并计算这些 nodes 到每个其他 node 的距离。然后这个可以被用于计算非常好的启发。

不管使用什么启发函数，A* 算法将总是搜索那些位于最短路径上的所有 nodes，因此这个技术在很大**开放**的 grid graphs 上不会给出任何性能提升，因为一个 path 搜索很少几乎很少搜索比最短路径上更多的 nodes，因为 graph 是开发的，简单的启发函数就能给出最好的代价估计。

下图显式了一个完整的 empty grid graph，和 3 个不同的优化路径。这个算法将必须搜索绿色区域的所有 nodes，因为他们都是一样好的（比如它们具有相同的长度）。素有这些 nodes 位于一个最优路径上，因为在一个 grid 中有很多优化路径。

![suboptimal](../../../Image/suboptimal.png)

The A* Pathfinding Project has algorithms for automatically selecting pretty good pivot points because it can be quite hard to select them in a good way manually. When I profile, I sometimes find that my manual placements of pivot points is worse than just randomly selected points.

## Placing Pivot Points Manually

当放置这些 pivot points，关于它们的一个关键事情是，它们应该在世界中的 dead ends（死角）。当很多路径可以扩展到 pivot point 并且仍然是一个最短路径时执行最佳。

下面图示中你可以看见紫色的 pivot points。左下角的 agent 请求到绿色 circle 的一个路径。

![pivotPointPlacement](../../../Image/pivotPointPlacement.png)

还有你可以应用的游戏特定的知识。例如在一个塔防游戏中，几乎所有单位都会移动向一个目标。因此如果你只是放置一个 pivot point 在 goal 上，所有 paths 都可以非常快地计算，因为每一个其他 node 到那个 point 的优化距离都是已知的。

## Placing Pivot Points Automatically

存在两个模式。或者所有的 points 被随机选择，或者应用一个算法，尽可能彼此之间远地选择 nodes。第二种方法给出更高质量的启发，但是它计算地更慢，因为它需要初始距离计算顺序地完成，因此多线程没有被使用。

在下图中，显示了一个对比，5个随机算则 point 和 5个 points 彼此远离。后者倾向被放置在 dead ends，或者在 map 的角落，给出更好的结果。

![random](../../../Image/random.png)

你应该使用的 pivot points 的数量是各种各样的。最近方案就是尝试不同的 values，并观察对你游戏的最近值。当达到一百个 pivot points 时，来自它们的消耗通常比减少搜索的 nodes 数量的收益更大。建议使用 1-100 之间的数量，尝试不同的 values 并观察最佳 value。

你可能注意到游戏的开始有一个 delay，直到 pathfinding 开始工作。这是因为它在忙着处理启发查询 heuristic lookups。如果你发现这个延迟太大成为一个问题时，切换到使用 Random 模式，而不是 Random Spread Out，或者减少 pivot points 的数量。
