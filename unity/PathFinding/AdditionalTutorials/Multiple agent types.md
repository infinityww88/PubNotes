# Multiple agent types

如何处理不同类型的 agent，例如不同 size 的 agents。

当你有不同 size 的 agents，它们通常不能使用相同的 routes 到 target（比如 recast graphs，一个 door 可以允许 height 1 agent 通过，但不能使 height 2 agent 通过）。幸运的是，可以很容地解决这个问题。最简单的方式是创建多个 graphs，每个 agent 类型一个。如果你有很多不同的 agent 类型，或者甚至一个连续的光谱，你可能想要将它们组合到一起，因为拥有大量的 graphs 将会增加内存使用，而且 scanning 将会花费更长时间。在 Seeker 组件上，可以设置 Seeker 可以使用哪些 graphs。

## Example

比如说我们有两个 agents：

![agents](../../Image/agents.png)

在 AstarPath inspector 中，则我们可以创建两个不同的 graphs，唯一的区别是 graphs 使用的 character radus（当然如果必要也可能是任何其他参数）。在这个例子中，使用了一个 recast graph（不同的 agent 可能具有不同的通过的高度），但是这对其他 graph type 也可以很容易完成。

![small_graph](../../Image/small_graph.png)

当 scanning 这些 graphs，我们将可以获得一个 result，看起来像下面这样。用于较小的 agent 蓝色 graph，和用于较大 agent 的紫色 graph。

![graph_visualization](../../Image/graph_visualization.png)

在 Seeker component 上，则我们可以设置每个 agent 应该使用哪个 graph。

![seeker](../../Image/seeker.png)

现在两个 agent 都会使用适合它们大小的 graphs。

## Other approaches for grid graphs

作为 grid graphs 上的一个代替方法，可以使 graph 根据到最近的 obstacle 的距离生成不同的 tags。这只需要一个 graph。

还有另一个非常灵活的方法，但是不幸的是，它需要一个很高的计算代价。对于一个 path 请求，可以提供一个 ITraversalProvider 对象，它允许代码精确地确定哪些 nodes 不应该被穿越。使用这种方法，我们可以添加自定义代码，相比于仅仅检查当前 node 是否可以通过，我们还可以检查它周围的所有 nodes，例如一个 3x3 方块或 5x5 方块（默认等价为 1x1 方块）。

下面的图片中，你可看到它使用 3x3 方块。注意它不想穿过它右边的挨着 obstacles 的 nodes，尽管它们是 walkable 的，因为它检查周围的 3x3 方块。

![grid_shape_traversal](../../Image/grid_shape_traversal.png)

ITraversalProvider 方法的主要优势是它可以处理可以使一个 node 不可通过的所有事情。例如你可能使用不同的 tags 来限制 agent 移动，然而即使你使用多个 graphs 不同的 agents 由于他们的 tag 仍然能够走到 not traversable 的区域，尽管 agent 有一个很大的 size。

**ITraversalProvider == A* 算法中的启发函数?**

The ITraversalProvider can be implemented like this:

```C#
class GridShapeTraversalProvider : ITraversalProvider {
    Int2[] shape;

    public static GridShapeTraversalProvider SquareShape (int width) {
        if ((width % 2) != 1) throw new System.ArgumentException("only odd widths are supported");
        var shape = new GridShapeTraversalProvider();
        shape.shape = new Int2[width*width];

        // Create an array containing all integer points within a width*width square
        int i = 0;
        for (int x = -width/2; x <= width/2; x++) {
            for (int z = -width/2; z <= width/2; z++) {
                shape.shape[i] = new Int2(x, z);
                i++;
            }
        }
        return shape;
    }

    public bool CanTraverse (Path path, GraphNode node) {
        GridNodeBase gridNode = node as GridNodeBase;

        // Don't do anything special for non-grid nodes
        if (gridNode == null) return DefaultITraversalProvider.CanTraverse(path, node);
        int x0 = gridNode.XCoordinateInGrid;
        int z0 = gridNode.ZCoordinateInGrid;
        var grid = gridNode.Graph as GridGraph;

        // Iterate through all the nodes in the shape around the current node
        // and check if those nodes are also traversable.
        for (int i = 0; i < shape.Length; i++) {
            var inShapeNode = grid.GetNode(x0 + shape[i].x, z0 + shape[i].y);
            if (inShapeNode == null || !DefaultITraversalProvider.CanTraverse(path, inShapeNode)) return false;
        }
        return true;
    }

    public uint GetTraversalCost (Path path, GraphNode node) {
        // Use the default traversal cost.
        // Optionally this could be modified to e.g taking the average of the costs inside the shape.
        return DefaultITraversalProvider.GetTraversalCost(path, node);
    }
}
```

Note

    This implementation only works for grid graphs, not layered grid graphs

然后可以这样使用：

```C#
ABPath path = ABPath.Construct(currentPosition, destination, null);

path.traversalProvider = GridShapeTraversalProvider.SquareShape(3);

// If you are writing your own movement script
seeker.StartPath(path);

// If you are using an existing movement script (you may also want to set ai.canSearch to false)
// ai.SetPath(path);
```

Note that a drawback with both of the grid specific approaches is that if you happen to try to request a path to a destination that cannot be reached, then the path will fail completely instead of making the AI move to the closest point it could get. You can solve this for some cases by setting the calculatePartial field to true before you start calculating the path:

注意，这个两种 grid 特定方式的一个缺点是，如果你恰好遇到尝试请求一个到不能到达的目的地的路径，则 path 将会完全失败，而不是使 AI 移动到它能够到达的最近 point。你可以通过在开始计算 path 之前设置 calculatePartical 字段为 true 来解决这个问题。

```C#
path.calculatePartial = true;
```

这将会使它走到最近的 node，只要根据 ITraversalProvider， target node 是一个 traversable node 就行。

