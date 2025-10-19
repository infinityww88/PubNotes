# astar

Pathfinder组件（Pathfinding/Pathfinder）是整个A* Package的核心，它管理所有graph，计算路径

Pathfinder组件最重要的两个部分是Graphs部分和Scan按钮

Add New Graph：

- Grid Graph
- Layed Grid Graph
- Navmesh Graph
- Point Graph
- Raycast Graph

Scan用来bake graph，生成寻路数据

将不同用途目的的物体放在一个layer。Layer用来组织objects

AIPath组件等价于NavAgent，用来在计算的路径上运动object

Modifier用于在路径计算之后进行进一步处理，例如简化路径

Graphs保存场景中的所有graphs，就像Lean Touch等asset一样，需要在Scene中创建一个全局对象。最多可以又256个graphs，但是通常只需要1、2个

最重要的两个类型的graph是Grid Graph和Recast Graph。Grid Graph以网格形式生成node（A*算法中的node），而Recast Graph从world自动计算navmesh

Scan按钮用于更新graph，this is also done on startup，一些graphs在修改graph设置的时候会自动更新，而scanning不会引起lag

GridGraph生成网格状nodes，网格可以放在任何位置，可以任意旋转

Node Size确定每个格子的大小（世界单位）

## GridGraph Workflow

- 创建Plane作为Ground，将它放在Ground Layer中
- 放置带有碰撞体的障碍物obstacle
- 创建obstacle layer，aster和navmesh使用layer组织gameobjects。将obstacle物体放在obstacle layer上
- 在场景中创建aster gameobject，添加Pathfinder组件
- 在Pathfinder组件中添加Grid Graph
- 在Grid Graph中调整Width和Depth来调整grid map覆盖的范围
- 在Height testing的Mask中移除obstacle
- 在Collision testing的Obstacle Layer Mask中添加obstacle layer，调整Diameter
- 点击Scan按钮更小graph
- 在Scene中创建寻路对象gameobject——AI，添加Capsule胶囊体作为表现，移除胶囊体上的碰撞体，在AI上添加AIPath(2D,3D)组件，在其中设置Pathfinding碰撞体信息。在AI上添加AI Destination Setter组件。在场景中创建一个Target gameobject，在AI Destination Setter中设置Target为创建的target gameobject
- 点击运行，运行时可以动态调整target的位置

Grid Graph Center可以调整grid map的位置，将Y设置-0.1略微低于ground，这时为了放置细微的浮点数错误，astar使用自上向下的射线检测地面、障碍物等信息。

## Height Testing

为了将node放置在他们正确的高度（terrain），A*系统在scene中发射一组射线来检查hit的点（将node放置到这个高度）。这就是Height Testing Setting。
一个射线，可选一个厚度thick而不是一条线，从grid之上的Ray Length个单位向下发射，node被放置在射线hit到的位置。当它没有hit到任何东西时，如果Unwalkable When No Ground开启则被作为unwalkable，否则node被放置在相对于grid的Y=0的位置。
我们需要改变使用的mask，默认地它包含everything，但是它也将包含obstacle layer中的物体，而我们不想这样。因此在Mask只包含Ground layer

## Collision Testing

当一个node被放置，它被检查walkability（可通过性）。这可以使用一个Sphere，Capsule或者一个Ray来完成。通常使用一个和AI character相同直径和高度的capsule，AI character在world中四处走动，可能还想添加一些margin，放置紧贴着obstacles行走。
要使系统知道放置的obstacles，需要改变Collision Testing的mask（使用layer传递要检测的gameobjects）。设置它只包含obstacles layer。

## Adding the AI

A*提供了用来移动物体的AI的低级和高级方式。低层方式需要自己编写移动脚本查询路径并移动物体。高级脚本Richth、RichAI和AILerp提供了常用高级移动功能。AIPath脚本用于任何graph，RichAI主要用于navmesh graph。AIPath和RichAI宽松的跟随path，AILerp脚本使用插值沿着path非常精确地移动，但可能并不真实。要使用哪个依赖于你的游戏。
设置AIPath.destination(Vecot3)来设置目的地

## Smoothing

平滑、简化得到的路径。路径平滑和简化脚本称为Path Modifier.

最直接的是Simple Smooth modifier。

Smoothers只是处理计算完的路径，并不考虑世界geometry或graph，所以小心不要应用过度平滑导致path通过unwalkable区域

FunnelModifier可以很大程度地简化一个path。这个modifier几乎总是和navmesh/racast graphs一起使用

## Logging settings

A*Inspector->Settings->Debug tab，在release时关闭log

