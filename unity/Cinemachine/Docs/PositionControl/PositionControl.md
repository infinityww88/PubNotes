使用 Position Control 行为指定移动 CinemachineCamera 的算法。要旋转 camera，使用 Rotation Control。

CinemachineCamera Live 时，它与 Unity Camera 的 transform（position，rotation）都被算法控制，不可再被编辑。

CinemachineCamera 没有提供何时更新 Unity Camera 的选项，不用关心在 Update，FixedUpdate、还是 LateUpdate 中更新相机位置，只需指定 target 就可以平滑跟踪。

Cinemachine 包含以下移动 CinemachineCamera 的行为：

- None：不进行过程化相机移动 CinemachineCamera
- Follow：以与 Tracking Target 固定的相对关系移动 CinemachineCamera
- Orbital Follow：以与 Tracking Target 可变的相对关系移动 CinemachineCamera，可选地接收 player input
- Third Person follow：使用 Tracking Target 的 pivot point，水平、垂直绕着 player pivot camera，跟随 tracking target 的旋转
- Position Composer：以与 Tracking Target 固定的屏幕空间 screen-space 相对关系移动 CinemachineCamera
- Hard Lock to Target：使用与 Tracking Target 相同的位置，CinemachineCamera 的位置总是 Tracking Target 的位置，Unity Camera 的位置又是 CinemachineCamera 的位置。Tracking Target 成为 Camera 的 Pivot。
- Spline Dolly：沿着曲线移动 CinemachineCamera，指定 Spline

相机控制有两个过程化行为：Position 和 Rotation。它们是两个独立的系统，尽管通常都使用相同的 target。但是可以让 camera 仅跟随位置，但是不旋转（不 look at 目标），此时 Target 仅作为 camera 的拖拽器，Rotation Control 可以是 None，这样位置被过程化控制，而旋转则可以通过脚本来手动控制。

# None

在哪个阶段同步 Unity Camera，在 Cinemachine Brain 中指定，Update、FixedUpdate、LateUpdate。

