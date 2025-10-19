# Graph Updates during Runtime

## Overview

有时在运行时更新 graph 是很必要的。或许 player 建造了一个新的建筑，或者一扇门被打开了。

Graphs 可以被完全重新计算，或者部分更新。如果你修改了整个 map，完全重新计算是很好的。但是如果只需要修改 graph 很小的部分，则部分 update 更加快速。

有很多方式可以更新 graph，同时有很多不同的情景你想要更新 graph。下面总结了一些场景的用例。但是 games 是非常不同的，因此一些 solution 可能适合你的游戏但是没有在这个列表里面。

| You want | How to do it |
| --- | --- |
| 重新计算整个 graph | Recalculating the whole graph |
| 精确设置哪些 nodes 是 walkable 的，哪些不是 | Using direct access to graph data 和 Utilities for turn-based game |
| 当一些 object 创建，销毁，或者在周围移动时更新 graph | Recalculating parts of graphs，尤其是 DynamicGridObstacles 和 Navmesh Cutting |
| 更新单个 node 的属性 | Using direct access to graph data 和 GraphUpdateScene |
| 动态加载和卸载 graphs（例如到一个文件中 | Saving and Loading Graphs |
| a smaller grid graph to follow the player around（例如一个 procedural world | ProceduralGridMover |
| 创建新的 nodes 并使用 code 连接它们 | PointGraph.AddNode 和 Writing Graph Generators |
| 使 graph 的一部分更难以穿越 | Recalucalting parts of graphs，Using direct access to graph data，和 GraphUpdateScene |
| 阻止一些 units 穿越一些 nodes，当时允许另一些 units | Working with tags，Recalculating parts of graphs，GraphUpdateScene 和 Using direct access to graph data |
| 在一个移动的 object 上 pathfinding（例如一艘船） | 查看 Moving example scene。现在并没有很好的文档 |
| 添加一个 obstacle，但是首先确保它没有 block 任何 unitys（用于塔防游戏） | Check for blocking placements |

## What to update

当更新 graphs 时，通常想要完成两种更新的一种。

- 你可能想要使用相同的设置重新计算 graph，就像它初始生成时那样被计算。但是如果你只更新 graph 一个很小的区域，重新计算整个 graph （使用 AstarPath.Scan）看起来很浪费。例如 player 可能只是想在塔防游戏中放置一个新的 tower
- 或者你可能想改变现有 graph 上的一些设置。例如，你可能想改变 tag 或者一些 nodes 上的穿越代价

只改变 graph 的一小部分就像它在开始时被计算的一样，可以在所有类型的 graph 执行，除了 NavMeshGraph，因为它通常只有完全重新计算才有意义。无论使用 scripting 还是 GraphUpdateScene 组件来完成这个工作，所做的都是设置 updatePhysics 字段为 true，尽管这个字段名不是很有描述性。

- Grid graphs 将会像你期望的那样工作，你可以指定 bounds 然后它为你做所有的事情。然而它可能重新计算一个被你指定的稍微大一些的 region，使得诸如侵蚀 erosion 被考虑到。
- Recast graphs 一次只能重新计算一个完整的 tile。因此当产生一个更新请求时，指定的 bounds 接触的所有 tiles 将会被完全重新计算。因此使用一个小 tile size 可以很好地避免非常大的重计算时间。但是不要太小，因为它本质上简并到一个 grid graph。如果你使用多线程，很大 tile 的重计算将会 offload 到其他线程中，来避免影响 FPS 太多。
- Point graphs 将会重计算穿越 指定的 bounds 的所有 connections。但是它不会查看作为 GameObject 被添加的新 nodes。为此，你需要使用 AstarPath.Scan。

如果你想改变现有 graph 上的属性，有很多东西可以改变。

- 你可以改变 nodes 上的 tags。这可以被用来 enable 一些 units 穿越一个 region，而阻止另一些 units。
- 你可以改变 nodes 上的 代价 penalty。这被用来使一些 nodes 比其他 nodes 更难/更慢 地穿越，使得一个 agent 将会更倾向其他的路径。但是有一些限制。你不能指定负数的代价，因为算法不能处理它（即使可以，系统将会慢得多）。然而一个重用的技巧是，设置一个非常大的初始代价（可以在 graph settings 中完成），然后从这个 high value 减少代价。但是注意这将会使 pathfinding 整体更慢，因为它必须搜索更多的 nodes。产生影响需要的 penalty values 相当高。没有真实的 penalty 单位，一个 1000 的 penalty 差不多对应一个 world unit 的 travel。
- nodes 的 walkability 也可以被直接修改。因此你可以使 bounds 内的所有 nodes 全部成为 walkable 或全部成为 unwalkable 的。

GraphUpdateScene 组件设置几乎是一对一地映射到 GraphUpdateObject，GraphUpdateObject 被用于通过脚本更新 graphs。因此建议越读 GraphUpdateScene 文档，即使你只想使用脚本更新 graph。

### Recalculating the whole graph

为所有 graphs 或只是一些完全重新计算，可以这样：

```C#
// Recalculate all graphs
AstarPath.active.Scan();

// Recalculate only the first grid graph
var graphToScan = AstarPath.active.data.gridGraph;
AstarPath.active.Scan(graphToScan);

// Recalculate only the first and third graphs
var graphsToScan = new [] { AstarPath.active.data.graphs[0], AstarPath.active.data.graphs[2] };
AstarPath.active.Scan(graphsToScan);
```

你还可以异步地重新计算 graphs。这并不保证很好的帧率，但是你至少可以显示一个 loading screen。

```C#
IEnumerator Start () {
    foreach (Progress progress in AstarPath.active.ScanAsync()) {
        Debug.Log("Scanning... " + progress.description + " - " + (progress.progress*100).ToString("0") + "%");
        yield return null;
    }
}
```

AstarPath.Scan

AstarPath.ScanAsync

### Recalculating parts of graphs

较小的 graph updates 可以通过 GraphUpdateScene 组件 或者 使用脚本完成。GraphUpdateScene 可以在 Unity inspector 中编辑。脚本更新则通过调用 AstarPath 类的一个方法完成，或者传递一个 Bounds object，或者传递一个 Pathfinding.GraphUpdateObject（这也是 GraphUpdateScene 在背后实际做的事情）。

```C#
// As an example, use the bounding box from the attached collider
Bounds bounds = GetComponent<Collider>().bounds;

AstarPath.active.UpdateGraphs(bounds);
```

```C#
// using Pathfinding; //At top of script

// As an example, use the bounding box from the attached collider
Bounds bounds = GetComponent<Collider>().bounds;
var guo = new GraphUpdateObject(bounds);

// Set some settings
guo.updatePhysics = true;
AstarPath.active.UpdateGraphs(guo);
```

这个方法将会在 queue 中放置一个 task，使其在下一个 path 计算之前完成。它必须被放在 queue 中，因为如果它直接计算，可能会影响 pathfinding，尤其是如果开启了多线程，并导致各种错误。这意味着你可能不会立即看到对 graph 的更新，但是它总是会在下一个 pathfinding 计算开始之前完成（几乎总是，查看 AstarPath.limitGraphUpdates）。

Recast graphs 还可以使用 navmesh cutting 伪更新 pseudo-updated。Navmesh cutting 可以在 navmesh 上为 obstacles 挖一个洞，但是不能添加更多的 navmesh surface。查看 Pathfinding.NavmeshCut 文档。这非常快，但是被重新计算整个 recast tile 更受限。

如果你在 Unity Editor 中操作一个已知的 graph，使用 GraphUpdateScene 组件通常是最简单的方法。例如，你可以很容易地改变一个指定区域的 tag 而不需要任何 code。然而如果你在运行时动态地更新，使用 code 更加容易。例如，如果在一个塔防游戏中，你更新 graph 使得新放置的建筑被考虑。

## Using Scripting

要更新一个 graph，你创建一个 GraphUpdateObject 并设置你想要的参数，然后你调用 AstarPath.UpdateGraphs 方法来 queue update request。

```C#
// using Pathfinding; //At top of script

// As an example, use the bounding box from the attached collider
Bounds bounds = GetComponent<Collider>().bounds;
var guo = new GraphUpdateObject(bounds);

// Set some settings
guo.updatePhysics = true;
AstarPath.active.UpdateGraphs(guo);
```

变量 bounds 引用一个 UnityEngine.Bounds 对象。它定义一个 axis aligned box，在其中 update graphs。通常你想要在新创建的 object 周围更新 graph。在这个例子中，bounding box 从挂载的 collider 获得。

但是确保这个 object 将会被 graph 识别。对于 grid graphs，你应该确保 object 的 layer 被包含在 collision testing mask 中，或者 height testing mask 中。

如果你不需要使用 grid graph 时重计算 nodes 上的所有参数，或者使用 point graph 时重计算所有的 connections，你可以设置 updatePhysics 为 false 来避免必要的计算。

```C#
guo.updatePhysics = false; 
```

### Using direct access to graph data

有些情况下，使用 GraphUpdateObject 来更新 graph 可能不方便。此时你可以直接更新 graph data。然而需要小心。当使用 GraphUpdateObject 时，系统为你做了很多事。

这里是一个例子，它改变一个 grid graph 中的所有 nodes，并使用柏林噪声来决定 nodes 是否是 walkable 的。

```C#
AstarPath.active.AddWorkItem(new AstarWorkItem(ctx => {
    var gg = AstarPath.active.data.gridGraph;
    for (int z = 0; z < gg.depth; z++) {
        for (int x = 0; x < gg.width; x++) {
            var node = gg.GetNode(x, z);
            // This example uses perlin noise to generate the map
            node.Walkable = Mathf.PerlinNoise(x * 0.087f, z * 0.087f) > 0.4f;
        }
    }

    // Recalculate all grid connections
    // This is required because we have updated the walkability of some nodes
    gg.GetNodes(node => gg.CalculateConnections((GridNodeBase)node));

    // If you are only updating one or a few nodes you may want to use
    // gg.CalculateConnectionsForCellAndNeighbours only on those nodes instead for performance.
}));
```

上面的 code 产生这个 graph。

![grid_perlin](../../Image/grid_perlin.png)

Graph data 必须只有在修改的时候时安全的才能这样做。Pathfinding 可能在任何时候运行，因此有必要首先暂停 pathfinding 线程，然后更新数据。最简单的方法时使用 AstarPath.AddWorkItem。

```C#
AstarPath.active.AddWorkItem(new AstarWorkItem(() => {
    // Safe to update graphs here
    var node = AstarPath.active.GetNearest(transform.position).node;
    node.Walkable = false;
}));
```

```C#
AstarPath.active.AddWorkItem(() => {
    // Safe to update graphs here
    var node = AstarPath.active.GetNearest(transform.position).node;
    node.position = (Int3)transform.position;
});
```

当 nodes 的连接性 connectivity 被修改了，系统自动重新计算 graph 的 connected components。你可以在 Pathfinding.HierarchicalGraph 的文档中获取更多的信息。

然而在 work items sequence 的中间，connectivity 可能不是最新的。如果你使用诸如 Pathfinding.PathUtilities.IsPathPossible 的方法或 Pathfinding.GraphNode.Area 属性，你应当首先调用 ctx.EnsureValidFloodFill 方法。然而通常这不是 work items 需要的（即不需要使用 Pathfinding.PathUtilities.IsPathPossible 和 Pathfinding.GraphNode.Area）

```C#
AstarPath.active.AddWorkItem(new AstarWorkItem((IWorkItemContext ctx) => {
    ctx.EnsureValidFloodFill();

    // The above call guarantees that this method has up to date information about the graph
    if (PathUtilities.IsPathPossible(someNode, someOtherNode)) {
        // Do something
    }
}));
```

如果你修改 walkability，你还需要确保 connections 被正确重新计算。这是对 grid graph 尤其重要。你可以使用 GridGraph.CalculateConnections 方法。注意它需要同时在改变 walkability 的 node 以及相邻的 nodes 上调用，因为他们可能需要改变它们的 connections 来添加和移除到那个 node 的 connection。如果你只更新一些 nodes，你可以使用 GridGraph.CalculateConnectionsForCellAndNeighbours 方法来避免必须迭代 graph 上的所有 nodes 并重新计算他们的 connections。

AddWorkItem 方法还可以以更多高级的方式使用。例如，如果需要，它允许你将计算分散到多个 frames 中：

```C#
AstarPath.active.AddWorkItem(new AstarWorkItem(() => {
    // Called once, right before the
    // first call to the method below
},
        force => {
    // Called every frame until complete.
    // Signal that the work item is
    // complete by returning true.
    // The "force" parameter will
    // be true if the work item is
    // required to complete immediately.
    // In that case this method should
    // block and return true when done.
    return true;
}));
```

## Debugging

一些东西例如 walkability 和 position 可以立即观察到改变。Tags 和 penalties 在 graph 上则不能直接可见。然而有一些 view mode 可以被开启以可视化 tag 和 penalties。

View mode 可以在 A* Inspector > Settings > Debug > Graph Coloring 编辑。如果你设置它为 Tags，所有 tags 将会在 graph 上以不同颜色显示。

![debug_tags](../../Image/debug_tags.png)

你还可以设置它显示 penalties。默认地，它将会自动调整自己使得具有最高 penalty 的 nodes 显示为 pure red，而具有最低 penalty 的 nodes 显示为 green。

![debug_inspector_penalties](../../Image/debug_inspector_penalties.png)

## Technical Details

当 updating 使用 GraphUpdateObject 传递，所有 graphs 将会循环一遍，而那些可以 updated 的（所有内置的）将会调用的 UpdateArea 函数。

Graphs 调用 Pathfinding.GraphUpdateObject.Apply，将每个更新的 node 发送给它， 然后 Apply 函数将会改变 penalty，walkability，或其他指定的参数。

Graphs 还可以使用自定义 update 逻辑，例如 GridGraph。你不必理解所有不同的函数调用才能去使用它，它们几乎是为那些想要理解 source code 人准备的。

### GridGraph Specific details

当更新 grid graphs 时，updatePhysics 变量很重要。如果它设置为 true，所有受影响的 nodes 将会使它们的 height 重新计算，然后检查它们是否仍然 walkable。当更新 gridgraph 时你通常想要它为 true。

当更新 GridGraph 时，GraphUpdateObject 的 Apply 函数（它可以改变 walkability，tags，penalties）将会为 bounds 内的每个 node 调用，它将检查 updatePhysics 变量，如果它为 true（默认），这个区域（bounds）将被扩展为 Collision Testing 设置中的直径，而其中的每个 node 都会被检查 collisions。但是如果为 false，Apply function 只会对区域内（bounds）的 nodes 调用，不会扩展。

### Navmesh based graphs

NavMesh based graphs（NavMeshGraph 和 RecastGraph）只支持更新 penalty，walkability and similar on already existing nodes or for recast graphs，来完全重新计算整个 tiles。不能使用 GraphUpdateObjects 创建新的 nodes（除非重新计算整个 tiles）。GraphUpdateObject 将会影响 bounds 包含的或相交的所有 nodes/triangles。

对于 recast graphs，你还可以使用 navmesh cutting 来更快地更新 graph。

### PointGraphs

Point graphs 会为 bounds 内的每个 node 调用 Apply。如果 GraphUpdateObject.updatePhysics = true，它还会重新计算所有穿越 bounds objects 的所有 connections。

## The Graph Update Object

GraphUpdateObject 包含一如何更新 node 的些基本变量。

### Inheriting from the GraphUpdateObject

可以继承 GraphUpdateObject 来覆盖一些功能。下面是一个例子，它以一个偏移量移动 nodes，同时仍然保持基本功能。

```C#
using UnityEngine;
using Pathfinding;

public class MyGUO : GraphUpdateObject {
    public Vector3 offset = Vector3.up;
    public override void Apply (GraphNode node) {
        // Keep the base functionality
        base.Apply(node);
        // The position of a node is an Int3, so we need to cast the offset
        node.position += (Int3)offset;
    }
}
```

然后你可以这样使用 GraphUpdateObject。

```C#
public void Start () {
    MyGUO guo = new MyGUO();

    guo.offset = Vector3.up*2;
    guo.bounds = new Bounds(Vector3.zero, Vector3.one*10);
    AstarPath.active.UpdateGraphs(guo);
}
```

## Check for blocking placements

塔防游戏中一个场景的事情是确保 player 放置的 towers 不会阻塞出生点到目标的路径。这看起来很难，但幸运的是有 API 可以完成这件事。

Pathfinding.GraphUpdateUtilities.UpdateGraphsNoBlock 方法可以用来先检查给定的 graph update object 是否将会导致两个或更多 points 之间的路径被阻塞。但是它要比正常的 graph update 更慢，因此你可能不想太频繁地调用它。

例如当 player 放置一个 tower 时，你可以实例化它，然后调用 UpdateGraphsNoBlock 方法来检查新放置的 tower 是否会阻塞路径。如果是，则立即移除 tower，并通知 player 选择的位置无效。你可以传递一个 nodes 列表给 UpdateGraphNoBlock 方法，因此你可以不仅确保 start 到 goal 没有被阻塞，还可以确保所有 units 到 goal 没有被阻塞，即它们可以到达目标（如果可以在敌人四处走动时放置 tower）。

```C#
var guo = new GraphUpdateObject(tower.GetComponent<Collider>().bounds);
var spawnPointNode = AstarPath.active.GetNearest(spawnPoint.position).node;
var goalNode = AstarPath.active.GetNearest(goalPoint.position).node;

if (GraphUpdateUtilities.UpdateGraphsNoBlock(guo, spawnPointNode, goalNode, false)) {
    // Valid tower position
    // Since the last parameter (which is called "alwaysRevert") in the method call was false
    // The graph is now updated and the game can just continue
} else {
    // Invalid tower position. It blocks the path between the spawn point and the goal
    // The effect on the graph has been reverted
    Destroy(tower);
}
```
