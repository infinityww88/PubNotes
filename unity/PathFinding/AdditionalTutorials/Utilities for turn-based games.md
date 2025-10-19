# Utilities for turn-based games

## Introduction

回合制游戏经常需要对 units 可以穿越哪些 nodes 以及穿越那些 nodes 的 cost 有更精细的控制，不同的 units 之间可能不同。另一方面，最大化 pathfinding 性能并不总是需要，因为几乎任何时间中，大多数单位都是静止的。

可以在每一个 path request 之前为 nodes 更新所有 movement costs 和类似属性，但是这不是非常干净的解决方案，因此 package 为此提供了其他的一些方法。

如果你需要更多控制，你可以看一下 ITraversalProvider 章节。

## Blocking nodes

最常见的情形是想要阻塞一些单位穿越特定 nodes，但是允许另一些单位。例如在回合制游戏中，通常想要阻止多个单位站在同一个 tile 上，但是一个 unit 明显不应该被自己阻塞。

为此，提供了 BlockManager 组件和随之的 SingleNodeBlock 组件。SingleNodeBlocker 本意用作 blocking 特定 nodes 的简易方法，而每个 SingleNodeBlock 精确 blocks 一个 node。BlockManager 组件将会保持对所有 SingleNodeBlocker 组件的追踪，并允许创建 TraversalProvider 实例，它们可以用在 paths 中来指定额外被阻塞的 nodes。

这里我们将创建一个新的 scene 和一些 scripts 来测试 API。

- 在你的 project 中创建并保存一个新的 scene，命名为 TrunBasedTest
- 添加一个 GameObject，命名为 BlockManager
- 为 BlockManager GameObject 上添加 BlockManager 组件
- 添加一个 sphere 并放置到 （1.5， 0， 2.5）。这会将它放置在一个 node 的中心
- 为 sphere 添加 SingleNodeBlock 脚本
- 将 BlockManager 赋予 SingleNodeBlocker 组件的 “manager” 字段
- 确保删除了 sphere 上的 collider，否则 sphere 将会被检测为 obstacle，而我们想要使用 SingleNodeBlocker for that
- 创建另一个 GameObject，命名为 A*，然后添加 AstarPath 组件到上面 (Menu > Pathfinding > Pathfinder)
- 添加一个很大的 plane 到 scene 中，只是用来表示 ground
- 添加一个 Grid Graph 到 AstarPath 组件，并设置 “Unwalkable when no ground” 为 false
- 如果点击 Scan button，你应该看见一个带有一个 sphere 的很小的 empty grid。注意这个 sphere 自己不阻塞 graph 中的任何 node

![grid_with_sphere](../../Image/grid_with_sphere.png)

![part1_inspector](../../Image/part1_inspector.png)

现在我们想要 SingleNodeBlocker 来实际阻塞一些位置，因此创建一个新的 C# 脚本，命名为 BlockerTest.cs，并添加下面的代码：

```C#
using UnityEngine;
using System.Collections;
using Pathfinding;

public class BlockerTest : MonoBehaviour {
    public void Start () {
        var blocker = GetComponent<SingleNodeBlocker>();

        blocker.BlockAtCurrentPosition();
    }
}
```

添加新 script 到 sphere。当游戏开始时，这个脚本使 SingleNodeBlocker 组件告诉 BlockManager 它现在占据那个 object 位置身上的 node。然而这还不够，因为没有 path 知道一个 node 以及被阻塞了。

要实际计算一个 path，我们将创建一个新的脚本，称为 “BlockPathTest.cs”，其包含下面的 code：

```C#
using UnityEngine;
using System.Collections.Generic;
using Pathfinding;

public class BlockerPathTest : MonoBehaviour {
    public BlockManager blockManager;
    public List<SingleNodeBlocker> obstacles;
    public Transform target;

    BlockManager.TraversalProvider traversalProvider;

    public void Start () {
        // Create a traversal provider which says that a path should be blocked by all the SingleNodeBlockers in the obstacles array
        traversalProvider = new BlockManager.TraversalProvider(blockManager, BlockManager.BlockMode.OnlySelector, obstacles);
    }

    public void Update () {
        // Create a new Path object
        var path = ABPath.Construct(transform.position, target.position, null);

        // Make the path use a specific traversal provider
        path.traversalProvider = traversalProvider;

        // Calculate the path synchronously
        AstarPath.StartPath(path);
        path.BlockUntilCalculated();

        if (path.error) {
            Debug.Log("No path was found");
        } else {
            Debug.Log("A path was found with " + path.vectorPath.Count + " nodes");

            // Draw the path in the scene view
            for (int i = 0; i < path.vectorPath.Count - 1; i++) {
                Debug.DrawLine(path.vectorPath[i], path.vectorPath[i + 1], Color.red);
            }
        }
    }
}
```

这个脚本将会每帧计算一个从它自己的位置到目标位置的路径，同时使用创建的 TraversalProvider 使路径避开指定 list 中的任何 obstacles。

BlockManager.TraversalProvider 有两个 modes：AllExceptSelector 和 OnSelector。如果设置 AllExceptSelector，则所有被 SingleNodeBlocker 阻塞的 nodes 将会被当做 unwalkable，除了指定的 list 中的那些。这可以用于如果你想要一个 unit 避开所有单位除了它自身，或者你可能想要它避开所有它自己 team 的 units 而不是对手的。如果设置 OnlySelector，则所有被 list 中的的 SingleNodeBlocks 阻塞的 nodes 都被当做 unwalkable。出于性能原因，尽可能保持 selector list 相对小。

- 创建一个新 GameObject，命名为 Target，并放置在 (3.5, 0, 3.5)
- 创建一个 GameObject 命名为 “Path Searcher”，并添加一个新的 BlockerPathTest 组件
- 将这个 object 移动到 (-2.5, 0. 3.5) 并赋值 “Block Manager” 和 “Target” 字段。

现在点击 play，应该可以看见一条红色的线从 “Path Searcher” 到 “Target”。注意它穿越了 sphere 就好像它不存在一样。这是因为我们还没有添加它到 searcher 上的 Obstacles list。

如果你停止 game，然后添加 sphere 的 SingleNodeBlocker 组件到 obstacles list，然后点击 play，就会看见红线避开了 sphere。

现在我们可以很容易地扩展这个例子，创建很多 red spheres，和很多 blue spheres，创建两个 searcher，一个只将 blue sphere 考虑为 obstacles，一个只将 red sphere 考虑为 obstacles。

## ITraversalProvider

上面的系统用于简单的情形，并且很容易使用。但是对于更复杂的例子，使用 ITraversalProvider interface 更好。任何 Path 可以被赋予一个 traversalProvider，它有两个方法：

```C#
bool CanTraverse (Path path, GraphNode node);
uint GetTraversalCost (Path path, GraphNode node);
```

根据 unit 是否应该穿越那个 node，CanTraverse 方法应该只返回 true 或 false。GetTraversalCost 方法应该返回穿越那个 node 的额外 cost。默认地，如果没有 tags 或 penalties 被使用，则 traversal cost 是 0。一个 1000 的 cost 差不多对应移动一个世界单位的 cost。

作为参考，默认实现将是：

```C#
public class MyCustomTraversalProvider : ITraversalProvider {
    public bool CanTraverse (Path path, GraphNode node) {
        // Make sure that the node is walkable and that the 'enabledTags' bitmask
        // includes the node's tag.
        return node.Walkable && (path.enabledTags >> (int)node.Tag & 0x1) != 0;
        // alternatively:
        // return DefaultITraversalProvider.CanTraverse(path, node);
    }

    public uint GetTraversalCost (Path path, GraphNode node) {
        // The traversal cost is the sum of the penalty of the node's tag and the node's penalty
        return path.GetTagPenalty((int)node.Tag) + node.Penalty;
        // alternatively:
        // return DefaultITraversalProvider.GetTraversalCost(path, node);
    }
}
```

通过实现一个自定义 ITraversalProvider，你可以任意按照自己游戏的需求来改变 penalties。注意 grid graph 出于性能原因，移除所有到 unwalkable nodes connections。因此即使你在 traversal provider 中移除 “node.Walkable &&“ 部分，grid graphs 的 path 还是不会穿越 unwalkable nodes（没有 connections）。你只可以使 nodes unwalkable，不能是 unwalkable nodes 重新 walkable。

Warning

    如果开启多线程，ITraversalProvider 方法将会在一个单独的线程中调用。这意味着你不能使用任何 Unity API（除了 math 等独立的 API），并且你需要使你的 code 是线程安全的。

当你实现一个 ITraversalProvider，你可以将它赋予一个 path，就像上面一样。

```C#
var path = ABPath.Construct(...);
path.traversalProvider = new MyCustomTraversalProvider();
```
