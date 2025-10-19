# A* Inspector

Sections:

- Graphs：保存scene中所有的graphs
- Setting：各种pathfinding和editor的设置
- Save & Load：允许从文件中保存和加载graphs
- Optimization：各种可以使用编译器指示符应用到系统的优化
- About：documentation
- Scan：重新计算所有graphs

## Graphs

当前scene中的所有graphs。可以有多个graphs，它们被保存在AstarPath/Pathfinding组件内（但不要创建多个AstarPath/Pathfinding组件）

每个graph有4个icon

- eye：在scene中显示或隐藏graph
- pen：重命名graph。如果有多个graphs，可以标记每个graph的意义
- i：info，显示graph中有多少node，必须先scan过
- x：删除graph

## Settings

### Pathfinding

- Thread Count：使用的pathfinding线程数

    None指示pathfinding在Unity thread作为coroutine运行。Automatic尝试根据计算机的内存和core的数量调整线程数。建议使用Auto settting中的一个，因为target平台是不确定的，很可能运行在老旧的平台。

    如果同时只有一个或两个characters活跃，可以只使用一个thread，因为不太可能需要额外的线程。多线程只是增加pathfinding吞吐量，并不能加快一个pathfinding的计算速度。

- Max Nearest Node Distance：搜索nodes的最大距离

    当搜索到一个point的最近node时，这个值限制允许的最远世界距离。当请求到达一个不可能到达的point的pathfinding时，只能搜索距离这个point的最近的可到达的node。这个值限制允许的node-point距离，如果超过这个距离，path将会失败。

- Heuristic（启发函数）

    通常成为H函数，是用来评估一个node到target的启发距离的。不同的启发函数影响pathfinding如何从多个可能的path中进行选择。

- Heuristic Scale

    heuristic的cale。如果使用小于1的值，pathfinder将搜索更多的nodes（更慢）。如果使用0，pathfinding algorithm将退化为dijkstra算法。这等价于将Heuristic设置为None。如果使用大于1的值，通常更快，因为它扩展更少的nodes，但是paths可能不是最优的。

### Advanced

- Heuristic Optimization（TODO）

- Batch Graph Updates

    Toggle时，graph更新将被batched并且更少执行。这对pathfinding吞吐量有正面影响，因为线程不必频繁地停止和启动，因此减少了每次graph update对消耗。所有对graph update仍然会被应用，它们只是被batched在一起以便可以在同一时间执行更多请求。

    但是如果想要graph update和applied的最小对延迟，则不要打开此选项。

    这只应用到使用UpdateGraphs方法请求的graph updates，而不是使用RegisterSafeUpdate或者AddWorkItem的请求。

    如果想立即应用graph updates，调用FlushGraphUpdates。

- Update Interval

    每个graph update batch之间最少的秒数。这个interval之内的请求batch到一起，否则就成为两个batch

- Prioritize Graphs

    Graphs将基于它们在inspector上的顺序优先选择。具有和target point距离小于prioritizeGraphsLimit的第一个graph将被选择而不是搜索所有的graphs

- Full Get Nearest Node Search

    对所有graphs做一个全面的GetNearest search。

    额外的搜索通常只在第一次快速搜索中看起来具有最近node的graph上执行。

    当这个选项打开时，additional搜索在所有的graphs上执行，因为第一次检查不总是完全精确。更技术一点地说，如果为true，GetNearestForce在所有的graphs上调用，否则只在GetNearest搜索返回最佳的graph上调用。

    通常关闭时比较快，但是开启时给出更好的搜索。当使用navmesh或或recast graph时，为了得到最好结果，这个选项应该与Pathfinding.NavMeshGraph.accurateNearestNode一起设置为true。

    对于PointGraph，这个选项没有什么影响，因为它只有一个搜索模式。

    AstarPath上保存的所有graphs都是对当前scene的描述，只是使用不同方法。当指定一个target point进行搜索时，默认在每个graph上进行一次A*搜索，然后再找出最短的那个。Prioritize Graphs和Full Get Nearest Node Search都是用来控制在哪些graphs进行搜索的，以避免对所有的graph进行搜索。但是通常一个scene具有两个graph就足够了。

- Scan on Awake

    如果为true，所有graphs都在Awake时被scan。这不包括从cache中的加载。如果关闭此选项，必须手动调用AstarPath.active.Scan()来开启pathfinding。或者还可以从一个文件中加载保存的graph。Graph就是node数据，需要scan一下得到，可以保存到文件中并从文件中加载。

### Debug

- Path Logging

    在控制台打印的消息数量

- Graph Coloring

    在sceneview中绘制nodes

- Show Search Tree

    nodes绘制到它们parent的line。只显示最近的path

- Show Unwalkable Nodes

### Color

设置sceneview中graph的显示颜色

## Save & Load

graphs就是node邻接数据。可以保存在文件中并从文件加载。还可以配置cached startup（避免在游戏开始时的长时间计算）

## 优化

包含一组编译器指示符，告诉编译器排除或包含一部分code。这将导致非常大的变化，例如移除或添加一个class的字段，或者改变一个方法的行为，而没有运行时消耗。
