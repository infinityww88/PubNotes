# CurvySplineSegment

可以针对每个segment（CP）进行不同设置

## 通用选项

### Bake Orientation

自动设置（改变）CP的transform rotation到动态计算到orientation。只对Dynamic Orientation有意义，因为在此模式下，spline到orientation只在两个anchor之间进行插值，而不是所有到CP都是anchor，因此对不是anchor的CP设置此选项，可以将CP的rotation对齐到插值计算经过此处的曲线的方向上。而static模式下，每个cp都是anchor，因此这个选项就没有意义了。开启这个选项后，CP的rotation总是随着曲线的变化自动更新，如果只想对齐一次的话，关闭这个选项，点击Bake Orientation to Transform按钮，相当于手动对齐一次

### Orientation Anchor

将一个CP设置为Anchor，只对Dynamic Orientation有意义，因为static模式下，每个CP都是Anchor

### Swirl

只用于Anchor

为当前anchor group添加盘绕，曲线上点的方向像漩涡一样随着曲线旋转

Anchor Group范围是从当前anchor到下一个anchor

- Segment：盘绕应用于每个segment
- AnchorGroup：盘绕按照F距离应用于整个Anchor Group
- AnchorGroupAbs：盘绕按照世界单位长度应用于Anchor Group

AnchorGroup与AnchorGroupAbs的区别在于前者盘绕角度turns与F成正比，后者盘绕角度与曲线长度成正比

#### Turns

盘绕多少轮（360度）

## Beier选项

主要控制控制点Handles

### Auto Handles

Handles自动设置（不能手动修改），来形成平滑的曲线。关闭时，显示两个Handles的transform，通过移动handles来控制曲线的弯曲

### Distance

只用于Auto Handles。Auto的Handles两端是对齐的，而且长度相同，唯一能调节的就是Handles的长度。Handles的长度的改变可以影响曲线的曲率。Distance用来调整auto handles的handles两端长度

### Handle In/Handle Out

在局部坐标系调整Handles，与在SceneView中调整handles transform是一样的。Auto Handles开启时，无法调整handles

### TCB选项

### LocalTension/Continuity/Bias

开启时，将独立设置每个CP的TCB的值，而不是使用spline定义的默认值。同时相应出现Tension/Continuity/Bias输入框，设置独立的T、C、B的值

### Synchronzie TCB

开启时，一个值被同时应用到segment的开始和结束。否则，segment两端的TCB的值都可以独立设置，T、C、B输入框每个出现两个，一个begin，一个end

## Meta CG选项

Meta CG Options是额外的组件，被Curvy Generator使用

### MeterialID

这个segment上生成的mesh使用的meterial的id（slot）

### HardEdge

确定这个CP是否构成一个hard edge。例如当被用于extrusion shape时，额外的顶点将被创建

### Max Step Distance

这个segment上生成的两个vertex之间最大的世界单位距离，被extrusion模块使用

#### Extended UV

使用这个section为一个横截面cross section的点定义uv坐标的u坐标。spline可以划分为不同的uv islands。一个uv island是uv坐标的一个范围，其与之前或之后的uv island不连续

- UVEdge

    当这个选项开启时，一个uv island从这个点开始创建。意味着这个点将有两个uv坐标：一个用于前面点island（以这个点为结束的uv island），一个用于下一个uv island（以这个点为开始点uv island）。这个选项不应用在闭合点spline上。开启时会出现First U和Second U输入选项

- First U/Second U

    当这个point是UVEdge（两个uv islands的边界），FirstU将定义这个point在第一个island的u坐标，SecondU定义其在第二个island的u坐标

- Explicit U

    当开启这个选项时，这个point的u坐标可以被显式地设置。不应用于闭合的spline