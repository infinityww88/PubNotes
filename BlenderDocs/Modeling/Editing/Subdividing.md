# Subdividing

## Subdivide

通过将选择的edges、faces分割为更小的单位来增加mesh的分辨率

- Options

  - Number of Cuts：每个edge切分的数量，默认为1，将edge切分为两半，将quad切分为4个部分

  - Smoothness：移动subdivision来维持近似曲率。非常类似Subdivision Surface Modifier

  - Quad Corner Type
    - Fan
    - Inner Vertices
    - Path
    - Straight Cut

  - Fractal：subdivided之后向随机方向偏移vertices

  - Along Normal：向Normal方向随机偏移而不是任意方向

- Un-Subdivide

  逆转Subdivided的结果。应该只在Subdivide之后立即使用。如果中间有过其他改变拓扑的编辑，可能导致未预期的结果

## Loop Subdivide

通过在选择的相交的edges ring上插入新的edges loops分割一组faces loop

- Smoothness

  使新创建的edge loops放置在插值的位置上，相对于它们分割的faces向外或向内偏移一定百分比，就像Subdivide Smooth tool，创建平滑弯曲效果。不设置smoothness，edge loops直接放置在被分割的平面上

  - Falloff：Smoothness的Falloff类型

- Offset Edge Slide

  默认Loop Subdivide只在face loop上创建新的edge loop。这个特性选择一组edge loops，然后在每个loop两侧各创建一个loop

- Subdivide Edge-Ring

  Loop Cut是对faces loop进行cut，这个特性可以选择一组指定对edges ring进行cut，例如可以只在faces loop对几个edges而不是所有对edges ring上cut

## Knife Tool

交互式划线方式切割subdivide geometry，或者绘制闭合线段创建hole

- Active Tools and Workspace setting

  Selected Only开关使得cut只在选择的元素上进行

- New cut（E）

  默认cut是连续地绘制线段。按E结束当前连续的绘制，开始一个新的绘制

- Midpoint Snap（Ctrl）

  绘制过程中，按下Ctrl使得cut线通过一个edge时，将cut这个edge的中心，而不是view空间下的投影交点

- Ignore snap（Shift）

  默认绘制过程中光标移动到edge附近时会snap到edge，按下Shift，关闭snap

- Cut Through（Z）

  默认Cut只在可见表面上进行，Cut Through无视阻挡表面将所有表面进行切割

- Angle constrain（C）

  使得每次鼠标移动与前一个cut点的连线总是对齐到45度。这是在View空间计算的，因此可能需要切换视角到垂直某个坐标平面上

- Close loop（Double LMB）

  双击LMB闭合当前连续的线段，并开始新的绘制。当鼠标移动到某个cut point/vertex时也会自动对齐，因此对齐到第一个point也会闭合当前连续的线段

- Draw a continuous line（LMB drag）

  默认鼠标移动只绘制一条线段，知道点击确定才开始绘制下一条。拖动LMB可以连续绘制

ESC/RMB曲线，LMB/Return确认

- Knife Project

非交互cut工具，将一个开放的geometry投影到另一个物体上，前者的outline成为后者的切割线。投影是在View空间进行的

Outline可以是wire或者boundary edges

在Object模式下，选择作为刀子的object以及要被切割的object，进入Edit模式，调整好视角，点击Knife Project功能。Cut Through可以切割所有被遮挡的geometry。可以模拟UModeler的Drawing工具。还可以删除Cut Through的两端faces，选择cut边缘的edge loop，选择Edge/BrideEdgeLoop工具将edge loop bridge，可以模拟UModeler的Push Hole功能

## Bisect

将一个mesh沿着特定平面切割为两半

在View空间中LMB点击并拖拽绘制一条直线确定切割平面的位置

- Plane Point，Plane Normal

  通过数字精确控制平面的位置

- Fill

  填充切割创建的切口，基于周围的geometry计算materials，UV maps，vertex colors

- Clear Inner，Clear Outer

  移除一侧的geometry

## Vertex Connect

很多时候使用Knife工具只是为了将现有的一些vertices连接起来，即在它们之间创建edge

Blender提供了两个工具简化这个过程

- Connect Vertex Path

  按照选择的vertex的顺序，就像手工knife cut一样一次点击每个vertex，创建cut edge将它们连接起来，分割经过的faces

- Connect Vertex

  类似Vertex Connect Path，但是vertex选择的顺序无关，只是将所有共享同一个face的vertices连接起来

## Bevel

创建倒棱或圆角的geometry，smooth edges和corners

- Amount(A)

  Bevel的程度，依赖Amount Type解释

- Amount Type(M)

  - Offset：新edge从原始处移动的距离
  - Width：bevel face的width
  - Depth：bevel face到原始处移动的垂直距离
  - Percent：新edge在连接edge上slide的距离的百分比

- Segment（S）

  Bevel Faces细分数量

- Profile

  Bevel Faces凹陷/凸出的曲率

- Vertex Only

  只有vertices被bevel，而不是edge

- Clamp Overlap

  限制相邻的bevel不会重叠覆盖

- Loop Slide（TODO）

- Mark Seams

  如果bevel的edge标记为seam，则新创建的用于bevel的edge也设置为seam

- Mark Sharp

  ～= Mark Seam

- Material

  赋予新创建的faces的材质id，默认-1，继承最近的现有faces，否则使用指定的slot的材质作为所有新创建的faces的材质

- Harden Normals

  Bevel新创建的faces每个vertex的法向量调整匹配周围的faces，而周围faces的法向量不受影响。这将使得周围faces flat，而bevel faces smooth到它们

  Custom Split Normals + Auto Smooth，Harden Normals自动设置

- Face Strength Mode

  设置bevel faces的Face Strength属性

- Outer/Inner Miter

  设置相交Bevel交面（斜接面）的圆滑程度，如何接触在一起
