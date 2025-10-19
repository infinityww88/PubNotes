# Wandering AI Tutorial

创建游荡 wandering AI.

不同的方法有不同的质量和性能，适合不同的场景。

## Method 1: Random point inside a circle

随机选择 player 周围的一个点。

```C#
Vector3 PickRandomPoint () {
    var point = Random.insideUnitSphere * radius;

    point.y = 0;
    point += transform.position;
    return point;
}
```


```C#
using UnityEngine;
using System.Collections;
using Pathfinding;

public class WanderingDestinationSetter : MonoBehaviour {
    public float radius = 20;

    IAstarAI ai;

    void Start () {
        ai = GetComponent<IAstarAI>();
    }

    Vector3 PickRandomPoint () {
        var point = Random.insideUnitSphere * radius;

        point.y = 0;
        point += ai.position;
        return point;
    }

    void Update () {
        // Update the destination of the AI if
        // the AI is not already calculating a path and
        // the ai has reached the end of the path or it has no path at all
        if (!ai.pathPending && (ai.reachedEndOfPath || !ai.hasPath)) {
            ai.destination = PickRandomPoint();
            ai.SearchPath();
        }
    }
}
```

你可以挂载这个脚本到任何具有内置移动脚本（AIPath/RichAI/AILerp）的 GameObject 上。

注意：确保没有其他也试图设置 AI destination 的组件挂载到 GameObject 上（例如 AIDestinationSetter 组件）

Advantages

- Very fast
- Simple code
- 可以用于所有 graph type

Disadvantages

- 忽略到 point 的实际距离，意味着如果 world 不是非常开发的（充满各种阻碍），有可能产生非常长的路径
- 对于非常接近 walls/obstacles 的 points 会产生轻微的偏差，因为任何生成到 obstacles 中的 points 都必须对齐到 graph 中的最近的 point

Misc

- 当 picking points 时，忽略 penalties（尽管在搜索到 point 的路径时 penalties 将会被考虑）

## Method 2: Random node in the whole graph

相比拾取当前位置周围的一个 node，你可以只是拾取 graph 中一个随机的 node，并尝试走向那个 node 的位置。

```C#
GraphNode randomNode;

// For grid graphs
var grid = AstarPath.active.data.gridGraph;

randomNode = grid.nodes[Random.Range(0, grid.nodes.Length)];

// For point graphs
var pointGraph = AstarPath.active.data.pointGraph;
randomNode = pointGraph.nodes[Random.Range(0, pointGraph.nodes.Length)];

// Works for ANY graph type, however this is much slower
var graph = AstarPath.active.data.graphs[0];
// Add all nodes in the graph to a list
List<GraphNode> nodes = new List<GraphNode>();
graph.GetNodes((System.Action<GraphNode>)nodes.Add);
randomNode = nodes[Random.Range(0, nodes.Count)];

// Use the center of the node as the destination for example
var destination1 = (Vector3)randomNode.position;
// Or use a random point on the surface of the node as the destination.
// This is useful for navmesh-based graphs where the nodes are large.
var destination2 = randomNode.RandomPointOnSurface();
```

依赖于你想将这个方法用于何处，可能想要在拾取一个 node 之后做一些检查：

- 检查 node 是否 walkable (see Pathfinding.GraphNode.Walkable)
- 检查 node 是否可以从 AI 位置到达 (see Pathfinding.PathUtilities.IsPathPossible)
- 其他一些和你游戏相关的检查。如果这些检查失败了，你可以拾取一个新的随机 node 并重新运行检查。除非有效的 nodes 非常少，而你想要快速找到一个可用的 node

Advantages

- Very fast (unless you use the generic approach above)
- Simple code 

Disadvantages

- 不能控制路径的长度

Misc

- 忽略 penalties

## Method 3: The RandomPath type

RandomPath 类型是一个 path type，相比于计算从一个位置到另一个位置的正常的 paths，这个 path 从 starting point 计算一个随机路径

```C#
RandomPath path = RandomPath.Construct(transform.position, searchLength);

path.spread = spread;
seeker.StartPath(path);
```

然而添加这些 code 到任何内置的 movement scripts 需要你创建一个派生的新的 class，并覆盖相关方法。因此其他方法更加容易。

Advantages

- 选择 point 和计算路径一步完成
- 每个 node 被认为有相同的概率被选择，没有方法 1 中 靠近 obstacles 的偏差
- 可以设置一个最小的 path const（searchLength）

Disadvantages

- 对于长路径可能很慢
- 不容易和内置移动脚本集成
- 对于 navmesh/recast graphs 工作得不是很好，因为每个 node 具有相同的概率被选择，而每个 node 的大小是不同的

Misc

- 考虑 penalties 

## Method 4: The ConstantPath type

ConstantPath 类型是一个 path 类型，它查找从 start point 可以到达的尽可能接近特定值的所有 nodes。所有这些 nodes 被发现之后，我们可以在这些 nodes 中拾取一个或多个随机位置。

```C#
ConstantPath path = ConstantPath.Construct(transform.position, searchLength);

AstarPath.StartPath(path);
path.BlockUntilCalculated();
var singleRandomPoint = PathUtilities.GetPointsOnNodes(path.allNodes, 1)[0];
var multipleRandomPoints = PathUtilities.GetPointsOnNodes(path.allNodes, 100);
```

如果你想将这个信息传递给内置移动脚本，你可以使用和方法1相同的方式

Advantages

- 可以在一个 path request 中拾取多个随机位置
- 一个 node 被选择的概率和它的表面积成比例（因此，如果所有 nodes 具有相同大小，例如使用 grid graph 时，每个 node 被认为具有相同的选择概率。没有方法1 中靠近 obstacle 的偏差
- 如果需要，可以后续对 nodes 进行自定义过滤
- 通常比方法3更快
- 对 navmesh/recast graphs 也工作的很好

Disadvantages

- 当必须搜索大量 nodes 可能会很慢

Misc

- 考虑 penalties

## Method 5: Breadth-first search

BFS 是一个简单搜索，它从 starting node 向外搜索，每次一个 node。它不考虑 penalties 或任何其他类型的代价。这意味着，在 grid graph 上搜索时，上下左右移动和对角移动具有相同的代价。

使用它的方法和方法4非常类似。

```C#
// Find closest walkable node
var startNode = AstarPath.active.GetNearest(transform.position, NNConstraint.Default).node;
var nodes = PathUtilities.BFS(startNode, nodeDistance);
var singleRandomPoint = PathUtilities.GetPointsOnNodes(nodes, 1)[0];
var multipleRandomPoints = PathUtilities.GetPointsOnNodes(nodes, 100);
```

使用和方法1一样的方法和内置的移动脚本集成。

Advantages

- 可以拾取多个随机位置，而不仅是一个
- 一个 node 被选择的概率和它的表面积成比例（因此，如果所有 nodes 具有相同大小，例如使用 grid graph 时，每个 node 被认为具有相同的选择概率。没有方法1 中靠近 obstacle 的偏差
- 如果需要，可以后续对 nodes 进行自定义过滤
- 没有对 pathfinding 系统必须的往返，这可以节省一些消耗
- 通常比方法4和方法3更快

Disadvantages

- 当搜索大量 nodes 时可能会很慢
- 不使用 pathfinding threads，因此失去了从 main Unity 线程 offload 工作的能力
- 对 navmesh/recast 工作得不是很好，因为依赖 navmesh 细节，paths 将会有很大的差别（更多更小的 nodes 意味着 BFS 不会到达很远）

Misc

- 不考虑 penalties 或任何其他 costs，只有遍历 nodes 的数量是相关的
