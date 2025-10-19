# Error messages

可能在console中看到的错误消息

## 路径错误消息

这些消息意味着A*系统无法找到有效路径。

- 不能找到接近start point的node

    当执行一个pathfinding时，系统查询到start point最近到node（grid graph中到tile，navmesh/recast中到三角形，point graph中的point）。

    确保请求path的start point是正确的。

    如果使用内置移动脚本，确保AI从graph上合理的地方开始。

    如果AI开始位置的确是正确的，你就是想从start point开始扩展搜索，则增加AstarPath.maxNearestNodeDistance。

- 不能找到接近end point的node

    类似上面的错误。但是搜索距离end point最近的node时，系统还有额外的限制：node不仅需要是walkable的，还必须能从start node搜索得到的（可达矩阵）。这个错误出现的一个常见情形是，例如AI被所在地图一段的一个小屋子里面，然后获得指令移动到很远的一个point。当试图查找end node时，必须查找很长的距离，因为当AI当前node是到达不了end point的。

- 没有到target的有效路径

    这个应该不会发生，除非为Path object提供了一个自定义的没有从PathNNContraint继承或者没有使用PathNNConstraint逻辑的NNConstraint。

    确保任何自定义的Pathfinding.NNConstraint从Pathfinding.PathNNConstraint继承

- 搜索整个area但不能找到target

    没有从start node到end node的可能的路径。这通常发生在使用tags并且配置它们使得一些tags不能通过的时候。A*预计算node之间的可达性。对于常规的可达性，可以直接判断。但是基于tags的则不可能这样做。因为两个node之间可能有很多可能的路径，当常规最优路径因为tags变得不可行的时候，其他次优路径就可能成为最优路径，因此只能通过重新搜索来确定有效路径。A*系统可能不止预计算可达路径，而是预计算了每两个node之间的可达路径。这样对于常规路径可达性，就可以直接返回结果。

- 没有开放points，start node没有开放任何node

    这个错误是上面错误的一个特殊情况。当只有一个node被搜索并且不能找到path的end时，log打印出来。这种特殊的错误通常是由于grid graph的一个简单的配置错误。如果AI有一个collider，而collider被包含在Height Testing layer mask中，则会发生graph在AI头上放置了一个node。而这个node不与周围的nodes连接，只是孤立的一个node，即没有开放nodes。

    这导致AI认为它被locked一个非常小的grid内，因此找不到离开的路径。

    确保AI所在layer不在Height Testing layer mask中

- 因为一个新的request取消当前path计算

    Seeker每次只计算一个request，新的request将会cancel之前的request。

- 通过脚本取消（Seeker.CancelCurrentPathRequest）

- Scene中没有graphs

    AstarPath组件中没有包含任何graph。如果通过file或者使用脚本创建一个graph，则可能是在加载完成之前请求路径查询。

## Graph错误

一些meshes被静态batched。

一些meshes被静态batched。这些meshes由于技术限制不能用于navmesh计算。在运行时script不能访问被静态batched的mesh的数据。一个方法是使用cached startup（Save & Load），在game没有playing时计算graph（backed）。

解决办法：

- 使用colliders而不是meshes来生成recast graph。这通常也更快，因为colliders通常比mesh具有更少的细节。colliders本身也是mesh，只不过不是用于显示。
- 在Editor中计算graph，然后在游戏开始时从文件中加载它。使用Cache Startup功能很容易完成这一点。这也可以有效提升有效startup的时间，因为从文件loading要比从头生成它更快。缺点是不能支持运行时生成的过程化关卡。
- 可以在运行时graph生成之后在把geometry标记为静态batch的，参考Unity StaticBatchingUtility

## 编译错误
