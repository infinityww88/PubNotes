# Working with tags

为 nodes 和 areas 添加 tags 是非常强大的功能。

它用于现在哪些 units 可以通过哪些 ground。

例如游戏世界中有一些小生物，一个玩家，和一些 AI。AI 和生物都随机在 world 中寻路。但是可能不行生物进入房子（即使门是开着的）。Tagging 可以很好地解决这个问题。如果为 indoor 区域标记 "Indoors" tag，然后确保没有生物可以通过这些 nodes，就可以了。

使用 tagging 第一步是将一些 nodes 标记一个 tag。然后再 seeker 组件上，有一个 Valid Tags 设置，它是一个弹出菜单，可以选择这个 unit 可以通过哪些 tags 的 nodes。第一个 tag（通常名为 Basic Ground）在开始时为每个 node 设置。然后当进行 pathfinding 时，seeker 会设置 path 可以通过哪些 tags，并基于这个约束找到一个 path。当搜索最近 node 时，它还会确保选择设置了 tag 的 node。

但是要注意一点，系统采取的一个优化措施是 flood fille areas，这样它可以知道从一个点到另一个点是否有一个 valid path。然而，它不能为所有 tags 如此。因此如果两个 regions 被一个其他 tag 的 region 分开但仍然是可达的，这些 region 会共享相同的 area id。这意味着，如果一个 unit 从这些 regions 一个开始，然后尝试找到到另一个 region 的 path，但是它不能穿越中间的 region，它会在停止之前搜索它可以到达的每个 node，这会花费额外的时间。

GraphUpdateScene 组件可以帮助 tagging nodes。它有一个设置 Modify Tags。如果要修改区域内的 nodes 的 tags 就设置它，然后 Set Tag 可以定义想要设置哪些 tags。

You can debug tags by changing the debug mode to Tags in A* Inspector –> Settings –> Debug –> Path Debug Mode (and make sure Show Graphs is toggled). This will render the graphs so that each tag get's a specific color which allows you to separate them easily.

Tags can also be named for ease of use. In A* Inspector –> Settings –> Tags you can set the names of the tags. These names will then be used in all tag selection fields.


