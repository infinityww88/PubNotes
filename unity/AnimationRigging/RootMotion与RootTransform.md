动画剪辑与 Root Transform 设置

位移主要由 ​​Root Transform Position XZ/Y​​ 提供；是否把曲线“烘焙进姿势”（Bake Into Pose）会改变“谁来承载位移”（根节点或骨骼曲线）。

例如：不勾选 ​​Root Transform Position XZ​​ 并在曲线里写入位移，可在预览/运行中看到角色移动；勾选后位移不再由曲线提供，而由 Pose/Root 控制。预览窗口对 Root T/Q 的修改在运行期不一定可见，正是这一机制所致。

Animator.ApplyRootMotion 与状态机过渡

启用 ​​Apply Root Motion​​ 时，Animator 会在每帧末尾用动画的 ​​Root Transform​​ 对角色 GameObject 施加一次“后写入”的位移/旋转，常会覆盖你在 Rig/脚本中对上游骨骼做的位置修改。
状态机 ​​Transition Offset​​ 也会在过渡时叠加额外的位移/旋转，属于“后处理”性质的叠加项。

动画导入时，不仅 Humanoid 标准化时会修改原始 clip 的数据，Root Transform Bake 也会改变动画数据。

Humanoid Avatar 中有很多内部机制，不能简单地以 Scene 中的 Transform Hierarchy 理解。

# Root Transform

Root Transform（根变换）是指动画中“角色整体运动的参考坐标系”。
它决定了动画播放时，角色的整体位置和朝向。

在 Unity 的 Humanoid 动画系统（Avatar）中，Root Transform 对应于动画数据中的“整体运动骨骼”，通常是：

- 对 Humanoid：Avatar 中的 Root（不是骨骼，而是 Unity 生成的虚拟根节点）；
- 对 Generic Rig：是你在导入设置中手动指定的一个骨骼（通常是 Hips 或上层骨骼）。

Root Transform 的作用是：

- 表示整个角色在动画中的平移（Position）和旋转（Rotation）；
- 用于在 动画导入（import） 和 重定向（retarget）时统一定义“角色的运动基准”。

# Root Motion

Root Motion（根运动） 是指 Unity 在播放动画时，是否使用动画中记录的 Root Transform 位移/旋转来实际移动角色。

假如有一个奔跑动画，导出时记录了角色 Root 在 Z 方向从 0-3 米的位移，说明角色在1秒内向前跑了 3 米。

* 如果开启了 Root Motion（Animator.applyRootMotion = true），Unity 会把这个 3 米的位移应用到角色的 Root Transform 上，角色会真的向前跑
* 如果关闭了 Root Motion，位移只存在于动画内部（只是骨骼动了），Root Transform 本身不会再世界坐标中移动

简单理解：Root Transform 是“动画数据的根”，Root Motion 是“是否使用这部分运动”。

# 导入设置

在 Animation Import Settings 中的 Root Transform 相关选项，就是控制动画中 Root Transform 的处理方式：

- Bake Into Pose：是否把 Root Transform 的运动烘焙到骨骼中（即，不让 Root Motion 带动整个模型）。
- Based Upon（Original/Center of Mass/Feet）：定义动画导入时以哪种方式确定 Root Transform。
- Offset：允许在导入时手动调整 Root Transform 的初始位置/旋转。

这些选项影响的，是动画片段(.anim)内部 Root Transform 曲线的结果；而 Root Motion 则是运行时是否用这些曲线更新角色的 Root Transform。

例如：

1. 动画数据中，Root Transform 在 Z 轴上移动了 0-3 米
2. Animator 中的 applyRootMotion：

   - 如果开启，Unity 每帧把 Root 的运动应用到角色 GameObject，角色在场景中真的向前移动了 3 米（Transform 被 Animator 修改）
   - 如果关闭，Unity 忽略这段 Root 位移（Animator 不修改 Root Transform），角色只是在原地摆腿


| 项目       | Root Transform             | Root Motion                  |
| -------- | -------------------------- | ---------------------------- |
| 位置       | 动画定义的参考根节点（如 Hips、虚拟 Root） | 是否用动画的位移驱动 Transform         |
| 所属层级     | 动画导入/重定向层                  | Animator 播放层                 |
| 调整方式     | Import Settings 面板         | Animator.applyRootMotion 或脚本 |
| 主要用途     | 决定动画坐标基准                   | 控制角色是否真实移动                   |
| 是否修改动画文件 | 是（影响导入曲线）                  | 否                            |
