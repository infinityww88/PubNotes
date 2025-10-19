**Animation Rigging 概述**  
**Animation Rigging** 是 **Unity** 的官方动画工具包，用于在已绑定骨骼的角色上创建可程序化的**控制层（Rig）**，通过一系列**约束（Constraints）**在运行时对骨骼进行**程序化动画**与**交互式调整**。它既可做**世界交互类 IK/Aim**（如手抓取、脚贴地、枪口/头部指向），也可做**变形类 Rig**（如盔甲、披风、配件的次级动画）。Rig 的计算以 **C# Animation Jobs** 实现，作为 **Playable Graph** 叠加在 **Animator** 之后执行，从而在不改动原始动画的前提下进行动态修正与叠加。

**工作原理与核心组件**  
- **Rig Builder**：挂在与 **Animator** 相同的 **GameObject** 上，构建可播放的 **Playable Graph**，并通过 **Rig Layers** 管理多个 Rig 的**启用/禁用**与**堆叠顺序**。  
- **Rig**：由一个或多个 **Rig 组件**承载，负责收集其子层级中的全部 **Constraint**，生成**有序的 IAnimationJobs 列表**；约束按**深度优先**遍历顺序求值，从而控制求解优先级。  
- **Rig Constraints（内置常用）**：如 **Two Bone IK**、**Chain IK**、**Multi-Aim**、**Multi-Parent**、**Override Transform**、**Blend Constraint**、**Twist Correction**、**Damped Transform** 等，用于 IK、目标指向、多父级切换、权重混合与扭曲矫正等。  
- **Rig Effectors / Bone Renderer**：为骨骼与目标点提供**可视化辅助**（仅编辑器可见），便于选择与调试。  
- **权重与可动画性**：每个 **Rig** 与 **Constraint** 都有 **Weight**，可**渐入渐出**或**脚本化控制**，实现与原始动画的平滑混合。

**典型应用场景**  
- **交互与瞄准**：手部抓取/握持、脚部贴地与对齐、头部/身体 **Aim**，以及**枪口指向**等运行时动态对齐。  
- **程序化次级动画**：盔甲/披风摆动、配件跟随、机械结构联动等**变形类 Rig**。  
- **动画修正**：对**动画压缩误差**进行校正，或在不同动画之间做**双向运动传递**（Bidirectional Motion Transfer）。

**快速上手步骤**  
1) 通过 **Package Manager** 安装 **Animation Rigging**（当前主流版本要求 **Unity 2023.2+**）。  
2) 在角色根对象添加 **Rig Builder**，确保与 **Animator** 作用于同一骨骼层级。  
3) 新建子对象作为 **Rig**，添加 **Rig** 组件，并将其指定到 **Rig Builder** 的 **Rig Layer**；在该层级下组织骨骼、目标点（Effectors）与约束。  
4) 选择约束并配置关键属性：例如 **Two Bone IK** 指定 **Root/Mid/Tip** 与 **Target/Hint**；**Multi-Aim** 指定 **Aim/Up 轴** 与 **Source Objects**。  
5) 通过脚本或 Animator 参数控制 **Rig/Constraint 的 Weight**，实现平滑开关与过渡；必要时用 **Bone Renderer** 辅助选择与可视化。

**使用建议与性能注意**  
- **分层与顺序**：将不同功能的 Rig 拆分到 **Rig Layers**，利用层级开关与**求值顺序**管理复杂度与优先级。  
- **权重渐变**：对 **Rig/Constraint Weight** 进行插值，避免手/脚“弹跳”或“撕裂”。  
- **更新时机**：Rig 在 **Animator 之后**执行；在复杂项目中可结合项目需求评估 **Update Timing** 与开销。  
- **范围控制**：仅在需要时启用相关 Rig，避免每帧不必要的求解；对远距离目标可降低 **Aim/Ik** 权重以保持自然感。