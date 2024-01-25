# Accessing graph data

Graph 的所有 data 都可以访问。有很多场景 API 需要一个 GraphNode 作为参数。有一些场景需要大量修改 graph data 来满足游戏。例如你可能有自己的自定义 tilemap 生成器，并需要将生成的 tilemap 传给 grid graph。

## Finding Nodes close to Positions

Here's how you get nodes

```C#
// Find the closest node to this GameObject's position
GraphNode node = AstarPath.active.GetNearest (transform.position).node;
if (node.Walkable) {
    // Yay, the node is walkable, we can place a tower here or something
}
```
有一些情况下可能只想得到特定 nodes，例如哪个 node 是最接近这个位置的 Walkable node。这可以通过使用 Pathfinding.NNConstraint 完成。对于这种情景，使用 Default NNConstraint 即可（它称为默认的，是因为如果没有指定任何东西时，它用于 path calls）。

```C#
GraphNode node = AstarPath.active.GetNearest (transform.positon, NNConstraint.Default).node;
```
这些 constraints 的搜索范围是没有限制的，但是非常大。最大距离可以在 A* Inspector -> Settings -> Max Nearest Node Distance or AstarPath.maxNearestNodeDistance 中设置。

### Closest Point on Nodes

GetNearest 方法返回一个 NNInfo 结构体，它包含两个字段。第一个字段是搜索的 node（或者 null，如果没有搜索到 node）。第二个字段是 position，它包含那个 node 上到查询为止的最近 point。在 grid graphs 上，nodes 被认为是 squares，因此 position 字段将会包含 square 内接近 query point 的最近的位置。在 navmesh based graphs 上（RecastGraph 和 NavMeshGraph），position 字段会包含最近 triangle 上的最近 point。Point node 没有 surface，因此 position 就是 node 的 position。

## Accessing graphs

所有 graphs 被存储在 Pathfinding.AstarData 类中。它将所有 graphs 包含在一个 array 中，并有很多方法在其中查找 graphs。最快的方法是使用提供的快捷方法。对于每种内置的 graph 类型，有一个 field 指向那个类型的第一个 graph。

```C#
GridGraph gridGraph = AstarPath.active.astarData.gridGraph;
PointGraph pointGraph = AstarPath.active.astarData.pointGraph;
RecastGraph recastGraph = AstarPath.active.astarData.recastGraph;
NavMeshGraph navmeshGraph = AstarPath.active.astarData.navmesh;
LayerGridGraph layerGridGraph = AstarPath.active.astarData.layerGridGraph;

NavGraph[] allGraphs = AstarPath.active.astarData.graphs;
```

## Getting nodes in a graph.

不同的 graphs 类型以不同的方式存储它们的 nodes。例如 grid graph 在一个很大 array 中存储所有 nodes，它们可以很容易地被索引来得到特定 cell index 的 node。recast graph 在单独的 tiles 中的 arrays 中存储 nodes。

获取 graph 中所有 nodes 最通用的高层方法是使用 GetNodes 方法，它在所有 graphs 上都存在。它使用一个 callback，它在每个 node 上调用。如果 graph 应该继续在剩余 nodes 调用 callback，callback 应该返回 true，返回 false 则 graph 停止遍历 nodes。使用 callback 而不是 iterator 是因为 callback 更快，对于很大的地图会有显著影响。

```C#
var gg = AstarPath.active.astarData.gridGraph;
gg.GetNodes (node => {
    // Here is a node
    return true;
});
```
注意：不要在遍历时更新 data。这会影响当时正在进行的 pathfinding（尤其是使用多线程的时候）。要安全地更新 node 数据，需要放在一个安全的 callback（AstarPath.RegisterSafeUpdaet）或者使用 AddWorkItem。

## GridGraph

Grid graph nodes 存储在一个很大的 array。它通过 node 的坐标进行索引，因此访问很容易。

```C#
var gg = AstarPath.active.astarData.gridGraph;
int x = 5;
int z = 8;
GridNode node = gg.nodes[z*gg.width + x];
```
有时在运行时想要改变 grid graph 的大小。则可以修改 unclampedSize 字段（它是 grid 的 world units 大小）。也可以修改 width 和 height 字段，但是之后需要调用 UpdateSizeFromWidthDepth 方法。在改变 graph 的 width 或 depth 之后，需要用 AstarPath.Scan 来重新计算它。

```C#
var gg = AstarPath.active.astarData.gridGraph;
gg.width = 80;
gg.depth = 60;
gg.UpdateSizeFromWidthDepth();
// Recalculate the graph
AstarPath.active.Scan ();
```

还可以使用 RelocateNodes 方法移动 grid graph 而不重新计算。相同的方法也可以用于其他 graphs，但是必须自己计算必须的 matrix。

## Layered Grid Graph

Layered grid graph 和 grid graph 几乎一样。但是 nodes 不是以相同的方式排序的。因为 layered grid graphs 可以包含多个 layers。需要一个额外的 layer 坐标。

```C#
var gg = AstarPath.active.astarData.layerGridGraph;
int x = 5;
int z = 8;
int y = 2; // Layer
LevelGridNode node = gg.nodes[y*gg.width*gg.depth + z*gg.width + x];
```

## Recast Graphs

Recast graphs 将 nodes 划分到很多 tiles 中。单个 tiles 以与 grid graph 存储 nodes 相同的方式存储到数组中。在每个 tile 内部，nodes 存储在一个数组中，没有任何内在的顺序。但是所有 nodes 都被添加到一个 axis aligned bounding box tree（AABB tree）中，以便能快速查找到一个 point 的最近 node。

```C#
var graph = AstarPath.active.astarData.recastGraph;
int tileX = 5;
int tileZ = 8;
RecastGraph.NavmeshTile tile = graph.tiles[tileZ*graph.tileXCount + tileX];
for (int i = 0; i < tile.nodes.Length; i++) {
    // ...
}
```

## PointGraph

Point graphs 简单存储 nodes 到一个数组中，没有任何内在顺序。

Point graph nodes 还包含一个 field 存储创造它的 GameObject，它可以用于任何目的。

```C#
var node = AstarPath.active.GetNearest (transform.position).node;
var pointNode = node as PointNode;
if (pointNode != null) {
    Debug.Log ("That node was created from the GameObject named " + pointNode.gameObject.name);
} else {
    Debug.Log ("That node is not a PointNode");
}
```

