Follow 过程化算法移动 CinemachineCamera，相对 Tracking Target 维持一个固定的相对位移。它还会应用 Damping，当 Target 开始移动或开始停止时产生平滑效果。

根据 Binding Mode，fixed offset 可以以很多方式解释。

属性：

- Binding Mode（绑定模式）

  如何解释相对 target 的 offset。

  - World Space

    offset 解释为 world space 中相对 Follow Target 原点的偏移。当 target 旋转时，camera 不会改变位置。

    Cinemachine 中，camera 专指 CinemachineCamera，因为 Unity Camera 总是与 Cinemachine 同步，Unity Camera 的各种相机参数，例如 FOV、远近平面、Len 等等都在 CinemachineCamera 上有 mirror 属性。

  - Lock To Target

    使 CinemachineCamera 使用 Target 的本地坐标系。当目标旋转时，相机会随之移动以保持 offset，并维持对目标的相同视角。

  - Lock To Target With World Up

    使 CinemachineCamera 使用 Target 的本地坐标系，同时将倾斜 tilt 和翻滚 roll 设为0。此绑定模式会忽略除偏航 yaw 外的所有目标旋转，即 camera 的 Y 向量总是指向 World Up。

    - tilt：绕着 Z 轴的旋转，倾斜（两侧）
    - roll：绕着 X 轴的旋转，翻滚（高低）
    - yaw： 绕着 Y 轴的旋转，偏航（左右）

  - Lock To Target No Roll

    使 CinemachineCamera 使用 Target 的本地坐标系，而将 roll 设置为 0，即禁止 camera 绕着 X 轴的翻滚。

  - Lock To Target On Assign

    使 CinemachineCamera 的方向保持 与 enable 时或指定 target 时 target 的本地坐标系相匹配。该偏移量在世界空间中保持恒定。相机不会随目标一起旋转。

  - Lazy Follow

    Lazy Follow 模式在相机本地空间中解释偏移量和阻尼值。

    此模式模拟了人类摄像师在接到跟随目标指令时会采取的操作。

    相机会尽量减少移动以保持与目标的相同距离；相机相对于目标的方向并不重要。

    无论目标如何定向，相机都会尝试保持与其相同的距离和高度。

- Follow Offset

  相机与目标之间的**期望**偏移量，CinemachineCamera 将根据该偏移量进行定位。将 X、Y 和 Z 设为 0 可将相机放置在目标的中心。默认值分别为 0、0 和 -10，这会将相机置于目标的后面。

- Position Damping

  相机在X、Y和Z轴上尝试保持偏移量的响应程度。数值越小，相机响应越灵敏；数值越大，相机响应越迟缓，效果越平滑。

- Rotation Damping

  在欧拉角阻尼模式下，相机跟踪目标俯仰（Pitch）、偏航（Yaw）和翻滚（Roll）的响应程度。数值越小，相机响应越灵敏；数值越大，相机响应越迟缓。

- Angular Damping Mode

  可采用欧拉角（Euler）或四元数（Quaternion）模式。在欧拉角模式下，可以为俯仰（Pitch）、翻滚（Roll）和偏航（Yaw）的阻尼分别设置独立数值，但可能会出现万向节锁问题。在四元数模式下，仅使用单一数值，且不受万向节锁影响。

- Quaternion Damping

  在四元数角度阻尼模式下，相机跟踪目标旋转的响应程度。

