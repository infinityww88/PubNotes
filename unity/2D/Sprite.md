# Sprite

Sprite是2d游戏中物体的图形表示单元，就像mesh之于3d物体

Sprite本质上就是一个平面mesh，所有的三角形勾勒出sprite图像的轮廓，而使用的图像来自于纹理或纹理集，因此三角形的每个顶点都具有纹理上的uv坐标

Sprite物体的中心称为pivot，即3d mesh pivot的2d版本，所有的三角形都基于这个点定义

Sprite Editor本质上就是在建立这中平面mesh

    确定表示sprite的图像所在的纹理
    创建构建轮廓的三角形和对应的轮廓
    编辑pivot

Sprite类提供了比直接访问Mesh更高级的接口，可以直接操作Sprite的各个属性，但是也提供了Mesh数据属性triangles/uv/vertices，因此可以使用这些mesh数据像deform mesh一样deform sprite
