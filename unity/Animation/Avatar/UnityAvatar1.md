# Unity Retarget 到新模型，脚没有严格贴合地面（陷入到地面以下，或者悬浮空中）

这其实是 **Unity 动画重定向（Animation Retargeting）** 中最常见、也是最容易让人困惑的现象之一。
出现 “脚陷地 / 悬空” 的核心原因在于：**两个模型的骨骼比例、骨骼初始姿态（Rest Pose / T-Pose）或 Avatar 映射基准不完全一致**。下面我来详细分解 Unity 是怎么做动画重定向的，以及为什么这会导致脚位置偏差。

---

## 🧩 一、重定向原理回顾

Unity 的 Humanoid 动画重定向流程大体如下：

1. **导入源动画（Source Animation）** → Unity 会根据其 Avatar 定义，将动画从具体骨骼空间转换为一个标准化的 “Humanoid Reference Pose” 数据（即动作的抽象人体动作，而不是骨骼的原始变换）。
2. **目标模型（Target Model）** 也有自己的 Avatar，Unity 会根据这个 Avatar，将标准人体的动作重新映射到目标模型的骨骼结构上。
3. 这个过程并不会修改动画文件本身的数据，而是运行时（或导入时）通过 Avatar 的定义动态转换的。

---

## 🦶 二、脚不贴地的常见原因

### **1️⃣ 骨骼比例（Bone Length）不同**

* 源模型与目标模型的腿长、脚踝到地面的距离不同。
* Unity 的重定向是按关节角度驱动的，而不是按“世界空间位置”约束的。

  > → 所以如果两个人体骨骼长度不一样，即使关节旋转完全相同，脚的位置在世界空间上也会不同。
* ✅ **解决方案**：

  * 尽量保持模型的骨骼比例接近；
  * 或者用 **Avatar Mask + IK Pass** 让 Unity 动态校正脚部接触（见后文）。

---

### **2️⃣ Rest Pose / T-Pose 不一致**

* Unity 在构建 Humanoid Avatar 时，会把模型的“骨骼初始姿态”（T-Pose 或 A-Pose）作为映射基准。
* 如果源模型和目标模型的 T-Pose 不一致（比如手臂角度不同，骨盆角度不同），那么重定向时整体姿态就会出现偏移，尤其是：

  * **骨盆（Hips）高度不同 → 直接影响脚部的地面位置。**
* ✅ **解决方案**：

  * 在导入模型前，进入 **Rig → Configure Avatar**；
  * 调整目标模型的 “Pose” 让它的 T-Pose 与源模型完全一致；
  * 确认 Avatar 验证器显示 “Pose is valid”。

---

### **3️⃣ Hips / Root Motion 定义不一致**

* Unity 的动画通常以 **Hips 或 Root Transform** 为动画的根。
* 如果：

  * 源动画的移动信息（Root Motion）保存在 Hips 上；
  * 而目标模型的 Root Transform 在 Hips 上方（如一个 “Root” 骨骼）；
  * 那么动画重定向后，整个身体的地面高度就会被偏移。
* ✅ **解决方案**：

  * 检查 Animator 的 “Root Motion Node”（在 Rig 设置中）；
  * 确保源模型和目标模型使用相同的 Root 骨骼；
  * 或者关闭 Root Motion，用 IK 或 Animation Layer 自行校正脚位置。

---

### **4️⃣ Avatar 映射有误**

* 若 Avatar Mapping 时，脚踝或脚底骨（Foot / Toe）没正确识别；
* 或者方向轴不一致（Y 轴向上 vs Z 轴向前）；

  > → Unity 重定向时就会认为“脚底”不是地面接触点，从而出现悬浮或陷地。
* ✅ **解决方案**：

  * 在 Avatar Configuration 里手动检查：

    * 左右脚的 “Foot” 和 “Toe” 是否映射到正确骨骼；
    * “Bone Orientation” 是否与人体标准一致。

---

### **5️⃣ 缺乏动画后处理（IK 修正）**

* Unity 重定向只保证骨骼的关节角度一致，不保证脚真的踩在地上。
* 如果需要让脚贴地，必须启用：

  * Animator → **Apply Foot IK**；
  * 或者使用 **OnAnimatorIK()** 自定义脚底校正逻辑；
  * 或者在 Animation Rigging 系统中添加 “Two Bone IK Constraint”。

---

## ⚙️ 三、常见修正方式总结

| 问题原因             | 现象       | 修正方法                                 |
| ---------------- | -------- | ------------------------------------ |
| 骨骼比例不同           | 脚悬浮或陷地   | 保持比例一致，或使用 IK 贴地                     |
| T-Pose 不一致       | 姿态歪、脚偏移  | 重新配置 Avatar Pose                     |
| Root Motion 结构不同 | 整体漂浮     | 统一 Root 定义或关闭 Root Motion            |
| Avatar 映射错误      | 单脚歪、旋转异常 | 手动检查并修正骨骼映射                          |
| 缺乏 IK 修正         | 贴地不精确    | 启用 Apply Foot IK / Animation Rigging |

---

## 🔍 四、建议调试步骤

1. 在 Animator 中播放动画，**禁用 Root Motion** 看是否仍然偏离；
2. 打开 **Avatar Configuration**，检查 “Pose” 和 “Mapping”；
3. 观察 **Hips** 和 **Foot Bone** 的世界坐标，确认地面 Y 值；
4. 临时启用 “Apply Foot IK”，看看是否改善；
5. 如果仍然偏差较大，导出两者的骨架长度数据比对。
