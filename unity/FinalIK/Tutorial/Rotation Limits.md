RotationLimit 是所有 Rotation limits 的抽象基类。包含通用的功能和静态帮助函数

RotationLimit 成员

- Vector3 axis：rotation limit 的主轴
- Apply()：应用 rotation limit 到 transform.localRotation。如果 limit 改变了 rotation，返回 true
- Vector3 secondaryAxis：一个任意的 secondary axis
- Vector3 crossAxis：axis 和 secondaryAxis 的叉乘积向量

RotationLimit 本身是 MonoBehavior 组件，在 LateUpdate 中调用 Apply。它本质上就是 IK solver 的后处理。在 IK 返回 pose 之后，每个 RotationLimit 将它所在 transform 重新约束到 Limit 定义的范围中。

这种后处理约束和物理引擎中碰撞约束、关节约束，以及所有用于游戏的约束技术一样，都是多个约束系统按照顺序求值，每个约束只考虑自己的约束逻辑完全不考虑有没有其他的约束，每个约束在前一个约束的结果基础上应用自己的逻辑，最终的结果就是所有这些约束的综合。例如群聚算法 Flock，有 3 个子系统组成，每个子系统独立地以特定逻辑约束每个单位的 transform，3 个子系统按照顺序求值，后面的子系统在前面的子系统的结果基础上求值。

因为一个约束的结果还要被后面的约束再次修改，因此后面的约束可能导致 GameObject 的状态重新违反了前面的约束。这是可能的，也是很常见的，尤其两个约束有冲突的时候。例如在一个复杂的物理关节构成的系统中，很难保证稳定并让系统满足所有的关节的约束，很容易看见这种破绽。这是没有办法的，也是可以接受的，因为多约束系统就是这样。例如约束 1 要求 GameObject 状态位于 [2, 8] 区间，约束 2 要求 GameObject 状态位于 [-20, -2] 区间。如果当前 GameObject 状态为 1，约束 1 先将 GameObject 状态约束到 2，然后约束 2 再将状态约束到 -2。最终状态就是 -2，这违反了约束 1，但是这无法避免，因为约束 1 和 2 本身就是冲突的，而结果 -2 已经是完全考虑 了约束 1 和 2，尽量接近约束 2 的右边界和约束 1 的左边界。最终结果体现了所有约束的综合效果，即可以隐约看见所有约束系统都在起作用。

RotationLimitHinge 将旋转只限制到一个平面上，平面垂直 axis。除此，RotationLimitAngle、RotationLimitPolygonal、RotationLimitSpline 都是定义了空间中的一个半空间，Transform 只能在这个半空间中自由选择，axis 指向这个半空间的方向。唯一的区别是定义半空间的方法不同

- RotationLimitAngle：定义了一个锥形自由旋转半空间，只需要 axis 和圆锥角度就可以
- RotationLimitPolygonal：使用一个空间中的多边形和 transform（作为中心）定义了一个不平坦的半空间，可以对这个多边形细分产生更平滑的曲面
- RotationLimitSpline：使用一个样条曲线和 transform（作为中心），定义了一个平滑曲面构成的半空间

Transform 在这个半空间中可以自由旋转，最多到达曲面表面。

RotationLimit 限制的是 Transform 相对于 Parent Transform 的旋转。对于 Root Transform 则是相对于 World Space。

RotationLimit 和 IK 没有关系，可以独立使用。它们只在 LateUpdate 中重新调整 Tranform 的 rotation 到定义的限制范围内。

RotationLimit 和 IK Solver 一样，可以 Disable 然后手动调用 Apply，来应用约束。
