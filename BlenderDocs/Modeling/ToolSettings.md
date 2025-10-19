# ToolSetting

## Option

Active Tool And Workspace Setting

### X-Mirror

Mesh Options panel到Mirror选项允许沿着 Local X 对称地变换 vertices。当变换一个元素（Vertex，Edge，Face）时，如果它有一个镜像对应者（local），它也相应地被对称变换。

Mirror的工作过程非常苛刻，使得它比较难于使用。创建对称mesh的更容易和更简单的方法是Mirror Modifier

### Topology Mirror

当使用X-Mirror来操作一个Mirrored Mesh Geometry时，被镜像的vertices必须具有严格镜像的location，否则就不认为是镜像的vertices（例如有一些轻微的偏差）

Topology Mirror选项则不仅考虑它们vertices的位置，还考察它们在Mesh Geometry中相对于其他vertices的相对关系。它查看整个拓扑结构来决定特定的vertices是否被认为是镜像的。结果就是非对称但是镜像的vertices也被认为是镜像的

Topology Mirror通常只对具有很多细节的geometry mesh可有效工作，而对于简单的geometry，例如Cube、UV Sphere，这个选项通常不能工作。就像巡航导弹是通过地形匹配方式寻路的，越是复制的地形，越能匹配。如果是广阔无垠的沙漠就会迷路。Topology Mirror也是如此，也是复杂的Mesh，越能良好地工作。（添加一个Blender Monkey就可以良好地使用Topology Mirror）

Blender中存在大量基于拓扑计算的技术，即只要结构关系相同，即使位置不是对称/相等的，也被认为是等价对应的。Unity中的Avatar技术也是基于拓扑计算的技术，用于人形动画骨骼的匹配

### Auto Merge

当Auto Merge选项开启时，只要vertex移动到另一个vertex指定阈值之内，它们就自动合并为一个。这个选项只影响交互式的vertex移动工具，以及Adjust Last Operation Panel的调整。如果一个vertex移动到一群vertices附加，于它们的距离都小于阈值，则于它们中的一个合并
