此CinemachineCamera扩展功能可为摄像机添加 target group 的取景能力：当拍摄目标属于CinemachineTargetGroup时，能够自动框选 frame 一个或多个目标。

该扩展可通过动态调整变焦或改变摄像机与目标的距离，确保目标始终以预设尺寸保持在画面中。

使用前提：CinemachineCamera的跟踪目标必须设置为CinemachineTargetGroup，且该目标组需包含至少一个有效成员，并设定非零的组范围尺寸。

- Framing Mode：指定 framing 时要如何处理屏幕维度

  - Horizontal：只考虑水平维度，忽略垂直 framing
  - Vertical：只考虑垂直维度，忽略水平 framing
  - Horizontal And Vertical：使用 horizontal 和 vertical dimensions 的最大者以获得最佳适配

- Adjustment Mode：如何调整 camera 的 depth 以得到想要的 framing。可以 zoom，dolly in or out，或者二者都有

  - Zoom Only：不移动相机，只调整 FOV
  - Dolly Only：移动相机，不改变 FOV
  - Dolly Then Zoom：在允许的移动范围内先调整摄像机位置，若仍需优化构图，则进一步调整视场角（FOV）来完成取景。

- Lateral Adjustment：可通过两种方式调整画面构图：一是水平或垂直移动摄像机位置进行重新取景；二是通过旋转摄像机角度来实现构图调整。
  - Change Position：Camera 水平、垂直移动，知道得到想要的 framing（构图）
  - Change Rotation：Camera 通过旋转得到想要的 framing（构图）

- Framing Size：targets 应该占据的 screen-space bounding box。1 表示填充全部的 screen，0.5 填充一半的 screen，依此类推。

- Center Offset：非 0 值会在 camera frame 中偏移 group

- Damping：framing 调整的平滑程度。更大的值，响应更慢，更平滑

- Dolly Range：为达成理想构图，摄像机可移动的允许范围。负值表示朝向目标移动，正值则表示远离目标移动。

- FOV Range：如果调整 FOV，会 clamp 到这个范围内。

- Ortho Size Range：如果调整 Orthographic Size，会 clamp 到这个范围内。
