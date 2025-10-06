扩展组件（Extensions）是用于增强CinemachineCamera行为的附加组件。例如，Deoccluder（防遮挡）扩展组件可以让相机避开那些遮挡相机目标物体视野的游戏对象（GameObject）。

Cinemachine 提供了多种扩展组件。也可以通过继承 CinemachineExtension 类来创建自定义的扩展组件。

要为 CMC 添加一个 extension：
- 选中 CinemachineCamera
- 在 Inspector 中，使用 Add Extension 下拉菜单选择要添加的 extension。选择的 behaviour 会添加到 CinemachineCamera GameObject 上

