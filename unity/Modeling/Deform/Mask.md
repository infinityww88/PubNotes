# Mask

使用特定形状限制只有特定区域的vertices才变形

Mask类似后处理，应用在deformer之后，即基于deformer变形后的mesh进行mask。将Mask放在Deformer之前是没有影响的

Mask是否定式的，掩码就是掩住不修改，只将要修改的部分暴露出来

## BoxMask

- InnerBounds与OuterBounds确定mask的内外边界
- Bounds根据deformer执行之后的顶点数据确定是否mask
- InnerBounds内部的vertices完全被掩住mask，不进行deform，恢复deform之前的数据
- OuterBounds外部的vertices完全暴露，没有mask，进行正常的deform
- Inner-Outer直接的进行线性插值，类似于羽化区域
- Factor调整整体mask的程度，0-完全没有mask，1-完全mask
- Invert反转mask区域和插值方向
- InnerBounds和OuterBounds通过各自的center和各自的extent确定范围，InnerBounds不超过OuterBounds

## SphereMask

- 类似BoxMask
- 通过半径确定一个内边界和外边界，内边界内部完全被掩住，不变形，即恢复初始位置，外边界外部完全暴露执行变形，内外边界之间进行插值

## Mask State

- Mask的原理

    每个MeshData带有一个MaskVertices顶点数组，一个CurrentVertices顶点数组。初始时MaskVertices与CurrentVertices初始化为相同的mesh的顶点数据。之后Deformer变形的数据保存在CurrentVertices，MaskVertices还保存初始的顶点数据。应用各种Mask时，Mask读取CurrentVertices（变形后的数据），基于内外边界计算顶点从CurrentVertices到MaskVertices应该进行的插值系数Factor，内边界内部Factor=1，即完全插值到MaskVertices（初始状态），外边界外部Factor=1，即完全插值到CurrentVertices，内外边界之间则计算一个0～1的Factor

- MaskVertices默认总是Mesh顶点的初始状态，无论应用了多少个Deformer。MaskState将当前CurrentVertices保存在MaskVertices，即让MaskVertices保存当前变形的数据，使得之后的Mask基于当前的数据进行插值

## VertexColorMask

- 不使用Box/Sphere的内外边界计算插值系数，而是通过顶点颜色的某个channel计算插值系数

## Vertical Gradient Mask

- 类似VertexColor，但是基于vertices的Z坐标值和一个下降曲线计算每个vertex的mask插值系数
- Falloff：下降曲线指数
