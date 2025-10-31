# Animator.applyRootMotion 与 Animator IK 回调无关，但两者常配合使用

## 一、两者的概念区别

| 概念                         | 作用对象                        | 控制内容             | 谁来决定它的值                                  |
| -------------------------- | --------------------------- | ---------------- | ---------------------------------------- |
| **Root Motion**            | 动画根节点（通常是 Hips 或 Root Bone） | 角色整体的**位置和朝向移动** | 动画曲线中记录的位移 + `Animator.applyRootMotion`  |
| **IK（Inverse Kinematics）** | 末端骨骼（如脚、手）                  | 角色**四肢关节的反向调整**  | Animator 内部 IK Solver 或 `OnAnimatorIK()` |

简单来说：

* Root Motion 控制**“整个人走到哪里”**；
* IK 控制**“脚放在哪里、手摆哪里”**。

## 二、两者的独立性

### **Animator.applyRootMotion**

是一个布尔属性：

```csharp
animator.applyRootMotion = true;
```

表示是否将动画中的 **Root Transform** 位移应用到 GameObject 上。

* 如果为 `true` → Animator 根据动画中的 Root 位移来移动整个角色；
* 如果为 `false` → 角色不会随动画移动，你可以手动用脚本移动它。

它只影响 **GameObject 的整体 Transform**（`position` 和 `rotation`），不会对骨骼、IK 或四肢产生影响。

### **Animator IK 回调**

指的是：

```csharp
void OnAnimatorIK(int layerIndex)
```

你可以在其中使用：

```csharp
animator.SetIKPosition(AvatarIKGoal.LeftFoot, somePosition);
animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, 1f);
```

来动态调整脚或手的位置。

它只影响**骨骼链的局部姿态（pose）**，不会自动改变角色整体的 `Transform`。

## 三、为什么说它们“无关”

因为：

* `applyRootMotion` 控制的是角色**整体运动**；
* IK 控制的是**局部关节姿态**；
* Unity 在动画评估流程中，它们属于两个不同阶段的处理逻辑。

简化的执行顺序如下：

```text
1️⃣ 动画采样 AnimationClip
2️⃣ 应用 Root Motion（若 enabled）
3️⃣ 计算 IK（包括 Apply Foot IK 或 OnAnimatorIK）
4️⃣ 更新骨骼姿态到 SkinnedMeshRenderer
```

→ 所以 IK 的调整不会改变 Root Motion 的轨迹，Root Motion 的位移也不会影响你在 IK 中手动设定的骨骼位置。
它们是两个**独立的系统**。

## 四、为什么它们“常配合使用”

虽然它们独立，但常常需要**一起用来实现自然的动作**。

举例：

* 一个行走动画带有 Root Motion（让角色向前移动）；
* 同时你希望脚步能够准确贴合地面（避免穿插或悬空）；
* 此时就会：

  ```csharp
  animator.applyRootMotion = true;
  void OnAnimatorIK(int layerIndex)
  {
      // 检测地面
      // 调整脚部位置
      animator.SetIKPosition(...);
  }
  ```

这样：

* Root Motion 负责“走”；
* IK 负责“贴地”。

如果关掉 Root Motion，只靠 IK 调整脚姿态，角色并不会移动位置；
如果只开 Root Motion 而不做 IK，脚可能会穿地或悬空。

所以两者虽然“无直接依赖关系”，但在实践中往往“成对出现”。

## 五、总结对比

| 项目            | Animator.applyRootMotion | Animator IK（或 Apply Foot IK）        |
| ------------- | ------------------------ | ----------------------------------- |
| 控制目标          | 整个角色的位移与旋转               | 局部骨骼（手、脚等）的姿态                       |
| 执行阶段          | 动画评估的前半段                 | 动画评估的后半段                            |
| 是否相互影响        | ❌ 否                      | ❌ 否                                 |
| 常见用途          | 让动画驱动角色移动                | 让四肢贴合目标（地面、物体）                      |
| 是否依赖 Humanoid | 可选（Generic 也可）           | 仅限 Humanoid                         |
| 是否可手动控制       | ✅ 脚本开启或关闭                | ✅ 在 `OnAnimatorIK()` 或 Playables 设置 |


**一句话总结：**

> `Animator.applyRootMotion` 控制角色整体的移动，
> `Animator IK` 控制局部的肢体调整。
> 二者内部机制无关，但常搭配使用以实现“会走又贴地”的自然动画。

# Animator IK 总是开启的吗

非常好的问题，这一点很关键，因为很多人以为 `OnAnimatorIK()` 是 “系统每帧都会调用” 的，但其实——**不是的**。
👉 `Animator.OnAnimatorIK()` 并不是总是开启，它只有在**特定条件**下才会被 Unity 调用。

下面我来完整解释它的触发条件、控制方式和常见误区 👇

## 一、`OnAnimatorIK()` 是什么

`OnAnimatorIK(int layerIndex)` 是 `MonoBehaviour` 的一个可选回调函数。
它在 **Animator 更新动画帧的最后阶段** 被调用，用于让你手动修改骨骼姿态（例如脚、手等末端骨骼）的位置或旋转。

```csharp
void OnAnimatorIK(int layerIndex)
{
    // 在这里设置手、脚的 IK 位置和旋转
}
```

## 二、触发条件（最重要）

Unity 只有在 **以下条件都满足时** 才会调用 `OnAnimatorIK()`：

| 条件                                                                              | 说明                                           |
| ------------------------------------------------------------------------------- | -------------------------------------------- |
| ✅ 1️⃣ `Animator` 组件处于启用状态 (`enabled = true`)                                    | 否则整个 Animator 都不会更新                          |
| ✅ 2️⃣ `Animator.updateMode != AnimatorUpdateMode.AnimatePhysics` **或** 已在物理步中更新 | 如果使用 `AnimatePhysics`，必须在物理帧中调用              |
| ✅ 3️⃣ 该 Animator 所驱动的对象有一个 **激活的脚本**，并且该脚本中定义了 `OnAnimatorIK()`                 | 没定义或被禁用的脚本不会触发                               |
| ✅ 4️⃣ Animator 控制的是一个 **Humanoid Avatar**                                       | 只有 Humanoid 模型支持 Unity 内置 IK（Generic 模型不会触发） |
| ✅ 5️⃣ 在 Animator Controller 中 **启用了 IK Pass**                                   | （重点！）每个 Layer 都有一个 "IK Pass" 复选框，必须开启。       |

## 三、关键条件详解：IK Pass

这往往是最容易忽略的一点。

在 Animator Controller 中：

1. 选中你的 Animator Layer；
2. 在右侧 “Layer Settings” 里；
3. 勾选 **“IK Pass”**。

路径：

> Animator Controller → Layers → [Base Layer] → “IK Pass” ✅

如果不勾选它，那么：

* 即使你的脚本有 `OnAnimatorIK()`；
* 即使你在里面写了 `SetIKPosition`；
* Unity 也**不会调用这个回调函数**。


## 四、验证方法

可以用简单代码验证是否被调用：

```csharp
void OnAnimatorIK(int layerIndex)
{
    Debug.Log("OnAnimatorIK called on layer " + layerIndex);
}
```

如果控制台没输出，说明：

* 要么你的 Animator 不是 Humanoid；
* 要么没勾选 IK Pass；
* 要么 Animator 被禁用了；
* 或者该脚本所在 GameObject 没被激活。

## 五、执行顺序

Animator 的更新顺序大致如下：

```
1️⃣ 采样动画（AnimationClip 数据）
2️⃣ 应用 Root Motion（如果 applyRootMotion = true）
3️⃣ 应用 Foot IK（如果 Animation State 勾选 Apply Foot IK）
4️⃣ 调用 OnAnimatorIK() —— 可手动设置手、脚、头等 IK 位置
5️⃣ 输出最终骨骼姿态到 SkinnedMeshRenderer
```

所以：

* Apply Foot IK → 是自动 IK；
* OnAnimatorIK → 是你自定义 IK；
  两者**不会冲突，但会按顺序叠加**。

## 六、常见误区

| 误区                                      | 实际情况                           |
| --------------------------------------- | ------------------------------ |
| ❌ “OnAnimatorIK 每帧都会自动调用”               | 只有启用 IK Pass 的 humanoid 动画层会触发 |
| ❌ “可以用 OnAnimatorIK 控制 Generic 模型”      | 不行，只对 Humanoid 生效              |
| ❌ “OnAnimatorIK 会覆盖动画”                  | 它在动画之后执行，但权重可控，不会完全覆盖          |
| ❌ “Apply Foot IK 和 OnAnimatorIK 是同一个东西” | 不同。前者是自动修正脚姿态，后者是开发者手动控制       |

## 七、总结表

| 项目                              | 是否影响 OnAnimatorIK 调用 |
| ------------------------------- | -------------------- |
| Animator.enabled = false        | ❌ 不调用                |
| Animator Avatar 不是 Humanoid     | ❌ 不调用                |
| Animator Controller 没勾选 IK Pass | ❌ 不调用                |
| 脚本未定义 OnAnimatorIK              | ❌ 不调用                |
| 脚本禁用或 GameObject 未激活            | ❌ 不调用                |
| 满足所有条件                          | ✅ 每帧调用一次（在动画评估末尾）    |

✅ **一句话总结：**

> `OnAnimatorIK()` 不是一直启用的；只有当 Animator 是 Humanoid 且动画层勾选了 “IK Pass” 时，Unity 才会在每帧动画更新的最后阶段调用它。

# Animation Rigging 的 TwoBoneIK 或 ChainIK 可以完全取代 OnAnimationIK 吗

> ✅ **大部分情况下，Animation Rigging 的 IK 可以功能上完全取代 `OnAnimatorIK()`**，
> 🚫 **但机制上它们并不等价** —— 在执行时机、可扩展性、控制粒度和性能开销上存在明显差异。

## 一、两者的定位与原理差异

| 对比项   | `OnAnimatorIK()`                             | Animation Rigging (TwoBoneIK, ChainIK 等)         |
| ----- | -------------------------------------------- | ------------------------------------------------ |
| 所属系统  | **Animator 内置 IK 系统**                        | **Animation Rigging 扩展包**                        |
| 生效前提  | Humanoid 模型 + Animator Controller 启用 IK Pass | 任意 Rig 类型（Humanoid 或 Generic）                    |
| 执行时机  | 动画评估的**最后阶段**（在动画姿态之后）                       | RigBuilder 构建的 **Rig Graph** 执行在动画后、约束链内         |
| 控制方式  | 代码中用 `SetIKPosition/Rotation`                | 在场景中搭建 Constraint 组件（可动画化）                       |
| IK 算法 | Unity 内部的固定算法                                | 可扩展的多种约束算法（TwoBoneIK、MultiAim、DampedTransform 等） |
| 精度与控制 | 简单、固定（单层 IK，手或脚）                             | 高度可控（层级混合、权重可动画化）                                |
| 可视化   | ❌ 无场景可视反馈                                    | ✅ 可视化 Gizmo、实时编辑                                 |
| 可动画化  | ❌ 不可（纯代码）                                    | ✅ 可被 Timeline / AnimationClip 驱动                 |
| 可扩展性  | ❌ 封闭式黑箱                                      | ✅ 模块化、可自定义 Constraint                            |

## 二、从功能角度来看：能否替代？

### TwoBoneIKConstraint —— 完全覆盖传统 Foot / Hand IK 功能

`TwoBoneIK` 对应一个标准两节骨骼链（如大腿 + 小腿 + 脚，或上臂 + 前臂 + 手）。

可以做到：

* 手/脚精准贴合目标；
* 支持中间关节弯曲方向（Pole Target）；
* 支持实时调整权重；
* 可与地形射线检测配合实现动态贴地。

这些正是你在 `OnAnimatorIK()` 里手动写代码实现的全部功能。

**所以功能层面，它确实可以完全取代 `OnAnimatorIK()`。**

### ChainIKConstraint —— 扩展 Beyond Animator IK

`ChainIK` 可以作用于任意长度骨骼链（>2 bones），
而 Unity 内置的 `OnAnimatorIK()` 仅能控制 **手、脚（4个 AvatarIKGoal）和头看向（LookAt）**。

所以 **Animation Rigging 甚至功能更强**：

* 你可以控制尾巴、触手、绳子等；
* 可用于机械臂、蛇形体等非人形结构。

## 三、但机制上差异明显（不能简单混用）

| 方面                           | OnAnimatorIK                        | Animation Rigging                                    |
| ---------------------------- | ----------------------------------- | ---------------------------------------------------- |
| **执行顺序**                     | 动画采样 → Apply Foot IK → OnAnimatorIK | 动画采样 → (Animator 输出 Pose) → RigBuilder 求解 → 输出到 Mesh |
| **是否依赖 Animator Controller** | 必须有 Animator Controller + IK Pass   | 只要有 Animator 或 PlayableGraph 都可                      |
| **是否能与 Playables 一起用**       | ❌ 很受限                               | ✅ 天然支持 Playables、Timeline                            |
| **是否支持多 Rig 层混合**            | ❌ 不支持                               | ✅ Rig Layer 可叠加、可动画化                                 |
| **是否能独立运行在非 Humanoid 模型**    | ❌ 不行                                | ✅ 支持 Generic / Creature / 机械骨骼                       |

## 🧠 四、什么时候仍可能选择 `OnAnimatorIK()`

虽然 Animation Rigging 功能更强，但 `OnAnimatorIK()` 仍有一些 **轻量化场景** 优势：

| 场景                              | 推荐方案             | 原因                       |
| ------------------------------- | ---------------- | ------------------------ |
| 临时脚本控制（测试用）                     | `OnAnimatorIK()` | 写几行代码即可，不需额外组件           |
| 需要实时响应（例如 AI 手伸向目标）             | 两者皆可             | 但 Animation Rigging 更平滑  |
| 低端平台 / 旧项目迁移                    | `OnAnimatorIK()` | 无需依赖 Animation Rigging 包 |
| 需要与 Animator State Machine 深度绑定 | `OnAnimatorIK()` | 内置流程简单易集成                |

## 五、性能差异

| 项目    | OnAnimatorIK | Animation Rigging             |
| ----- | ------------ | ----------------------------- |
| 执行频率  | 每帧一次（每层一次）   | RigGraph 可有多个 RigLayer，每层独立评估 |
| 计算复杂度 | 很低（少量矩阵求解）   | 较高（依赖 Burst/Jobs，性能可接受但有调度成本） |
| 可优化性  | 只能禁用 IK Pass | 可按层权重裁剪或关闭 RigBuilder         |

总的来说，**Animation Rigging 计算更多但更可控**。在现代项目中，一般不会成为瓶颈。

## 六、总结表

| 对比维度        | OnAnimatorIK  | Animation Rigging |
| ----------- | ------------- | ----------------- |
| Humanoid 依赖 | ✅ 是           | 🚫 否              |
| 可视化         | 🚫 无          | ✅ 有               |
| 可动画化        | 🚫 否          | ✅ 可               |
| 可扩展性        | 🚫 固定         | ✅ 自定义约束           |
| 用途范围        | 手、脚、头 LookAt  | 任意骨骼链             |
| 执行时机        | Animator 更新阶段 | RigBuilder 执行阶段   |
| 性能          | 更轻            | 稍高，但并行化           |
| 是否能完全取代     | ⚙️ 功能上 ✅ 可以   | 机制上 🚫 不完全等价      |

## **一句话总结**

> ✅ **Animation Rigging 的 TwoBoneIK 与 ChainIK 功能上可以完全取代 `OnAnimatorIK()`，并提供更强控制、更广适用性和可视化优势。**
> 🚫 但它是基于 Playables 的独立系统，执行时机与 Animator 的 IK 回调不同，无法直接混用。
> 如果是新项目或需要复杂 IK，建议全面使用 **Animation Rigging**；
> 如果只是旧项目轻量贴地或简单脚本控制，`OnAnimatorIK()` 仍然足够。
