# Writing Graph Generators


A* Pathfinding Project 中的所有 graphs 都被写为系统的 add-ons。这使得添加自己特殊的 graph 类型相对容易。

这里将展示如何设置一个可以在 A* system 中使用的基本的 Graph Generator。

The complete script can be found here PolarGraphGenerator.cs

## A Basic Graph

最简单的 graph 看起来可能是这样：

```C#
using System.Collections.Generic;
using UnityEngine;
using Pathfinding;
using Pathfinding.Serialization;
using Pathfinding.Util;

// Inherit our new graph from the base graph type
[JsonOptIn]
// Make sure the class is not stripped out when using code stripping (see https://docs.unity3d.com/Manual/ManagedCodeStripping.html)
[Pathfinding.Util.Preserve]
public class SimpleGraph : NavGraph {
    protected override IEnumerable<Progress> ScanInternal () {
        // Here we will place our code for scanning the graph
        yield break;
    }

    public override void GetNodes (System.Action<GraphNode> action) {
        // This method should call the delegate with all nodes in the graph
    }
}
```

这个 graph 并不产生任何 nodes，但是它将会出现在 “Add New Graph” list 中 greyed out。现在让我们开始创建一些 scanning 逻辑。

## Scanning

首先，创建一个包含上面代码的脚本，但是重命名为 PolarGraph 并保存为 PolarGraph.cs.

ScanInterval 方法在 graph 应该给 scan 时将会调用。Scan 方法应该创建大量 nodes，并创建它们之间 connections。我们将会创建一个 Polar Graph，类似一个 grid，但是排列为同心圆而不是 rows。接下来使用 circles 表示同心环的数量，使用 steps 表示每个 circle 中的 nodes 数量。注意在下图中，你看见的是 nodes 之间的连接。Nodes 自己被放置在 line segments 之间的交点上。

![polarGraph](../../../Image/polarGraph.png)

第一步是创建一个临时数组，来保存 nodes，并添加一些变量来配置 graph。我们将会使用 PointNode node 类型，它是被 PointGraph 使用的，因为它基本包含我们想使用的相同的东西。

```C#
public int circles = 10;
public int steps = 20;

public Vector3 center = Vector3.zero;
public float scale = 2;

// Here we will store all nodes in the graph
PointNode[] nodes;

GraphTransform transform;

// Create a single node at the specified position
PointNode CreateNode (Vector3 position) {
    var node = new PointNode(active);
    // Node positions are stored as Int3. We can convert a Vector3 to an Int3 like this
    node.position = (Int3)position;
    return node;
}

public override IEnumerable<Progress> ScanInternal () {
    // Create a 2D array which will contain all nodes
    // This is just a tempoary array to make it easier to reference different nodes
    PointNode[][] circleNodes = new PointNode[circles][];
    yield break;
}
```

## Editor

Graph 还没有出现在 Add New Graph 列表中，因为这需要一个 graph editor，我们现在就来创建它。

创建一个新的脚本，在 AstarPathfindingProject/Editor/GraphEditors/ 或任何其他 editor 目录中。命名其为 PolarGeneratorEditor.cs.

下面是一个非常简单的 polar graph editor。复制这些代码到刚创建的脚本中。之后，你就能够创建这个 graph。

```C#
using UnityEditor;
using Pathfinding;

[CustomGraphEditor(typeof(PolarGraph), "Polar Graph")]
public class PolarGeneratorEditor : GraphEditor {
    // Here goes the GUI
    public override void OnInspectorGUI (NavGraph target) {
        var graph = target as PolarGraph;

        graph.circles = EditorGUILayout.IntField("Circles", graph.circles);
        graph.steps = EditorGUILayout.IntField("Steps", graph.steps);
        graph.scale = EditorGUILayout.FloatField("Scale", graph.scale);
        graph.center = EditorGUILayout.Vector3Field("Center", graph.center);
    }
}
```

CustomGraphInspector 属性告诉系统这个类是一个用于 PolarGraph 的自定义 editor，graph list 中显式的名字将是 Polar Graph。

## Adding nodes

现在我们需要开始实际创建一个 graph。下面的每个 code 片段应该放到 Scan 函数中。

我们将使用一个放置 matrix 以开启 nodes 的 rotation，positioning 等等。

数组中的第一个 array 应该是中心 node，我们将它放在 Vector3.zero. Node positions 被存储为 Int3. Int3 是分量为 int 的 Vector3。

```C#
// Create a 2D array which will contain all nodes
// This is just a tempoary array to make it easier to reference different nodes
PointNode[][] circleNodes = new PointNode[circles][];

// Create a matrix which just moves the nodes to #center
// and scales their positions by #scale
// The GraphTransform class has various utility methods for working with it
transform = new GraphTransform(Matrix4x4.TRS(center, Quaternion.identity, Vector3.one*scale));

// Place the center node in the center
circleNodes[0] = new PointNode[] {
    CreateNode(CalculateNodePosition(0, 0, transform))
};
```

接下来，假设我们在一个给定的 circle 和 angle 上有一个 node。我们需要计算这个 node 的位置。

```C#
static Vector3 CalculateNodePosition (int circle, float angle, GraphTransform transform) {
    // Get the direction towards the node from the center
    var pos = new Vector3(Mathf.Sin(angle), 0, Mathf.Cos(angle));

    // Multiply it with the circle number to get the node position in graph space
    pos *= circle;

    // Multiply it with the matrix to get the node position in world space
    pos = transform.Transform(pos);
    return pos;
}
```

接下来，我们设置剩下的 graph，一个 circle 一个 circle，一个 node 一个 node。

```C#
// The size of the angle (in radians) each step will use
float anglesPerStep = (2*Mathf.PI)/steps;

for (int circle = 1; circle < circles; circle++) {
    circleNodes[circle] = new PointNode[steps];
    for (int step = 0; step < steps; step++) {
        // Get the angle to the node relative to the center
        float angle = step * anglesPerStep;

        Vector3 pos = CalculateNodePosition(circle, angle, transform);
        circleNodes[circle][step] = CreateNode(pos);
    }
}
```

现在我们已经设置了所有 nodes 到它们的正确位置，但是它们之间没有 connections。因此，我们来添加连接。

```C#
// Iterate through all circles
// circle 0 is just the center node so we skip that for now
for (int circle = 1; circle < circles; circle++) {
    for (int step = 0; step < steps; step++) {
        // Get the current node
        PointNode node = circleNodes[circle][step];

        // The nodes here will always have exactly four connections, like a grid, but polar.
        // Except for those in the last circle which will only have three connections
        int numConnections = circle < circles-1 ? 4 : 3;
        var connections = new Connection[numConnections];

        // Get the next clockwise node in the current circle.
        // The last node in each circle should be linked to the first node
        // in the circle which is why we use the modulo operator.
        connections[0].node = circleNodes[circle][(step+1) % steps];

        // Counter clockwise node. Here we check for underflow instead
        connections[1].node = circleNodes[circle][(step-1+steps) % steps];

        // The node in the previous circle (in towards the center)
        if (circle > 1) {
            connections[2].node = circleNodes[circle-1][step];
        } else {
            // Create a connection to the middle node, special case
            connections[2].node = circleNodes[circle-1][0];
        }

        // Are there any more circles outside this one?
        if (numConnections == 4) {
            // The node in the next circle (out from the center)
            connections[3].node = circleNodes[circle+1][step];
        }

        for (int q = 0; q < connections.Length; q++) {
            // Node.position is an Int3, here we get the cost of moving between the two positions
            connections[q].cost = (uint)(node.position-connections[q].node.position).costMagnitude;
        }

        node.connections = connections;
    }
}
```

第一个 node 是一个特殊情况。它具有到第一个 circle 上所有 nodes 的 connections。

```C#
// The center node is a special case, so we have to deal with it separately
PointNode centerNode = circleNodes[0][0];
centerNode.connections = new Connection[steps];

// Assign all nodes in the first circle as connections to the center node
for (int step = 0; step < steps; step++) {
    centerNode.connections[step] = new Connection(
        circleNodes[1][step],
        // centerNode.position is an Int3, here we get the cost of moving between the two positions
        (uint)(centerNode.position-circleNodes[1][step].position).costMagnitude
        );
}
```

Now the only thing left to do, is to make the nodes walkable, the default value is unwalkable. This tutorial will not cover the checking for obstacles or similar, but if you read up on Unity's Physics class you should be able to get that working.

现在唯一剩下的事情是，使 nodes 成为 walkable，默认值是 unwalkable。这里不会覆盖检查 obstacles 之类的事情，但是如果你熟悉 Unity Physics class 就可以轻松完成。

```C#
// Store all nodes in the nodes array
List<PointNode> allNodes = new List<PointNode>();
for (int i = 0; i < circleNodes.Length; i++) {
    allNodes.AddRange(circleNodes[i]);
}
nodes = allNodes.ToArray();

// Set all the nodes to be walkable
for (int i = 0; i < nodes.Length; i++) {
    nodes[i].Walkable = true;
}
```

如果你已经放置前面所有 snippets 到 Scan function 中，你就拥有了一个可以工作的 scan function。

最终要能够 scan graph，需要实现 GetNodes 方法。因为所有 nodes 被存储在一个数组中，这非常简单。

```C#
public override void GetNodes (System.Action<GraphNode> action) {
    if (nodes == null) return;

    for (int i = 0; i < nodes.Length; i++) {
        // Call the delegate
        action(nodes[i]);
    }
}
```

现在你应该可以创建这个 graph，编辑参数，并且如果你点击 Scan，这个 graph 将会出现在 Scene View 中。Cool！

然而，如果你取消选择 inspector 并重新选择它，你的 setting 并没有被保存。

这是因为我们需要添加一个最后的东西，序列化。

所有 graph 设置被序列化到 JSON 中。对于要序列化的字段，我们必须添加一个属性到它上面。JsonMemeber 属性会告诉 serializer 我们想要序列化这个字段。

The complete script can be found here PolarGraphGenerator.cs

## More Stuff

更多的方法可以被覆盖来定制其他功能。尤其是 Getnearest 和 GetnearestForce 方法。这控制着到一个 point 的最近 node 如何被发现。有一个默认实现，但是它会搜索 graph 中的所有 nodes，如果 graph 中包含很多 nodes，这将会很慢。如果你想要区别默认实现绘制 graph，你还可以覆盖 OnDrawGizmos 方法。

如果你需要序列化更多信息，你可以覆盖 SerializeExtraInfo，DeserializeExtraInfo，还有如果你需要在 nodes 被加载之后设置 nodes，你可以覆盖 PostDeserialization 函数。

## The End

你现在应该能够像其他 graph 一样使用 graph。

