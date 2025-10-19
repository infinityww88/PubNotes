# Modeling characters for optimal performance

设计 character Models 以优化渲染和动画速度。

使用这些技术可以帮助提高角色动画和渲染速度，但是可能降低想要达到的视觉效果。最终需要在效果和性能之间寻求平衡。

## 使用单一的 skinned Mesh Renderer

对每个角色只使用一个 skinned Mesh Renderer。Unity 使用可见性剔除和 bounding volume 更新来优化动画。

## 使用尽可能少的 Materials

只在对不同的部分使用不同的 shaders 时使用多个 materials，例如对于眼睛使用一个特别的 shader。但是通常一个角色，2 到 3 个材质就足够了。

## 使用尽可能少的 bones

有时你需要为角色创建大量 bones，例如当你想要大量的定制 attachments（挂载点）。

对于 Generic 和 Humanoid 类型可以有附加骨骼。当你没有动画播放这些额外骨骼时，对它们的处理可以忽略不计。

出于性能原因，使用 linear blend skinning，每个 vertex 最大4个影响骨骼。

## 最小化 polygon count

多边形数量应该依赖于想要达成的视觉质量，以及运行的平台的性能。它们是相互对立的因素。

- Meshes 使用更少的多边形，程序运行地更快。因为每个 vertex，edge，face 都需要计算资源
- Meshes 使用更多的多边形，GameObject 就可以有更多更精细的外观，因为更小的多边形给你更多对 shape 的控制

## 保持 forward 和 inverse kinematics 分离

当 Unity 导入 animations，它烘焙 bakes 一个 Model 的 IK nodes 到 FK，因此 Unity 根本不需要 IK nodes。然而，如果它们留在 Model 中，则 Unity 仍然将它们包含到计算中，即使它们不影响动画。你既可以在 Unity 中删除多余的 IK nodes，也可以在 3D 建模程序中。要使用移除 IK nodes 的功能，在建模时保持 IK 和 FK hierarchies 分离。


