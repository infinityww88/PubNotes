# Splines

一个Curvy spline使用一个CurvySpline组件构建，它使用带有CurvySplineSegment组件的子GameObjects表示控制点

你可以通过创建Connection连接两个或多个控制点

除非特别说明，Spline和ControlPoint API返回的所有position和rotation向量都是局部于Spline GameObject的

## Spline

Spline是通过数学方法创建的曲线。给定一些参考点（控制点）和一个time值，它们返回空间中的一个点。当使用不同的time值调用数学公式时，就会得到一组空间点。这些连接的点构成了你要使用的曲线

一些spline类型比其他类型需要更多的参考点，一些spline类型使用额外的参数定义曲线，但是基本上它们以相同的方式工作

## 控制点 vs 片段Segment

控制点和曲线段非常类似于折线的端点和线段

一个曲线段就是一个控制点，但反过来不一定是，因为总有一个控制点没有对应但曲线段

## 单位

### F

一个spline线段点通过输入一个time(0-1)到spline公式来计算得到，因此所有处理segment的API方法都有一个F（fragment）参数。不要误认为F是百分比，F=0.5不一定表示curve segment按长度的中心。因为曲线的数学公式对于参数time不是线性的。F=0，表示曲线段的起点，F=1，表示曲线段的终点

### TF

就像F之于segment，所有处理整个spline的API方法使用TF（total fragment）参数来确定整个曲线上的一个点。TF=0表示曲线的起点，TF=1表示曲线的终点。TF也是不与曲线长度成正比的

### Distance

F和TF可以很好的用来确定曲线上的点，但是绝大多数用户希望基于真实世界单位长度来工作。Curvy可以在distance和fragment（F，TF）直接进行转换，因此你可以自由地使用想要的单位。在Curvy API中，localDistance参数跨越一个segment长度（对于segment level方法），distance跨越整个曲线长度（对于spline level方法）

所有单位只定义在curve可见的部分上。不构成一个segment的控制点不能使用这些单位定位到

Curvy在内部只使用fragments（F，TF），因此每个接收distances的方法需要在内部被转换成fragments

### Spline Types

- Linear
- Catmull-Rom
- TCB
- Bezier

