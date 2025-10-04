这个 Position Control behaviour 严格限制 CinemachineCamera 沿着预定义 spline 移动。

Dolly：滑动台架；移动式摄影车；用移动车移动；移动摄影车。

使用 Camera Position 属性指示将 Camera 放在 spline 的什么地方。

开启 Automatic Dolly 以自动化的方法将 camera 移动到 spline 的一个位置：或者一个固定的速度，或者朝向距离 Tracking Target 最近的 spline 上的位置，或者以你设计的自定义方式。

提示：在使用 Target Automatic Dolly 功能时，请谨慎选择 spline 形状。对于围绕某点形成弧形的样条线，该功能可能会出现问题。举个极端的例子，假设有一条完美的圆形样条线，而追踪目标位于圆心。在这种情况下，样条线上离目标最近的点是不稳定的，因为圆形样条线上的所有点与目标的距离都相等。此时，即便将追踪目标移动很小的距离，也可能导致相机在样条线上移动很大的距离。

![SplineDollyInspector](../../Images/SplineDollyInspector.png)

# 属性

- Spline：camera 沿着这条 spline 运动。
- Camera Position：在 spline 上的哪里放置 camera。直接 animate 这个属性，或者开启 Automatic Dolly。这个值以 Position Units 指定的单位。
- Position Units：测量 Path Position 的单位。

  - Knot：value 是 knot index。0 表示 spline 的第一个 knot（控制点），1 代表第二个 knot，以此类推。Non-integer values 表示 knots 中间的插值位置。
  - Distance：沿着 spline 的距离，以正常的距离为单位。0 表示 spline 的起点，1 表示 spline 上距离起点 1m 的位置。
  - Normalized：归一化的 distance，0 表示 spline 起点，0.1 表示 spline 上 10% 的位置，0.9 表示 spline 上 90% 的位置。

- Spline Offset

  相机相对于样条线上某点的位置。其中X轴垂直于样条线，Y轴朝上，Z轴平行于样条线。通过该属性可调整相机与样条线本身的相对偏移。

- Camera Rotation

  如何设置相机的旋转和上方向。这将影响 screen composition（屏幕构图，画面的方向、大小），因为相机的瞄准行为始终会遵循 Up 方向。

  - Default：不修改 camera 的 rotation 或 up 方向。相反，使用 Cinemachine Brain 的 World Up Override 属性。
  - Path：使用 current point 的 spline up vector 和 tangent。
  - Path No Roll：使用 current point 的 spline up vector 和 tangent，但是将 roll 设置为 0.
  - Follow Target：使用 Tracking target transform 的 up vector 和 rotation。
  - Follow Target No Roll：使用 Tracking target transform 的 up vector 和 rotation，但是将 roll 设置为 0.

- Automatic Dolly：控制是否自动沿着 spline 移动。

  - Method：控制 automatic dollying 如何发生。你可以通过编写自定义 SplineAutoDolly.ISplineAutoDoly 类来实现自己的扩展。

    - None：不执行 automatic dollying。你必须通过设置 PathPosition 来控制 CinemachineCamera 的位置。
    - Fixed Speed：Camera 以固定的速度沿着 path 移动，可以设置速度。
    - Nearest Point To Target：将相机定位到样条线上距离追踪目标位置最近的点。CinemachineCamera中必须设置追踪目标。您还可以指定相对于最近点的偏移量，以微调相机的位置。

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

