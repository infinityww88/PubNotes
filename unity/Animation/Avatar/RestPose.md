# **Blender → Unity 动画坐标基准一致性** 

当你从 Blender 导出模型（例如 FBX）时，**Rest Pose（静止姿态）会被导出到 Unity**。

Unity 会在导入模型时把它记录为 **“Bind Pose”**（绑定姿势）或 **骨骼初始姿态**。

> 动画片段中的关键帧只是“相对于 Rest Pose 的变换偏移”，
> Unity 会通过导入的骨骼 Bind Pose 还原出每帧的最终姿态。

---

## 🧩 一、Blender 动画的本质：基于 Rest Pose 的偏移

在 Blender 中：

* 骨架（Armature）的每个骨骼都有一个 **Rest Pose**（也叫 Bind Pose）。
* 动画关键帧（无论是 Location / Rotation / Scale）记录的是：

  ```text
  当前 Pose = Rest Pose × 动画变换（关键帧）
  ```
* 因此，Blender 的 `.blend` 文件并不会在动画数据中重复记录骨骼的原始位置，只记录相对偏移。

---

## ⚙️ 二、导出到 FBX 时发生的事

当你从 Blender 导出 FBX 时：

1. **每个骨骼的 Rest Pose（静止姿态）都会被写入 FBX 的骨骼层级中**：

   * 以骨骼的 `bindPoseMatrix` / `Transform` 的形式。
   * 包含位置、旋转、缩放。
   * 这是骨骼在未动画化时的姿势。

2. **动画数据**（关键帧）只导出“相对于 Rest Pose 的变换曲线”：

   * 例如关键帧曲线控制的是 bone 的局部旋转、位置；
   * FBX 不会重复导出整个姿态，只导出变化。

---

## 🧩 三、Unity 导入 FBX 时的处理

Unity 导入 FBX 后，会做以下事情：

1. **创建骨骼层级（Transform 结构）**：

   * 由 FBX 中的 Bind Pose 定义；
   * 这对应 Blender 的 Rest Pose。

2. **建立每个骨骼的初始矩阵**：

   * Unity 内部保存为 `BindPoseMatrix`；
   * 这用于蒙皮（SkinnedMeshRenderer）的逆变换（inverse bind pose）。

3. **解析动画关键帧**：

   * Unity 从 FBX 中读到的动画曲线是相对于骨骼局部坐标的；
   * 然后根据 Bind Pose（初始姿态）进行组合，得到最终姿态。

所以：

> Unity 在导入时确实获得了 Rest Pose，并以 Bind Pose 的形式保存。
> 动画片段才能正确地“相对化”地驱动模型骨骼。

---

## 🧠 四、如果没有导入 Rest Pose，会发生什么？

如果没有正确导出 / 导入 Rest Pose（例如导出错误）：

* 骨骼的初始位置会错乱；
* 动画播放时会出现：

  * 整体漂移；
  * 旋转轴不对；
  * 动作姿态扭曲；
  * 关节翻转等问题。

这类错误通常出现在：

* Blender 中修改了骨骼姿态但没 Apply Rest Pose；
* 或导出时选项错误（如 `Apply Transform` 选项导致 Rest Pose 改变）。

---

## 🧩 五、Humanoid 与 Generic 的差异

| 类型               | Rest Pose 用法                               | Unity 的处理方式                              |
| ---------------- | ------------------------------------------ | ---------------------------------------- |
| **Generic Rig**  | 动画直接基于导入的 Bind Pose（即 Blender 的 Rest Pose） | Unity 保留骨骼 Transform，直接播放关键帧             |
| **Humanoid Rig** | 导入时 Unity 会分析 Rest Pose，生成 Avatar 映射       | Rest Pose 被用来确定人形骨骼的 T-Pose，并转换为标准人形骨架空间 |

对于 **Humanoid** 模型，Rest Pose 会参与计算标准化的 T-Pose；
对于 **Generic** 模型，Rest Pose 就是动画的参考零姿态。

---

## 🧩 六、验证方式（你可以实验）

### ✅ 实验 1：查看 Unity 中的 Rest Pose

* 导入一个 FBX 模型（Generic）。
* 在 `Scene` 里展开模型骨骼层级。
* 如果关闭 Animator，再看每个骨骼 Transform 值，就是导入时的 Rest Pose。

  > 它和 Blender 的 Rest Pose 完全一致。

### ✅ 实验 2：清空动画

* 在 Unity 中将 Animator 暂停在 0 帧（无动画状态）。
* 模型保持的姿态，就是从 FBX 导入的 Rest Pose。

---

## ✅ 总结一句话：

> **Blender 导出的 FBX 中包含了每个骨骼的 Rest Pose（作为 Bind Pose）。Unity 在导入时保存这些数据，用作动画应用的坐标参考。动画关键帧只记录相对于该 Rest Pose 的局部偏移。没有 Rest Pose，动画就无法正确复现姿态。**
