# Using nodes

Pathfinding是在nodes的graph上完成的。Nodes彼此之间以各种方式连接。Grid graph中每个tile是一个node，它们和相邻的4个或8个tiles连接。在Navmesh/recast graphs中每个三角形是一个node，node位于三角形的中心

## 插值和Position相近的Nodes

通常你想找到世界中哪个node距离一个point最近。

```C#
// 查找距离GameObject位置最近的node
GraphNode node = AstarPath.active.GetNearest(transform.position).node;
if (node.Walkable) {
    // 这个位置是可通过的，可以在此放置一个tower或什么东西
}
```

使用NNConstraint限定只查找特定的nodes

```C#
GraphNode node = AstarPath.active.GetNearest(transform.position, NNConstraint.Default).node;

var constraint = NNConstraint.None;
// 限定只查找walkable nodes
constraint.constrainWalkability = true;
constraint.walkable = true;

// 限定只搜索tag 3或tag 5的nodes
// tags是bitmask
constraint.constrainTags = true;
constraint.tags = (1 << 3) | (1 << 5)

var info = AstarPath.active.GetNearest(transform.position, constraint);
var node = info.node;
var closestPoint = info.position;
```

这些constraints的搜索范围是没有限制的，可以非常大。可以在A* Inspector->Setting->Max Nearest Node Distance或者AstarPath.maxNearestNodeDistance设置最大搜索距离。如果最近node比最大距离远，则GetNearest方法返回null node。

## Node上距离target position最近的位置

GetNearest方法返回一个NNInfo结构，包含两个字段

- node：包含最佳node（或者null如果没有搜索失败）
- position：包含node上距离查询point最近的位置

## Node connections

每个node保存它连接到哪些nodes。GetConnections方法可以访问一个node的所有连接。它使用一个delegate，这个delegate对node的每个连接的node调用一次。

```C#
GraphNode node = ...;
node.GetConnections(otherNode => {
    Debug.DrawLine((Vector3)node.position, (Vector3)otherNode.position);
});
```

## Node properties

node.position表示node在world space的位置，Int3而不是Vector3

如果node是walkable的，可以访问node上各种属性，例如tag和penalty（惩罚）

bool walkable = node.Walkable;
unit tag = node.Tag;
unit penalty = node.Penalty;

可以在运行时改变node的属性

node.RandomPointOnSurface() => Vector3 获得node表面上的一个随机位置

node.SurfaceArea() => float 返回node的表面积

## TriangleMeshNode

Mesh nodes用于navmesh和recast graph

Vector3 cloestPoint = node.CloestPointOnNode(somePoint); // 3D空间中最近的位置

Vector3 cloestPoint = node.CloestPointOnNodeXZ(somePoint); // 从上向下看XZ平面最近的位置

if (node.ContainsPoint(somePoint)) // 检查一个位置是否在node中（当从上向下看的时候）

获得三角形的vertices  
Int3 v0 = node.GetVertex(0);  
Int3 v1 = node.GetVertex(1);  
Int3 v2 = node.GetVertex(2);

或者

Int3 v0, v1, v2;  
node.GetVertices(out v0, out v1, out v2);

## Reachability（可达性）

判定character是否可以到达一个特定node

Pathfinding系统通过计算graphs的connected components来预计算哪些nodes可以从哪些nodes到达，可达矩阵。每个Node的area字段设置为它的connected component的索引。如果两个nodes具有相同的area意味着它们之间有一个有效路径。

```C#
var node1 = AstarPath.active.GetNearest(point1);
var node2 = AstarPath.active.GetNearest(point2);
if (PathUtilities.IsPathPossible(node1, node2)) {
    // 两个node之间有有效路径
}
```

计算这些areas或connected components的过程成为flood filling。

还可以给IsPathPossible方法提供一个tag mask或着一个nodes列表

List\<GraphNode> reachableNodes = PathUtilities.GetReachableNodes(node); // 查找一个给定node的所有可达nodes

还有一些方法可以查找一个node指定距离内所有可达的nodes
