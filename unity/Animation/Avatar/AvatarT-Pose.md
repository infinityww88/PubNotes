![](FullAvatarMask.gif)

如上图所示，角色跑步动画的初始 Avatar Mask 是全部骨骼都开启（不屏蔽），动画正常播放，无论是在 Inspector Preview 中还是在 Scene 中。

然后为动画选择一个屏蔽全部骨骼的 Avatar Mask，动画会变成双手向前弯曲，双腿向后弯曲的姿势。当 Animator 没有播放任何动画，但是开启了 Rig Builder，模型也会变成这个姿势。这并不是模型的 Rest Pose，这个姿势从何而来？

屏蔽所有骨骼时发生了什么？

## 在 Humanoid Rig 下：

* Unity 不直接使用 FBX 的 Rest Pose。
* Humanoid Clip 是相对于 **Avatar 的 T-Pose（Unity 内部标准骨架姿态）** 的偏移（delta）。
* 当一个骨骼被 Mask 屏蔽时，Unity 仍然会把 **Clip 的偏移应用到 Avatar Root** 的计算中，但忽略骨骼曲线。

这里关键点：

> **Humanoid Clip 的“零帧”姿态不是 Rest Pose，而是 T-Pose + Clip 内部偏移**

因此，当你屏蔽所有骨骼时：

1. 每个骨骼都没有使用 Clip 的旋转。
2. 但 **Humanoid 系统仍会尝试对骨骼进行“标准化”**，生成一个默认姿态。
3. 这个默认姿态通常是 **Clip 的初始帧在 Avatar T-Pose 的偏移结果**，而不是原始 Rest Pose。

结果就是你看到的双手向前、双腿向后的奇怪姿势。

## Generic Rig

对于 Generic Rig：

* 屏蔽所有骨骼时，Unity **没有动画曲线作用**。
* 按理来说应该回到 **模型的 Bind Pose（Rest Pose）**。
* 但如果动画 Clip 中 **Root Motion / Root Transform 仍然存在偏移**，或者 Animator Controller 有层叠动画、状态机 blend，模型仍可能显示偏移姿态。

## 总结原因

| 原因                         | 详细说明                                                                  |
| -------------------------- | --------------------------------------------------------------------- |
| Humanoid 的 Clip 是相对 T-Pose | Clip 内部存储的是相对于 Avatar T-Pose 的 delta，而不是 Rest Pose                    |
| 屏蔽骨骼只阻止骨骼旋转应用              | Root Motion 仍可能影响模型，或者 Humanoid 系统在计算姿态时使用 T-Pose + 初始偏移              |
| 所以屏蔽所有骨骼后                  | 骨骼显示的姿势 = Clip 初始帧的偏移姿态，不是模型原始 Rest Pose                              |
| Generic Rig 时              | 如果 Root Motion 或状态机有作用，也可能出现非 Rest Pose，尤其在 Animator Layer Blend 的情况下 |

## 解决方案 / 验证方法

1. **Humanoid + 全屏蔽 Avatar Mask**

   * 想要回到 Rest Pose，可以创建一个空动画 Clip（T-Pose 或 Bind Pose），然后播放它而不是原 Clip。
   * 或者在 Animator Layer 上关闭该动画层。

2. **Generic + 全屏蔽 Mask**

   * 骨骼会回到模型 Rest Pose，但要确保 Root Motion 不影响位置/旋转。

3. **调试姿态**

   * 打开 **Animation窗口 → Show All Bones**
   * 检查每个骨骼的 Local Rotation 是否有 delta，确认 Humanoid Clip 是否相对于 T-Pose。

## 关键点记忆

> 在 Humanoid 中，Clip 的“零姿态”并非模型原始 Rest Pose，而是 Avatar T-Pose 的偏移；
> 全部屏蔽骨骼后，Unity 仍会显示这个“零姿态”，所以不是 Rest Pose。

# Avatar T-Pose

**Humanoid 动画系统的很多奇怪现象都源于 T-Pose 与 Rest Pose 的关系**。

## 模型的 Rest Pose（Bind Pose）

* **Rest Pose** 是模型在建模软件里**骨骼的默认姿态**。
* 它存在于模型的骨骼网格里，是 FBX/Blend 等文件里 Mesh 与骨骼绑定时的基础姿态。
* 特点：

  * 反映骨骼与顶点的绑定关系
  * 每个骨骼的局部坐标固定，用于计算 skinning
  * Blender/Maya 里通常就是 T-Pose、A-Pose 或者设计者建模姿势

> 换句话说，Rest Pose 是 **模型自身骨骼的真实初始姿态**，和动画无关。

## Avatar T-Pose（Unity 的 Humanoid 专用）

* **Avatar T-Pose** 是 Unity Humanoid 系统在导入模型时**内部生成的标准姿态**。
* 它不是模型原始 Rest Pose，而是 Unity 根据 Humanoid Mapping 自动生成的骨架姿态：

  * 双臂水平展开（X 轴约 90°）
  * 双腿垂直、脚尖向前
  * 面向 +Z 方向
* 目的是提供一个 **跨模型统一的骨骼参考系**，便于动画重定向（Retargeting）。

## Rest Pose 与 Avatar T-Pose 的关系

| 项目     | Rest Pose        | Avatar T-Pose                                                       |
| ------ | ---------------- | ------------------------------------------------------------------- |
| 来源     | 模型原始骨骼           | Unity 根据 Humanoid Mapping 计算                                        |
| 作用     | 绑定 Mesh、定义骨骼初始状态 | 定义 Humanoid 骨骼标准姿态，用于动画重定向                                          |
| 是否一定相同 | ❌ 不一定            | ✅ Humanoid 系统强制为标准 T-Pose                                           |
| 是否可编辑  | 可以修改模型骨骼         | 只能通过 Avatar Definition 设置（Create From This Model 或 Copy From Other） |

**关键区别：**

* **Rest Pose** = 模型真实骨骼初始状态
* **Avatar T-Pose** = Unity 内部标准化姿态，用作动画偏移参考
* 当 Clip 播放时，Humanoid Clip 的旋转是 **相对于 Avatar T-Pose 的 delta**，而不是 Rest Pose。

## 为什么会导致屏蔽所有骨骼时姿势异常

1. Clip 存储的是相对于 **Avatar T-Pose 的偏移**。
2. 屏蔽骨骼时，Clip 的旋转不会应用，但 Humanoid 系统仍会尝试把骨骼摆到 **Clip 初始帧对应的 T-Pose 偏移位置**。
3. 因此，即便你屏蔽了动画，骨骼也不一定回到模型原始 Rest Pose，而是显示 **T-Pose + Clip 初始偏移** → 出现手脚弯曲的奇怪姿态。

## Character is not in T-Pose 有何影响

`Character is not in T-Pose` 或 “不符合 T-Pose” 在 Unity Avatar 配置阶段确实很关键，因为它直接影响 **Humanoid Avatar 是否能成功创建以及能否正确重定向动画**。

###  一、提示 “不符合 T-Pose” 的含义

当你在 **Rig → Configure Avatar** 界面中配置为 **Humanoid** 类型时，Unity 会检测模型当前的骨骼姿态是否满足标准的 **T-Pose 要求**：

标准 T-Pose（Unity 要求）大致为：

* 角色站直；
* 双臂与地面平行，沿 X 轴展开；
* 手掌向下（Z 轴指向前）；
* 双腿与身体成自然站姿；
* 脊柱朝上；
* 头朝前。

如果检测到某些主要骨骼（尤其是上臂、下臂、手、腿）姿态偏离太多，Unity 就会报出：

> ⚠️ “Character is not in T-Pose”

### 二、影响范围

是否会“失败”，要看严重程度：

| 情况                                     | 影响              | 说明                                           |
| -------------------------------------- | --------------- | -------------------------------------------- |
| **轻微偏离**（例如手臂略微下垂、手掌角度不完全水平）           | ✅ Avatar 仍可创建成功 | 但重定向后的动画可能出现轻微错位，如手臂旋转或脚部偏差                  |
| **严重偏离**（例如手臂下垂超过45°、骨骼姿态不对齐、某些骨骼朝向反了） | ⚠️ 可能创建失败       | Unity 无法自动推断人形映射方向，会导致 “Invalid Avatar”      |
| **骨骼朝向混乱或轴不正**（比如骨骼 Z 轴未朝向子骨骼）         | ❌ 必然创建失败        | Unity 无法构建 Humanoid 骨架，直接报红 “Avatar invalid” |

### 三、失败的后果

如果创建失败：

* Unity 会显示：**Avatar invalid**（在 Rig 界面预览图下方出现红色警告）
* “Apply” 按钮会被禁用；
* 该模型的 Rig 类型会退回到 **Generic**；
* 你将无法：

  * 使用 Animator Controller 的 **Humanoid 重定向功能**；
  * 使用 Unity 的 **IK（Foot IK、LookAt IK）**；
  * 使用 **Animation Rigging** 的 Humanoid 约束；
  * 在 Animation Clip 导入选项中使用 “Root Transform” 相关设置。

### 四、解决方式

#### 方法 1：使用 **Enforce T-Pose**

点击 “Enforce T-Pose”，Unity 会自动调整骨骼局部旋转，使角色尽可能接近标准 T 姿态。
如果调整后预览界面变绿（所有骨骼显示正常），则说明修正成功。

#### 方法 2：手动调整

在 “Muscles & Settings” 窗口中可切换到 **Pose** 视图，手动旋转骨骼关节（尤其是上臂、前臂、手掌）来微调到符合 T-Pose。

#### 方法 3：在 3D 软件中修正

如果骨骼朝向本身就错误（例如骨骼 Z 轴不朝向子骨骼），就必须回到 **Blender / Maya** 等 DCC 工具中修正骨骼朝向，然后重新导出 FBX。

### 五、判断 Avatar 是否成功创建

判断是否成功的标志：

* 进入 Avatar 配置界面后，右上角显示：
  ✅ “Valid”（绿色）
  ❌ “Invalid”（红色）
* 或在 Inspector 的 “Rig” 面板里，看到 “Avatar Definition → Create From This Model” 一栏下方显示 “Avatar (Humanoid)” 并且预览小人是绿色的，就表示创建成功。

### 六、总结表格

| 状态          | 是否能创建 Avatar | 影响               |
| ----------- | ------------ | ---------------- |
| 完全符合 T-Pose | ✅ 成功，姿态正确    | 动画重定向稳定          |
| 轻微不符合       | ⚠️ 一般能成功     | 重定向略有偏差          |
| 严重不符合       | ❌ 失败         | 无法使用 Humanoid 功能 |
| 骨骼朝向混乱      | ❌ 失败         | 必须重新导出模型         |

## 总结

* **Rest Pose**：模型本身骨骼的默认姿态（建模时定义）
* **Avatar T-Pose**：Humanoid 系统标准化的姿态，用于跨模型重定向
* **Humanoid Clip**：存储的旋转是 **相对于 Avatar T-Pose** 的增量
* **屏蔽骨骼时显示的姿态** = Clip 初始帧在 Avatar T-Pose 基础上的偏移，而不是模型 Rest Pose

# 创建 avatar 时，为什么希望模型的 pose 接近标准 T 姿态

这其实是 Unity **Humanoid 重定向系统的核心原则**之一。

为什么 Unity 希望模型的 **Pose 接近标准 T-Pose**？简而言之：

> 因为 **T-Pose 是 Humanoid 系统的“统一参考姿态”（Reference Pose）**，所有重定向、肌肉驱动、IK 与动画映射都是基于它计算的。

下面我们一步步展开解释它的原因和机制。

## 一、T-Pose 是 Humanoid 系统的“中立参考姿态”

在 Unity 的 **Humanoid Avatar** 系统中，每个模型在导入时，都会被标准化为一种**统一的人体结构描述**（称为 *Human Description*）。

为了让不同模型之间的骨骼、朝向、动作能对应，Unity 需要一个**共同参考系**。
→ 这个共同参考姿态就是 **T-Pose**。

也就是说，T-Pose 就像一个“世界坐标原点”，所有人体关节的方向和默认旋转都以它为基准。

## 二、T-Pose 的数学意义：定义“零姿态（Zero Pose）”

对于 Humanoid Avatar 而言，T-Pose 是模型的 **零旋转状态（zero rotation）**：

* 每个关节的 **Muscle 值 = 0**
* 每个骨骼的 **local rotation = identity（单位旋转）**
* 这是“肌肉系统”的初始状态（neutral pose）

所以，当 Unity 把动画数据从一个模型（A）重定向到另一个模型（B）时，它的逻辑是：

```
源模型的骨骼旋转 = 源模型当前旋转 * 源模型 T-Pose^-1
目标模型骨骼旋转 = 上式结果 * 目标模型 T-Pose
```

如果模型的 T-Pose 偏差太大（例如手臂放下 30°），那么：

* 逆矩阵计算就会引入误差；
* 重定向后的动画关节会错位（例如手臂下垂过多或上扬）；
* 导致角色姿态怪异或脚手漂浮。

## 三、T-Pose 确保了所有骨骼朝向一致

Unity Humanoid 期望：

* 上臂的本地 X 轴沿着手臂方向；
* 前臂的本地 X 轴也指向手；
* 脊柱沿着 Y 轴；
* 朝前的方向是 Z。

如果模型导入时姿态不是标准 T-Pose（比如 A 形或手臂垂下），那么骨骼的局部旋转与 Unity 预期会有偏移。

这会导致：

* **肌肉控制方向错乱**；
* **动画重定向旋转不匹配**；
* **IK 拉伸方向反了**；
* **镜像姿态错误（左手右手角度不对）**。

## 四、为什么是 T 而不是 A？

你可能会问：为什么 Unity 要选 “T” 而不是 “A” 或 “I”？

因为：

* **T-Pose 最大化了各主要关节的独立性**：手臂与身体完全分开，方便检测肩部方向；
* **关节轴定义最明确**；
* **适配性最好**：所有常见动作（如举手、下垂、转臂）都能从 T 姿态平滑插值；
* **早期 DCC 标准**（Maya、MotionBuilder）中也是以 T-Pose 作为标准参考。

所以它成了业界通用的绑定标准。

## 五、如果偏离 T-Pose，会导致的问题

| 偏离类型         | 影响                               |
| ------------ | -------------------------------- |
| 手臂下垂（A-Pose） | 重定向后手臂角度偏低，举手动作变歪                |
| 手臂上扬（反T）     | 动画中手臂常常超伸                        |
| 脊柱前倾         | 动画整体前倾，行走时身体“塌”下去                |
| 骨骼轴反向        | Unity 无法判断前后方向，导致 Avatar invalid |

## 六、简化理解

你可以把 **T-Pose 想成“坐标校准姿态”**：

所有动画文件都会被转换成“相对 T-Pose 的旋转变化” → 然后再根据目标模型的 T-Pose 恢复到它自己的形态。

这就像把所有地图都对齐到同一个经纬度坐标系，否则无法在不同地区（模型）之间正确定位（重定向）。

## 七、总结

| 项目                 | 说明                             |
| ------------------ | ------------------------------ |
| 为什么需要 T-Pose       | 它是 Humanoid 系统的统一参考姿态          |
| 数学意义               | 定义每个骨骼的零旋转（identity）           |
| 对重定向的影响            | 决定动画旋转映射精度                     |
| 偏离 T-Pose 的后果      | 动画错位、手臂歪斜、IK 异常、Avatar invalid |
| Enforce T-Pose 的作用 | 自动把模型恢复到标准参考姿态                 |

如果你想，我可以画一张示意图（或生成一张图）对比 “模型当前姿态 vs 标准 T-Pose vs 重定向误差” 的视觉效果，这样更直观地理解为什么 T-Pose 是整个系统的“参考零点”。是否希望我帮你生成这张图？
