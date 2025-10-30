Animation Rigging（应该是一切 Animator Pose 的后处理系统）在启用 Humanoid Avatar 之后，只能改变骨骼的旋转，不能改变骨骼的位置，或者说其对 Bone 的位置的修改会被覆盖掉，人形骨骼只能保持 Avatar 定义的标准位置，只有旋转可以被处理。

```
在 Humanoid Rig 中，所有后处理机制（Rigging、IK、Constraint、脚本）只能真正修改骨骼的旋转；
位移只有 Root 层有效，其他骨骼的位置在 Avatar 定义中是固定的。
```

- Humanoid 的动画不是直接写入骨骼 Transform，而是写入一个 内部的姿态缓存（HumanPose）。
- Animator 每帧计算完动画，会把结果存入 HumanPoseHandler 的缓存中。
- 然后 Unity 会在 内部求解阶段（C++ 层） 把这个姿态转换成真正的骨骼 Transform。
- 对用户脚本或 Rigging 来说，你访问到的 Transform 实际上是这一求解结果的“快照”。
- 因此，你在 RigBuilder 或脚本中对骨骼 Transform 的修改，是在这个快照上修改的，不是直接写入 Animator 的内部缓存。

下一帧开始时：

```
Animator 在更新阶段又会重新根据 HumanPose 缓存重新写入 Transform（完全覆盖你的修改）。
```

所以从根本上来说，你的修改根本没有“流入动画系统”，只是短暂地改变了一份临时内存数据。

假设你启用了 Animator（Humanoid）+ RigBuilder，一帧的执行顺序（简化）如下：

```
1. Animator.Update()               ← 计算 HumanPose，重建所有骨骼姿态
2. Avatar 求解阶段 (C++层)         ← 把 HumanPose 应用到 Transform 层
3. RigBuilder.LateUpdate()         ← 你在 Rigging 或 Constraint 中修改 Transform
4. SkinnedMeshRenderer.Update()    ← 使用动画系统缓存的骨骼矩阵进行蒙皮
5. Unity 引擎内部同步 (C++层)     ← 再次将 Animator 的内部缓存刷新到 Transform
6. 你的修改消失，下帧重新开始
```

这里关键是在第 5 步：

SkinnedMeshRenderer 渲染时使用的不是 Transform，而是 Animator 内部缓存的姿态数据。SkinnedMeshRenderer 并不是直接采样 Scene 里骨骼 Transform 的位置。对于 Humanoid，它使用的是 Animator 内部维护的骨骼姿态缓存（HumanPoseSolver 的结果）。RigBuilder 修改的 Transform 并不会立即影响这份缓存。

注意有一些后处理（例如 Rigging 的 TwoBoneIK 或 ChainIK）看起来是改变了 Bone 位置，但它们不是真的靠改写 Bone 的 Position 修改的骨骼位置，而是靠旋转骨骼链，计算并修改 Bone 的 Rotation 改变的骨骼链让末端骨骼到达某个位置的。

## SkinnedMeshRenderer

SkinnedMeshRenderer 并不是直接使用场景中骨骼 Transform 的世界位置与旋转来驱动蒙皮变形的。

SkinnedMeshRenderer 采样骨骼的位置和旋转的来源是不同的：

- 位置来源于 Animator 内部的 Avatar Pose 缓存，在这里骨骼的位置永远是标准的、不变的，后处理机制（例如 Animation Rigging 或 Final IK）对骨骼位置的修改不会被写入内部的 Avatar Pose
- 旋转来源于场景中的 Bone Transform 旋转，这就是为什么后处理机制对骨骼的旋转是有效的，因为 SkinnedMeshRenderer 从这里读取旋转，并且会写入到 Avatar Pose 缓存中

```
旋转（rotation） 会来自骨骼当前 Transform（即 Scene 里的姿态）；

但 位移（position） 通常来自 Animator 内部的人形 Avatar Pose 缓存（HumanPoseHandler / AvatarTransformStream），而不是直接读 scene 里的骨骼位置。
```

这样做是因为人形骨骼具有特殊性，无论是从常识还是 Avatar 内部各种计算，只改变骨骼旋转，不能改变骨骼位移都是有利的。

## Root Motion

Root Bone 的位置是特殊的，它是直接从 Animator 的 root motion buffer 更新的，因此可以在后处理中直接改变根位移 Root Motion，并同时更新 Animator 的 Root Transform。方法是调用 Animator.ApplyBuiltinRootMotion()。

通过修改根骨骼（Root/Hips）的位置可以实现整体位移（Humanoid 允许这一层的 position 生效）。

# Generic 骨骼中的情况

切换为 Generic Rig，RigBuilder 的位移修改会立即生效。

或者 在 Animator 关闭或不启用 Avatar 时，再使用 RigBuilder 操作骨骼。

在 Generic Rig 中：

- 动画系统直接修改骨骼 Transform；
- SkinnedMeshRenderer 直接从骨骼 Transform 读取矩阵；
- 没有 HumanPose 缓存层；

即 Generic Rig 符合通常理解的情况，SkinnedMeshRenderer 对骨骼的位置和旋转的采样都是从场景中的 Transform，这里没有 Avatar 内部的 HumanPose 缓存。

所以 RigBuilder 改动的 Transform 会立刻体现在蒙皮渲染中。

这也是为什么所有 procedural animation（程序动画）都建议用 Generic Rig。
