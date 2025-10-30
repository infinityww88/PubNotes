# Unity Avatar 重定向的工作原理

Unity 的 **Avatar 动画重定向（Animation Retargeting）** 是 Unity Mecanim 系统的核心功能之一，用于让**同一套动画数据（动作）在不同角色模型之间共享和复用**。
下面我会系统地讲清楚它的 **原理、流程、关键机制和常见误区**。

## 一、基本概念：Avatar 与 Retargeting 的目标

在 Unity 中，动画文件（例如 FBX 内的 AnimationClip）并不是直接绑定到模型的具体骨骼上，而是通过一个叫做 **Avatar** 的中介结构来实现通用化。

**目标：**

> 不同角色（比例不同、骨骼命名不同）也能使用相同的动画。

为此，Unity 在导入模型时会生成一个 **Avatar**，它建立了：

* 模型骨骼层级（Transform Hierarchy）
* 与 Unity 标准人形骨架（Humanoid Rig）之间的对应关系

这个对应关系就是“骨骼映射”（Human Bone Mapping）。

## 二、Mecanim 重定向的基本工作流程

当一个 Humanoid 动画在另一个 Humanoid 模型上播放时，Unity 会经历以下步骤：

### 源动画模型的 Human Pose 提取

从动画文件（或 Animator Controller 的动画 Clip）中读取每一帧：

* 不是直接用骨骼的局部旋转；
* 而是通过源 Avatar 的映射关系，把这些旋转、位移信息转化为一种通用格式——
  👉 **Human Pose（人形姿态）**

Human Pose 是 Unity 内部定义的一组“标准人体骨骼姿态参数”，比如：

```
Spine rotation, LeftUpperArm rotation, RightLowerLeg rotation...
```

这些参数不依赖具体模型结构。

### Human Pose 到目标 Avatar 的骨骼转换

接着 Unity 通过目标模型的 Avatar，把这组“通用姿态参数”重新投射（retarget）到目标角色的骨骼上：

* 计算目标角色每个骨骼的局部旋转；
* 根据目标模型骨骼比例自动调整动作幅度；
* 最终得到能驱动目标骨骼动画的 **骨骼局部矩阵（Transform）序列**。

换句话说：

> **Animation Clip → 源 Avatar → Human Pose → 目标 Avatar → 目标角色骨骼动画**

## 三、Avatar 的内部结构

一个 Avatar 文件包含两个核心部分：

1. **Skeleton Definition**（骨架定义）

   * 角色模型的骨骼层级、名字、BindPose。

2. **Human Description**（人形定义）

   * 骨骼与标准人形骨骼的对应关系（head、spine、leftUpperArm...）
   * 人体比例、T-Pose 信息等。

Unity 通过这两个部分来实现统一的骨骼空间。

## 四、Retargeting 的坐标与比例调整机制

Unity 做重定向时需要解决两个关键问题：

### 坐标系差异

不同模型的骨骼方向、Roll 值、Rest Pose 不同。
Avatar 在导入时会计算一个 **骨骼到标准姿态（T-Pose）** 的旋转偏移矩阵，用于校正方向。

### 比例差异

Unity 根据 Human Pose 的“标准化骨骼长度”重新缩放动作。
比如：

* 动画中抬手到头顶；
* 短手的人模型也能刚好抬到自己的头顶。

这就是 **动画动作与模型比例无关** 的原因。

## 五、Humanoid vs Generic 的区别

| 类型           | 是否支持动画重定向 | 用途               |
| ------------ | --------- | ---------------- |
| **Humanoid** | ✅ 支持      | 用于人形角色（自动匹配关节）   |
| **Generic**  | ❌ 不支持     | 自定义骨架（动物、机器人、武器） |

Generic Rig 的动画只能在完全相同的骨骼层级上播放；
Humanoid Rig 的动画可以跨模型共享。

## 六、常见细节与误区

| 情况                         | 说明                                |
| -------------------------- | --------------------------------- |
| 🔹 骨骼映射错误                  | 导致 Avatar 无法创建或动作扭曲               |
| 🔹 角色不是标准 T-Pose           | 影响重定向的姿态精度                        |
| 🔹 动画中有 Root Motion        | Unity 会用 Avatar 的 Root 定义决定整体移动方向 |
| 🔹 Facial / Hand bones     | Unity Humanoid 默认不包含表情骨、手指以外的小骨骼  |
| 🔹 Retarget 到不同性别或比例差异大的人物 | 需要微调 Avatar 或添加 Avatar Mask       |

## 七、简化理解

你可以把整个系统理解成这样：

> **动画文件的骨骼姿态** → 转换成 **标准人体的动作描述** → 再根据 **目标模型的骨架比例和方向** → 计算出 **目标骨骼的姿态**。

类似于：

> 翻译语言 A → 译成“通用人体语义” → 翻译成语言 B。

## 八、附加知识：HumanPoseHandler

在脚本层面，Unity 提供了一个类：

```csharp
var handler = new HumanPoseHandler(avatar, transform);
HumanPose pose = new HumanPose();
handler.GetHumanPose(ref pose);  // 从角色获取姿态
handler.SetHumanPose(ref pose);  // 应用姿态到另一个角色
```

这就是手动访问和应用重定向的接口。

---

# Unity 是如何把动画文件的骨骼姿态转换成标准人体动作（Human Pose）的？它会不会修改动画文件？


> ✅ 这个过程由 **Unity 的 Mecanim 动画系统（Animation Retargeting 引擎）在运行时动态完成**，
> 🚫 Unity **不会修改动画文件本身的数据**（无论是 FBX、anim、还是 Clip）。

下面详细拆解一下。

## 一、转换过程由谁完成

在 Unity 中，这个“骨骼姿态 → 标准人体姿态”的过程由以下模块协同完成：

| 模块                                   | 作用                                                |
| ------------------------------------ | ------------------------------------------------- |
| **AvatarBuilder**（导入阶段）              | 读取模型骨骼结构并建立骨骼到标准人形骨架的映射（HumanDescription）         |
| **Mecanim Retargeting Engine**（运行阶段） | 在播放动画时，把动画曲线数据转换为“Human Pose”参数                   |
| **HumanPoseHandler**（可脚本访问）          | 提供运行时访问/修改 Human Pose 的接口（底层其实也是调用 Mecanim 的内部流程） |

所以整个过程不是在导入文件时改动数据，而是：

> **导入时生成映射关系 → 播放时实时计算重定向**

## 二、Unity 的数据流：什么时候发生什么

### 1️⃣ 导入阶段（Import）

当你导入一个带动画的 FBX 时：

* Unity **读取原始骨骼动画曲线**（rotation/position/scale）
* 并 **生成 Avatar**（存放 Human Mapping）
* **AnimationClip 仍然保存的是原始骨骼空间数据**，比如：

  ```
  BoneName.rotation.x / .y / .z / .w
  ```

  它不会被改写成“Humanoid”姿态。

### 播放阶段（Runtime）

当动画通过 **Animator（设置为 Humanoid 类型）** 播放时：

* Mecanim 引擎实时将 Clip 中每帧的骨骼数据
  转换成 **标准人形坐标系（Human Pose）**
* 然后再从 Human Pose 转换到当前目标 Avatar 的骨骼姿态

整个过程在内存中完成，不会回写或改变 AnimationClip 数据。

可以理解为一个实时的“双向映射”：

```
骨骼空间 <--> Human Pose <--> 目标骨骼空间
```

## 三、举个更直观的例子

假设你有：

* 源动画文件：[Man_A@Walk.fbx](mailto:Man_A@Walk.fbx)
* 目标模型：Woman_B.fbx

导入后：

1. Unity 为两者各自生成一个 Avatar（Man_A Avatar、Woman_B Avatar）；
2. 动画 Clip（Walk）仍然是“Man_A 骨骼空间”的原始动画；
3. 播放时：

   * Mecanim 把 Man_A 的骨骼动画 → HumanPose；
   * 然后 HumanPose → Woman_B 的骨骼姿态；
   * 最后驱动 Woman_B 的骨架。

👉 注意：
FBX 文件里的骨骼曲线依然保持原样，没有被改动。

## 四、内部计算示意（简化公式）

对于某个骨骼节点：

```
目标骨骼旋转 = AvatarB⁻¹ × (标准人形旋转) × AvatarB
标准人形旋转 = AvatarA × 源骨骼旋转 × AvatarA⁻¹
```

其中：

* `AvatarA` / `AvatarB`：分别是源/目标 Avatar 中记录的骨骼到 HumanPose 空间的变换矩阵；
* Unity 在运行时通过这些矩阵进行实时换算。

## 五、动画文件数据不会变的原因

**原因 1：** AnimationClip 是资源（Asset），Unity 不会在运行时修改任何 Asset 文件。
**原因 2：** 同一 AnimationClip 可以被多个 Avatar 复用，如果修改数据会破坏共享机制。
**原因 3：** 重定向涉及实时比例和方向计算，结果依赖于目标模型比例，不能静态存储。

## 六、如果你需要“静态转换”

如果你确实希望**生成一个新的动画文件**，让它“看起来像是已经针对另一个模型重定向过”的：

* 可以使用：

  * **Animation Baker 工具（Bake To Clip）**
  * 或者 Unity 的 **AnimationUtility** API 手动烘焙；
* 这样 Unity 会把运行时重定向后的骨骼姿态“烘焙”成一个新的 AnimationClip。

这就是 **离线重定向（Bake Retargeted Animation）** 的方式。

## 总结

| 阶段   | 操作主体                       | 是否修改动画文件 | 说明                    |
| ---- | -------------------------- | -------- | --------------------- |
| 导入模型 | AvatarBuilder              | ❌ 否      | 建立 Human 映射，不动原始动画    |
| 播放动画 | Mecanim Retargeting Engine | ❌ 否      | 实时把骨骼姿态转换为 Human Pose |
| 烘焙动画 | 用户/工具                      | ✅ 可选     | 手动生成新动画文件（Bake）       |

# 源模型和目标模型是否都需要进行 avatar 映射

> ✅ **是的，源模型和目标模型都必须有 Avatar 映射（Human Description）**，
> 否则 Unity 无法进行 Humanoid 动画重定向。

下面我们详细讲讲 **为什么必须两个都有**、**Unity 内部是怎么用它们的**、以及**有哪些特殊情况**。

## 一、为什么需要两个 Avatar

Unity 的 Humanoid 动画重定向过程本质上是：

```
源动画骨骼空间  →  HumanPose（标准人形空间）  →  目标骨骼空间
```

而 Avatar 就是实现这两个转换的关键映射表：

| Avatar 角色                    | 作用                                                       |
| ---------------------------- | -------------------------------------------------------- |
| **源 Avatar（Source Avatar）**  | 定义：源模型的骨骼 → 标准人形骨骼 的对应关系。用于将动画数据转化为标准化的人形姿态（Human Pose）。 |
| **目标 Avatar（Target Avatar）** | 定义：标准人形骨骼 → 目标模型骨骼 的对应关系。用于把 Human Pose 应用到目标骨架上。        |

换句话说：

> Avatar 就像“语言翻译字典”。
> 你需要一份“源语言 → 通用语言”的字典，也需要一份“通用语言 → 目标语言”的字典。
> 缺一不可。

## 二、Unity 内部如何使用这两个 Avatar

在播放时，Unity 的 **Mecanim Retargeting Engine** 会做以下事情：

1. 读取源动画（AnimationClip）上的 Avatar 绑定信息；
2. 通过源 Avatar，把动画中每一帧的骨骼姿态 → 转换为 **HumanPose（标准人形姿态）**；
3. 通过目标 Avatar，把 HumanPose → 转换为目标模型骨骼的局部旋转；
4. 最终驱动目标模型的 Animator。

因此，两个 Avatar 是成对工作的。

## 三、如果只有一个 Avatar，会怎样？

### 只有目标 Avatar：

这种情况其实是常见的：

* 当动画 Clip 是 **独立的 .anim 文件**（没有 Avatar）
* 但它来源于某个 Humanoid 动画文件（比如导入时勾选 “Import as Humanoid”）

在这种情况下：

* AnimationClip 内部其实仍然包含了“源 Avatar”的结构信息（HumanPose 曲线）
* Animator 播放时仍然可以找到并用目标 Avatar 来匹配

👉 所以如果 AnimationClip 是 **Humanoid 类型**，即使文件本身没有独立 Avatar 资源，它依然隐式绑定了“源 Avatar”的人形定义。

### 没有目标 Avatar：

如果目标模型的 Animator 没有关联 Avatar：

* Unity 就无法知道目标骨骼对应标准人形的哪些关节；
* 播放 Humanoid 动画时，会报错：

  ```
  Avatar is not valid for Humanoid animation
  ```
* 动作不会播放。

所以目标模型一定要有 Avatar。

### 没有源 Avatar：

如果动画源不是 Humanoid 类型（例如 Generic 或 Legacy）：

* 它的 AnimationClip 不会存有人形映射；
* 那它的动画数据是纯粹的骨骼局部旋转曲线；
* Mecanim 无法把这些曲线转化为 HumanPose；
* 因此 **不能进行重定向**。

除非你手动把该动画文件重新导入并指定 Avatar Definition = “Create From This Model”，使其变成人形类型。

## 四、正确配置方式总结

| 文件类型                            | 是否需要 Avatar                | 说明                               |
| ------------------------------- | -------------------------- | -------------------------------- |
| **源动画 FBX（带动作）**                | ✅ 必须有（用于导入 Humanoid 动画）    | 生成 AnimationClip + 源 Avatar      |
| **目标模型 FBX（要播放动画的角色）**          | ✅ 必须有                      | Animator 会用此 Avatar 播放 HumanPose |
| **.anim 文件（从 Humanoid FBX 导出）** | 🔸 不单独需要，但隐式绑定源 Avatar 的映射 | 仍然可以在任何有 Avatar 的模型上播放           |

## 五、如何检查是否具备 Avatar

在 Unity Project 视图中选择 FBX 或模型文件：

* **Rig 面板**：

  * Animation Type：应设置为 **Humanoid**
  * Avatar Definition：

    * Create From This Model → 表示模型自己定义 Avatar；
    * Copy From Other Avatar → 表示使用别的模型的 Avatar；
  * 下面会显示 **“Configure Avatar” 按钮**，点击可打开人形映射界面。

只要这两者都设置成 Humanoid 并且 Avatar 映射正确，就能进行动画重定向。

## 六、总结一句话

> Unity 动画重定向依赖“Avatar ↔ HumanPose ↔ Avatar”的双向映射。
> 因此源动画和目标模型**都需要 Avatar 映射**。
> 源 Avatar 提供“动画的语义”，目标 Avatar 提供“角色的解读方式”。
