# Vertex Data（顶点数据）

## Face

输出当前渲染的face是正面（1）还是背面（-1）

## Object Scale

返回当前gameobject的scale。Scale可以从ObjectToWorld或者WorldToObject变换矩阵得到

## Template Vector Data

通过Data dropdown访问shader模板中定义的顶点数据。输出类型根据选择的data类型不同而不同

SubShader/Pass/Data

## Vertex Bitangent

输出顶点在局部坐标系的副切线，考虑来object和tangent符号。副切线是Vertex Normal和Vertex Tangent的叉乘积

如果这个节点最终连接到的不是Output Node的Vertex Offset或者Vertex Normal，则输出值将被插值

## Vertex Color

输出一个3D模型上的顶点颜色。如果节点最终连接的不是Vertex Offset或者Vertex Normal，则输出值被插值

## Vertex Normal

输出局部坐标系中顶点的法向量。数据直接从Mesh中导出，并且包含相对于物体原点的vertex normal。这意味着normal向量值不会改变，而不管物体当前的transform是怎样的。这在Local Vertex Normal或者创建绑定在物体上、无论物体如何改变position、rotation还是scale都保持不变的效果是非常有用的。与其他Vertex Data一样，取决于这个node的最终在哪里被使用（vertex或者fragment/surface函数），它或者直接输出值（vertex函数），或者针对每个像素输出插值结果（fragment/surface函数）

参见World Normal

## Vertex Position

与VertexNormal类似，但是输出局部坐标系中的顶点位置

参见World Position

## Vertex Tangent

参见Vertex Normal

## Vertex Tangent Sign

参见Vertex Tagent。具体地说，它输出tangent的w channel

## Vertex TexCoord

直接从Mesh中输出UV坐标，不进行任何Tilling和Offset计算
