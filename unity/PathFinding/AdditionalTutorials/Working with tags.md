# Working with tags

使用 tags 来限制不同的 characters 可以在哪里行走。

为 nodes 和 areas 添加 tags 是非常强大的功能。它被用于限制哪些 units 可以在哪些地面行走。

例如，想象你有一些小生物，一个 player，和一些 AIs 在你的 world 中。AIs 和 小生物在世界中随机地 pathfind。但是你不想小生物爬到 houses 中。这样 tagging（打标签）就是解决这个问题的非常好的方法。如果你把所有的 indoor 区域标记为 "Indoors" 并确保没有小生物可以在这些 nodes 上行走，就可以了。

Tagging 的过程是：

- 使用一个 tag 标记一些 nodes
- 在 Seeker 组件上有一个 Valid Tags 设置。这是一个 popup，你可以设置哪些 tags 是可穿越的。
- 第一个 tag（通常命名为 Basic Ground）在开始时设置到所有的 nodes 上
- 当 pathfinding 时，seeker 将会设置 path 可以穿越哪些 tags（在 editor 中设置的那些），然后它将尝试使用这个约束查询出一个路径
- 当搜索最近的 node 时，它还会确保选择具有一个 valid tag 的 node

![tagpopup](../../Image/tagpopup.png)

需要注意的是，系统执行的一个优化是 flood fill areas 因此它知道是否可以从一个位置到另一个位置有一条有效的 path（预先计算 node 之间的矩阵，记录任意两个 node 是否可达）。然而，它不能为所有 tags 这样做，因此如果两个 regions 被一个具有另外 tags 的 region 分离，但是对 unit 仍然是可穿越的。这些 regions 将会共享相同的 area id。这意味着，如果一个 unit 从一个 regions 开始，试图发现一条到另一个 region 的路径，但是它不能穿越中间的 region，它将会在停止之前搜索每个它可以到达的 node，这会花费一些额外的时间。

当 tagging nodes，GraphUpdateScene 组件是非常好的帮助。它有一个 Modify Tags 的设置，设置它是否应该修改 polygon 中 nodes 的 tags。还有 Set Tag 设置，它定义如果 Modify Tags 被设为 true，使用哪个 tag 来标记这些 nodes。

可以通过改变 debug mode 为 Tags（在 A* Inspector > Settings > Debug > Path Debug Mode）（并确保 Show Graphs is toggled）来调试 tags。这将导致渲染 graphs 时，每个 tag 获得一个特定的颜色，允许你将它们很容易地分离开来。

Tags 还可以命名以方便使用。在 A* Inspector > Settings > Tags 中，你可以设置 tags 的名字。这些名字将会被用于所有 tag selection fields（popup）。
