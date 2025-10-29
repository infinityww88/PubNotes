# Bidirectional Motion Transfer

Bidirectional motion transfer 是一个 authoring（创作）workflow，让你 transfer 现有 motion 到 active constraints 上，或者反之将来将 active constraints 的 motion transfer 回到原始 motion source 上，同时保留 motion 的视觉精确性。

这个 workflow 使用 Animation Window 来选择想要的 clip，并在 Scene View 中预览约束的结果。

“Transfer motion to skeleton” 和 “Transfer motion to constraint”是 constraint 组件可用的选项。你应该使用 Rig 组件来 transfer 整个 Rig 的 motion，或者使用 RigBuilder 组件来 transfer 整个 hierarchy 的 motion。

![baking_option_menu](Image/baking_option_menu.png)

不是所有 constraints 都可以被 Transfer motion。Physics-based constraints 例如 Damped Transform 不能从现有 motion 推测。

其他 constraints 可以被 transferred，但是有限制。例如 Twist Chain constraint 约束 rotations。它覆盖 positions 和 in-between 中间的 chain rotations。Transfer motion 的结果不会精确代表 source animation。

下面的约束支持 Transfer motion 到 constraint，但是具有限制：

| Constraint | Limitations |
| --- | --- |
| Two Bone IK Constraint | 	无 |
| Multi-Aim Constraint | Roll-Axis motion 不保证完全一样 |
| Multi-Parent Constraint | 无 |
| Multi-Position Constraint | Disabling constrained axes 可能改变最终结果 |
| Multi-Referential Constraint | 无 |
| Multi-Rotation Constraint | Disabling constrained axes 可能改变最终结果 |
| Twist Chain Constraint | 中间 chain transforms 被覆盖 |
| | | 