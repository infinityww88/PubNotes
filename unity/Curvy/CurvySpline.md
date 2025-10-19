# CurvySpline

## 通用选项

- Interpolation插值

    定义曲线的类型：Linear，Bezier等等，曲线本质上就是在不同的控制点之间进行插值

- Restrict To 2D

    曲线将只能在X/Y平面编辑。如果Perference中的“Use Tiny 2D Handles”被启用，没有工具会显示，你可以直接拖拽ControlPoint的gizmos

- Closed

    曲线是否闭合，也就是最后一个控制点是否构成一个到第一个控制点的曲线段

- Auto End Tangents（仅用于开放的Catmul/TCB曲线）

    当开启时，第一个和最后一个控制点自动计算曲线方向

- Orientation

    确定如何计算曲线方向

    - None：曲线没有方向
    - Static：每一个控制点都是Orientation Anchor，每个segment在两个端点CP的transform rotation之间进行平滑插值
    - Dynamic：默认只有第一个CP是Orientation Anchor，其他CP需要开启Orientation Anchor选项才能成为Anchor

## 全局Bezier选项

- Default Distance %

定义使用Auto Handles时默认的Bezier Handle长度

## 全局TCP选项

- Tension

定义被控制点使用的全局tension（拉力）

- Continuity

定义被控制点使用点全局连续性

- Bias

定义被控制点使用全局Bias

- Set Catmull/Cubic/Linear

预制TCB参数来模拟一个特定类型的曲线

## 高级设置

这些设置都是针对每一条曲线可以不同的

### Show Gizmos/Color/Active Color

可以为不同的曲线设置不同的显示颜色

### Cache Density

确定cache density

### Max Points Per Unit

每个世界单位长度采样点的最大数量。采样用于caching，spline rasterization，和shape extrusion等等

### Use Pooling

控制点缓冲池，被CurvyGlobalManager对象管理

### Use Threading

特定操作可以在多个线程中同时执行。线程本身有消耗，因此只对重型曲线使用线程

### Check Transform

每一帧检查所有CP的transforms，重新计算曲线。如果要在code中直接改变曲线或者进行曲线动画，需要开启这个选项

### Update in

确定曲线什么时候进行更新

- Update
- FixedUpdate
- LateUpdate

## 事件

spline相关Unity事件，可以在inspector中编辑，主要针对控制点的变化（添加/删除）

### OnRefresh

spline每次刷新后执行

### OnAfterControlPointChanges

一个或多个控制添加或删除时执行

### OnBeforeControlPointAdd

在一个控制点被添加之前调用，取消这次事件可以阻止添加一个CP

### OnAfterControlPointAdd

在一个控制添加之后调用

### OnBeforeControlPointDelete

在一个控制点被删除之后调用，取消这次事件可以阻止删除一个CP

## CurvyUISpline

CurvyUISpline组件继承自CurvySpline，并且应该被用于pixels而不是世界单位。和CurvySpline唯一的区别就是Cache Density考虑了pixels

