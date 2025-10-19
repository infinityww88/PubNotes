# Pathfinding in 2D

2D游戏中可能想要很多类型的pathfinding。主要有两种：

- Top-down pathfinding。从上向下看的游戏的寻路
- Platformer pathfinding。平台游戏寻路。类似超级马里奥。但是当前A* package还不支持这种类型的寻路。可以大量使用point graphs并创建自定义connections来实现，但是这并不是开箱即用的功能

## Graph support

- Grid graph和Layered grid graph可以很好地支持XY plane。事实上，grid graphs可以任意旋转，而仍然可以工作。对于2D游戏，应该选中grid graph上的2D toggle，这将会旋转graph使它对齐到XY平面上。如果使用2D collider，还要开启Use 2D Physics checkbox。
- Point graph也支持XY平面的pathfinding。类似grid graph，如果开启来Raycast设置并且使用2D collider，需要开启Use 2D Physics。
- Recast Graphs可以旋转到XY平面上工作（或者旋转到任何方向）。然后它们当前不支持2D colliders，或者使用sprites作为光栅化过程的输入。如果使用正常的mesh则可以工作。Navmesh graphs的幕后运行和Recast Graphs一样，recast graphs只是一种自动化生成navmesh的手段。因此它们也可以在任何方向上工作。但是必须确保graph的up方向是想要的up方向。例如如果你想要在XY平面上使用navmesh，你需要设置rotation field为(-90, 0, 0)，不能简单地在Blender中旋转mesh。

## Graph Updtes

### Navmesh Cutting

Navmesh cutting可以用于更新任何方向上的2D recast和navmesh graphs。但是要确保navmesh cuts正确的旋转。Navmesh cuts表示为垂直投影到graph表面上的2D outlines。对于非水平的graph使用navmesh，useRotationAndScale必须开启。

### 2D collider

当使用graph updates，3D游戏中通用方式是

```C#
var guo = new GraphUpdateObject(GetComponent<Collider>().bounds);
AstarPath.active.UpdateGraphs(guo);
```

但是对于2D游戏使用collider2D的这段代码不会工作。原因是2D colliders是无穷细的，因此它的包围盒没有体积。因为graph检查一个node位置是否在一个bounds中，它们永远不会更新一个node，因为没有node可以位于一个没有体积的包围盒中。要解决这个问题可以沿着Z轴扩展bounds，确保包含所有nodes。

```C#
var bounds = GetComponent<Collider2D>().bounds;
bounds.Expand(Vector3.forward * 100);
var guo = new GraphUpdateObject(bounds);
AstarPath.active.UpdateGraphs(guo);
```

## Movement Scripts

AIPath支持任何方向上的grid graphs、navmesh、recast graph的移动，它自动检测graphs的方向。你可能希望关闭gravity设置来放置agent从map掉落。Point graphs没有可定义的up direction，因此AIPath脚本不能知道它是如何朝向自己的。如果你知道想要的方向，你可以简单修改AIPath脚本来强制它使用一个特定的方向

```C#
// 在AIPath.cs中查找类似下面的代码行
// movementPlane = graph != null ? graph.transform : GraphTransform.identityTransform;
// 然后将其替换成
var graphRotation = new Vector3(-90, 0, 0);
movementPlane = new GraphTransform(Matrix4x4.TRS(Vector3.zero, Quaternion.Euler(graphRotation), Vector3.one));
```

RichAI不支持任何除了XZ平面的旋转。但是在将来会支持。

AILerp支持任何方向graph的移动。对于2D游戏你可能想要+Y作为agent的forward方向而不是3D游戏中常见的+Z。如果是这样，开启rotationIn2D选项。

## Local avoidance

Local avoidance工作在XY平面。唯一要做的事情就是修改RVOSimulator组件的movementPlane设置为XY。

