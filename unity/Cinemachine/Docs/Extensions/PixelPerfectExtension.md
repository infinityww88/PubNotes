Pixel Perfect Camera 与 Cinemachine 都会修改摄像机的正交尺寸（orthographic size）。若在同一场景中同时使用这两个系统，它们会相互争夺摄像机的控制权，导致异常效果。而 Cinemachine Pixel Perfect 扩展功能正是为了解决此兼容性问题而设计。

Cinemachine Pixel Perfect 是 CinemachineCamera 的一个扩展，它专门用于调整 CinemachineCamera 的正交尺寸。该扩展能自动检测场景中的 Pixel Perfect Camera 组件，并利用其配置参数来计算 CinemachineCamera 的最佳正交尺寸，从而确保精灵（Sprites）始终以像素完美的分辨率进行渲染。

如需为您的 CinemachineCamera 添加此扩展，请在 CinemachineCamera 的检查器（Inspector）窗口中使用 "Add Extension" 下拉菜单进行操作。请务必将此扩展添加到项目中的每一个 CinemachineCamera 上。

对于每个附加了此扩展的CinemachineCamera，Pixel Perfect Camera组件会在播放模式下或启用"Run In Edit Mode"时，计算出一个最能匹配该CinemachineCamera原始尺寸的像素完美正交尺寸。此举旨在实施像素完美计算的同时，尽可能贴近每个CinemachineCamera最初的构图框架。

当Cinemachine Brain组件在多个CinemachineCamera之间进行切换融合时，摄像机过渡期间的渲染画面会暂时无法保持像素完美状态。只有当视角完全切换至单个CinemachineCamera后，画面才会重新恢复像素完美效果。

以下是这个扩展当前的限制：

- 当设置了像素完美扩展的CinemachineCamera需要跟踪目标组（Target Group）时，若使用Framing Transposer组件进行定位，可能会出现明显的画面卡顿现象。
- 如果Pixel Perfect Camera组件上启用了"Upscale Render Texture"选项，能够匹配CinemachineCamera原始正交尺寸的可用像素完美分辨率方案将大幅减少。这可能导致经过像素完美计算后，CinemachineCamera的实际取景范围与预期构图产生较大偏差。
