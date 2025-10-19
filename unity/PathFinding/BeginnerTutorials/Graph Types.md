# Graph Types

A*工程中包含很多graph类型，而且还可以编写自己的graph类型。

## Grid Graph

最直接的graph。它产生网格状的nodes。它对绝大多数scenes都很适用，尤其在需要运行时更新graph的时候（例如RTS或者Tower Defence）。然而在处理具有大片开放空间的大世界时从性能和内存视角来看不是很好，因为它使用相同的node密度表示所有regions，而不管它们是否需要哪些细节。

Grid graph还可以被配置成六边形graph（Hexagonal）。

## Navmesh Graph

Navmesh Graph是另一个主要的Graph Type。Navmesh使用三角形mesh而不是方块（Grid graph）或point（Point graph）表示pathfinding数据。

这非常适合对不需要在运行时改变的graph进行平滑和快速pathfinding的场景（RPG，FPS）。

它通常比Grid Graph要快，因为它包含更少的nodes，因此只需要少量搜索。它返回的path可以被直接使用，但是强烈建议配合使用funnel modifier。

可以使用Recast Graph生成navmesh，也可以使用3D建模软件程序手动制作navmesh。

Navmesh应该是一个polygon描述walkable area的mesh，vertices应该总是位于mesh的edges上，而不是其中。此外，将很长的edges分割产生相似大小的polygon产生更好的path，而不是很大或很小的polygons相互邻接。

## Point Graph

Point Graph是最简单的graph，但是允许大量的定制，它包含一组用户放置的连接在一起的points。Point Graph扫描root transform，并将它所有的child transform作为nodes。然后它使用recast检查nodes之间的连接，以查看它们是否应该连接在一起。用户只需放置points，系统在point之间发送射线检测，如果中途没有遇到障碍物，则连个point是可以连接的。

Point Graph很难获得平滑的路径，因为它没有描述walkable区域，但是raycast modifier已经做得尽可能好了。

一个问题是当请求一条路径时，最近的点（最优路径）可能是wall另一侧的点，因此得到很怪异的路径，character先走到墙的另一侧，然后再走向目标。因此不要使用过于稀疏的nodes。只要nodes足够多，就足够接近Grid Graph和Navmesh。

## Recast Graph

Recast Graph是A*工程中最先进的graph。它基于Recast，一个开源navmesh和navigation系统，使用C++实现。Recast graph体素化world（将world光栅化为许多cube），然后构建navmesh，之后就可以想navmesh一样使用了。

它可以在几秒中之内就构建手动mesh building需要花费数小时建立的稳定的mesh。

## Layered Grid Graph

支持包含重叠区域的world，例如有多层的房子。从某些方面上说它是有点受限的。它只支持4个邻接node，而不是8个，而且比grid graph需要更多的内存。但是它在重叠区域上工作得很好。

