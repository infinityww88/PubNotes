# Lattice

Blender之外通常称为deformation cage

由一个3维不可渲染的vertices grid组成。通常用于Lattice Modifer来变形物体

## Editing

Flip：从基础位置镜像vertices的displacement

Make Regular：reset lattice到一个正规grid，并且每个cell缩放为一个单位的立方体

## 属性

Points：沿着各个轴的细分网格数量

Interpolation Type：Linear，Cardinal，Catmull-Rom，B-Spline

Outside：只使用lattice的表面vertices

Vertex Group：影响的vertex group和每个vertices的weight
