# Controllers

控制器被用来沿着曲线对齐或移动GameObjects以及Curvy Generator数据例如挤压volumes或者paths

- Spline Controller：使用它来沿着曲线对齐或移动GameObjects
- Path Controller：于Curvy Generator Paths一起工作
- Volume Controller：于Curvy Generator Columes一起工作

## 通用设置

### Update In

确定控制器何时更新：Update/LateUpdate/FixedUpdate

### Spline/Path/Volume

控制器跟随的源对象

### Use Cache

只用于Spline控制器

合适的时候使用缓存数据。Cached数据不够精确但是更快

## Position

### Position Mode

position是世界单位（绝对）距离还是相对距离。相对位置在0-1之间。对于Spline，相对位置是TF，而对于paths和volumes，它是整体长度的比率

### Position

使用上面Mode的Position数据

## Cross Position

Volume Controller only

定义横截面的位置

### Cross Range

定义controller使用的横截面中的范围。基点（point 0引用的point）可以被Shift修改

### Cross Position

在定义的Cross Range中的位置

### Cross Clamping

定义当试图移动出定义好的range时应该怎么办

## Move

### Move Mode

定义速度使用绝对还是相对距离，参考Position Mode

### Speed

Move Mode下的速度

### Direction

运动的方向

### Clamping

定义当source的终点到达时怎么办

- Clamp：控制器停止
- Loop：控制从另一段重新开始
- PingPong：控制器切换方向

### Play automatically

开启时，进入Play Mode时，控制器自动播放

## Connections Handling

Spline Controller only

指定当一个Spline Controller到达一个Connection时应该如何运动

- Use Current Spline：控制器沿着曲线继续运动，就像没有connection一样
- Use Follow Up Spline：如果存在Follow-Up，则沿着包含Follow-Up的曲线继续运动，否则仍然在当前曲线上运动
- Use Random Spline：随机选择一个连接的spline继续运动
- Use Follow Up other Random：如果存在Follow-UP，则沿着包含Follow-Up的曲线继续运动，否则随机选择
- Use Custom behavior：定一个你自己的连接曲线选择逻辑。你可以通过设置一个继承自ConnectedControlPointsSelector的类的实例赋予控制器来实现

### 允许方向改变

当开启时，允许控制改变它当运动方向以连续当前进。如果在一个Follow-Up继续运动，它将使用Follow-Up的heading。如果在一个随机的connection上运动，它将反转运动方向如果连接是选择的曲线的end，或者向前运动如果连接是选择的曲线的begin

### Reject divergent splines

如果曲线与当前曲线在连接处过于奇异（在connection出的切线夹角过大，即不像是连续的曲线）则将其从随机选择的曲线中排除

### Reject current spline

当前曲线应该从connection随机选择的曲线中排除

## Orientation

控制器通过对齐一个Source Vector（基于控制器source曲线）到一个Target Vector（基于控制器对象）定义object的旋转

### Source

定义source向量

- None：没有向量对齐。如果希望控制GameObject在运动时保持原来的rotation则选择这个选项
- Tangent：使用曲线点的Tangent向量
- Orientation：使用曲线点的向上向量

### Target

定义控制器GameObject的旋转轴向量，用来对齐曲线点的Source向量

### Ignore direction

如果开启，orientation（向上向量）忽略控制器的运动方向，否则当控制器反向运动时，向上向量反转

### Lock Rotation

强制控制器不改变旋转方向

### Direction Damping Time

在指定的时间段中为Tangent/Direction（切向量）添加平滑阻尼

### Up Damping Time

在指定的时间段中为Up/Orientation（向上向量）添加平滑阻尼

## Offset

在横截面上为GameObject添加一个偏移向量，基于曲线的向上向量

### Offset Angle

从向上向量开始的[-180, 180]之间的角度，定义偏移的方向。在一个平面中，旋转只需要一个角度；在3d空间中，旋转需要一个旋转轴和一个角度；本质是一样的，只不过在平面中旋转轴是确定的，就是垂直平面的轴

### Offset Radius

偏移距离

### Compensate Offset（偏移补偿）

控制器速度将自动修改以将偏移一起的更长或更短的移动距离考虑在内

## Events（Unity Event）

### OnInitialized

控制器初始化时调用。你通常不必等到控制器初始化时再设置它的属性

### OnControlPointReached

当经过一个控制点时调用

### OnEndReached

当end或start到达时调用

### OnSwitch

当在connection处切换spline时调用

## 高级设置

### Force Frequent Updates

默认地，Unity在Edit Mode下更少地调用script的Update。ForceFrequentUpdates强制script在Edit Mode下与Play Mode一样频繁地调用Update。通常用户不需要使用这个功能。但是如果在Edit Mode下使用Camera时会非常有用

### Preview

在Edit Mode下开始或停止运动的预览
