# Performance

## Tips for improving the performance

- 减少 PuppetMaster ”Solver Iteration Count“（为所有 muscles 改变 Rigidbody.solverIterationCount）到你可以工作的最小值。更少的 solver interaction 使 muscles 更脆弱，因此你可能必须增加 PuppetMaster ”Muscle Spring“
- ”Fix Target Transforms“ 在你的 character 总是 animated 时应该关闭
- ”Visualize Target Pose“  在 Editor 中花费一些性能，但是不是在 built game 中
- 将 Update Joint Anchors 保持关闭以提升性能，以模拟精确度为代价
- ”Angular Limits“ 和 ”Internal Collisions“ 在关闭时可以减少物理引擎的工作负担
- 当使用 BehaviourPuppet 时，增加 PuppetMaster “Collision Threshold”。它决定多大强度的碰撞才能被 BehaviourPuppet 处理，增加这个 value 将会使 puppet 的 behaviour 在碰撞时 jerky（抽筋）
- 减少 muscles 的数量。你真的需要 3 个 spine muscles 或者 feet or hand muscles 吗？
- 在使用 BehaviourPuppet 时，在 Physics settings 中减少 “Default Contact Offset” 将减少昂贵的 OnCollisionStay 广播
- 在 Project Settings/Time 增加 Fixed Timestep 到最大的 tolerable value
- 保持你的 puppets 彼此分开。更少的碰撞意味着更少的工作，无论是对于 Physics engine 还是 PuppetMaster
- 当不需要任何物理模拟时，为 puppets 设置 PuppetMaster mode 为 Disabled 
- 对于只需要 colliders 用于碰撞检测或 raycasting 的 puppets，设置 PuppetMaster mode 为 Kinematic
- 当你不需要使用任何 Puppet Behaviours 也不需要在碰撞的情况下获得调用，将 MuscleCollisionBroadcaster 中的 OnCollisionEnter/Stay/Exit functions 注释掉
- PuppetMaster 还可以运行一个 flat hierarchy ragdoll。只需要右键点击 PuppetMasterheader，并在 context menu 中选择 ”Flatten Muscle Hierarchy“
