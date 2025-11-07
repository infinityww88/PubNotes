ArticulationBody 与 Rigidbody 时完全不同的物理系统（基于 Featherstone 算法的刚体树），但它和普通的 Rigidbody（基于经典刚体求解器） 仍然能互相碰撞、交互。

| 特性   | Rigidbody（传统刚体）                            | ArticulationBody（关节系统刚体）    |
| ---- | ------------------------------------------ | --------------------------- |
| 求解算法 | 基于迭代求解器（Sequential Impulse / Gauss-Seidel） | 基于 Featherstone 算法（树状结构动力学） |
| 结构形式 | 任意连接刚体                                     | 必须组成树结构（无环）                 |
| 稳定性  | 对刚性关节系统不稳定（容易抖动）                           | 针对机械臂、机器人关节优化，高精度稳定         |
| 控制方式 | AddForce/AddTorque                         | 通过关节驱动力、目标位置等物理方式控制         |

# 二者如何交互

Unity 在底层物理接口中（基于 PhysX）做了 求解器桥接（Solver Bridge）：

* 虽然 ArticulationBody 由 Articulation Solver 管理，
* 而 Rigidbody 由 RigidBody Solver 管理，
* 但 Unity 在每一帧物理更新时，会将两者的 接触碰撞（Contact Pairs） 统一注册到同一个 碰撞检测阶段（Narrow Phase）。

然后 Unity 做了两步工作：

1. 碰撞检测统一

   所有 Collider（无论挂在 Rigidbody 还是 ArticulationBody 上）都由同一个 PhysX 碰撞系统管理，所以两者能产生碰撞接触。每个系统按各自的机制解析碰撞，直到再无碰撞。

2. 力反馈桥接

   当 ArticulationBody 与 Rigidbody 发生接触时：

   - PhysX 仍会生成 contact manifold；
   - Unity 会将接触力分配到两边系统；
   - Articulation solver 接收外力（external force），RigidBody solver 也得到相反的力，所以它们在动力学上也能正确相互作用。

总之就是，检测碰撞共用，发生碰撞，就分别按各自的逻辑机制解析碰撞，求解力，直到相互之间没有碰撞。因此它们天然就可以相互交互。

# 这意味着什么

## 可以

- 相互碰撞、推开、压住；
- Articulation Body 会被普通刚体击退；
- 也可以推动普通刚体；
- 都能通过 Physics 接口（如 Physics.OverlapSphere）被检测到。

## 不可以

- 它们的约束系统不兼容（例如 HingeJoint 无法连接 ArticulationBody）；
- 力反馈不是完全精确（因为桥接在 solver 阶段不是完全同步）；
- 在复杂混合系统中可能出现轻微能量漂移或响应延迟。

```
Articulation bodies and rigidbodies are part of the same PhysX simulation and can interact via collisions.
However, joints can only connect bodies of the same type.
```

## 混合使用注意事项

### 1. 不要混合关节系统

- Joint 系列组件（如 HingeJoint, ConfigurableJoint）只能用于 Rigidbody；
- ArticulationBody 的连接是通过父子层级结构形成的树（parent 字段）；
- 禁止用 Joint 去连接 ArticulationBody，否则无效或抛错。

正确：

```
Rigidbody --(HingeJoint)--> Rigidbody
ArticulationBody(parent) --> ArticulationBody(child)
```

错误：

```
Rigidbody --(HingeJoint)--> ArticulationBody
```

但是 Joint 可以连接一个 ArticulationBody 的 root，反过来 ArticulationBody 关节不可以连接任何 Rigidbody。Joint 也不可以连接任何不是 Root 的 ArticulationBody。

### 2. 避免双求解器链路

PhysX 中的 Articulation solver 和 Rigidbody solver 是独立执行的两个阶段。
如果一个系统通过复杂的层级或碰撞与另一个系统强耦合（例如机械臂推着一堆连杆刚体），
会导致 求解顺序不一致 → 出现轻微穿透、力反馈延迟或能量爆炸。

- 机械装置（机器人、机械臂、车辆悬挂系统）尽量全部使用 ArticulationBody；
- 环境与被交互的物体（地面、箱子、球等）使用 Rigidbody；
- 交互点保持简单（单点接触即可）。

尽管 AB 和 RB 可以相互交互，但是交互越简单越好。

### 3. 要让 Rigidbody 成为 ArticulationBody 的子节点

- Unity 在更新 Articulation 时会覆盖子物体 Transform；
- 如果一个 Rigidbody 位于 ArticulationBody 层级之下，会被错误驱动；
- 表现为：抖动、被拉扯、甚至穿透地面。

正确：

```
Root (empty)
 ├─ ArticulationBody_Robot
 └─ Rigidbody_Box
```

错误：

```
ArticulationBody_Robot
 └─ Rigidbody_Box
```

### 4. 物理求解层注意事项

Articulation 求解器默认假定各 link 的质量相对合理（一般 1~100 kg 范围）。
如果关节连接的两个物体的质量差异过大（如 1000x 以上），会导致：

- ArticulationBody 推动时反应迟缓；
- 甚至力反馈不稳定。

保持 ArticulationBody 与交互的 Rigidbody 质量差在 1:10 ~ 1:100 以内。这也给定了物理关节系统质量设计的指南，即应该怎样设定物体的质量大小。

### 5. 使用 Continuous Collision Detection（CCD）

ArticulationBody 默认使用高精度运动积分，但 Rigidbody 默认是离散碰撞检测。
高速运动时（例如机械臂甩动击打刚体），Rigidbody 可能穿透。

建议为 Rigidbody 开启 CCD：

```C#
rigidbody.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
```

### 6. 不要用 Rigidbody.MovePosition() 去“推” ArticulationBody

MovePosition() 属于 kinematic 位移，绕过物理求解器，ArticulationBody 会感知不到外部位移，力反馈失真。

如果要推动机械臂，应：

- 对 ArticulationBody 使用 AddForce() / AddTorque()；
- 或设置 jointDrive.target、jointPosition；
- Rigidbody 则用物理力交互。

### 7. 性能代价

- Articulation Solver 要解整个树结构的方程组；
- 复杂链条的求解成本远高于多个独立 Rigidbody；
- 每帧求解复杂度接近 O(n³)。

建议：尽量保持 ArticulationBody 链路简短（5~10 link），不要几十个。

### 8. 调试时启用 “Gizmos > Articulation Bodies”

可以可视化关节约束、驱动力方向，帮助确认交互力是否合理。

此外，可以在 Physics Debug 视图中观察：

- Contact Pairs；
- Solver Iterations；
- Articulation Substeps。

### 9. 混合场景测试时降低 Time.fixedDeltaTime

Articulation 对时间步长敏感。

推荐使用：

```C#
Time.fixedDeltaTime = 0.005f; // 比默认的 0.02 精细4倍
```

否则高速或强力运动时会产生能量不守恒。

# 总结

| 问题                                    | 原因                                            |
| ------------------------------------- | --------------------------------------------- |
| 为什么 Rigidbody 和 ArticulationBody 能交互？ | 因为它们共享同一个 PhysX 碰撞检测系统，Unity 在求解阶段做了力反馈桥接。    |
| 是否完全兼容？                               | 只能碰撞与力交互，不能用关节或约束混合连接。                        |
| 实际意义                                  | 可以让机器人（Articulation）与普通物体自然交互，例如机械臂推箱子、夹起物体等。 |
|||


| 分类        | 错误做法                              | 正确做法                           |
| --------- | --------------------------------- | ------------------------------ |
| 层级关系      | Rigidbody 挂在 ArticulationBody 子节点 | 分离层级，平级放置                      |
| 关节连接      | Joint 连接 ArticulationBody         | 用 ArticulationBody.parent 构造链  |
| 推动力方式     | MovePosition() 位移                 | AddForce() / targetPosition 驱动 |
| 碰撞检测      | 默认 Discrete                       | 开启 Continuous                  |
| 质量差异      | 超过 1000x                          | 控制在 1:100 内                    |
| Time Step | 0.02f                             | 建议 0.005f                      |
| 混合复杂度     | 大量混合链                             | 明确分层：机械体 vs 环境体                |
