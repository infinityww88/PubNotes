# **Unity 内置 IK（Animator 内置 IK）** 与 **Animation Rigging（可编程约束系统）** 的区别和替代关系。

很多人都容易混淆这两者，但其实它们虽然功能重叠（都能做 IK），但**定位完全不同**。

---

## ✅ 简短结论（一句话先讲清楚）

> **Animation Rigging 可以完全取代 Animator 的内置 IK 功能**，而且功能更强、更灵活。
> Unity 官方也推荐：**在新项目中用 Animation Rigging 取代旧的内置 IK。**

---

## 🧩 一、两种 IK 系统的来源与本质区别

| 对比点       | Animator 内置 IK                                     | Animation Rigging                          |
| --------- | -------------------------------------------------- | ------------------------------------------ |
| **来源**    | Unity Animator 自带的传统功能（Mecanim 系统）                 | Unity 的扩展包（com.unity.animation.rigging）    |
| **实现方式**  | 在 `Animator` 的 **OnAnimatorIK()** 回调中，通过代码控制（固定流程） | 基于可视化的 **RigBuilder + Rig Constraints** 系统 |
| **控制层级**  | 运行在 Animator 最后一层的 “IK pass”                       | 可插入 Animator 的任意层，并支持多层混合                  |
| **可定制性**  | 只能控制几种固定的 IK 目标（手、脚、看向方向）                          | 任意骨骼、任意约束、任意数量、可自定义结构                      |
| **兼容性**   | 仅对 Humanoid 有效                                     | 支持 Humanoid、Generic、自定义骨架                  |
| **精度与功能** | 简单、高效，但功能有限（LookAt、FootIK、HandIK）                  | 强大，支持复杂链、动态权重、Constraint、Procedural 动作     |

---

## ⚙️ 二、Animator 内置 IK（旧系统）

### 🧩 特点：

* 在 Animator 导入 Humanoid Rig 时可开启 “IK Pass”；
* 在脚本中实现：

  ```csharp
  void OnAnimatorIK(int layerIndex)
  {
      animator.SetIKPosition(AvatarIKGoal.LeftHand, target.position);
      animator.SetIKRotation(AvatarIKGoal.LeftHand, target.rotation);
      animator.SetLookAtPosition(lookAtTarget.position);
  }
  ```
* 用来实现：

  * 手脚贴物体；
  * 角色注视某方向；
  * 简单脚部 IK（踩地）。

### ⚠️ 局限：

* 只能用于 **Humanoid Rig**；
* 控制的目标是固定的（左/右手脚、头看向）；
* 无法叠加多个 IK 或创建自定义链；
* 无法在 Timeline 或 Animator Graph 中可视化；
* 无法组合其他约束（如 TwoBoneIK + MultiAim 等）。

---

## 🧠 三、Animation Rigging（现代系统）

### 🧩 特点：

* 工作在 Animator 之后，由 `RigBuilder` 组件驱动；
* 可以创建多个 `Rig`，每个 Rig 内可包含多个 `Constraint`；
* 可控制任意骨骼；
* 可在 Timeline、Animator Layer、代码中控制权重；
* 支持多种约束类型：

  * TwoBoneIKConstraint（IK）
  * MultiAimConstraint（看向）
  * MultiPositionConstraint
  * ChainIKConstraint
  * DampedTransform
  * 等等。

### 🧩 优势：

* 支持 **Generic** 模型；
* 可搭配 Timeline 制作程序动画；
* 可做 **手部持物、角色与场景交互、布娃娃混合控制、动态姿态修正**；
* 支持运行时动态权重混合；
* 支持自定义 Rig Constraint（C# 可扩展）。

---

## ⚖️ 四、两者在运行流程上的位置

Unity 动画求解顺序：

```
AnimationClip（Animator 动画输出）
     ↓
Animator IK（旧系统的 IK Pass）
     ↓
Animation Rigging (RigBuilder 执行)
     ↓
最终骨骼姿态输出到模型
```

> 所以 Animation Rigging 实际上可以放在 Animator 之后，对最终骨骼再做二次修正。
> 这意味着它功能上确实是“超集”。

---

## 🚀 五、实际应用建议

| 场景                         | 推荐方案                    |
| -------------------------- | ----------------------- |
| 简单人物看向、脚贴地                 | Animator 内置 IK 足够       |
| 复杂交互（角色抓取物体、武器对齐、身体姿态动态调整） | Animation Rigging       |
| 程序控制的动态 IK（比如动态摄像机跟随姿态修正）  | Animation Rigging       |
| Timeline 中控制 IK 动作         | 只有 Animation Rigging 支持 |
| 非 Humanoid 模型（动物、机器人）      | 只能用 Animation Rigging   |

---

## 🧩 六、一个常见误解

> “Animation Rigging 是 Animator IK 的升级版吗？”

不完全是。
它实际上是一个 **通用的骨骼约束系统（Rig Constraints System）**，
其中只是**包含 IK 作为一种约束类型**。

也就是说：

* Animation Rigging 不只是做 IK；
* 它还可以做 LookAt、Copy Rotation、Parent Constraint、Aim、Multi-Referencing 等；
* 它和 Blender 的约束系统（Constraint System）概念几乎一样。

---

## ✅ 总结一句话：

> **Animation Rigging 完全可以替代 Unity 内置 IK，而且功能更强、更灵活、可扩展，支持 Timeline 和任何骨架类型。**
> 除非你只需要极简单的人形 IK（比如角色注视目标），否则都建议使用 Animation Rigging。
