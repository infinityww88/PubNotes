# Writing Modifiers

Modifiers 是 post-process paths 的小脚本，例如简化它们，或者平滑它们。

它们使用可扩展的 add-on 架构构建在系统中，这意味着添加你自己的 modifier 很容易。

这里编写一个和内置的 SimpleSmooth 类似的 simple path smoother modifier。

## New Script

创建一个新的 C# 脚本，命名为 ModifierTutorial.cs。

现在我们将要制作一个 modifier，它可以挂载到任何具有 Seeker 的 GameObject。为此我们需要从 MonoModifier 继承。

这个 class 将会处理 Seeker 和 Modifier 之间的基本通信，并且可以非常好地帮助编写这个 modifier。
它是一个抽象类，因此一些函数需要在我们的 modifier 中实现。

```C#
using UnityEngine;
using System.Collections;
using Pathfinding;

public class ModifierTutorial : MonoModifier {
    public override int Order { get { return 60; } }
    public override void Apply (Path p) {
    }
}
```

现在我们拥有了最基本的 modifier，它实际上不做任何事情，但是它将作为之后编写 modifiers 的模板。

这里已经添加了 using Pathfinding 语句，因为 MonoModifier 存在于 Pathfinding 命名空间中。

还有一个 Order 属性，它决定相对于其他 modifiers，这个 modifier 将被调用的顺序。越高的值越晚被调用。内置的 modifiers 使用 0-50 范围内的值，因此我们设置这个 modifier 的顺序为 60，这样它将在所有内置 modifiers 之后被执行。

Apply 函数是我们将要放置 code 的地方，它将在 path 需要 post-processing 时被调用。

提供的 Path object 是我们将要 post-process 的 path。

## Smoothing

我们将要使用的算法是相当简单的，它应该只绘制一定程度靠近在一起的 points，而我们将要操作 Pathfinding.Path.vectorPath 数组，Pathfinding.Path.path 数组应该从不改变，因为这可能破坏其他 modifier。

尽管首先我们需要检查 path 是否成功，以及 vectorPath 数组是否不是 null，否则可能遇到 NullReferenceExceptions。

还有，我们如何 smooth 这个 path，如果它只包含一个 single segment。此时我们将会跳过这种情况。

```C#
public override void Apply (Path path) {
    if (path.error || path.vectorPath == null || path.vectorPath.Count <= 2) {
        return;
    }
```

然后对于实际 smoothing，算法将会工作如下：

Subdivide path 为更小的 segments，然后循环整个 path array，然后移动每一个 point 除了第一个和最后一个，到它的相邻的 points，重复多次，知道 path 足够平滑。

```C#
public int iterations = 5;

public int subdivisions = 2;

public override void Apply (Path path) {
    if (path.error || path.vectorPath == null || path.vectorPath.Count <= 2) {
        return;
    }
    // Subdivisions should not be less than zero
    subdivisions = Mathf.Max(subdivisions, 0);

    // Prevent unknowing users from entering bad values
    if (subdivisions > 12) {
        Debug.LogWarning("Subdividing a path more than 12 times is quite a lot, it might cause memory problems and it will certainly slow the game down.\n" +
            "When this message is logged, no smoothing will be applied");
        subdivisions = 12;
        return;
    }

    // Create a new list to hold the smoothed path
    List<Vector3> newPath = new List<Vector3>();
    List<Vector3> originalPath = path.vectorPath;

    // One segment (line) in the original array will be subdivided to this number of smaller segments
    int subSegments = (int)Mathf.Pow(2, subdivisions);
    float fractionPerSegment = 1F / subSegments;
    for (int i = 0; i < originalPath.Count - 1; i++) {
        for (int j = 0; j < subSegments; j++) {
            // Use Vector3.Lerp to place the points at their correct positions along the line
            newPath.Add(Vector3.Lerp(originalPath[i], originalPath[i+1], j*fractionPerSegment));
        }
    }

    // Add the last point
    newPath.Add(originalPath[originalPath.Count-1]);

    // Smooth the path [iterations] number of times
    for (int it = 0; it < iterations; it++) {
        // Loop through all points except the first and the last
        for (int i = 1; i < newPath.Count-1; i++) {
            // Set the new point to the average of the current point and the two adjacent points
            Vector3 newpoint = (newPath[i] + newPath[i-1] + newPath[i+1]) / 3F;
            newPath[i] = newpoint;
        }
    }

    // Assign the new path to the p.vectorPath field
    path.vectorPath = newPath;
}
```

Note that the new path gets assigned to the p.vectorPath field, that will enable other scripts to find it.

注意这个新的 path 被赋予 p.vectorPath 字段，这将使其他 scripts 能够找到它。

## Pooling

为了更高效地使用内存，你可以 pool 这个 lists，减轻 GC 的工作。

```C#
// Get an empty list from the pool
List<Vector3> newPath = Pathfinding.Util.ListPool<Vector3>.Claim();
List<Vector3> originalPath = p.vectorPath;

...

// Assign the new path to the p.vectorPath field
p.vectorPath = newPath;
// Pool the previous path, it is not needed anymore
Pathfinding.Util.ListPool<Vector3>.Release(originalPath);
```
