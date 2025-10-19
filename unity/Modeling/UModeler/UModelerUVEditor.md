# UV Editor

纹理映射是将mesh的3d顶点投影到2D空间以及操作这些投影位置的过程

UV Editor支持很多texture mapping函数

## Overview

- UModeler创建的模型自动生成UV，还可以手动编辑。两种类型的uv可以同时存在一个mesh中
- LMB双击polygon自动将它unwrap并缝合，最简单方便的unwrap polygons的方法
- Alt/Cmd：Cmaera panning
- 可以分次分批unwrap不同的polygon，每次unwrap可以选择最合适的unwrap方法
- 不同的unwrap方法在unwrap之前进行调整相应参数
- 在UV Editor workspace area中可以使用各种transform工具编辑uv 元素（vertex/edge/face）

## Toolbar

- 通常改变uv元素会影响相邻的polygons。这意味着所有重叠的uv元素（vertex/edge）将会被一起transform。但是如果按住CTRL+SHIFT，将可以独立地移动uv 元素（将共享元素split）
- 重叠的edges将被显示为绿色以方便编辑UVs
- Snap：UV transform将被Grid Snap Size和Rotation Snap Size影响，以指定的单位移动/旋转uv元素
- Show Texture：在工作区域显示当前纹理
- Show All Polygons：不管polygons使用什么材质，显示所有polygons
- Material List：选中物体上的材质列表
- Cursor：2D cursor，将作为transformation，flip，90 rotation的pivot。可以被拖拽，移动时对齐到最近的点

## Unwrap Group

### Plane/View Unwrap Tool

- 对着指定的平面投影一个mesh（polygons）
- Margin：与0-1uv矩形边界的margin
- Spacing：uv island之间的space
- Separate All：每个polygon将成为一个单独的uv island。否则，只有连接的polygons才成为一个uv island
- Axis：选择投射的axis，plane的法线方向
  - Normal：连接的polygons的法线方向（平均法线）
  - View：Camera方向
  - X/Y/Z
- Unwrap：unwrap按钮

### Cube Unwrap Tool

- Cube映射将选中的polygons在包围盒的6个平面上进行投影，创建6个uv island

### Auto Layout Tool

- 使用Auto Layoutunwrap多个选中的polygons

### Cancel Tool

- 从unwrap的uv island中移除选中的polygons，它们的uv坐标将变成自动生成的

## Selection Group

- 就像Mesh Editor一样，提供各种用于选择元素的工具
- 对于Invert、Loop、Shared选择工具，至少要有一个元素被选中
- 对于All/None选择工具，不需要提前选择元素
- Loop：选择从当前选中的edges开始的loop的edges
- Shared：独立unwrap共享edges的polygons时，共享edges在uv上将是分离的（split），这个工具选择在3D空间中与选择的edges重叠的edges

## Quick Transform Group

- 快捷变换工具
- 按住SHIFT（+CTRL），变换的polygons的共享edges将被分离，执行独立的transform
- 如果打开2D Cursor，它将成为变换的pivot

### Flip Tool

- 水平反转/垂直反转/对角反转
- 默认是元素中心，2D Cursor

### Rotate Tool

- 以90度的步长围绕元素中心或2D Cursor选择元素

## Alignment Group

- Alignment with Line：选择一组元素，将它们对齐到top/vertical center/bottom/left/horizontal center/right
- Boundary Alignment Tools：将选择的polygons或UV islands对齐到最后一个的包围框（AABB boundary box）

## Weld and Break Group

### Sew Tools

- 缝合，可以认为是split的逆过程，将重叠但分离但edges重新合并在一起
- uv与mesh元素中，vertex、edge不是对应的，只有polygon是对应的
- 前提条件（二者之一）
  - 选择两组edges
  - 选择一组edges，并且存在对应的（3D空间中）重叠edges
- 缝合在一起的edges的所有vertex在uv上一起编辑，即对每个共享它的polygon具有相同的uv坐标
- uv编辑与mesh编辑是完全的独立的，没有关系的。只有三角形polygons是对应的，uv坐标与顶点坐标不是一一对应的。uv edit本质是在为三角形polygons编辑每个点的uv坐标，一个在mesh中被共享的顶点在uv编辑中可能对应两个独立的顶点，渲染每个polygon时使用不同的uv坐标，尽管它们的顶点坐标是相同的
- 为了方便编辑，有时会需要一些共享顶点的uv坐标也保持相同，这就是缝合，即一起transform。分离的话就是每个polygon单独编辑每个顶点的uv坐标，尽管它们的顶点在3D空间中可以共享相同的位置
- uv坐标与顶点坐标没有对应关系，uv坐标是为三角形设置的。因此缝合理论上可以缝合任何不相关polygons的edges，因为uv编辑本质是调整polygon的uv的，缝合edges只是让两个polygons的uv edges一起transform而已
- Move/Sew：沿着选择的border edges移动第一个uv island到另一个选择的uv island，将两个选择的edges group缝合在一起，来合并两个uv islands，得到一个uv island。可以用来快速联合两个单独的uv island

### Weld Tools

- 合并选择的uv坐标到 第一个/平均值/最后一个 uv坐标

### Detach Tools

- 将选择的polygons从它们之前所属的任何集合中分离split出来形成一个新的uv island

## Arrange Group

### Packing Tool

- 在纹理空间以不重叠的方式放置uv元素
- Margin：纹理空间（0～1矩形）和元素的间隙
- Space：元素之间的间隙
- Pack：运行packing

### Fit Tool

- 缩放选择的元素使它们适应到texture space中（0～1）

## Misc Group

### Export Tool

- 导出uv outlines到一个.png格式的文件中，之后使用它绘制纹理
- Line Color：outlines的颜色
- Transparent Background
- Background Color
- Resolution
