# Graph Updates during Runtime

## Overview

有时需要在运行时更新 graph。例如 player 构造了一个新的建筑，或者一扇关着的门被打开了。 Graphs 可以完全重新计算或者部分更新。如果改变了整个地图，最好完全重新计算，但是对于局部很小的更新，只更新部分 graph 则快得多。

完全重新计算所有 graphs 或者其中几个：

```C#
// Recalculate all graphs
AstarPath.active.Scan();

// Recalculate only the first grid graph
var graphToScan = AstarPath.active.data.gridGraph;
AstarPath.active.Scan(graphToScan);
```

还可以异步重新计算 graphs。这不保证很好的帧率，但是至少可以显示一个 loading screen。

```C#
public IEnumerator ScanGraphs () {
    foreach (var progress in AstarPath.active.ScanAsync()) {
        yield return null;
    }
}
```

小的 graph updates 可以通过使用 GraphUpdateScene 组件（可以在 Unity Inspector 中编辑）完成，也可以使用脚本（使用一个 Bounds 或者 Pathfinding.GraphUpdateObject 调用 AstarPath 的方法）完成。GraphUpdateScene 组件幕后实际就是使用 GraphUpdateObject 来更新 map 的。

```C#
AstarPath.active.UpdateGraphs (myBounds);
AstarPath.active.UpdateGraphs (myGraphUpdateObject);
```
这个方法会在 queue 中放置一个任务，并在下一个 path 计算之前完成计算。它必须放在 queue 中，因为如果直接执行，可能干扰 pathfinding，尤其是启动多线程的情况下可能导致各种错误。这意味着，可能不能立即看到 graph 的更新，但是它总是在下一个 pathfinding 开始前被更新。

Recast graphs 还可以使用 navmesh cuting 进行伪更新。NavMesh cutting 可以在 navmesh 上伪 obstacles 切出一个洞，但是不能为 navmesh 添加更多 surface。这更快，但是比重新计算整个 recast tile 更受限.

如果工作在 Unity Editor 中已知的 graph 上，使用 GraphUpdateScene 组件通常是最简单的。例如，你可以很容易地改变一块特定区域的 tag，而不需任何编码。但是如果要在运行时动态进行这些操作，使用 code 更容易。例如在塔防游戏中，动态更新地图来适应新放置的建筑。

## What to update

graphs 更新的通常是两种东西:

- 可能使用相同的设置重新计算 graph，但是如果只在很小的区域内更新 graph，重新计算整个 graph（使用 AstarPath.Scan）会很浪费。例如在塔防游戏中，player 只放置了一个新塔（改变结构）
- 或者想在现有 graph 上改变设置，例如可能想要更新某些 nodes 的 tag 或 penalty（改变设置：tag，penalty）

对于除了 NavMeshGraph 之外的所有 graph，可以使用 graph 开始生成时使用的设置以相同的方式重新计算 graph 的一小部分（NavMeshGraph 通常只有完成重新计算才有意义）。为此可以使用 scripting 或者 GraphUpdateScene 组件并设置 updatePhysics 为 true。updatePhysics 可能不是描述的很准确，但是保持为 true。

Grid graphs 会像预期那样工作，你可以指定 bounds，它会更新所有东西。但是它重新计算的区域可能比你指定的略大一些，以确保将一些向外延伸的侵蚀也算在内。

Recast graphs 每次只能重新计算一个完整的 tile。因此当生成一个更新请求时，bounds 接触的 tiles 都会完全重新计算。因此最后使用小一点的 tile 以避免大量的重计算时间。但是不要太小，因为否则它将退化成 grid graph。如果使用多线程，tile 重计算的很大一部分会分散到单独的线程以避免影响 fps。

Point graphs 会重新计算通过 bounds 的所有 connections。但是它不会考虑作为 GameObjects 新添加进的 nodes。为此需要使用 AstarPath.Scan。

如果想要改变现有 graph 上的属性，有很多东西可以修改。

可以改变 nodes 的 tags。这可以用于允许一些 units 穿越一些 region，而阻止另一些 units。

可以改变 nodes 的 penalty。这可以让一些 nodes 比其他 nodes 更难更慢地通过，使得 agent 更青睐其他的 path。但是有一些限制。不能指定负数的 penalties，因为算法不能处理这种情景。但是一个场常见的技巧是设置一个很大的初始 penalty（可以在 graph settings 中设置），然后修改一些 nodes 为更小的 penalties。但是这会使得 pathfinding 总体更慢，因为系统要搜索更多的 nodes。需要的 penalty 相当高。尽管没有实际的 penalty 单位，但是值为 1000 的 penalty 大约对应穿越一个世界单位的距离。

还可以直接修改 nodes 的 walkability。因此可以使得一个 bounds 内的所有 nodes 全部 walkable 或全部 unwalkable。

GraphUpdateScene 组件 settings 几乎一对一映射 GraphUpdateObject，后者用来在脚本中动态更新 graphs。因此建议学习一下 GraphUpdateScene 组件，即使打算只使用脚本更新 graph。

## Using Scripting

要更新 graph，创建一个 GraphUpdateObject 并设置想要的参数，然后调用 AstarPath.UpdateGraphs 方法来 queue 这个更新。

```C#
// using Pathfinding; //At top of script
var guo = new GraphUpdateObject(myBounds);
// Set some settings
guo.updatePhysics = true;
AstarPath.active.UpdateGraphs (guo);
```

myBounds 变量引用一个 UnityEngine.Bounds 对象。它定义一个 axis aligned box，里面的 graphs 是要被更新的区域。通常会想要更新新创建的 object 周围的 graph。如果这个 object 有一个 collider，可以很容易指定 bounds：

```C#
var guo = new GraphUpdateObject(GetComponent<Collider>().bounds); 
```

但是要注意确保这个 object 被 graph 识别。对于 grid graph，应该确保 object 的 layer 被包含在 collision testing mask 或者 height testing mask。

如果不需要重新计算 nodes（使用 grid graph）或 connections（使用 point graph）上的所有参数，可以设置 updatePHysics 为 false，来避免不需要的计算。

## Using direct access to graph data

一些情况下，使用 GraphUpdateObject 更新 graph 不是很方便。此时，可以直接更新 graph data。但是注意，使用 GraphUpdateObject 时，系统为你考虑了很多事情。

Graph data 必须只有在它安全的情况下才能被修改。Pathfinding 可能在任何时候运行，因此需要首先暂停 pathfinding 线程，然后在更新数据。最简单的方式是使用 AstarPath.RegisterSSafeUpdate，但是使用 AstarPath.AddWorkItem 更灵活，并且性能更好。

```C#
AstarPath.RegisterSafeUpdate (() => {
    // Safe to modify graph data here
});
```
有一些事项需要注意，以确保改变 graph data 后，pathfinding data 是最新的。如果改变了 walkability 或者任何 node 的 connections，必须调用 AstarPath.FloodFill 以重新计算哪些节点可以从哪些节点到达（这用于快速决定一个 path 是否可行）。

如果改变了 walkability，还需要确保 connections 被正确地重新计算。这对用 grid graph 最为重要。可以使用 GridGraph.CalculateConnections 方法。注意这需要在改变了 walkability 的 nodes 和它们的相邻节点上都调用。因为它们可能必须改变它们的 connections 来添加或移除 node。

要得到安全的 callback 来修改 graph data，可以使用 AddWorkItem 方法，而不是 RegisterSafeUpdate 方法。它允许将计算分配到多个 frames 中，并且允许 batch FloodFill 调用，使得多个 graph updates 不必每次运行一下 FloodFill。这可以通过 AstarPath.QueueWorkItemFloodFill 方法完成。FloodFill 会在所有 work items 完成后完成。

```C#
AstarPath.AddWorkItem (new AstarPath.AstarWorkItem (
() => {
    // 调用一次，就在下面方法第一次调用开始之前
},
force => {
    // 每帧调用一次，直到完成。通过返回 true 通知 work item 完成。
    // 即这个 work item 可以在多帧完成，如果当前一帧的计算没有完成，返回 false。最后一帧返回 true。
    // 如果 work item 需要立即完成，force 参数必须为 true。这样这个方法将会阻塞并在完成时返回 true。
    return true;
}
));
```

## Viewing the results of updates

walkability 和 position 这些属性改变后立即可见，但是 tags 和 penalties 则不能。但是有一些其他 view mode 可以开启来查看 tags 和 penalties。

The viewing mode can be edited at A* Inspector -> Settings -> Debug -> Path Debug Mode. If you set it to "Tags" all tags will be visible as different colors on the graph.

You can also set it to show penalties. By default it will automatically adjust itself so that the node(s) with the highest penalty will show up as pure red and the node(s) with the lowest penalty will show up as green.

## Technical Details

当使用 GraphUpdateObject 来更新时，所有的 graphs 都会被循环，那些可以被更新的（所有内置的 graph 类型）都会调用它们的 UpdateArea 函数。

graphs 调用 Pathfinding.GraphUpdateObject.Apply 到每个受影响的 node 来更新 nodes，Apply 函数然后回改变 penalty，walkability，以及其他指定的参数。Graphs 还可以使用自定义更新 logic。不需要理解所有不同的函数调用才能使用它，那些都是用来给想要修改源代码的人使用的。

### GridGraph specific details

当更新 grid graphs 时，udpatePhysics 变量很重要。所有受影响的 nodes 会重新计算它们的高度，然后检查它们是否仍然可以通过。当更新 grid graph 时，通常将这个选项保留为 true。

当更新一个 GridGraph 时，GraphUpdateObject 的 Apply 函数（改变 walkability，tags，和 penalties）会为 bounds 内的每个 node 调用，它会检查 updatePhysics 变量，如果为 true（默认值），这个 area 会以 Collision Testing settings 中指定的直径扩展，扩展后的区域内的每个 node 都会检查 collisions。如果为 false，只会为指定区域内的 nodes 调用 Apply 函数，不会扩展并检查。

### Navmesh based graphs

基于 NavMesh 的 graphs（NavMeshGraph 和 RecastGraph）只支持在现有 nodes 上更新 penalty，walkability 和 similiar，或者 recast graphs 来完全重新计算 tiles。不能使用 GraphUpdateObject 来创建新 nodes（除非重新计算全部 tiles）。GraphUpdateObject 会影响包含在 GUO bounds 内或与之相交的全部 nodes/triangles。

对于 recast graphs，还可以使用 navmesh cutting 来快速更新 graph。

### PointGraphs

Point graphs 会在 bounds 内的每个 node 上调用 Apply。如果 GraphUpdateObject.updatePhysics 设置为 true，它会重新计算全部（穿越 bounds object）的 connections。

## The Graph Update Object

GraphUpdateObject 包含一些关于如何更新每个 node 的基本变量，例如 bounds，

### Inheriting from the GraphUpdateObject

可以继承 GraphUpdateObject 来覆盖一些功能。

Here's an example of a GraphUpdateObject which moves nodes by some offset while still keeping the base functionality.

```C#
using Pathfinding;
public class MyGUO : GraphUpdateObject {
    public Vector3 offset = Vector3.up;
    public override void Apply (Node node) {
        // Keep the base functionality
        base.Apply (node);
        // The position of a node is an Int3, so we need to cast the offset
        node.position += (Int3)offset;
    }
}
```

You could then use that GUO like this:

```C#
 public void Start () {
    MyGUO guo = new MyGUO ();
    guo.offset = Vector3.up*2;
    guo.bounds = new Bounds (Vector3.zero,Vector3.one*10);
    AstarPath.active.UpdateGraphs (guo);
}
```

## Check for blocking placements

塔防游戏一个常见需求时确保玩家放置的 tower 不会阻塞出生点和 goal 之间的 path。

Pathfinding.GraphUpdateUtilities.UpdateGraphsNoBlock 方法可以用来检查一个给定的 graph update object 是否会导致两个或更多的 points 之间变成阻塞的。但是这比通常的 graph update 要慢，因此不要过于频繁地使用它。

例如当玩家放置一个 tower 时，可以实例化它，然后调用 UpdateGraphsNoBlock 方法来检查新放置的 tower 是否会阻塞 path。如果是，则立即移除 tower，然后通知 player 选择的位置无效。可以传递一个 nodes 的列表给 UpdateGraphsNoBlock 方法，这样可以确保不仅从 start 到 goal 之间的 path 没有阻塞，还能确保所有 units 仍然可以到达 goal。

```C#
var guo = new GraphUpdateObject (tower.GetComponent<Collider>.bounds);
var spawnPointNode = AstarPath.active.GetNearest (spawnPoint.position).node;
var goalNode = AstarPath.active.GetNearest (goalNode.position).node;
if (GraphUpdateUtilities.UpdateGraphsNoBlock (guo, spawnPointNode, goalNode, false)) {
    // Valid tower position
    // Since the last parameter (which is called "alwaysRevert") in the method call was false
    // The graph is now updated and the game can just continue
} else {
    // Invalid tower position. It blocks the path between the spawn point and the goal
    // The effect on the graph has been reverted
    Destroy (tower);
}
```
