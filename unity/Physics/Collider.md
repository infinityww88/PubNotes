# Rigidbody 的 Collider

一个 Rigidbody 的形状可以由多个 Collider 复合构成。但是这些 Collider 必须在 Rigidbody 自身上，或者在它的直接 Child GameObject 上：

```
A Collider will be associated with the first Rigidbody component it finds in its parent hierarchy.
However, only Colliders on the Rigidbody’s GameObject or its immediate children will move with it as part of the same physical body.
```

一个 Rigidbody 只会影响它所在 GameObject 自身的 Collider，以及它的「直接子物体（immediate children）」上的 Collider。

如果 Collider 位于更深层的嵌套（例如「子物体的子物体」），它不会被视为该 Rigidbody 的一部分，而是被 Unity 物理系统当成一个“独立的静态 Collider”。

但只有「直接子物体」才会自动被识别为 Rigidbody 的“组成部分”。

当 Rigidbody 和 Collider 间有非空 Transform 层级（中间节点）时，Unity 会认为这中间的 Transform 可能在独立移动或缩放，于是打断了刚体与碰撞体的绑定关系。这样的 Collider 不会被认为 Rigidbody 的一部分，而是会被当做静态 Collider。

这样做是为了避免复杂层级造成的非线性物理行为（例如局部缩放导致体积不正确、惯性计算错误）。

# 复合 Collider 的改变

一个 Rigidbody 的 Collider 可以由多个 Collider 复合构成，它们通常在运行时是不变的，被视为一个整体。

但是实际上可以在运行时改变 Rigidbody 的 Child Collider 的 Transform（移动、旋转、缩放），也就是在运行时改变了物体的形状，并且物理引擎可以正常响应，与正常的 Collider 碰撞解析一样。

但是注意，和任何静态 Collider 发生位移、旋转、缩放一样，如果 Collider 变化碰撞到了其他的 Rigidbody 的 Collider，是否会影响（推开）被碰撞的 Rigidbody，依赖碰撞双方的类型和 rigidbody sleep/wakeup 的状态。

假设 Collider 发生变化的 GameObject 为 A，碰撞到 Collider 为 B。A 可以是 Static Collider（纯 Collider，没有 Rigidbody），可以是 Kinematic Rigidbody，可以是 Rigidbody，B 是 Rigidbody：

1. A 整体位移、旋转、缩放

   - 如果 A 是 Static Collider，需要 B wakeup 才会响应碰撞
   - 如果 A 是 Kinematic Rigidbody 或 Rigidbody，不需要 B wakeup 就可以响应碰撞

2. A 的 Child Collider 发生位移、旋转、缩放

   - 如果 A 是 Static Collider 或 Kinematic Rigidbody，需要 B wakeup 才会响应碰撞
   - 如果 A 是 Rigidbody，不需要 B wakeup 就可以响应碰撞

可见：

- 对于 Static Collider， 总是需要 Rigidbody wakeup 才会响应碰撞
- 对于 Rigidbody Collider，不需要 Rigidbody wakeup 就可以发生碰撞
- 对于 Kinematic Rigidbody Collider，当整体运动时，表现得像 Rigidbody，当自身形状发生变化（Child Collider 运动）时，表现地像 Static Collider。

物理引擎根据这些规则和 Rigidbody 的 Sleep 状态，进行过滤，选择本次模拟哪些碰撞处理，哪些碰撞不处理（Sleep）。

物理引擎之所以能正常响应，是因为 Collider 碰撞检测和 Rigidbody 碰撞反馈解析是两个独立的系统。Collider 碰撞检测会检测到任何 Collider 的碰撞，不管这些 Collider 是怎样被运动的，被脚本、被 Rigidbody 物理、被动画等等，它都不管，只要有碰撞它就解析，并报告。Rigidbody 收到自己的 Collider 发生碰撞就按照标准算法开始解析碰撞，直到碰撞分离或状态平衡下来。

# Unity 如何处理 Rigidbody Collider 形状变化

可以在运行时移动、旋转或缩放 child Collider 的 Transform，Unity 会自动更新该 Collider 在刚体本地空间中的位置与旋转。但这种操作有性能代价（尤其在每帧变动时），并且不能产生非刚体的形变（不会真正“拉伸”或“重塑”物理形状）。

当多个子 Collider 组成一个 Rigidbody 时，Unity 会把这些 Collider 合并为一个复合碰撞体（Compound Collider），并在物理世界中把它们注册为一个整体。

```
Parent (Rigidbody)
 ├─ Collider A (Box)
 └─ Collider B (Sphere)
```

Unity 会为这个 Rigidbody 创建一个物理刚体，并在其下注册两个局部 Collider 实例，分别记录它们在 Rigidbody 本地空间中的位置、旋转、大小。

当你在运行时改变 Child Collider 的 Transform：

- Unity 会检测到该 Collider 的 Transform.hasChanged = true；
- 它会在下一帧物理更新（FixedUpdate）时重新计算这个 Collider 的本地变换；
- 并更新物理世界中的该 Collider的包围体（AABB）与形状变换。

这样，Collider 会跟随变换移动或旋转，物理模拟依然有效。

但是需要注意以下几点

## 1. 性能影响（Physics shape rebuild）

每次改变子 Collider 的局部位置或旋转，Unity 都要：

- 更新该 Collider 在物理引擎（PhysX）的形状缓存；
- 重建该 Collider 所属的 compound body 的部分数据结构；
- 更新 broadphase 中的包围盒信息。

如果你在每帧都修改大量子 Collider 的 Transform（例如模拟骨骼碰撞体），会导致严重性能开销。

因此 Unity 官方建议：尽量不要在每帧修改 Collider 的 Transform，除非你明确知道性能成本。

## 2. 不能实现 soft deformation，仍然是刚体变形

改变缩放只会更新 Collider 的“几何缩放”，不会改变物理体积（质量、惯性张量）在运行时动态更新。
这意味着：

- 缩小 Collider，不会自动减轻 Rigidbody 的质量；
- 想更新惯性，需要重新设置 Rigidbody.ResetCenterOfMass() 或 Rigidbody.ResetInertiaTensor()；
- 若频繁修改，会导致物理不稳定。

## 3. 不支持 SkinnedMesh 的实时变形碰撞

如果想让 Collider 跟随角色骨骼动态变形：

- Unity 不会自动更新 Collider 随骨骼的形状变化；
- 需要手动在 Update 或 LateUpdate 中同步骨骼的局部变换到相应 Collider；
- 但这样代价很高，不建议每帧修改大量 Collider。

# 最佳实践

| 目的                 | 推荐做法                                                      |
| ------------------ | --------------------------------------------------------- |
| 少量子 Collider 随部件移动 | 可以直接改 Transform，性能可接受                                     |
| 大量骨骼 Collider 动态更新 | 使用 Animation Rigging 或 Physics Proxy（通过 Rigidbody Attach） |
| 动态形变体积             | 不能用刚体 + Collider 实现，需用 MeshCollider 或自定义体积算法              |
| 碰撞包跟随动画            | 在 LateUpdate 中同步局部位姿到 Collider                            |
