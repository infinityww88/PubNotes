# 便捷工具和 shortcuts

Cinemachine 包含一些 user interface 工具和 shortcuts 帮助 target 合适的 Cinemachine 元素，来根据你的需要设置，并且让配置过程更容易。

### Pre-built Cinemachine Cameras

Cinemachine package 对用于特定 use cases 的 pre-built Cinemachine Cameras 包含一系列 shortcuts。

要使用 pre-built Cinemachine Cameras，在 Editor 菜单中，选择 GameObject > Cinemachine，然后选择要给 camera type：

- State-Driven Camera

  创建一个 Manager Camera，它 parent 一组 Cinemachine Cameras，并且根据 animation state changes 来处理它们。参考 Cinemachine State-Driven Camera reference。

- Targeted Cameras > Follow Camera
- Targeted Cameras > Target Group Camera
- Targeted Cameras > FreeLook Camera
- Targeted Cameras > Third Person Aim Camera
- Targeted Cameras > 2D Camera
- Cinemachine Camera

  创建一个默认 Cinemachine Camera，没有 preselected behaviors。用它来创建一个 passive Cinemachine Camera 或者从头构建你自己的自定义 Cinemachine Camera。这个 camera 会被放置和旋转拍匹配当前 Scene View Camera。

- Sequencer Camera
- Dolly Camera with Spline
- Dolly Cart with Spline
- Mixing Camera
- ClearShot Camera

## Cinemachine Handle toolbar

Cinemachine Handle toolbar 使一组 3D controls，可以在 Scene View 中可视化操作 CinemachineCamera 参数。可以使用 handle tools 来快速高效、交互式地调整选中 object 的参数，而不是在 inspector 中不直观地调整。

当你选择一个 CinemachineCamera 类型 GameObject，toolbar 自动出现在 Scene View toolbar Overlay 中，并带有关联的 handle。

类似在 Scene View 中编辑 Collider（Box，Sphere）。

Handle tools 包括：

- Field of View Tool

  FOV tool 可以调整 Vertical FOV，Horizontal FOV，Orthographic Size，或者 Focal Length（物理相机）。

- Follow Offset Tool

  Follow offset 使一个到 Follow Target 的 offset。可以拖拽 handle 来增加或减少 Follow offset position。

- Far/Near Clip Tool

  拖拽调整 far clip plane 和 near clip plane。

- Tracked Object Offset Tool

  这个 offset 从 camera 放置的地方开始。当目标区域不是被跟踪的 object 的中心时，拖放 handle 来增加和减少 tracking target position

## Saving in Play Mode

Cinemachine 提供了一个特殊功能，可以保留 Play Mode 中进行的调整。但是它不保存结构化的改变，例如添加和删除一个 behavior。除了特定属性，Cinemachine 在退出 Play Mode 时保留绝大多数 Cinemachine Cameras 的设置。

当退出 Play Mode 时，Cinemachine 扫描 Scene 来收集 CinemachineCameras 上任何改变的属性。Cinemachine 保存这些修改。Edit > Undo 命令可以反转这些修改。

在 CinemachineCamera 的 Inspector 上点击 Save During Play 来开启这个功能。这是个全局属性，不是针对某个 camera 的。

Cinemachine 组件有一个特殊属性 \[SaveDuringPlay\]，可以开启这个功能。特定字段可以通过 \[NoSaveDuringPlay\] 从被保存的属性中排除。

还可以在自定义脚本（非 Cinemachine Camera 脚本）中使用这两个属性，来请求相同的功能。
