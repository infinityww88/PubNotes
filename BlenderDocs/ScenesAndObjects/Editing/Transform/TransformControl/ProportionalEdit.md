# Proportional Edit

变换选择的元素，同时使变换影响周围的元素。距离选择的元素越近的未选择元素将被更远的移动得更多（它们按照距离选择的元素的相对距离成比例移动）。当需要平滑变形一个元素稠密的mesh的表面时非常有用。

Blender还提供了Sculpting工具，包含brushes和tools，可以成比例编辑一个mesh而不必看到单个的顶点

## Object Mode

Proportional Editing通常用于Editing Mode，操作vertex/edge/face，但是它也可以用于Object Mode，此时它操作整个objects而不是mesh元素

## Edit Mode

- Influence

    通过WheelUp/WheelDown来增加/减小影响半径。

- Options
  - Enable/Disable（O，Alt-O）：关闭时，transform只影响选择的元素。O想象成原型的画刷，Alt-O与Alt-A类似（取消之意）

- Projected from View
  
  影响的元素是在View空间中落在Influence原型区域内所有的vertex。关闭Projected from View时，被Influence选择的unselected元素按照在World 3D空间中距离selected元素的距离成比例变换。否则，被选择的unselected元素按照投影到view平面的2D空间中距离selected元素的距离成比例变换

- Connected Only

  不仅仅使用radius，proportional falloff沿着连接的geometry扩散，而不是简单地计算3D空间中的相对距离。例如可以proportional edit一个手上的手指而不影响其他手指，因为尽管这些手指物理上是连接的，但是一个手指上的元素到另一个手指上的元素的距离要比这个手指上的元素之间的距离远的多，而proportional falloff是沿着连接扩散的。只用于Edit Mode。

- Falloff

  Proportional Falloff的curve profile

  - Constant：No Falloff，完全一起移动
  - Random Falloff
  - Linear Falloff
  - Sharp/Root/Sphere/Smooth/Inverse Square
