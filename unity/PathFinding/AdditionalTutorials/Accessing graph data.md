# Accessing graph data

如何访问 graphs 和 nodes。

Graphs 中的所有数据都是可访问的。很多情况下，API 期望一个 GraphNode 作为参数，因此你需要能够发现它们。并且可能有些其他情形，你需要大量修改 graph data 来满足你的游戏。例如，你可能拥有你自己的定制 tilemap 生成器，并且你需要传递那些数据到 grid graph。

## Accessing graphs

所有 graphs 被存储在 Pathfinding.AstarData 类中。它包含一个拥有所有 graphs 的数组，以及很多便捷方法在其中查找 graphs。然而最快的方法是使用提供的 shortcut。对于每种内置类型的 graph，有一个指向那个类型第一个 graph 的 field。

```C#
GridGraph gridGraph = AstarPath.active.data.gridGraph;
PointGraph pointGraph = AstarPath.active.data.pointGraph;
NavMeshGraph navmeshGraph = AstarPath.active.data.navmesh;
RecastGraph recastGraph = AstarPath.active.data.recastGraph;
LayerGridGraph layerGridGraph = AstarPath.active.data.layerGridGraph;

NavGraph[] allGraphs = AstarPath.active.data.graphs;

// You can set the name of a graph in the graph inspector
var graph = AstarPath.active.data.FindGraph(g => g.name == "My Custom Graph Name");
```

## Getting nodes in a graph

不同的 graphs 以不同的方式保存它们的 nodes。例如，grid graph 保存所有 nodes 到一个巨大的数组中，它可以被索引来轻松地获取指定 index 上的 node。Recast graph 存储所有 nodes 各自 tiles 的数组中（stores all nodes in arrays in separate tiles）。

获取一个 graph 中所有 nodes 的通用的高级方法是使用 GetNodes 方法，它存在于所有类型的 graphs 中。它采用一个 callback，对每个 node 进行调用。之所以使用一个 callback 而不是 iterator，是因为对于很大的 graphs callbacks 显著地比 iterator 更快。

```C#
var gg = AstarPath.active.data.gridGraph;

gg.GetNodes(node => {
    // Here is a node
    Debug.Log("I found a node at position " + (Vector3)node.position);
});
```

Warning

    不要更新 nodes 中的数据。这可能影响同时在运行的 pathfinding（尤其是使用多线程的时候）。要安全地更新 node data，你需要在一个安全的 callback 中完成。你可以使用 AstarPath.AddWorkItem 请求一个安全的 callback。

### GridGraph

Grid graph nodes 被存储在一个很大的数组中。它通过 node 的坐标来索引，因此它们可以容易地访问。还有一些便捷方法来访问 nodes：

```C#
var gg = AstarPath.active.data.gridGraph;
int x = 5;
int z = 8;
GridNodeBase node = gg.GetNode(x, z);
```

有一些情形，你想要在运行时改变 grid graph 的 size。为此你可以修改 unclamped size 字段，它是 grid 的世界单位 size，或者你可以使用 SetDimensions。当你改变了 graph 的 width 或 depth，你需要使用 AstarPath.Scan 重新计算 graph。

```C#
var gg = AstarPath.active.data.gridGraph;
var width = 80;
var depth = 60;
var nodeSize = 1.0f;

gg.SetDimensions(width, depth, nodeSize);

// Recalculate the graph
AstarPath.active.Scan();
```

可以使用 RelocateNodes 方法移动 grid graph 而不重新计算它。相同的方法还可以用于其他 graphs，但是之后你必须自己计算必须的 matrix。

### Layered Grid Graph

Layered grid graph 的工作几乎就像 grid graph。但是因为 layered grid graphs 可以包含多个 layers，因此一个额外的 layer 坐标是必须的。

```C#
var gg = AstarPath.active.data.layerGridGraph;
int x = 5;
int z = 8;
int layer = 0;
GridNodeBase node = gg.GetNode(x, z, layer);
```

### NavmeshGraph/RecastGraph

Recast graphs 将 nodes 划分为许多 tiles。单独的 tile 存储到一个数组中，就像 grid graph 存储它的 nodes。在每个 tile 中，nodes 存储到一个数组中，但没有固定的顺序。然而所有 nodes 还被添加到一个 axis aligned bounding box tree（AABB tree），以便可以高效地查询到一个 point 的最近的 node。Navmesh graphs 和 recast graphs 完全一样，但是它们总是使用一个单个的 tile。

```C#
var graph = AstarPath.active.data.recastGraph;
int tileX = 5;
int tileZ = 8;
NavmeshTile tile = graph.GetTile(tileX, tileZ);

for (int i = 0; i < tile.nodes.Length; i++) {
    // ...
}
// or you can access the nodes like this:
tile.GetNodes(node => {
    // ...
});
```

### PointGraph

Point graphs 简单地存储 nodes 到一个数组中，但没有固定顺序。

Point graph nodes 还包含一个 field，包含它们创建自的 GameObject，可以被用于任何目的。

```C#
var node = AstarPath.active.GetNearest(transform.position).node;
var pointNode = node as PointNode;

if (pointNode != null) {
    Debug.Log("That node was created from the GameObject named " + pointNode.gameObject.name);
} else {
    Debug.Log("That node is not a PointNode");
}
```

你还可以在运行时点击 nodes 到 point graph 中：

```C#
AstarPath.active.AddWorkItem(new AstarWorkItem(ctx => {
    var graph = AstarPath.active.data.pointGraph;
    // Add 2 nodes and connect them
    var node1 = graph.AddNode((Int3)transform.position);
    var node2 = graph.AddNode((Int3)(transform.position + Vector3.right));
    var cost = (uint)(node2.position - node1.position).costMagnitude;
    node1.AddConnection(node2, cost);
    node2.AddConnection(node1, cost);
}));
```
