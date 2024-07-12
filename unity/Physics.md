# Physics

GameObject 有两个 bound。一个是 MeshFilter 通过 mesh 计算，一个是通过 MeshCollider 计算。

Bounds 有两个属性构造：center + size，还暴露 min 和 max 两个属性，分别对应 bound 的左下角和右上角。

MeshFilter.sharedMesh 在 local 空间计算的 Bounds，MeshCollider 在 world 空间计算 Bounds。因此：

- 通过 mesh 计算的 Bounds size 和 shape 是固定的（除非 mesh vertices 更新），不能反映 GameObject 在 world 的变化。例如当 GameObject 旋转时，Bounds 也在 world 中旋转（它只在 local 空间是 AABB 的）
- 通过 Collider 计算的 Bounds 会根据 GameObject 在 World 空间中的变化而更新，总是反映 GameObject 在 World 中的实时 AABB。但是 collider.bounds 不会随着 GameObject 的变化而立即更新，而是在多个 frame 中逐渐更新，具有最终一致性

要立即得到 GameObject 在 world 空间的实时 AABB bounds，只能通过 mesh.vertices 和 transform 手动计算。

Physics.SyncTransforms() 将 Transform 的改变立即应用到 Physics 引擎。当 Transform 改变时，它或它 children 上的任何 Rigidbody 或 Collider 需要被 repositioned，rotated，或 scaled。这些改变默认是在多个帧之间被物理引擎异步同步的。这个函数可以立即刷新 transform 的改变到物理引擎。

游戏开发要大量使用影子跟随技术，GameObject 属性要在多个帧之间逐渐追上目标值，达成最终一致，异步追随，将计算随时间分散到多个帧中。这是游戏编程经常用到的技术。越是复杂的系统越高度依赖这种技术，例如物理系统，UI 布局，Curvy Spline 等等。正是因为很多重要的系统都是如此，正常编程中不仅要应用这个技术，还要时刻注意那些系统的状态都不是立即能得到最新版本的，必须遵循最终一致的原则来使用它们。

因为正式一点的系统几乎总是要使用影子追随技术，因此在实际编程中应尽可能使用它，无论功能复杂还是简单，以熟悉熟练这种技术。只需要两个子系统：

- 计算和设置 target value
- 属性追随 target value

例如物理系统的 collider.bounds 在 transform 变换后，不能立即更新，而是在 4~5 个帧之后才更新反映 collider 的 AABB 包围框。假设使用 collider.bounds 进行 Physics.BoxCast 投射，然后根据 HitPoint 移动 transform，如果根据 diff vector 进行 Translate，就会出现问题。因为 Collider.bounds 只会在几个 frame 之后更新，再此期间 bounds 保持不变，因此会导致这些帧中每一帧中都能得到 diff vector，如果将它直接累加到 transform，就会导致 transform 会移动多个 diff vector。要解决此问题，有两个方法：

- 移动 transform 后，调用 Physics.SyncTransforms() 立即将 Transform 同步到 Collider
- 使用最终一致（影子追随）技术，不使用 diff vector Translate，而直接将 Transform.position 设置到 target Position  

这个行为在 Editor 和 Application 是不一样的。Editor 的 Play Mode 中，Transform 的改变会立即应用到物理引擎中，但是在 Application 中 Transform 改变只会异步同步到物理引擎。

Physics 的 BoxCast、SphereCast 等体积投射，Target Collider 必须是 solid（有明确的体积） 的，例如 BoxCollider，如果一个维度的厚度为 0，投射时会得到奇怪的结果，Cast 返回 true 报告有 intersection，但是返回的 RaycastHit.point 却是 transform.position。因为要保证 Collider 具有明确的体积。

BoxCast、SphereCast 这些 Cast 方法投射时，Source Collider 和 Target Collider 必须是分离的，不能有重叠。重叠的 Collider 不会包括 intersection。

要检查 Collider 是否有重叠，使用 OverlapBox，OverlapSphere 这些方法。

物理方法尽可能在 FixedUpdate 中执行。如果使用 UniTask，使用 UniTask.Yield(PlayerLoopTiming.FixedUpdate) 将物理计算放在 FixedUpdate 中。

