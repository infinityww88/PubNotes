# Transformation

## Mirror

在指定轴上镜像一组选择的元素

Edit Mode的Mirror和Object Mode的Mirror类似。等价于在选择的pivot point处指定的轴上对每个vertex/edge/face执行-1 scaling.

X/Y/Z key

## Shrink Fatten

选择的vertices/edges/faces沿着normal放大或缩小，不考虑当前pivot point（transform orientation）

- Offset Even（S/Alt）

缩放每个vertex的偏移获得更加平均的厚度

## Smooth

- Smooth Vertices

## Push/Pull

将选择的元素（Objects、vertics、edges或者faces）向着pivot point push/pull相同的距离

## Shear

平行surface移动超过另一个

Axis location通过pivot point定义。选择的元素沿着当前view的horizontal轴移动。所有位于axis x轴之上的东西都移动与鼠标相同的方向（shear）但总是平行于X轴。X轴之下的部分向相反方向移动

- Offset：移动的距离
- Axis：定义想象的shear平面的一个axis

## To Sphere

使被选择的元素基于中心趋向于球形

## Warp

围绕着3D cursor按照特定角度弯曲。总是依赖3D cursor，不考虑Pivot Point。

Warp半径依赖于选择的元素距离Cursor的距离

Warp的结果依赖于View空间

Warping Text需要将text转化为mesh

## Bend

3D Cursor + Mouse Cursor

半径控制曲率，旋转角度控制弯曲程度
