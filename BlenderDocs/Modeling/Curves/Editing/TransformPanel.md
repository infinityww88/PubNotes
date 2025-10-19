# Transform Panel

N key弹出Transform Panel

在ObjectMode中，Transform Panel编辑Object的位置/旋转/缩放

在Mesh Edit Mode中，Transform Panel编辑vertex、edge和face的median的position（不编辑rotate、scale）

在Curve Edit Mode中，与Mesh Edit Mode类似，如果选择了一个control point/handle，则编辑cp的position，否则编辑一组cp/handle的median位置

对于Nurbs曲线，还有第4个分量w，控制这个cp的权重

- Space：position信息相对于World space还是Local space

- Radius：控制沿着spinal curve的extrusion/bevel的width。Radius将在cp之间插值

- Tilt：控制normals（显示为箭头）在每个cp处的twist。只用于3D曲线。在cp之间插值。可以控制曲线法向量沿着曲线的扭转，如果进行extrusion就可以明显地看见
