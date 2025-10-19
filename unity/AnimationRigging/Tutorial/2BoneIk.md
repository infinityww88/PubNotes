Root 下面有 model（包含骨骼）和 Rig。Root 具有 Animator 组件，其中的 AnimatorController 包含一个动画（AnimatorController 与 Animancer 等价，相当于 Animancer 包含了一个 State）。这个动画不仅 animate 了模型的骨骼，还 animate 了 Rig 下面的 IK target （lfik 以及 rfik），使在世界空间中绘制出 foot 的移动轨迹。lfik 和 rfik 下面各自有一个 Two Bone IK Constraint，这相当于 FinalIK 的 limbik（limb 称为 3-segment 就是有三个骨骼构成的两段，最后一个 bone 没有 child。分别约束左右腿的 大腿-小腿-脚 这个骨骼链，lfik 和 rfik Transform 本身是骨骼链的 target。因为 target 被动画 animate，而骨骼链由被 target 通过 ik 控制，因此形成了行走的动画。身体的上下左右振动和摇摆是动画中输出的，不是 IK 的效果，IK 是在振动摇摆基础上控制左右腿骨骼链。

可见 Animator 上的动画可以 animate Hierarchy 下面的任何骨骼（Transform），而不仅仅是模型中的骨骼。动画片段文件包含的数据只是每个骨骼的名字和骨骼随时间的 transform 数据（通过关键帧插值而来）。当被 Animator 使用并输出是，Animator 就是简单地在 Hierarchy 下面查找同名的 Transform，然后将输出的 transform 数据赋给它，仅此而已。因此对于 Generic 动画，只要模型的骨骼具有和动画片段中记录的骨骼具有相同的名字，就可以被它活动。对于 Humanoid 动画，多了一个 Avater 间接层，使得动画可以 retargeting。

TwoBoneIK Constraint 指定 3-bones 骨骼链（上臂-前臂-手，或者大腿-小腿-脚），然后指定 target 和 Hint，Hint 就是弯曲平面（Pole 或 Bend Goal）。对于 target position 和 rotation 以及 Hint 都有一个单独的 weight 控制各自的权重。

Maintain Target Offset 是 3-bones 中的末端骨骼 tip（effector，效应器）和 IK 目标 target 之间的 position、rotation 是否被维持（是脚在 IK 过程中始终保持和地面平行）