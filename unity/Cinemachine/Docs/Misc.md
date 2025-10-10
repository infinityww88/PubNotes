# Position Control

- 最简单的 Control 是 HardLockToTarget

  它直接将 CC（CinemachineCamera）跟随 Target 的 position。并提供一个 Dampping 参数，可以平滑跟随行为。

  Damping 是 CC 运动到 Target 位置需要的时间，Damping 越小，CC 跟随越快，Damping 越大，CC 跟随越慢越平滑。如果 Damping = 0，则 CC 就被简单固定到 Target 的 position 上。

- 其次是 Follow

  Follow 提供了一个 target 上的 Offset，CC 跟随这个 Offset，而不是 Target 的 center。

  Binding Mode 定义 CC 如何绑定在 Target 上：

  - Lock To Target：

- OrbitalFollow

  Sphere OrbitalFollow 类似 Follow 的 Offset，但是 Offset 是在 Target 上一个固定的点，而 Orbital Follow 在 Target 周围建立指定半径的球面，CC 可以这个球面上运动，CC 追踪球面上的位置，最终会到达球面，但是有一个 Damping 的过程，并且提供了和 Follow 一样的 Damping 参数，Damping 是追踪到达目标的时间，Damping 越小，则 CC 固定在球面上。

  在球面上的运动不是任意的，而是氛围水平、垂直两个过程，类似浑天仪，先沿着水平 circle 运动，在沿着垂直 circle 旋转。其中水平运动的范围都可以设置，默认运动范围为 [-180, 180]，垂直运动的范围是 [-10, 45]。

  ThreeRig 则是 Sphere 的扩展，它通过从上到下定义三个大小不同的 circle，和连接三个 circle 的弧线，定义一个椭球面，CC 追踪在这个椭球面上运动。
