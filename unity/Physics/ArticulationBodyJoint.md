# Aritculationbody  可以在运行时调整它的Anchor Position 和 AnchorRotation 吗，还是只能在创建时初始化一次？

## 一、结论先讲：

> **`ArticulationBody.anchorPosition` 和 `anchorRotation` 只能在创建时设置一次，运行时无法安全修改。**

* Unity 的 **ArticulationBody 是基于树结构（Articulation Tree）** 的刚体系统，
  所有关节锚点（anchor）和约束参数在 **树构建阶段（初始化）** 就被传入底层的 PhysX articulation solver。
* 一旦启用了物理模拟（`Play` 或 `Enable`），这些锚点就会被锁定。

Unity 官方明确说明（来自 `ArticulationBody` API 文档与物理系统设计）：

> “ArticulationBody anchors are defined at creation and cannot be modified at runtime. To change anchors, rebuild the articulation hierarchy.”

## 二、为什么不支持运行时修改？

原因是：

* Articulation 是一个**整体求解系统**，所有 joint 的约束方程一次性建立在求解器内部；
* Anchor 改变意味着整个链的雅可比矩阵（Jacobian）要重新构建；
* PhysX 当前版本（4.x～5.x）**不支持在运行中动态改变 articulation joint anchor**。

要修改它，就相当于要销毁并重新创建 articulation 结构。

## 三、如果确实需要在运行时调整关节锚点，有三种替代方案：

### 方法 1：重建 articulation 链

```csharp
// 停止模拟
myArticulationBody.enabled = false;

// 修改 anchor 参数
myArticulationBody.anchorPosition = new Vector3(0, 0.1f, 0);
myArticulationBody.anchorRotation = Quaternion.Euler(0, 90, 0);

// 重新启用
myArticulationBody.enabled = true;
```

> ⚠️ 这样做只能在非常简单结构下偶尔生效；
> 复杂结构会直接报错或行为未定义（因为底层求解器无法动态重构）。
> 通常要销毁并重新创建整个 articulation。

### 方法 2：在关节下插入一个中间 Transform

如果你只是想**动态偏移锚点位置**（例如调整连接点），可以：

* 保持 ArticulationBody 的 anchor 不动；
* 在 joint 下插入一个子对象；
* 移动该子对象，间接调整连接点相对位置。

```text
Root (ArticulationBody)
 └── JointPivot (empty GameObject)
      └── ChildBody (ArticulationBody)
```

> 移动 `JointPivot` 就能改变子关节的相对连接点，
> 不需要重建 articulation tree，也不会打断求解。

### 方法 3：使用 `xDrive` / `targetPosition` 来模拟 anchor 移动

如果你的需求只是让子关节“移动到一个新的相对位置”，
可以通过驱动参数（`ArticulationDrive.target` 或 `xDrive.targetPosition`）实现。
这是 **推荐的物理安全方式**。

## 四、总结

| 能否修改 | 参数                                | 说明                |
| ---- | --------------------------------- | ----------------- |
| ❌    | `anchorPosition`                  | 运行时修改无效或会破坏求解器。   |
| ❌    | `anchorRotation`                  | 同上。               |
| ✅    | `xDrive.target`, `targetPosition` | 可以安全运行时改变，模拟位置变化。 |
| ✅    | 通过插入额外 transform 间接调整             | 灵活安全，不破坏求解。       |


### 总结一句话：

> 🔹 **`anchorPosition` / `anchorRotation` 是结构参数，只能初始化一次。**
> 🔹 若要动态偏移连接点，要么重建 articulation，要么用中间 transform 来“假移动”。

#  Rigidbody Joint 可以在运行时调整它的Anchor Position 和 AnchorRotation 吗，还是只能在创建时初始化一次？

## 一、结论先说：

> ✅ **Rigidbody 系统的 Joint（如 FixedJoint、HingeJoint、ConfigurableJoint 等）可以在运行时修改 anchor 与 connectedAnchor。**
> 它是**支持实时调整的**，不需要重建整个物理结构。

## 🧠 二、原因与原理

Unity 中的传统刚体（`Rigidbody`）关节系统是基于 **独立约束（constraint）模型** 的：

* 每个 Joint 都是一个独立的“约束组件”，
* 它在每个物理步中单独求解，不依赖全局的“树”结构。

因此，改变它的参数（例如锚点位置、角度、限制范围）只会影响这一约束本身，
不会破坏整个求解体系。

## 三、可在运行时修改的典型参数

| Joint 类型              | 支持运行时修改的关键字段                                                                       | 说明         |
| --------------------- | ---------------------------------------------------------------------------------- | ---------- |
| **HingeJoint**        | `anchor`, `axis`, `connectedAnchor`, `limits`, `useLimits`                         | 都可以随时改。    |
| **ConfigurableJoint** | `anchor`, `connectedAnchor`, `axis`, `secondaryAxis`, 各种 `xMotion/yMotion/zMotion` | 全部可改。      |
| **FixedJoint**        | `anchor`, `connectedAnchor`                                                        | 可以随时更新连接点。 |

修改这些字段时，Unity 会自动更新内部的物理约束定义（PhysX constraint frame），下一帧立即生效。

## 四、注意事项

1. **修改锚点会造成短暂的力冲突**

   * 因为锚点瞬间“跳变”，可能导致下一帧时约束有残余力。
   * 如果希望平滑过渡，可以在几帧内插值修改锚点位置。

2. **不要在 Joint 仍然失效（例如 connectedBody = null）时改参数**

   * 因为 Joint 未连接时，某些物理求解状态会被暂存为无效。

3. **大量实时改动会有性能开销**

   * 每次修改都要重新构建该 Joint 的约束数据。
   * 一般在几十个以内同时改动问题不大。

## 五、和 ArticulationBody 的对比总结

| 特性          | Rigidbody Joint          | ArticulationBody Joint      |
| ----------- | ------------------------ | --------------------------- |
| 求解方式        | 独立约束求解（local constraint） | 全局树状求解（articulation solver） |
| Anchor 是否可改 | ✅ 可在运行时修改                | ❌ 初始化后不能改                   |
| 性能          | 稍慢但灵活                    | 稍快但结构刚性                     |
| 用途          | 普通机械、角色关节、软体连接           | 机器人、机械臂、车辆悬挂等刚性系统           |
| 动态结构调整      | 支持（Destroy / Reconnect）  | 不支持（需重建整个树）                 |

**一句话总结：**

> * `Rigidbody Joint` → 灵活、可实时调整、易于搭建动态结构。
> * `ArticulationBody` → 高精度、刚性结构，但参数几乎都是“只读配置”，初始化后固定。
