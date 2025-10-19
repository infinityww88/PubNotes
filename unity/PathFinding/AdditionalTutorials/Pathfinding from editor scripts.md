# Pathfinding from editor scripts

如何在 play mode 之外使用 pathfinding，例如 editor script。

Editor mode 中的 Pathfinding 和 play mode 中的工作完全一样，唯一主要的区别是 path 请求是同步的，比如说它们会立即计算。通常 path 请求时异步的，需要花费多个 frames 来计算。

但是要使它工作，你必须首先初始化 pathfinding system，因为在 editor mode，graphs 可能没有被反序列化，并且 graphs 可能没有被 scanned。AstarPath.FindAstarPath 方法将会确保 AstarPath.active 属性被设置，并且所有 graphs 已经被反序列化（它们在内部被存储为 byte 数组）。

```C#
// Make sure the AstarPath object has been loaded
AstarPath.FindAstarPath();

AstarPath.active.Scan();
```

如果你认为你个 graph 可能已经被 scanned，但是你不确定，则你可以先检查一下。一个很好的指示时这个 graph 是否有任何 nodes。

```C#
// Check if the first grid graph in the scene has any nodes
// if it doesn't then it is not scanned.
if (AstarPath.active.data.gridGraph.nodes == null) AstarPath.active.Scan();
```

在此之后，你可以像往常一样请求 paths。下面的例子直接使用 AstarPath 组件，但是使用一个 Seeker 组件应该可以。

```C#
ABPath path = ABPath.Construct(transform.position, target.position);
AstarPath.StartPath(path);
// Everything is synchronous so the path is calculated now

Debug.Log("Found a path with " + path.vectorPath.Count + " points. The error log says: " + path.errorLog);

// Draw the path in the scene view
for (int i = 0; i < path.vectorPath.Count - 1; i++) {
    Debug.DrawLine(path.vectorPath[i], path.vectorPath[i+1], Color.red);
}
```
