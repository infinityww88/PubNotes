# Parenting Object

## Make Parent

复杂的模型有单独的部分组合而成

Transform Parent会影响Children

选择至少两个objects（parent最后选择），Ctrl-P => Set Parent To菜单

最后一个选择的object是active object，前面的objects都将作为它的children（siblings）

- Parent Inverse（TODO）

  当objects被设置parent时，当前parent的transform信息被保存在object（child）中的一个隐藏的parent inverse矩阵。

- Parent Types

  可以将以下类型设置为object的parent

  - Object
  - Bone
  - Vertex
  - Vertex（Triangle）

  可以将以下Modifier or Constraint设置为object的parent

  - Bone Rlative
  - Armature Deform
  - Lattice Deform
  - Path Constaint
  - Follow Path
  - Curve Deform

## Object Parent

- Keep Transform

  非常类似Object Parent，但是保留child只之前的parent坐标系的transform

## Bone Parent

将骨骼armature中的一个特定bone指定为一个object的parent，使得object可以跟着这个bone transform

选择objects和armature，切换到Pose Mode，选择parent bone，Ctrl-P

- Relative Parenting

  为每个bone toggle的选项。类似Bone Parent但是有一个区别

  在Bone Parent中，如果将一个bone设置为一些objects的parent，然后选择bone进入edit模式，移动这个bone，再切换到pose模式，children objects将回到pose mode下的位置，而不是edit mode下跟随bone而修改的位置。而在Relative模式，edit mode下修改的位置在pose mode下仍然有效

## Vertex Parent

对于curve、surface、mesh、和lattice objects，可以使用它的一个vertices或points作为其他objects的parent。可以将一个或一组vertices作为一个object的parent。这样child/children将会随着parent mesh的deform而移动

- Vertex Parent from Edit Mode

  在Object Mode下选择children和parent object。Tab进入Edit Mode，在parent object选择一个或**三个**vertex，Ctrl-P

- Vertex Parent from Object Mode

  在Object Mode下，child和parent之间距离最近的vertices将作为parent vertices

## Clear Parent

选择child，Alt-P

- Clear and Keep Transformation

  clear parent并且保留parent对它施加的transform

- Clear Parent Inverse

  不移除parent关系，但是清除Parent Inverse矩阵。使用一个空矩阵identity，children的transformation将在parent空间解释，而parent inverse矩阵将使child的transformation在world空间解释
