# Structure

Mesh中所有东西都是使用vertices、edges和faces构建的

Face

    tris、quads、n-gons

quads可以良好地deform，因此非常适合animation和subdivision建模

避免对角色动画使用triangles

Normal/Auto Smooth

    定义一个sharp edge。当mesh设置为smooth shading时，只有小于指定angle当face才被smoothed（放在一个smooth group），而不是整个mesh放在一个smooth group中。

Normal/Custom Split Normals

    tweak/fake shading，是normals指向不同于默认的自动计算的normals。通常用于game development，帮助权衡low-poly物体带来的问题（最常见的例子是low-poly trees，brushes，grass等等，以及rounded corners）。

    使vertex在所有共享它的face上有各自的normal（与所在的face的normal相同）

Topology

- Loops

    一组连续地构成loops的edge和face

    Loops是一个操作一个mesh特定连续区域快速和强大的工具，以及有机体角色的必要条件