CCDIK 包含一个 IKSolverCCD solver。

IKSolverCCD : IKSolverHeuristic

IKSolverAim 也是 IKSolverHeuristic 的子类。

IKSolverHeuristic 没有 pole 的概念，因此不控制 bones 弯曲的方向，因此可以用于很长的 chain。

IKSolverTrigonometric 提供了 Bend Plane 的功能，IKSolverLimb 因此也具有 bend plane 的功能。

IKSolverAim 是 IKSolverHeuristic 的子类，它自己实现 pole 的功能。

IKSolverCCD 则是没有 pole 的功能，因此骨骼链可以想任何方向弯曲。

因此 IKSolverCCD 通常用于很长的骨骼链（例如机械臂）。而 IKSolverLimb 和 IKSolverAim 则通常用于生物骨骼，因此生物骨骼不能随意弯曲。

IKSolverCCD 成员只在 IKSolverHeuristic 之上提供了 FadeOutBoneWeights 和 包含 CCD 算法的 Solver 方法。

CCD IK 的用法非常简单，就是这个 target position 和 bones 即可。可以可选地和 Rotation Limit Angle 组件一起使用 CCD，来限制每个 bone 的 rotation limit。RotationLimit 被放置在 bones chain 上的每个 bone 上。

RotationLimit 有 Rotation Limit Angle 或 Rotation Limit Hinge。

CCD IK 只提供了 IKPosition 的功能，没有 IKRotation 功能。这是 IKSolverHeuristic 的特性。只有 IKSolverTrigonometric 提供了 IKPosition 和 IKRotation 的功能。

IKSolverAim 也是 IKSolverHeuristic，因此也只有 IKPosition。

CCD IK demo 中，没有设置 target，在 Play 时选中 Constrained CCD Arm 会在末端 Hand 处显示一个 Move Handle。这可能是 FinalIK 为 CCD IK 组件提供的 Editor 脚本实现的，即当未设置 target 时，在末端 bone 处显示一个 Move Handle，然后可以在 scene 中拖拽这个 handle，结果的 position 被设置为 IKPosition，因此 Hand 总是跟随 Move Handle。当设置了 target 时，Move Handle 就消失了，而 IKPosition 总是被设置为 target position，即 Hand 总是跟随 target transform。不要将 end bone（Hand）设置为 target，因为这是没有意义的。Target 的唯一目的就是自动设置 IKPosition，然后 IK 旋转 bones，而 bones 包含了 end bone。因此这样做就像一个循环，改变了 end bone 的位置，然后 IK 计算 end bone 如何到达这个位置。这会导致 IK 结果的不稳定。

RotationLimitAngle 定义了一个 bone 可以旋转的锥形体，RotationLimitHingle 在 parent space 定义了一个旋转轴和一个旋转范围，bone 只能绕着这个旋转轴在这个范围内旋转，即铰链 joint。

CCD IK 2D 将 rotation 限制到 XY 平面。这个 XY 平面是 Root Bone 的 XY 平面，而不是世界空间的 XY 平面。因此 Root Bone 旋转时，弯曲所在平面也会旋转。

Target 在 Root 空间中的 Z 值被忽略。
