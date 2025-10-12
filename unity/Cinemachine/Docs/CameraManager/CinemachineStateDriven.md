Cinemachine State-Driven Camera 组件允许你将 CinemachineCameras 与 Animation State 关联起来。当某个状态被激活时，与之关联的 CinemachineCamera 也会随之激活。这使得你可以为特定的动画状态定义特定的相机设置和行为。例如，你可以为 Walk 状态设置一个相机，为 Run 状态设置另一个相机。当动画目标改变状态时，State-Driven Camera 会在这些相机之间进行混合过渡。

State-Driven Camera 的动画目标是带有 Animator 组件的 GameObject，该 Animator 由 Animator Controller 控制。

为每个子 CinemachineCamera 分配常规的追踪目标（Tracking Targets）。如果某个子 CinemachineCamera 没有追踪目标，State-Driven Camera 可以提供自己的追踪目标作为备用。

State-Driven Camera 有一个列表，用于将子 CinemachineCameras 分配给不同的动画状态。你可以为 State-Driven 的子级定义默认混合和自定义混合。你不需要为所有状态都定义相机。如果你为默认状态定义了相机，那么它将被用于任何没有特定相机定义的状态。

如果为某个给定状态定义了多个相机，State-Driven Camera 将选择优先级最高的那个。如果同一状态的多个相机具有相同的优先级，State-Driven Camera 将选择在列表中最早出现的那个。

在 Inspector 中，State-Driven Camera 会列出其 CinemachineCamera 子级。使用这个列表可以添加和删除子 CinemachineCameras，并分配它们的优先级。
