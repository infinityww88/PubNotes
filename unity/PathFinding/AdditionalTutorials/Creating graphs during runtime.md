# Creating graphs during runtime

如何从脚本中在运行时创建 graphs。

如果出于一些原因你不能在 Unity Editor 在设计时创建 graph 并设置它的 settings，可以通过脚本直接创建 graphs。

Note

    你可以在文件中保存和加载 graph settings 和完全 scanned graphs。通常你可以在 unity editor 中定义大多数 settings，然后在游戏开始时使用脚本只调整一些 values 然后 re-scan graph

你可以像下面这样创建一个 graph：

```C#
// This holds all graph data
AstarData data = AstarPath.active.data;

// This creates a Grid Graph
GridGraph gg = data.AddGraph(typeof(GridGraph)) as GridGraph;
```

Graph objects 拥有所有暴露在 graph editor 中的设置，因此你可以设置它们为任何你想要的值，然后 scan 这个 graph。

```C#
// This holds all graph data
AstarData data = AstarPath.active.data;

// This creates a Grid Graph
GridGraph gg = data.AddGraph(typeof(GridGraph)) as GridGraph;

// Setup a grid graph with some values
int width = 50;
int depth = 50;
float nodeSize = 1;

gg.center = new Vector3(10, 0, 0);

// Updates internal size from the above values
gg.SetDimensions(width, depth, nodeSize);

// Scans all graphs
AstarPath.active.Scan();
```

如果你想要使用你自己的 nodes 和 connections 创建一个完全自定义 graph，你可以使用一个 point graph，想这样：

```C#
// This holds all graph data
AstarData data = AstarPath.active.data;

// This creates a Point Graph
PointGraph graph = data.AddGraph(typeof(PointGraph)) as PointGraph;

AstarPath.active.Scan(graph);

// Make sure we only modify the graph when all pathfinding threads are paused
AstarPath.active.AddWorkItem(new AstarWorkItem(ctx => {
    // Add 2 nodes and connect them
    var node1 = graph.AddNode((Int3) new Vector3(1, 2, 3));
    var node2 = graph.AddNode((Int3) new Vector3(4, 5, 6));
    var cost = (uint)(node2.position - node1.position).costMagnitude;
    node1.AddConnection(node2, cost);
    node2.AddConnection(node1, cost);
}));

// Run the above work item immediately
AstarPath.active.FlushWorkItems();
```

或者你可以创建你自己的定制 graph type，更多信息查看 Writing Graph Generators.


