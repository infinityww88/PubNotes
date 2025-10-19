# Getting into Shapes

Shapes 在 Archimatix 中非常重要，因为它们是 mesh 生成的根基。

参数化 Shapes 的例子是 Circle，Rectangle，Arch。更多复杂的例子包括齿轮，模具 profile，四瓣花。

即使更复杂的 shapes 也可以使用 boolean 操作来构成。这些操作组合 shapes 和 thicken，round，deform Shape 的 shape modifiers。

不像拓扑建模工具 topological modeler（blender），vertices 和 polygons 被直接复制和操作，Archimatix 是一个参数化建模工具，meshes 是从一组规则中拓扑化生存，然后被 controllers 修改。这些 rules 和 controllers 可以被你创作，或者你可以组合 Archimatix 自带的很多参数化 shapes。这些 “living” 智能的 shapes 然后可以被 参数化 mesh generators 装配来创作你自己的车辆，武器，建筑和城市结构。Shape 变成很多不同的 meshes 的参数化生成器，尽管它自己也是参数化的。

参数化 shapes 在通过结构化设置构成时更加强大，而不是使用 free-form 曲线手动绘制，因为特定的几何学逻辑可以被包含在里面。例如，使用几个 controls（例如 radius 或者 springHeight）来操作一个拱形比手动绘制容易得多。

尽管 Archimatix 提供拓扑化编辑 shapes 的能力（手动），例如，点击一个 vertex 并移动它，但是这个工具的真正的能力只有当 shapes 被 handles 和嵌入的 logical 关系处理时才真正发挥出来。

一个简单的例子是那些难于手动（每次一个 vertex）创建的参数化 shape，例如 circle。世界中很多东西是从圆形的筒仓，加农炮管，城塞城堡等等创建的。我们不需要定义 circle 上的每个 point，只需要一个 center 和一个指定半径的 point。Circle 的规则可以快速地创建所有的 vertices。这个例子展示参数化建模只需要必要的少许参数，基于公式，就可以快速创建正确的形状。

Archimatix 不仅提供了大量的预置表达常见建筑、机械、数学拓扑的参数化形状，它还支持创建自定义参数化 curve 逻辑，可以让设计者定义什么样的 handles 最适合那个形状。

例如，我们想要创建一个特定类型的小木屋，它创建自 I shape，以及一个从形状扩展出的半圆。尽管村庄中每个小木屋的比例都是独特的，但是所有的小木屋共享 I-with-a-circle 拓扑，而这个拓扑自身是一个村庄文化。如果这样的一个 shape 在 library 还没有，你可以 编码 code 一个，并定义应该使用哪些参数来允许其他人创建很多 I-shaped 房屋的变体。然后这个 shape 可以被 mesh generators 装配，来非常容易地生成大量独特的房屋，而共享同一个艺术风格。在此情景，你可以制造一个新的 shape type，它可以在以很多排列组合被实例化，其不仅仅包括基本的平移，旋转，缩放等变换，因此生成你的世界中生成一个又一个村庄。

久而久之，你可能会构建一个特定于你的游戏的艺术风格的 shapes library。这些 shapes 可能被用于项目中的其他艺术家使用，制造你的艺术风格的事物，而没有两个 shape 的实例是重复的。

## Positioning Controls

一个 shape 的定位控制参数是那些用于其他 objects 的参数的子集，因为它的天性：它核心是一个 2D 的工具。不管 shape 在 3D 空间中被它的使用者如何旋转，诸如一个 ShapeMerger 或者一个 Mesh generator，在它的局部定义中，它总是被认为是在 X-Y 平面。

### Translation

一个 shape 提供 Trans_X 和 Trans_Y，不包括 Trans_Z. 一个 Shape 的 Translation handle 是一个 Point Handle，而不是一个 Position Handle（3轴 Gizmos），指示它不能进行 3D 移动。

### Rotation

类似的，没有 Rot_X 和 Rot_Z，只有 Rot_Z，表示只能在 X-Y 平面旋转。

### Alignment

Alignment 也只限定在 x 和 y 轴上。

## Texture Controls（纹理控制）

这对一个 shape 的纹理控制意味着什么呢？因为 shape 是一个 mesh 的生成器输入，你可以在 shape level 控制 mesh 纹理的特定方面。例如，你想要从一个 PlanSec extruder 中生成的 mesh 在 plan（两端） 上是表面分明的（每个面有单独的法向量），但是在 section（侧面）是平滑的。你可以通过设置 plan shape 的 breakAngle 为比如说 10 度，而设置 section shape 的 breakAngle 为 100 度来达成。

Shape 描述可以包含 UV 坐标，使得到描述中的一个特定的 point 应该 跨越 span U=0 到 U=1.23
