此 CinemachineCamera Position Control 行为会根据 CinemachineCamera 的追踪目标以可变关系移动Unity相机。

若添加 Cinemachine 输入轴控制器行为，相机位置可由玩家输入驱动，从而允许玩家动态控制相机相对于目标的位置。

Orbital Follow 以两种方式操作：

- Sphere：在此模式下，相机会被定位在围绕目标的一个球面上的任意一点
- ThreeRig：在此模式下，相机会被定位在由围绕目标的三条圆形轨道所定义的样条线拉伸而成的曲面上的任意位置。

相机在该曲面上的精确位置由轨道跟随组件中的三个轴向值决定：水平轴、垂直轴和半径轴。其中半径控制缩放比例，允许相机靠近或远离目标。您可以通过自定义脚本、动画器或自行设计的其他方式来控制这些数值。

如果为 CinemachineCamera 附加输入控制器，玩家就可以使用Unity的输入控件来控制相机在定义曲面上的位置。这样玩家就能将相机移动到目标周围轨道曲面上的任意位置。

![OrbitalFollowInspector](../../Images/OrbitalFollowInspector.png)

属性

- Target Offset

  Target 本地坐标系中从 object 中心的偏移。用来精细调整 orbit position，尤其是期望的 orbit focus 不是跟踪的 object 的中心。

- Binging Mode 绑定模式：用来解释 offset 的坐标空间，即过程化算法如何使用 Offset

  - Lock To Target On Assign
  - Lock To Target With World Up
  - Lock To Target No Roll
  - Lock To Target
  - World Space
  - Lazy Follow

- Position Damping
- Angular Damping Mode
- Rotation Damping
- Quaternion Damping
- Orbit Style
  - Sphere
  - ThreeRing
- Radius：在 Sphere Mode，它定义了 surface sphere 的半径
- Top，Center，Bottom：在 ThreeRing Mode，它定义了 3 个 orbit rings 的高度和半径，orbit rings 用于创建 orbit surface。这些值是相对于 target 的 origin 的。
- Spline Curvature：Three Ring Mode 中，它定义了连接 3 个 orbit rings 的线的紧绷程度 tautness，线更直还是更曲。这个线决定了 surface 的最终形状，类似车床建模 Lathe 的 profile（轮廓曲线）。
- Recentering Target：定义水平重新居中的参考框架。轴心中心将动态更新，始终保持在选定对象的后方。
  - Axis Center：静态 referenc额frame。Axis center value 不是动态更新的。
  - Parent Object：Axis center 动态调整到 parent object forward 之后
  - Tracking Target：Axis center 动态调整到 Tracking Target forward 之后
  - LookAt Target：Axis center 动态调整到 LookAt Target forward 之后

- Horizontal Axis：相机在曲面上的水平位置（绕Y轴旋转）。数值以度为单位，"范围"定义了允许的数值限制。若勾选"环绕"选项，当数值超出范围边界时会循环回绕。此处可定义一个中心位置，当轴驱动器中启用了重新居中逻辑时，该中心位置将被使用。
- Vertical Axis：相机在曲面上的垂直位置（绕X轴旋转）。在球体模式下数值以度为单位，但在三环模式下为任意单位。范围定义了允许的数值限制。若勾选"环绕"选项，当数值超出范围边界时会循环回绕。此处可定义一个中心位置，当轴驱动器中启用了重新居中逻辑时，该中心位置将被使用。
- Radial Axis：通过缩放轨道来控制相机与目标之间的距离。该值为轨道高度和半径的标量倍数。范围定义了允许的数值限制。若勾选"环绕"选项，当数值超出范围边界时会循环回绕。此处可定义一个中心位置，当轴驱动器中启用了重新居中逻辑时，该中心位置将被使用。
- Recentering：若对一个 axis 开启 re-center，Recentering 会平滑地将 axis value 返回到其 Center。
  - Wait：若对一个 axis 开启 re-center，它会在最后一个 user input 之后等待这个值指定的时间（秒），然后开始 re-centering 过程。
  - Time：re-center 开始后，完成 re-center 过程要花费的时间（秒）。


