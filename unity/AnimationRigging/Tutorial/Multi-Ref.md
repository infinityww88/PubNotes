Multi-Referential 设置一组 Reference GameObjects，然后每次选择其中一个，这个 GameObject 就像剩下所有 Ref GameObject 的 parent 一样。这个约束通常用来操作一组 Rig manipulator。例如同时移动双手或双脚（两个 TwoBoneIK bone chain）的 effector。这些 effector 本身具有 IK Rig 约束，然后它自己又被 M-Ref 组件操纵。

RigTransform 用来添加到 Rig 下面的 manipulator，这些 GameObject 作为 Rig 约束效应器，它本身上也可以有 Rig 组件，也可以没有，这和是否是 manipulator 没有关系。这个组件 RigTransform 的主要用途是在 Scene View 显示一个图标以便可以快速选中它，因为它们通常是 Empty GameObject。

Multi-Referential 用来同时操纵其他 Rig effectors，可以说是二级 effectors，它以 parent-like 操作一组 effectors，然后这些 effectors 又操作各自的 Rig 约束。


