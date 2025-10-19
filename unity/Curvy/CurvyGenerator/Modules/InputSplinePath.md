# InputSplinePath

从一个CurvySpline创建一个Path（理论上的曲线）

## Slots

### Output

- Path

## 通用参数

- Use Cache：使这个模块使用spline的位置和切线的cached近似模拟
- Use Global Space：使用输入spline控制点的局部坐标还是全局坐标

    默认使用的是局部坐标。有时使用全局坐标可能更方便，但是这样做会导致模块的输入随着spline transform更新而更新，这将增加CPU的使用率

## 范围参数

定义输入spline的那些部分被下游的模块使用。例如，如果你设置Range为从CP0001到CP0002，则只有这个segment被下游使用。这对于限制物体放置或者mesh推挤到曲线的固定部分，使它独立于spline的整体长度非常有用

- StartCP：定义开始的Control Point。如果spline是闭合的，并且没有设置EndCP，这将导致一个shift，即选择的CP被视为spline的开始
- EndCP：定义结束的Control Point
