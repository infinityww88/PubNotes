ClearShot Camera 组件在它的子相机中选择一个对 target 具有最佳质量的一个。

使用 Clear Shot 为 scene 设置复杂的多相机覆盖，来保证对 target 有一个清晰的 view。

这是一个非常有用的工具。带有 Cinemachine Deoccluder 或其他 **镜头质量评估** 扩展的 CinemachineCamera 子级会分析 **目标遮挡情况**、**最佳目标距离**等镜头参数。Clear Shot 利用这些信息来选择最佳的子级进行激活。

要为所有 CinemachineCamera 子级使用单个 Cinemachine Deoccluder，请将 Cinemachine Deoccluder 扩展添加到 ClearShot 游戏对象上，而不是添加到其每个 CinemachineCamera 子级上。此 Cinemachine Deoccluder 扩展将应用于所有子级，就像每个子级都拥有该 Deoccluder 作为其自身的扩展一样。扩展是相机的后处理，复合相机（CameraManager）对外表现为一个单一相机，无论它内部选择哪个子相机，都可以应用统一的后处理。

如果多个子相机具有相同的 shot 质量，Clear Shot camera 选择具有最高优先级的那个。

还可以在 ClearShot children 之间设置自定义 blend。
