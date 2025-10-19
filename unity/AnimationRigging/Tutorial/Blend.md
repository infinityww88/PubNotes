Animation Rigging 用于 Animator 输出的动画骨骼，但是这个动画可以是 Humanoid 动画，也可以是 Generic 动画。

AnimationRigging 的约束中，target 必须是 Animator 下面的 bone（tranform），否则没有作用。Source 可以是 Animator 外的 Transform，也可以是 Animator 下面的 bone。

Bone 有两种定义，一种是 joint，一种具有长度的 bone。例如：

joint0 -> joint1 -> joint2

这里可以说有 3 个 bones（joint0，joint1，joint2），也可以说有两个 bones（joint0-joint1， joint1-joint2）

Blend 约束在计算多个 source transform 的平均位置和旋转，应用到 target transform 上。
