CC 不再围绕着 Tracking Target 运动，而是沿着世界空间中的预定义 Spline 移动。

Dolly：滑动台架；移动式摄影车；用移动车移动；移动摄影车。

Automatic Dolly 可以自动移动 camera

- 到 spline 的某个位置
- 以固定速度移动
- 移动到距离 Tracking Target 最近的 spline 上的位置

提示：在使用 Target Automatic Dolly 功能时，请谨慎选择 spline 形状。对于围绕某点形成弧形的样条线，该功能可能会出现问题。举个极端的例子，假设有一条完美的圆形样条线，而追踪目标位于圆心。在这种情况下，样条线上离目标最近的点是不稳定的，因为圆形样条线上的所有点与目标的距离都相等。此时，即便将追踪目标移动很小的距离，也可能导致相机在样条线上移动很大的距离。

![SplineDollyInspector](../../Images/SplineDollyInspector.png)

# 属性

- Spline：camera 沿着这条 spline 运动。

- Camera Position

  在 spline 上的哪里放置 camera。
  
  要沿着 spline 移动 camera，或者直接 animate 这个属性，或者开启 Automatic Dolly。
  
  这个值使用 Position Units 指定的单位。

- Position Units：测量 Path Position 的单位。

  - Knot：value 是 knot index。0 表示 spline 的第一个 knot（控制点），1 代表第二个 knot，以此类推。Non-integer values 表示 knots 中间的插值位置。
  - Distance：沿着 spline 的距离，以正常的距离为单位。0 表示 spline 的起点，1 表示 spline 上距离起点 1m 的位置。
  - Normalized：归一化的 distance，0 表示 spline 起点，0.1 表示 spline 上 10% 的位置，0.9 表示 spline 上 90% 的位置。

- Spline Offset

  相机相对于样条线上某点的位置。其中X轴垂直于样条线，Y轴朝上，Z轴平行于样条线。
  
  通过该属性可调整相机与样条线本身的相对偏移。

  这个偏移是 Spline 上的点的局部坐标系，不是 CC 的坐标系。其 forward 总是沿着曲线的切线方向。

- Camera Rotation

  CC 沿着 Spline 移动时的旋转如何定义。

  如何设置相机的旋转和上方向。这将影响 screen composition（屏幕构图，画面的方向、大小），因为相机的瞄准行为始终会遵循 Up 方向。

  - Default
  
    不修改 camera 的 rotation 或 up 方向。相反，使用 Cinemachine Brain 的 World Up Override 属性。

    CC 的 Up 固定为 Brain 的 World Up 指定的方向，另外 CC 的 Forward 总是 Spline 的切线方向，根据左手定则，就可以确定 CC 的+X 方向。

  - Path：使用 current point 的 spline up vector 和 tangent。
  - Path No Roll：使用 current point 的 spline up vector 和 tangent，但是将 roll 设置为 0（不绕着 Z 轴翻滚）
  - Follow Target：使用 Tracking target transform 的 up vector 和 rotation。
  - Follow Target No Roll：使用 Tracking target transform 的 up vector 和 rotation，但是将 roll 设置为 0.

- Automatic Dolly：控制是否自动沿着 spline 移动。

  - Method：控制 automatic dollying 如何运行
  
    可以通过编写自定义 SplineAutoDolly.ISplineAutoDoly 类来实现自己的扩展。

    - None：不执行 automatic dollying。只能通过设置 Camera Position 来控制 CinemachineCamera 的位置。
    - Fixed Speed：Camera 以固定的速度沿着 path 移动，可以设置速度

      速度的单位仍然根据 Position Unit 定义：

      - Distance：正常距离单体，米
      - Normalized：归一化比例，如果速度 = 1，则每秒完成转一圈 spline
      - Knot：控制点，如果速度 = 1，则每秒完成一个控制点的距离

    - Nearest Point To Target：将相机定位到样条线上距离追踪目标位置最近的点。CinemachineCamera中必须设置 Tracking Target。还可以指定相对于最近点的偏移量，以微调相机的位置。

      - Position Offset：将 CC 放在 Spline 上距离 Tracking Target 的最近点后，再偏移 Offset，单位为 Position Unit。

        Offset 不是 Vector3，而是 float，因此是在 Spline 上的前后偏移，而不是空间中的 3D 偏移。
      
      - SearchRadius：在 CC 当前位置的两侧任意一侧，最多搜索这么多 waypoint（Knot）。0 表示全部搜索。

      - SearchResolution

        当在两个 WayPoints 直接搜索时，这个值控制将这两个 WayPoints(Knots) 分割为多少个直线段。值越高，结果越精确，但是也更消耗性能。

- Damping

  控制相机向其样条线上目标点移动的积极程度。数值越小，相机移动越快；数值越大，相机移动越迟缓沉重。

  - Position

    相机在样条线局部空间中沿X、Y或Z方向维持偏移的积极程度。  

    - X轴：垂直于样条线的方向。用于平滑路径瑕疵，可能导致相机偏离样条线。  
    - Y轴：由样条线局部上方向定义的轴。用于平滑路径瑕疵，可能导致相机偏离样条线。  
    - Z轴：平行于样条线的方向。不会导致相机偏离样条线。  

    数值越大，相机越积极维持偏移，路径瑕疵被平滑的效果越明显，但可能牺牲严格贴合样条线的效果。

  - Angular Damping

    相机试图维持目标旋转的积极程度。仅在相机旋转模式不为"默认(Default)"时生效。

    Default 时总是等于 Brain 中定义的 World Up。

SplineDolly 就是让 CC 沿着要给预定义 Spline 移动，通常不需要设定 Tracking Target，但是有两种情况需要设定 Tracking Target：

- 当 Camera Rotation 设置为 Tracking Target，即 CC 的旋转会同步 Tracking Target 的旋转，此时需要设置 Tracking Target
- 当 AutoDolly 设置为 Nearest Point To Target，CC 会被设置到 Spline 上距离 Tracking Target 上最近的点，此时需要设置 Tracking Target
