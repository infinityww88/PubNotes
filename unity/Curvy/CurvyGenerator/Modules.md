# Modules

模块是Curvy Generator的工作间。一个模块通常接收其他模块产生的输出。通过连接模块间的输入输出创建模块之间的关系。一个模块slot可以是可选的，或者接收或生成数组

CurvyGenerator是一套独立的体系，它使用Shape，Path，Volume等概念。只不过它选择使用CurvySpline来生成需要的Shape或者Path

Shape、Path是理论上到曲线，等价于Spline

Volume是理论上3D空间中到体积，等价于Mesh

## OnRequestProcessing

通常地，数据从一个模块的输出流入另一个模块的输入。一个例外是，有一些模块实现来IOnRequestProcessing接口。不像普通模块，这些模块从下游模块得到一个请求，然后开始处理并返回数据。因此从graph上看，RequestProcessing是上游模块，但是它不是主动像下游推送数据，而是在下游模块请求时才产生并发送数据

这对于那些本质上没有分辨率的数据非常有用（例如shape或者path），其从下游接收需要的栅格化的细节：当一个模块需要一个path时，它发送一个包含参数（From/To/Resolution/etc...)的request到树的上游。第一个实现IOnRequestProcessing的模块则产生被请求的数据然后想通常那样向下发送

这样工作的模块它们的名字和slot显示为绿色，而接收其输出的正常模块只有input slot显示为绿色

## Module Colors

没有正确配置的模型title显示为红色。

可选模块为灰色，可以被连接以完成更多的功能

slot可以一个或多个相同类型的数据，或者产生一个数据数组

### Input类别模块

| 模块 | Input | Output | Description |
| --- | --- | --- | --- |
| Input Spline Path | | Path | 从一个CurvySpline创建一个Path |
| Input Spline Shape | | Shape | 从一个CurvySpline创建一个Shape |
| Input Spots | | Spots | 创建一个Spots的集合 |
| Input Meshes | | VMesh[] | 从Unity Meshes中创建VMesh数组 |
| Input GameObject | | GameObject[] | 从Unity GameOjbects/Prefabs中创建GameObjects |

## Modifier类别模块

| 模块 | Input | Output | Description |
| --- | --- | --- | --- |
| TRS Path | Path | Path | Translate/Rotate/Scale一个path |
| TRS Shape | Shape | Shape | Translate/Rotate/Scale一个Shape |
| TRS Mesh | VMesh | VMesh | Translate/Rotate/Scale一个VMesh |
| Path Relative Translation | Path | Path | 将一个Path相对于它的横截面方向进行偏移 |
| Mix Paths | Path, Path | Path | 联合两个Paths |
| Mix Shape | Shape, Shape | Shape | 联合两个Shapes |
| Variable Mix Shapes | Shape, Shape | Shape | Combine two Shapes in a way that varies through a shape's extrusion |
| Conform Path | Path | Path | 将一个Path投影project到一个colliders/terrains上 |

## Build类别模块

| 模块 | Input | Output | Description |
| --- | --- | --- | --- |
| Shape Extrusion | Path, Shape | Volume, Volume(Hollow，可选) | 沿着一个Path推挤一个Shape |
| Volume Mesh | Volume | VMesh[] | 从Volume创建一个VMesh |
| Volume Caps | Volume, Volume[] | VMesh[] | 生成Volume Caps到VMeshs |
| Rasterize Path | Path | Path | 栅格化一个Path |
| Volume Spots | Path or Volume, Bounds[] | Spots | 沿着一个Path或Volume克隆物体 |

## Create类别模块

| 模块 | Input | Output | Description |
| --- | --- | --- | --- |
| Create Mesh | VMesh[] Spots | | 从VMeshes中创建Mesh资源（磁盘资源）|
| Create GameObject | GameObject[], Spots | | 从GameObject中初始化GameObjects/Prefabs |
| Create Path Line Renderer | Path | | 将一个Path输入给一个Line Renderer |

## Misc

| 模块 | Input | Output | Description |
| --- | --- | --- | --- |
| Debug Volume | Volume | | 可视化一个Volume |
| Debug VMesh | VMesh | | 可视化一个VMesh |
| Debug Rasterized Path | Path | | 可视化一个栅格化到Path |
