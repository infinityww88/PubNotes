# Rigging workflow

本节展示定义一个 Animation Rig 必须的步骤和组件。

AnimationRigging 专门用于 Animator 骨骼动画的 Rig Constraints，Unity Constraints 则是通用的 Rig Constraints。

## 核心组件

一个 Animation Rig 是一个 GameObjects 的 hierarchy，其使用 4 个关键组件：

- Animator：如果添加到 Root GameObject，它使 Hierarchy 变成 animatable 的。Animation Rigging 操作 Unity animation system 的 top，因此需要一个 Animator
- Rig Builder：如果添加到 Root GameObject，这个组件允许 animated hierarchy 被一个多个 Rigs 修改，它将 Rigs 组织到 Layers 中
- Rig：如果添加到 animatable hierarchy 中的 GameObjects，Rigs 用作 source objects 和修改 animated hierarchy Pose 的 Constraints 的容器。可以调整一个 Rig 的 weight 来控制它对最终 Pose 的贡献度
- Constraints：如果添加到 Rig GameObjects 或其 Children，这些组件指示 Rig 要执行的操作

要使 hierarchy 对 Animation Rig 有效，必须有 Rig Builder 组件。一旦 Rig Builder 组件被添加到 Animator Root，可以创建一个 Rig GameObject 作为 Animator Root 的 Child GameObject。当开启 animaiton rigging 时，Rig GameObject 必须包含 Rig 组件。然后连接 Rig 到 Animator，Rig GameObject 需要被赋予到 Rig Builder 组件的 Rig Layer 字段中。这将关联 Animation Rig 和 Animator。

![rig_setup](Image/rig_setup.gif)

下图表示了一个 Aniamtor 和 Animation Rig 组件内部依赖的图解概览

![rig_setup_overview](Image/rig_setup_overview.png)

一旦带有 Rig 组件的 Rig GameObject 被连接到 Rig Builder 组件，将带 Rig Constraints 组件的 Rig 元素（effector GameObject，效应器）添加到 Rig GameObject 下面。不同的 rig elements 被组织为层次化结构来创建任何种类的 Rig，以满足任何 rigging 需求。

用于 Constraints 的 Source GameObjects，例如 Target Effectors 或者 Hint Effectors（IK Pole 或 Bend Goal，提示 IK 的 GameObject），可以被放置在它们关联的 Rig GameObject 下面。在下面的图示中，Left Leg 作为 Rig element，它包含一个 Two Bone IK Constraint 组件，同时它也是两个 LeftFootEffector 和 LeftLegHint source objects 的 parent。

![source_object_example](Image/source_object_example.png)

## Rig Builder Component

Rig Builder component 和 Animator 组件在一起（同一个 GameObject）。Rig Builder 影响 Animator 所在的 hierarchy。

![rig_builder_setup](Image/rig_builder_setup.gif)

使用 Rig Layers，Rig Builder 组件允许多个 multiple Rigs 的 stacking，它们可以在任何时候 enabled/disabled。

![rig_builder_layers](Image/rig_builder_layers.gif)

Rig Builder 在 Animator 上，影响 Animator 所在的 Hierarchy，并连接各个 Rig。

每个 Rig 放在 Rig Builder 下面。每个 Rig 定义一个 Riging。每个 Rig 下面有一组 Constraints，每个 Constraint 定义一个约束。

Rig Builder 包含一组 Rigs 作为 Layers。可以在运行时开启或关闭其中的某个 Rig。

## Rig Component

Rig 组件：一个给定 Rig 的所有 Rig constraints 的主要入口。

这个 component 被指定 Rig Builder 下面的 Rig Layer 字段。

每个 control rig hierarchy 只应该有一个 Rig component。

对于 multiple rigs，多个 control rig hierarchies 可以被指定到不同的 Rig Layer，并且独立地 enabled/disabled。

Rig component 的主要目的是收集它的 local hierarchy 下面的所有 Constraint 组件，并产生一个 IAnimationJobs 的有序列表（求值顺序），然后它们将**在 Animator 求值之后**被应用（先应用 Animation Clip 的数据，然后应用 Rig Constraint 的数据）。

Jobs 的求值顺序按照组件的顺序以及 rig hierarchy 的构造方式定义，因为 constraints 是通过 GetComponentsInChildren 收集的，它遵循 DFS 遍历顺序：

![eval_order](Image/eval_order.png)

换句话说，对一个 GameObject 下面的 constraints 进行分组，允许 user 通过改变 hierarchy 管理这些 constraints 的求值顺序。

Control Rig Hierarchies（Rig GameObject 下面的 Hierarhcy）应该包含所有必要的 rig elements，例如 effectors（例如 IK Target），constraints（IK Constraint），以及 constraints definitions 所需的其他 objects/elements。

一个 Control Rig Hierarchy root 应该与 skeleton root（Animator 下面的 Bones Root）在同一个 level，二者都在 Animator GameObject 下面。换句话说，它不应该在 skeleton hierarchy（骨骼）下面，而是在它旁边。

![rig_weight](Image/rig_weight.gif)

Rig components，就像所有 Constraint 组件，有一个 Weight 属性可以被 animated，scripted 以 enable/disable 或 ease-in/ease-out 整个 control rig hierarchy。

## Bone Renderer Component

Bone Renderer 组件允许定义一个 transforms hierarchy 来绘制 bones，用于可视化和在 rigging process 进行选择。

Bones 的外观可以被定制。Bone size，shape 和 color 可以被修改。Local axes 的三脚架也可以被显示，而且它们的 size 可以调整到满足偏好。可以从几种默认外观中选择一个：Pyramid，Line，或 Box。

![bone_looks](Image/bone_looks.png)

## Rig Effectors

类似 Bones，Rig Effectors 允许添加视觉 gizmos 到 transforms，用于可视化和选择。它们可以被添加到和 RigBuilder 或 Rig 组件相同的 hierarchy 中的任何 transfor，因此可以可视化任何 Rig 元素。

Effectors 在 GameView 是不可见的。一个特殊的 Scene View overlay 被添加用来管理和定制 Rig hierarchy 中的 effectors。

![rig_effector_setup](Image/rig_effector_setup.gif)

Effectors 的外观也可以被定制。Effector Size，Shape，Color，Offset Position 和 Offset Rotation 可以被修改。Shape 可以是 Project 中任何可用的 Mesh Asset（因此可以定制外观）。Multiple effectors 可以同时创建，删除，编辑。

![rig_effector_shapes](Image/rig_effector_shapes.png)

## Rig Transform

如果 rig hierarchy 的一个特定 GameObject 对于 manipulation 很重要，但是不被任何 rig constraints 引用，则需要添加 Animation Rigging/Setup 下面的 RigTransform 组件。如下图所示的，为了使用它们 parent transform（IK）同时操作 TwoBoneIK 示例的 left 和 right foot IK targets（lfik 和 rfik），就需要添加 RigTransform 组件以得到期望的行为。

![rig_transform_manipulation](Image/rig_transform_manipulation.gif)
