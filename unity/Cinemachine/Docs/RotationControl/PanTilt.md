不依赖 LookAt Target，只是简单水平、垂直绕着 YX 轴旋转。可以通过两个 Axis（Pan、Tilt）控制 CC 的旋转。

但是 Tracking Target 和 LookAt Target 可以为 CC 提供绕转的坐标系。

- Reference Frame

  定义 pan 和 tilt 旋转的参考坐标系 reference frame。

  一旦指定了某个参考坐标系，CC 就同步到那个坐标系的 Identify Quaternion（即本地坐标轴与参考坐标系坐标轴一致，注意只是方向一致，Rotation Control 并不操作 CC 的位置）。
  
  然后 Pan Axis 和 Tile Axis 的输入就在参考坐标系中解释，即 CC 绕着参考坐标系的 XY 轴旋转。

  并且，如果运行时，参考坐标系物体（Parent Object，Tracking Target，LookAt Target）也在旋转，CC 也会相应旋转，总之 CC 的旋转在参考坐标系中解释。

  - Parent Object：如果 CinemachineCamera 有父级对象，则使用该父级对象的本地坐标轴作为参考框架；如果没有父级对象，则使用世界坐标轴。
  - World：使用 World axes 作为 reference frame
  - Tracking Target：如果 CinemachineCamera 设有 Tracking target，则使用该 Tracking target 的本地坐标轴作为参考框架；若无追踪目标，则使用世界坐标轴。
  - LookAt Target：如果 CinemachineCamera 设有 LookAt target，则使用该 target 的本地坐标轴作为参考框架；若无父级对象，则使用世界坐标轴。

- Recenter Target

  CC 旋转回正到哪里。

  - Axis Center：回正到这个 axis 定义的 Center Value

    默认 Axis Center。Pan Axis 的 center 和 Tilt Axis 的 center 在 world frame 中定义了一个向量，它将成为 CC 的 rest forward 向量。当 CC forward 偏离这个向量后，会平滑地恢复到这里。

  - Tracking Target Forward / LookAt Target Forward

    直接将 Tracking/LookAt Target 的 Forward 向量（世界空间中）作为 CC 的 forward 的 rest 方向。

    注意 CC 的 forward 恢复到哪里跟 Reference Frame 没有关系，即使 Reference Frame 指定为 LookAt Target，Recenter Target 也可以指定为 Tracking Target Forward，因为它只是为恢复位置指定了一个世界空间中的向量，是一个相对 Axis Center 的快捷方式。

    当指定了 Tracking Target 或 LookAt Target 之后，recenter 中的 center 就没有作用了，因为直接使用它们的 forward 定义 CC 的 forward 恢复方向。

    另外，这只是指定了 CC Rest 时的方向，当 Pan 或 Tilt 时，仍然基于 Reference Frame 的坐标系进行。

- Pan Axis

  控制 camera 的水平旋转。

  - Value：axis 的当前 value，单位为度
  - Center：如果开启 Recentering，Recentering 过程 recenter 的 value
  - Range：Value 的最小值和最大值
  - Wrap：如果开启，当到达 range 的终点时，Value 回转 wrap，形成一个 loop

- Tilt Axis

  控制 camera 的垂直旋转。

  - Value
  - Center
  - Range
  - Wrap

- Recentering

  如果为一个 axis 启用，Recentering 会平滑地将 axis value 返回到其 Center。

  - Wait：如果为一个 axis 启用 Recentering，在最新的 user input 之后，recentering 过程开始之前，等待时间（秒）
  - Time：Recentering 过程完成花费的时间

