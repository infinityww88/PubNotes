# Properties

## Shape

- Dimension

  默认一个新的curve设置为3D曲线。2D曲线约束cp在XY平面上

- Resolution Preview/Render U

  定义每对cp（segment）上栅格化计算的顶点数（细分程度）

  Preview U定义3D view中的细分程度，Render U定义最终曲线渲染的细分程度。如果Render U=0，则Preview U同时用于渲染

- Twist Method

  Minimum/Tangent/Z-Up

- Smooth（TODO）

- File Mode

  Bevel时填充哪个部分

- Fill Deformed（TODO）

  在应用所有可能deform曲线的modification之后填充曲线

- Radius/Stretch/Bounds Clamp（TODO）

  Curve Modifier相关

## Geometry

- Offset

  沿着曲线法向量平行移动extrusion

- Extrude

  沿着local Z（法向量，twist）向正反方向extrude曲线，就像extrude edges一样，生成face

- Taper Object

  Taper沿着曲线的width变换（和radius类似）。Tappering一个curve导致它向着一端变细。还可以通过move/scale/rotating taper曲线的控制点来改变被tapered object上的Taper比例

  Taper Object只能是另一个Curve

  taper曲线沿着local X求值，使用local Y控制width

  必要条件：

  - 必须是open curve
  - taper被独立地应用到被extruded object到所有曲线（一个object可以有多个spline）
  - 如果taper object有多个curve，只使用第一个
  - 缩放从左边第一个cp开始沿着曲线移动到右边最后一个cp
  - 负数scale也是可能的（taper曲线上负数local Y），但是可能造成不自然的效果
  - 可能需要增加曲线resolution来观察taper的更多细节
  
  Taper就是作为一个数学上的变换曲线使用的，因此应该设置为2D曲线。求值坐标系是Local，但是Local没有可视化的网格，因此通常将它对齐到Global坐标系，使用Global的网格观察它的变化。求值从left到right。因此left第一个cp在x认为在原点处，即x=0，right最后一个cp的x=1。Taperd曲线沿着曲线标准化到0～1之间在taper曲线中采样

  Taper既用于extrude，也用于bevel。当bevel指定start-end区间时，默认start-end作为原始曲线的一部分在taper曲线采样。激活Map Taper则将start-end作为在taper上采样的整体，既start=0， end=1

- Bevel

  - Depth

    Bevel的size
  
  - Resolution

    Bevel横截面的smoothness
  
  - Object

    控制extruded curve。只能是另一个curve（2D/3D， Closed/Open）

  - Fill Caps

    封闭beveled curve的ends
  
  - Bevel Start/End

    Bevel的曲线的区间
  
  - Bevel Mapping Start/End（TODO）

## Path Animation（TODO）

## Active Spline

Active Spline面板用于Edit Mode中控制当前选择的spline的属性

- Common Options

  - Cyclic U：闭合当前选择的曲线
  - Resolution U：改变每个segment的解析度
  - Smooth：对任何3Dgeometry使用Smooth Shading

- Bezier Options

  - Interpolation Tilt：segment上的tilt如何极速昂

  - Radius：beveled curve的radius如何计算

- Nurbs（TODO）
