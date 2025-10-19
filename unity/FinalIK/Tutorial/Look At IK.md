应该是类似 AimController，在切换 LookAt IK Target 时，产生平滑过渡效果的。

切换 LookAtController 的 target 为 Look At Target (1) 和 Look At Target (2)，或者设置它为 null 来关闭 LookAtIK。调整 LookAtController 参数观察不同的效果。

LookAtIK 和 AimIK 非常想，甚至可以替换，都是指定 spine 的骨骼链，旋转 spine 来完成解析，只有很少的区别：

1. AimIK 指定任何一个 bone 作为 Aim Transform，而 LookAtIK 明确指定 head bone
2. LookAtIK 还可以指定 eyes bones

LookAtController

## Generic

- LookAtIK ik：引用的 IK 组件

## Target Smoothing

- Transform target：look at 的目标
- weight
- offset：对 target position 的偏移

  ```C#
  ik.solver.IKPosition = target.position + offset;
  ```

- Target Switch Smooth Time：切换 target 花费的时间

- Weight Smooth Time：Blend in/out LookAtIK weight 的时间

## Turning Towards The Target

- Smooth Turn Towards Target：允许使用下面的参数平滑转向 Target（旋转 Root Transform，就像 AimIK 一样）
- Max Radians Delta：使用 Vector3.RotationTowards 旋转向 target 的速度
- Max Magnitude Delta：使用 Vector3.RotationTowards 移向 target 的速度
- SlerpSpeed：Slerp 向 target 的速度
- Pivot Offset From Root：相对于 Root Transform 的 pivot，围绕这个位置旋转 Root Transform
- Min Distance：相距 first bone 的最小 look 距离，防止由于距离太近导致 solver 解析失败

## RootRotation

- Max Root Angle：Root Transform 将会被旋转使 root forward 与 root-target 之间的角度在这个范围内
