# Animation Rigging Menu

Animation Rigging 菜单包含有用的功能来帮助 rigging workflow。

![](Image/RiggingMenu.gif)

## Align

使用 Align 来对齐一个 GameObject 的 Transform，Position，或 Rotation。这在需要对齐 effectors 到 bones，或者 props 到 effector 时尤其有用。

要使用 Align，选择你想要对齐的 GameObject，然后选择你想要对齐到的 GameObject。

在 Animaiton Rigging 菜单 中，选择合适的 align 选项：

| Tool | Description |
| --- | --- |
| Align Transform | 对齐 GameObject 的 Position 和 Rotation |
| Align Rotation | 对齐 GameObject 的 Rotation |
| Align Position | 对齐 GameObject 的 Position |
|||

## Restore Bind Pose

使用 Restore Bind Pose 选项来恢复 Skinned Mesh Renderer 原始 imported 时的 bind pose（Blender 的 Rest Pose，动画片段的参考 Pose，所有动画数据记录的都是基于这个参考 Pose 的偏移量）。这可以用来恢复一个 skinned mesh 的原始 character pose。这个选项只为被 skinning 使用的 bones 恢复 poses。如果 mesh 只 skinned 到 hierarchy 中的部分骨骼，Restore bind pose 选项可能不能如预期工作。

## Rig Setup

Rig Setup 在选择的 Object 上，为 Animation Rigging 设置必需的组件。

要使用 Rig Setup，选择一个想要创建 constraints 的 Animator GameObject。然后选择 Rig Setup 选项。这会在选择的 GameObject 上创建一个 RigBuilder 组件，以及一个名为 Rig 1 带有 Rig Component 的 child GameObject，其将被添加到 RigBuilder layers。

注意：Rig Setup 在 Animator 组件选项中也能找到。

## Bone Renderer Setup

使用 Bone Renderer Setup 选项来创建一个 BoneRenderer 组件，其中的骨骼是从所选中的 GameObject Hierarchy 的 Children SkinnedMeshRenderer 组件中提取出来的。要使用 Bone Renderer Setup，选择 root GameObject 并选择 Bone Renderer Setup。

Bone Renderer Setup 在 Animator component 选项中也能找到。
