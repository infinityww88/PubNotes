# Foot IK 是什么

`AnimationClipPlayable.SetApplyFootIK(bool value)` 是 Unity `Playable` 动画系统（即 Animation Playables API）中的一个接口，用于**控制当前 `AnimationClipPlayable` 是否启用脚部 IK（Foot IK）**。

## 一、接口定义

```csharp
public void SetApplyFootIK(bool value);
```

**命名空间：**

```csharp
UnityEngine.Animations
```

**作用对象：**

```csharp
AnimationClipPlayable
```

## 二、作用原理

在 Unity 动画系统中，**Foot IK**（脚部反向动力学）是一种让脚部自动贴合地面的机制。
它并不是动画本身的一部分，而是 Unity Animator 在播放动画时根据骨骼姿态自动修正的结果。

当你调用：

```csharp
clipPlayable.SetApplyFootIK(true);
```

这会告诉 Unity：

> 在播放该 `AnimationClipPlayable` 时，启用内置的脚部 IK 系统。

这与 Animator Controller 的 **“Apply Foot IK”** 勾选框功能是等价的。
只不过前者用于 **Animation PlayableGraph**（代码控制的动画系统），后者用于 **Animator Controller**（状态机系统）。

## 三、典型使用场景

1. **手动播放动画时开启脚部贴地：**

   ```csharp
   var playableGraph = PlayableGraph.Create();
   var playableOutput = AnimationPlayableOutput.Create(playableGraph, "Output", animator);

   var clipPlayable = AnimationClipPlayable.Create(playableGraph, walkClip);
   clipPlayable.SetApplyFootIK(true);  // 启用脚部 IK

   playableOutput.SetSourcePlayable(clipPlayable);
   playableGraph.Play();
   ```

   → 当 `walkClip` 播放时，角色的脚会自动与地面对齐，而不是严格按照动画曲线。

2. **精细控制不同动画段的 IK：**

   * 对走路动画启用脚部 IK；
   * 对跳跃动画关闭脚部 IK；
   * 对上半身动画无关的 Clip 保持关闭。

## 四、注意事项

| 注意点                      | 说明                                                          |
| ------------------------ | ----------------------------------------------------------- |
| **1️⃣ 必须使用 Humanoid 模型** | 只有人形（Humanoid）动画支持 Foot IK。Generic 动画模型设置此选项不会生效。           |
| **2️⃣ 与动画本身无关**          | 该选项不会修改动画数据，只在播放时计算 IK 修正。                                  |
| **3️⃣ 不会影响上半身骨骼**        | Foot IK 只影响脚部及腿部骨骼链。                                        |
| **4️⃣ IK 精度依赖地面检测**      | 系统会基于内部算法推算“地面”高度，即使场景中没有碰撞体，它仍然会假定脚部贴合虚拟地面（通常是角色当前原点所在平面）。 |

## 五、与 Animator 的对应关系

| Animator Controller                   | Playables API 对应                                          |
| ------------------------------------- | --------------------------------------------------------- |
| Animation State 的 “Apply Foot IK” 复选框 | `clipPlayable.SetApplyFootIK(true)`                       |
| Animator 的 “Foot IK” 全局选项             | `Animator.applyRootMotion` 与 `Animator` IK 回调无关；但两者常配合使用。 |


## 六、总结

| 功能         | 说明                             |
| ---------- | ------------------------------ |
| **方法名**    | `SetApplyFootIK(bool value)`   |
| **作用**     | 控制是否启用 Unity 内置的脚部 IK 校正       |
| **影响范围**   | 当前 `AnimationClipPlayable` 播放时 |
| **适用模型类型** | 仅限 Humanoid                    |
| **常用场景**   | 行走、站立、上下坡等需要脚部贴地的动画            |


# Foot IK 工作原理

Unity Animator 的 **“Apply Foot IK”**（无论是 Animator Controller 里的复选框，还是 Playable API 的 `SetApplyFootIK(true)`）确实表现得像“脚会贴地面”，但很多人误以为它真的在做 **物理射线检测** 或 **地面碰撞检测** —— 实际上 **不是这样**。

下面详细解释它的原理与误区 👇

## 一、误区澄清：Foot IK 并不真的检测地面

> ✅ **Unity 的 Foot IK 不是物理 IK**
> ❌ 它不会对场景地形（Collider、Mesh、Layer 等）进行任何检测。

启用 “Apply Foot IK” 后，Unity **只是根据模型的人形骨架和 Animator 内部的人体描述（Human Description）**，计算一个**合理的脚部支撑姿势**，让脚底更贴近角色的参考平面（通常是 Humanoid 的原点水平面），而不是场景中的实际地面。

也就是说：

* 它**没有用 Physics.Raycast**；
* 它**不需要地面 Collider**；
* 它**也不需要 Layer 或 Tag 配置**。

## 二、原理概述：Humanoid 内部的虚拟地面与反向动力学

当你在 Animator 的 Animation State 上勾选 **Apply Foot IK**，Unity 在内部为该状态启用了一个 **简单的反向动力学求解器（IK Solver）**，它会：

1. 在角色的 Humanoid 定义中找到两只脚的末端（`LeftFoot` 和 `RightFoot`）；
2. 将脚底目标位置“对齐”到角色的**参考平面**（通常是根节点 `Hips` 投影到世界的 Y 平面）；
3. 调整腿部骨骼链（大腿骨、小腿骨、脚骨）的旋转，使脚底贴合该平面；
4. 同时保持上半身姿态尽量不变。

所以它的“地面”其实是一个**虚拟平面（abstract plane）**，并不与场景物理地面对应。

## 三、推测的算法模型（近似逻辑）

假设角色的 `root` 位于世界坐标 `(x, y, z)`，Unity 可能这样计算：

```text
虚拟地面高度 = root.y
```

然后：

1. 若脚底低于该高度 → 向上抬脚；
2. 若脚底高于该高度 → 向下放脚；
3. 再通过 IK 调整大腿、小腿、脚关节角度，让脚底平行于该平面。

所以你会看到：

* 即使角色离地 10 米高，脚部仍然“贴”在一个看不见的平面上；
* 即使没有地面 Collider，脚 IK 仍然生效；
* 但如果角色上半身在做剧烈动作（如跳起），IK 通常被忽略或补偿不足。

## 四、为什么 Unity 要这样设计？

Unity 的 Foot IK 设计目标并不是“物理贴地”，而是：

> 在 **Humanoid 动画重定向** 过程中，修正因为骨骼比例或姿态差异造成的脚底穿插或悬空问题。

例如：

* 源动画是标准人形；
* 目标模型腿短一些；
* 动画导入时启用 “Apply Foot IK”，Unity 会自动调整腿部角度，使脚底仍然在地面附近。

它是一种**动画后处理（pose correction）**，而不是实时物理 IK。

## 五、如果你需要真正的地面检测

那就需要：

1. **使用 Animator IK 回调：**

   ```csharp
   void OnAnimatorIK(int layerIndex)
   {
       RaycastHit hit;
       if (Physics.Raycast(transform.position + Vector3.up, Vector3.down, out hit))
       {
           animator.SetIKPosition(AvatarIKGoal.LeftFoot, hit.point);
           animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, 1.0f);
           // 同理设置右脚
       }
   }
   ```

   这样才能真正检测场景中的地面。

2. 或使用 **Animation Rigging** 包创建自定义 “Foot Placement Rig”；

3. 或第三方 IK 系统（如 Final IK）实现动态脚步贴地。

## 六、总结对比表

| 功能项             | Animator “Apply Foot IK” | OnAnimatorIK / Animation Rigging |
| --------------- | ------------------------ | -------------------------------- |
| 是否检测物理地面        | ❌ 否                      | ✅ 是                              |
| 是否仅作用于 Humanoid | ✅ 是                      | ✅ 可选（支持任意 Rig）                   |
| 主要用途            | 动画姿势微调、重定向修正             | 实时贴地、物理交互                        |
| 可控制程度           | 自动、有限                    | 完全自定义                            |
| 性能开销            | 极低                       | 较高（需要 Raycast 与 IK 求解）           |

**结论：**

> Animator 的 “Apply Foot IK” 只是让 Unity 在播放 humanoid 动画时应用一个**虚拟平面的 IK 修正**，并不会检测或使用场景地面。
> 若要真正根据地形或碰撞体让脚贴地，需使用 `OnAnimatorIK()` 或 Animation Rigging 的 IK Solver。
