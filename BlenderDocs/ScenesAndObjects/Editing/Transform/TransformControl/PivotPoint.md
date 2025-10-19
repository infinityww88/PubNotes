# Pivot Point

当旋转/缩放一个object或者一组vertices/edges/faces，通过偏移pivot point（旋转/缩放参考中心）以更方便地操作物体。

在3D View header的Pivot Point菜单中选择不同的Pivot Point Mode。

## Bound Box Center

Selection的AABB外接包围盒，平行于World Axis

Pivot Point位于Box中心

- In Object Mode

  Box基于每个object的origin计算，object的mesh大小无关

  当选择单个object，rotation发生在origin

- In Edit Mode

  Box基于被选择的元素的size计算，object origin无关

## 3D Cursor

Rotate/Scale相对于3D Cursor进行

## Individual Origins

Origin就是object自己默认的Pivot，可以放置在任何地方，是Local坐标系的原点，Mesh vertices都是基于这个点记录的

- In Object Mode

    如果选择了一组物体的话，每个物体都保持在原地，围绕各自的pivot进行相同数量的rotate/scale，相当于对每个object 分别执行了rotate/scale

- In Edit Mode

    和Object Mode一样，每个被选择的元素独立进行rotate/scale，围绕元素的中心median（平均中心）（作为pivot）

## Median Point

Median(Center)，平均中心，Center Of Gravity（质心）

- In Object Mode

  Median是所有选择object origin的平均中心

- In Edit Mode

  所有元素（vertices）的平均中心。当选择多个元素island时，就有更多vertices的island具有更大权重

## Active Element

Active Element可以是一个Object，一个Vertex，一个edge，或者一个face。Active Element是最后一个被选择的那个，在Object Mode以高亮的橘色显示，在Edit Mode以白色显示。

- In Object Mode

  Active Object保持在原地，其他Objects围绕Active Object的origin

- In Edit Mode

  - Pivot总是active element的median（active element所有vertices的平均中心）
  - transform是transform被选择元素的vertices（无论是edge还是face）。如果未选择的元素与选择元素共享一些vertices，它们也会有一定程度的transform