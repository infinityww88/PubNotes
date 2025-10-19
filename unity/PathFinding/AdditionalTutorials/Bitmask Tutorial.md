# Bitmask Tutorial

Package 中不同地方有一些对 bitmask 的使用。

最常见对 bitmasks 的使用是当查询到一个 point 的最近 node 时选择哪些 graphs 被搜索。NNConstraint 类有一个 graphMask 定义哪些 graphs 将被搜索。

```C#
// Create a constraint that will search only the graphs with index 0 and 3
NNConstraint nn = NNConstraint.Default;

nn.graphMask = 1 << 0 | 1 << 3;

var info = AstarPath.active.GetNearest(somePoint, nn);
```

The Seeker.StartPath method also takes a parameter called 'graphMask' which is just forwarded to the Path.nnConstraint object. It can be used in the same way.

```C#
seeker.StartPath(startPoint, endPoint, null, 1 << 0 | 1 << 3);
```
