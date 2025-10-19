# Structure

## Splines

Splines是Curves的子结构，它们是构造curve object的独立的元素。一个Curve object可以由多个不同的spline构成，就像mesh object可以有不同的非连续的mesh部分在同一个object下面。一个Spline定义curve的形状，可以通过修改控制点进行变换。

- Control Points

控制点连接其他控制点来构成（计算）spline。控制点可以被选中和变换来修改spline的形状

## Spline Types

- Poly

  简单的折线，不再控制点之间进行任何曲线插值计算（或者说进行最简单的0阶插值计算，即y=x）。

  Poly Curves用于converting meshes to curves。

- Bezier

  边界Bezier曲线的主要元素是控制点和handles。一个segment是两个CP之间的部分。Handles定义segment的曲率

  - Handle Types

    - Automatic：具有完全自动的长度和方向，被Blender设置以保证最平滑的结果。这些handles被移动之后转换为Aligned handle
    - Vector：handle两个部分总是指向上一个或下一个CP，使得它们创建类似Poly的曲线。这些handles被移动后转换为Free Handle
    - Aligned：这些handles总是在一条直线上，因此创建连续平滑的曲线
    - Free：这些handles的两个部分独立调整，因此可以创建不连续的尖角

- Nurbs

  Bezier曲线是近似。Bezier Circle是近似circle，而Nurbs Circle是真正的circle。Nurbs的控制点具有权重，它控制CP对曲线的影响程度