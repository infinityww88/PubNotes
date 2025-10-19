和 AimBoxing 非常类似，区别在于：

- 没有使用 PunchPin 对象，而是使用一个手动输入（调整）的 Swing Direction，在 IK 之前修正 ik.solver.axis，即先将 ik.solver.axis 设置到这个方向，然后 IK 过程将 aim transform 的这个 local axis 对齐到 target 上。这个步骤本质仍然是确保在静态动画中木棒通过打击的位置，因此需要手动调整这个 vector，直到合适
- 使用 Neck 作为 Aim Transform，而不是额外添加到 skeleton 上的一个 empty GameObject，同时 bones 添加了从 spine 到 neck 的 4 个 bones，也说明 Aim Transform 可以是 bones 的 end bone
- 使用 ik.solver.axis 调整瞄准方向，而不是使用 forward
