**“Additive Reference Pose”** 是 Unity 动画系统中较高级的一项设置，主要服务于 **Additive（叠加）动画模式**。
很多人见到它会糊涂，因为它跟普通动画（非 additive）完全没关系。
我们来完整拆解它的含义、作用、以及使用场景。

## 一、Additive 动画模式是什么？

在讲 “Additive Reference Pose” 之前，我们要先理解 “Additive Animation” 概念。

### 普通动画（非 Additive）：

> 每一帧都定义了一个**绝对姿态**。
> 也就是：每个骨骼的旋转、位置都直接替换掉当前状态。

例如：

* “走路”动画：每帧定义角色腿、手、身体的绝对角度；
* 播放后角色的姿态完全由动画决定。

### Additive 动画（叠加动画）：

> 动画记录的是“**相对于某个基准姿态（Reference Pose）**的偏移量”，
> 播放时，这个偏移量会**叠加到当前姿态上**。

也就是说：

* Additive 动画不会替换当前姿势；
* 而是“在现有姿势上加一点变化”。

举例：

* 有个角色在“待机”状态；
* 你想让他“在原地呼吸”；
* 呼吸动画是“胸口上下起伏”的微小动作；
* 如果呼吸动画是 **Additive**，那么它可以“叠加在任意姿势上”（站立、举手、持枪姿势都能叠加）。

## 二、“Additive Reference Pose”的作用

Additive 动画的关键在于：

> 它的每一帧都表示“相对于一个参考姿态的差值”。

这个“参考姿态”就是: **Additive Reference Pose**

## 三、它的具体功能

在 Unity 的动画导入设置中：

> **Additive Reference Pose** 用于告诉 Unity：
> “这段动画的偏移是基于哪一帧的姿态计算的？”

Unity 需要这个参考姿态来计算“每帧相对于它的差值（Δrotation、Δposition）”。

## 四、Additive Reference Pose 的两个主要选项

在 Animation Importer → “Animation” 标签页中，你会看到：

### 1️⃣ **Reference Pose Frame**

> 选择动画中哪一帧作为参考姿态（默认是第 0 帧）。

Unity 会用该帧的骨骼姿态作为基准，
然后计算每一帧与这帧之间的差值。

举例：

* 假设第 0 帧是“站立”；
* 第 20 帧“上身往前倾”；
* 那么第 20 帧的 additive 值 = “前倾角度 – 站立角度”。

### **Reference Pose Clip**（或 “Custom Pose”）

> 你可以使用另一个动画片段的某一帧作为参考姿态。

这适合这样一种情况：

> 当前动画的起始帧不是你想要的参考姿势，
> 而是另一个动作的某一帧才是“中性姿势”。

例如：

* 你有一个“呼吸_additive”动画；
* 它录制时参考的是另一个“Idle”动画的第 5 帧；
* 你就可以在 “Additive Reference Pose” 里选那个 Idle Clip。

## 五、它的计算原理（更技术一点）

在 Additive 模式下，Unity 在导入时会执行类似这样的操作：

```text
delta_rotation = frame_rotation * inverse(reference_pose_rotation)
delta_position = frame_position - reference_pose_position
```

这些 Δ 值就是 Unity 播放时叠加到当前姿态上的变化。

如果 Reference Pose 选错了，比如选成动画末尾的姿势，那整个 Additive 动画会变得错乱（比如全身倾斜或漂移）。

## 六、一个直观例子

假设你做了一个 **呼吸动画**：

* 在第 0 帧：角色静止站立；
* 在第 30 帧：胸部抬起；
* 在第 60 帧：回到原位。

你想让这个呼吸动作“叠加”到任意站立姿势上。
你在 Unity 设置：

| 选项                          | 值        |
| --------------------------- | -------- |
| **Animation Type**          | Humanoid |
| **Motion**                  | Additive |
| **Additive Reference Pose** | Frame 0  |

Unity 会把每帧的变化都视为“相对第 0 帧”的偏移量。
这样无论角色现在举枪、坐下还是走路，都能加上“轻微呼吸”的动作。

## 七、常见误区

| 误区                              | 解释                            |
| ------------------------------- | ----------------------------- |
| “Additive Reference Pose 会修改动画” | ❌ 不会修改原始 FBX，只在导入时计算偏移。       |
| “任意动画都能设成 Additive”             | ❌ 必须是姿态变化小、基于同一姿势的动画，否则偏移不合理。 |
| “Humanoid 模型才能 Additive”        | ❌ Generic 模型也可以，只要数据一致。       |
| “Reference Pose 不重要”            | ❌ 非常重要！选错会导致动画偏移或姿态扭曲。        |

## 八、实际使用建议

| 动画类型          | 是否使用 Additive | Reference Pose 建议 |
| ------------- | ------------- | ----------------- |
| 呼吸、微动、颤抖      | ✅             | 选首帧或中性帧           |
| 攻击、跳跃、翻滚      | ❌             | 无需 Additive       |
| 上半身 recoil 动作 | ✅             | 选 idle 或 aim pose |
| 动捕修正动画        | ✅             | 用原始静止帧作为参考        |

## 九、总结一句话

> **Additive Reference Pose** 告诉 Unity：
> “Additive 动画的所有帧都相对于哪个姿势进行偏移计算。”
> 它决定了动画被叠加到其它动作时的“中性基准”。
