此 CinemachineCamera 旋转控制行为会根据外部 stimulus（例如用户输入）进行相机的平移和倾斜操作。

该组件本身不会读取用户输入；它可以由Cinemachine输入轴控制器组件驱动，也可以通过您自行设计的其他方式来控制。

- Reference Frame

  定义 pan 和 tilt 旋转的参考 reference frame。

  - Parent Object：如果CinemachineCamera有父级对象，则使用该父级对象的本地坐标轴作为参考框架；如果没有父级对象，则使用世界坐标轴。
  - World：使用 World axes 作为 reference frame
  - Tracking Target：如果CinemachineCamera设有 Tracking target，则使用该 Tracking target 的本地坐标轴作为参考框架；若无追踪目标，则使用世界坐标轴。
  - LookAt Target：如果CinemachineCamera设有 LookAt target，则使用该 target 的本地坐标轴作为参考框架；若无父级对象，则使用世界坐标轴。

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

