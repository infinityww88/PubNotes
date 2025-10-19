# Snapping

Blender有两种类型的snap操作

- snap选择或3D cursor到给定的点
- 在move/rotate/scale期间snap选择到场景中的elements

## Snap Menu

激活

- Object Mode：Object/Snap菜单
- Edit Mode：Mesh/Snap菜单
- Shift+S

选项

- Selection To Grid：当前选择物体到最近的grid point
- Selection To Cursor：当前选择的元素/物体到3D Cursor位置
- Selection To Cursor（Offset）：将一组元素/物体相对位置不变地使它们的中心移动到3D Cursor
- Selection To Active：移动选择到当前激活物体到原点
- Cursor To Selected：将3D Cursor移动到当前选择到中心
  还被Pivot Point选项影响
  - 当激活Bounding Box Center pivot point，3D Cursor移动到所有objects包围盒到中心
  - 当激活Median Point，3D Cursor移动到所有objects到平均中心
- Cursor To Center：将3D Cursor移动到World空间原点
- Cursor To Grid：将3D Cursor移动到最近到Grid
- Cursor To Active：将Cursor移动到当前激活（最后一个选择的）物体的原点上

## Transform Snapping

在transform（Move/Rotate/Scale）期间对齐objects或elements到各种类型到场景元素

点击3D View header上到磁铁按钮开启transform snapping

### Snap Element

- Increment

  对齐到Grid Points。当在Orthographic View时，对齐increment随着zoom level改变，因为grid精度随着zoom level改变

- Vertex

  对齐到鼠标下面mesh objects的vertices

- Edge

  对齐到鼠标下面mesh objects的edges

- Face

  对齐到鼠标下面mesh objects到surfaces。对retopologizing很有用

- Volume

  对齐到鼠标下面发现的第一个object的volume区域。和其他选项不同的是，这个选项控制被transform元素的深度（View Space相机空间的Z坐标）。用来快速将物体移动和目标物体相同的区域，以便进行进一步的调整，而不是用于精确对齐的。否则就需要分别沿着X/Y/Z三个平面依次移动才能将物体移动到目标区域

- 可以通过Shift-LMB激活多重对齐模式

### Snap Target

  决定那个selection到哪部分对齐到target objects

- Active

  移动active elements/objects到target

- Median

  移动selection到平均中心到target（保持相对位置）

- Center

  移动当前transformation原点到target。Transformation原点不一定是object原点，它实际上是pivot point。Pivot Point有很多选项

- Closet

  将selection距离target最近到点移动到target

## Additional Snap Options

- Absolute Grid Snap：对齐到grid，而不是increments（step）。Increase option
- Project Onto Self：Edit Mode，可以对齐到自身元素
- Align Rotation To Target：对齐到target到rotation
- Project Individual Elements：Snap to Face。将独立到元素（例如vertex）对齐到其他objects到表面上
- Snap Peel Object：Snap to Volume。当寻找volume center时，将objects认为是一个整体
- Affect：限制snap影响当transform类型（Move/Rotate/Scale）

## Multiple Snap Targets

当开启Snapping并transform一个selection时，可以按A标记当前snapping point，然后标记任意多个points，而selection将会对齐到所有marked points到平均位置。将一个point标记多次将会增加它到权重
