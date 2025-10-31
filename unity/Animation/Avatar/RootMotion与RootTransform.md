动画剪辑与 Root Transform 设置

位移主要由 ​​Root Transform Position XZ/Y​​ 提供；是否把曲线“烘焙进姿势”（Bake Into Pose）会改变“谁来承载位移”（根节点或骨骼曲线）。

例如：不勾选 ​​Root Transform Position XZ​​ 并在曲线里写入位移，可在预览/运行中看到角色移动；勾选后位移不再由曲线提供，而由 Pose/Root 控制。预览窗口对 Root T/Q 的修改在运行期不一定可见，正是这一机制所致。

Animator.ApplyRootMotion 与状态机过渡

启用 ​​Apply Root Motion​​ 时，Animator 会在每帧末尾用动画的 ​​Root Transform​​ 对角色 GameObject 施加一次“后写入”的位移/旋转，常会覆盖你在 Rig/脚本中对上游骨骼做的位置修改。
状态机 ​​Transition Offset​​ 也会在过渡时叠加额外的位移/旋转，属于“后处理”性质的叠加项。

动画导入时，不仅 Humanoid 标准化时会修改原始 clip 的数据，Root Transform Bake 也会改变动画数据。

Humanoid Avatar 中有很多内部机制，不能简单地以 Scene 中的 Transform Hierarchy 理解。

# Root Transform

Root Transform（根变换）是指动画中“角色整体运动的参考坐标系”。
它决定了动画播放时，角色的整体位置和朝向。

在 Unity 的 Humanoid 动画系统（Avatar）中，Root Transform 对应于动画数据中的“整体运动骨骼”，通常是：

- 对 Humanoid：Avatar 中的 Root（不是骨骼，而是 Unity 生成的虚拟根节点）；
- 对 Generic Rig：是你在导入设置中手动指定的一个骨骼（通常是 Hips 或上层骨骼）。

Root Transform 的作用是：

- 表示整个角色在动画中的平移（Position）和旋转（Rotation）；
- 用于在 动画导入（import） 和 重定向（retarget）时统一定义“角色的运动基准”。

# Root Motion

Root Motion（根运动） 是指 Unity 在播放动画时，是否使用动画中记录的 Root Transform 位移/旋转来实际移动角色。

假如有一个奔跑动画，导出时记录了角色 Root 在 Z 方向从 0-3 米的位移，说明角色在1秒内向前跑了 3 米。

* 如果开启了 Root Motion（Animator.applyRootMotion = true），Unity 会把这个 3 米的位移应用到角色的 Root Transform 上，角色会真的向前跑
* 如果关闭了 Root Motion，位移只存在于动画内部（只是骨骼动了），Root Transform 本身不会再世界坐标中移动

简单理解：Root Transform 是“动画数据的根”，Root Motion 是“是否使用这部分运动”。

# 导入设置

在 Animation Import Settings 中的 Root Transform 相关选项，就是控制动画中 Root Transform 的处理方式：

- Bake Into Pose：是否把 Root Transform 的运动烘焙到骨骼中（即，不让 Root Motion 带动整个模型）。
- Based Upon（Original/Center of Mass/Feet）：定义动画导入时以哪种方式确定 Root Transform。
- Offset：允许在导入时手动调整 Root Transform 的初始位置/旋转。

这些选项影响的，是动画片段(.anim)内部 Root Transform 曲线的结果；而 Root Motion 则是运行时是否用这些曲线更新角色的 Root Transform。

例如：

1. 动画数据中，Root Transform 在 Z 轴上移动了 0-3 米
2. Animator 中的 applyRootMotion：

   - 如果开启，Unity 每帧把 Root 的运动应用到角色 GameObject，角色在场景中真的向前移动了 3 米（Transform 被 Animator 修改）
   - 如果关闭，Unity 忽略这段 Root 位移（Animator 不修改 Root Transform），角色只是在原地摆腿


| 项目       | Root Transform             | Root Motion                  |
| -------- | -------------------------- | ---------------------------- |
| 位置       | 动画定义的参考根节点（如 Hips、虚拟 Root） | 是否用动画的位移驱动 Transform         |
| 所属层级     | 动画导入/重定向层                  | Animator 播放层                 |
| 调整方式     | Import Settings 面板         | Animator.applyRootMotion 或脚本 |
| 主要用途     | 决定动画坐标基准                   | 控制角色是否真实移动                   |
| 是否修改动画文件 | 是（影响导入曲线）                  | 否                            |

# Bake Into Pose

Bake Into Pose 是和 Root Motion（根运动）有关的一个选项，用来控制某些根节点动画（比如位移或旋转）是否被烘焙进骨骼姿态本身。

“Bake Into Pose” 的意思是：把特定的根节点运动（Root Motion）烘焙到角色的姿态（Pose）里，而不是留在 Root Transform 上。

换句话说，如果你勾选了某个方向的 Bake Into Pose，则这个方向上的根节点动画将不再体现在 Animator 的 Root Transform 上，而是“烘焙”进各个骨骼的相对姿态中。

在 Unity 的 Animation Importer（模型导入器）的 Rig > Root Transform 部分，你通常能看到以下选项：

* Root Transform Rotation

  * Bake Into Pose
  * Based Upon (Root Node / Original / Center of Mass)

* Root Transform Position (Y)

  * Bake Into Pose
  * Based Upon (Root Node / Original / Center of Mass)

* Root Transform Position (XZ)

  * Bake Into Pose
  * Based Upon (Root Node / Original / Center of Mass)

假设你有一个走路动画：

* 动画文件中，角色的 hips 骨骼在前后移动（前后摇摆）
* 而角色的 root transform（动画中的根节点）也同时向前移动（通常称为 in-place vs with-motion 动画）。

对这个动画：

* 如果勾选 “Bake Into Pose”：

  角色的根节点将保持原地不动（不再前进），而骨骼动画会被调整，使得看起来角色在原地走路。

  也就是说，根节点的运动被“烘焙”到了姿态里。

* 如果不勾选 “Bake Into Pose”：

  根节点会随着动画移动（角色整体往前走），骨骼只是相对根节点摆动。
  
  这时 Animator 的 Root Transform 会随着动画一起移动。

## 与 Root Motino 的关系

Unity 的 Root Motion（根运动）系统使用 Root Transform 上的移动来驱动角色的实际位移。

| 选项状态                     | 结果                               | 用途                 |
| ------------------------ | -------------------------------- | ------------------ |
| **Bake Into Pose = ON**  | 根运动被烘焙到骨骼姿态中，不输出 Root Motion     | 用于原地动作（如 idle、原地跳） |
| **Bake Into Pose = OFF** | 根节点产生 Root Motion，可由 Animator 提取 | 用于行走、奔跑等移动动画       |

## 简单对比

| 场景                  | 是否勾选 Bake Into Pose | 效果                            |
| ------------------- | ------------------- | ----------------------------- |
| 原地走路动画（in-place）    | ✅ 勾选                | 动作看起来在原地走，不会带动角色移动            |
| 向前行走动画（with motion） | ❌ 不勾选               | 动画带有根运动，可以用于 Root Motion 驱动移动 |
| 跳跃上升动画              | Y轴 不勾选              | 让 Root Motion 提供垂直位移          |
| 跳跃落地动画              | Y轴 勾选               | 固定角色位置，只播放落地姿态                |

## 为什么分成三个方向的烘焙

“Bake Into Pose” 在 Unity 动画导入器中不是单一的复选框，而是分成三个方向的类别：

- Root Transform Rotation
- Root Transform Position (Y)
- Root Transform Position (XZ)

这其实反映了 Unity 对“根运动 (Root Motion)”的三个不同维度的独立控制。这可以让你可以分别控制不同方向的 Root Motion 的烘焙。一旦烘焙特定方向（分量）上的运动，Root Transform 在这个方向（分量）上就没有运动，在这个方向（分量）上是静止的。

Unity 在处理根节点（Root Transform）运动时，会将其分解成：

1. 旋转（Rotation）
2. 位置的垂直方向（Y轴）
3. 位置的平面方向（XZ平面）

这是因为一个完整的动作往往在这三个维度上的“根运动”意义不同：

| 维度                | 示例        | 是否通常需要烘焙                   |
| ----------------- | --------- | -------------------------- |
| **Rotation**      | 角色转身、旋转方向 | 通常不烘焙（要提取 Root Motion）     |
| **Position (Y)**  | 跳跃、下蹲、上台阶 | 有时要烘焙（取决于是否要角色真的升高）        |
| **Position (XZ)** | 行走、奔跑     | 通常不烘焙（希望 Root Motion 驱动位移） |

假设你有一个“跳跃并前进”的动画：

- Root 在 XZ 平面 上移动（角色前进）
- Root 在 Y 方向 上上升下降（跳跃弧线）
- Root 还有一定的旋转（面朝方向变化）

如果只给一个全局 “Bake Into Pose”，你没法单独控制：比如，我想让跳跃真的前进，但不想让它真的升高。

因此 Unity 把这三种维度拆开，让你能细粒度地控制：

| 控制项                              | 说明             | 举例                                   |
| -------------------------------- | -------------- | ------------------------------------ |
| **Root Transform Rotation**      | 控制是否将旋转烘焙进姿态   | 若勾选，则角色看起来旋转了，但 Animator Root 不会真的转向 |
| **Root Transform Position (Y)**  | 控制是否将垂直位移烘焙进姿态 | 若勾选，则跳跃看起来会上下动，但实际 Animator Root 不会上升         |
| **Root Transform Position (XZ)** | 控制是否将水平位移烘焙进姿态 | 若勾选，则角色看起来在原地走，Animator Root 不会向前移动           |

它们在动画中的区别：

| 选项状态             | Root Transform 实际运动 | 动作外观              |
| ---------------- | ------------------- | ----------------- |
| 全部不勾选            | Root 随动画前进、旋转、上下浮动  | 动画带完整 Root Motion |
| 勾选 Position (XZ) | Root 不再水平移动（原地走）    | 原地动作              |
| 勾选 Position (Y)  | Root 不再上下移动         | 防止角色浮空或陷地         |
| 勾选 Rotation      | Root 不再旋转           | 角色原地旋转但 Animator Root 朝向不变        |

## Based Upon

每个维度下方还有一个 “Based Upon” 选项，例如：

- Root Node
- Original
- Center of Mass

它定义了在不烘焙的情况下，Root Motion 应该基于哪个参考点提取。

比如角色的“行走方向”可能基于骨骼的原始朝向或实际运动方向。

“Based Upon” 是配合 “Bake Into Pose” 一起使用的关键选项，决定了当不烘焙（即 Bake Into Pose 关闭）时，Unity 从哪里提取 Root Motion。这些 Root Motion 是要记录到 Clip 中 Root Transform 的动画曲线的。如果烘焙，就不需要 Root Transform 的动画曲线了，因为移动或旋转已经被添加到模型骨骼中了。

### Root Transform 的提取流程

当 Unity 导入一个动画时，它需要知道：

“这个动画的根运动（Root Motion）到底是哪个节点的运动？”

动画文件（如 FBX）里通常有一层根节点（root / hips / armature），Unity 需要根据某个基准来提取这个根节点的移动或旋转，用作 Animator 的 Root Motion。

于是它提供了一个选项：

Based Upon（基于什么来确定 Root Transform 的初始参考点）。

1. Original

   根运动基于动画文件中原始的根节点数据。

   Unity 直接使用 FBX 文件中记录的 Root Transform（通常是模型导出时的“根骨骼”或“hips 父节点”）的平移 / 旋转。

   不会进行任何额外的对齐或居中计算。

   适用于：

   - 你的动画文件已经正确定义了根节点的运动。
   - 你希望在 Unity 中保持导出时的运动轨迹。

   例如，Blender 中已经设置好 root 控制器（hips 的 parent bone）移动角色，Unity 会原样使用它的位移与旋转。

2. Root Node

   根运动基于你在 “Root Node” field 中指定的骨骼节点。

   如果 FBX 动画有多层层级骨骼，例如：

   ```
   root
   └── hips
        └── spine ...
   ```

   你可以在 Root Node 下拉框中选择使用 Root 或 Hips。

   Unity 会以你选择的 Bone 为根来提取 Root Motion（就是采样这个 Bone 随时间的 position 和 rotation）。

   适用于：

   - 模型导入后 Unity 没能自动识别正确的 Root。
   - 或者你想人为指定一个不同的骨骼层级来作为根运动的来源。

   例如，如果角色的骨架结构中 hips 才是移动的主要骨骼，而上层 “root” 只是空节点，你可以手动设置 “Root Node = hips”。

- Center Of Mass

  根运动基于角色在每帧的重心（物理上或几何上的中心点）进行提取。

  - Unity 会在每帧计算角色骨骼整体的中心位置（通过骨骼权重或物理近似）
  - 然后把这个中心点作为 Root Transform 的参考。
  - 通常用于动作捕捉（MoCap）导入，特别是没有单独“root bone”的数据。

  适用于：

  - 来自动捕系统的动画，没有明确的 root 节点。
  - 动作中身体重心始终在运动，但文件里没有真正移动的根骨骼。

  例如，一段 mocap 的跳跃动画里，所有骨骼都在动，但没有根骨骼。选 “Center of Mass” 能让 Unity 推算出整体的上升、下降轨迹。

对照表：

| 选项                 | 含义             | 典型用途              |
| ------------------ | -------------- | ----------------- |
| **Original**       | 使用 FBX 原始根节点轨迹 | 有明确定义 root 控制器的动画 |
| **Root Node**      | 使用指定骨骼节点轨迹     | 想手动指定提取的骨骼层级      |
| **Center of Mass** | 使用所有骨骼的中心点运动   | 没有 root 骨骼的动捕数据   |

# Loop Pose

Root Motion 动画提取、Bake Into Pose、Base Upon、Loop Pose 都是动画 Clip 相关，都是在 Animation Tab 页面中。如果模型的 Mesh、骨骼、动画 分开导出到不同的 FBX 文件，那么：

- Mesh 和 Armature 在一个 FBX 文件，因为要为 Armature 定义 Avatar
- 动画片段单独导出到一个文件，它需要 Avatar 进行标准化，选择模型文件中的 Avatar
- Root Motion 相关选项都在 Clip 模型的 Animation Tab 中寻找

Loop Pose 的作用是 ```尝试在动画的首帧与末帧之间自动平滑姿势，以使动画能够无缝循环（Loop）。```

- 它并不会强制性修改动画帧；
- 而是在播放时，让 最后一帧和第一帧之间的过渡更加平滑；
- 目的是让循环动画（如走路、跑步、呼吸等）衔接自然。

| 选项            | 功能                                        |
| ------------- | ----------------------------------------- |
| **Loop Time** | 告诉 Unity 这个动画可以循环播放（Animator 会在播放结束时回到首帧） |
| **Loop Pose** | 让 Unity 调整帧间过渡，使得首尾姿势衔接更平滑，不突变            |

一般来说，如果你想让动画循环播放，就要同时勾选这两个选项。

## 工作原理

Unity 在导入动画时，会分析动画的：

* 骨骼姿态（每个骨骼的旋转与位置）
* Root Motion（根节点的平移与旋转）

然后：

- 检查 首帧 和 末帧 的差异；
- 在播放循环时自动插值或补偿差值；
- 让过渡不产生“抖动”或“瞬间跳跃”。

这不是修改动画数据本身（FBX 文件不变），而是 Unity 播放动画时做的“姿态平滑处理”。

假设你有一段 60 帧的“走路动画”：

- 第 0 帧：角色左脚着地
- 第 59 帧：角色右脚刚抬起，还没回到左脚着地
- 第 60 帧 回到第 0 帧时：姿态不一样 → 看起来“脚一跳”！

如果你勾选：

✅ Loop Time：动画会循环播放；

❌ Loop Pose：循环会出现轻微跳动；

✅ Loop Pose：Unity 会自动调整，使第 59 帧的末姿与第 0 帧姿态平滑衔接，看起来脚连续走动。

Loop Pose 让动画的“首尾姿势”在循环播放时平滑衔接，避免出现突变或跳帧感。它不会修改动画文件，只在播放时做自动姿态补偿。

Loop Pose 不修改动画文件，它会分析第一帧 Pose 和最后一帧 Pose，然后计算一个补偿偏移量，这个补偿偏移量记录到 Clip 中。当 Clip 循环播放，并且播放到两个 Loop 切换时，在当前 Loop 的最后一帧和下一个 Loop 的第一帧分别应用偏移量补偿，使动画看起来是连续的。

Loop Pose 只适用于首帧与末帧的微小差异。如果差异过大，即使应用偏移补偿，仍然突变明显。

## Loop Match 指示器

Loop match 指示器显示动画首尾用于 looping 的质量。红色表示最差，绿色表示最好，黄色为中间状态。

一旦 loop match 指示器为绿色，开启 Loop Pose 会确保 pose 的循环看起来没有瑕疵。

## Loop Pose 的作用范围

| 类型                      | 是否受影响                                  |
| ----------------------- | -------------------------------------- |
| **骨骼动画**                | ✅ 受影响（Unity 会平滑首尾骨骼姿势）                 |
| **Root Motion**         | ✅ 受影响（Unity 会补偿 Root Transform 位置/旋转差） |
| **非骨骼对象（Transform 动画）** | ✅ 同样可以平滑插值                             |
| **动画曲线（float curves）**  | ❌ 不受影响                                 |

## 场景误区

| 误区                           | 解释                                         |
| ---------------------------- | ------------------------------------------ |
| “Loop Pose 会修改原始动画文件”        | ❌ 不会，它只影响 Unity 播放时的内部补偿。                  |
| “Loop Pose 一定能让动画完美无缝”       | ❌ 不一定。如果首尾差太大（比如位置、朝向完全不同），Unity 只能部分平滑。   |
| “Loop Pose 对 Root Motion 没用” | ❌ 有用，Unity 会计算 Root Transform 的平移/旋转差并补偿它。 |

## 使用建议

| 动画类型                | Loop Time | Loop Pose | 说明          |
| ------------------- | --------- | --------- | ----------- |
| 走路 / 跑步 / 呼吸 / 挥手   | ✅         | ✅         | 常规循环动作，建议全开 |
| 攻击 / 跳跃 / 受击        | ❌         | ❌         | 一次性动作，没必要循环 |
| 原地跳跃（想循环播放）         | ✅         | ✅         | 保证首尾姿势一致平滑  |
| 带 Root Motion 的移动动画 | ✅         | ✅         | 确保根运动连续衔接   |

# 总结

“Bake Into Pose” = 把根节点的运动烘焙进动画姿势中，而不是输出给 Root Motion。

无论是 Generic 还是 Humanoid 都有一个 Root Motion 和 Root Transform，动画片段额外记录一个 Root Transform 的运动曲线。运行时 Root Transform 的运动将输出给 Animator GameObject（如果开启了 Apply Root Motion）。

无论是 Generic 还是 Humanoid 动画片段，都面临一个问题，如果模型原本有整体的移动、旋转，在导入到 Unity 场景中，是让 Animator GameObject 移动/旋转，还是它保持不动的，只让下面的模型骨骼移动/旋转。

只要没有 Bake Into Pose，就存在 Root Motion，就需要采样 Root Motion，将它记录为 Root Transform 的动画曲线。无论如何采样的 Root Motion，如何选择的 Root Transform，Unity 动画系统保证：

- 不 Apply Root Motion：Root Transform（Animator GameObject）不会运动，模型动画整体移动由 Root 下面的 Bone Hierarchy 完成
- Apply Root Motion：Root Transform（Animator GameOjbect）本身的运动用于实现模型动画整体的运动

如果模型本身就没有 Root Motion，那么是否 Apply Root Motion 没有区别。Apply Root Motion 只在模型有 Root Motion（提前采样）时起作用，控制 Animator GameObject 是否被动画驱动而移动旋转。

无论如何确定 Root Transform（真实 bone，还是虚拟中心），最终都会在动画片段中采样这个点的运动（位移、旋转），然后在 Clip 中为 Root Transform 单独记录这个动画曲线。在运行时播放动画，只要 Apply Root Motion，这个采样的运动就会应用到 Animator GameObject 上，让它来带动整个模型的整体运动。只要不 Apply Root Motion，模型就只会在原地播放动画，Animator GameObject 不被 Animator 驱动。Bake Into Pose（rotation，Y，XZ）可以让你选择将一部分 Root Motion 的运动烘焙到模型中，这样不 Apply Root Motion（Animator GameObject 不动）的时候，模型仍然在这部分分量上有运动。
