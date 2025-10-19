# Editing graph connections manually

如何编辑 graph 结构。

通常 graph 几乎都是正确的，但有时你需要进行一点修复。这对 point graph 非常常见，这里几乎都是用于 graph type。然而这些方法一定程度上也用于其他一些 graph types。

## The NodeLink component

如果你有一个 point graph，你想要添加一个 connection，或者移除一个现有 connection，或者修改一些 connection 的 cost，则你可以使用 NodeLink 组件。Point Graphs 通常从一个 GameObject 集合中创建。你可以添加 NodeLink 组件到一个 node，然后设置 target 到另一个 node。通过改变 options 这个组件可以添加一个 connection，移除一个现有 connection（如果存在），或者改变 connection 的 cost。这些新的 connections 和 point graph 原始创建的 connections 完全一样。

![nodelink](../../Image/nodelink.png)

有一些 keyboard shortcuts 可以更容易地修改 graph。你可以在 Unity 中找到 menu item，Edit > Pathfinding.

- alt + ctrl + L (alt + cmd + L on macOS): 连接两个 nodes。连接两个 nodes，如果他们之间没有 NodeLink 连接。如果它们以及连接了，则显式删除它们的连接
- alt + ctrl + U (alt + cmd + U on macOS): 取消两个 nodes。这移除连接两个 nodes 的 NodeLink 组件。无视 NodeLink 是否被配置为添加还是删除一个 connection
- alt + ctrl + B (alt + cmd + B on macOS): 销毁选中的 GameObjects 上的所有 NodeLink 组件

## Editing graph connections using code

你也可以使用 code 修改 graph 连接.

```C#
AstarPath.active.AddWorkItem(new AstarWorkItem(ctx => {
    // Connect two nodes
    var node1 = AstarPath.active.GetNearest(transform.position, NNConstraint.None).node;
    var node2 = AstarPath.active.GetNearest(transform.position + Vector3.right, NNConstraint.None).node;
    var cost = (uint)(node2.position - node1.position).costMagnitude;
    node1.AddConnection(node2, cost);
    node2.AddConnection(node1, cost);

    node1.ContainsConnection(node2); // True

    node1.RemoveConnection(node2);
    node2.RemoveConnection(node1);
}));
```