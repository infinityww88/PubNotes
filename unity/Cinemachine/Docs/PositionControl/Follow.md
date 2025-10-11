Follow 过程化算法移动 CinemachineCamera，相对 Tracking Target 维持一个固定的相对位移。它还会应用 Damping，当 Target 开始移动或开始停止时产生平滑效果。

根据 Binding Mode，fixed offset 可以以很多方式解释。

属性：

- Binding Mode（绑定模式）

  如何解释相对 target 的 offset。

  **注意所有 Binding Mode 都不会导致 CC 旋转，进一步，所有 PositionControl 都不会影响 CC 旋转**。下面 Binding Mode 中所说的旋转，指的是 CC 的位置绕着 Target 的旋转（RotateAround），但是 CC 本身并不会旋转，镜头朝向总是固定的。

  - World Space

    offset 解释为 world space 中相对 Follow Target 原点的偏移。当 target 旋转时，camera 不会改变位置。

    CC 跟踪的位置简单等于世界坐标系中：target.position + offset。当 target 旋转时，CC 的位置不会绕着 target 旋转（CC 本身更不会旋转，RotationControl 控制 CC 本身的旋转）。

    Cinemachine 中，camera 专指 CinemachineCamera，因为 Unity Camera 总是与 Cinemachine 同步，Unity Camera 的各种相机参数，例如 FOV、远近平面、Len 等等都在 CinemachineCamera 上有 mirror 属性。

  - Lock To Target

    使 CinemachineCamera 使用 Target 的本地坐标系。当目标旋转时，相机会随之移动以保持 offset，并维持对目标的相同视角。

    简单来说，每帧更新时，都重新计算 CC 的跟踪位置：即 target.InverseTransform(target.position + offset)。

    当 target 旋转时，CC 的位置会绕着 Target 旋转（CC 本身不会旋转）。

  - Lock To Target On Assign

    在 Editor 模式时，类似 Lock To Target，CC 的位置会随着 Target 的旋转绕着 Target 旋转（因为使用 Target 的本地坐标系）。Editor World Space 模式，CC 位置不会绕着 Target 旋转。

    在进入 Runtime 时，当 CC activated 或每次重新指定 target 时，首先执行一次和 Lock To Target 一样的计算过程，将 offset 从 Target 本地坐标系变换到世界坐标系，target.InverseTransform(target.position + offset)，然后将变换后的位置与 Target 位置的 Offset 作为 World Space 的偏移，之后就像 World Space 一样运行，在没有指定新的 Target 期间，使用 CC 始终使用这个计算的世界空间 Offfset 跟随 Target，CC 的位置不会随着 Target 的旋转变换。

  - Lock To Target With World Up / Lock To Target No Roll

    这两个是 Lock To Target 的受限情况。Lock To Target 总是实时从 Target 坐标系变换 Offset 到世界空间作为 CC 的位置。

    Lock To Target With World Up：Target 每次旋转后，将旋转 EulerAngle 的 tilt（X 轴俯仰旋转）和 roll（Z 轴的翻身旋转）设置 0，只使用 yaw（Y 轴的偏航旋转），用这个三个角度（0，yaw, 0）构建一个 Quaternion，来变换 offset。注意这只是变换 Offset 的 Quaternion，Target 则按照正常旋转。最终效果就是 CC 的位置只绕着 Target 的 Y 轴旋转（水平绕转），不会绕着 Target 的 Z 轴和 X 轴旋转。

    Lock To Target No Roll：类似 With World Up，但是它是每次只将 Roll（Z 轴的翻身旋转）设置为 0，只使用 tilt（俯仰）和 yaw（偏航）两个旋转。使用 (tilt, yaw, 0) 构建一个 Quaternion 来从 Target 本地坐标系变换 offset。最终效果就是 CC 可以绕转 target 水平（yaw）和垂直（tilt）绕着，但不会绕着 target 的轴旋转。

    无论是哪种都是围着 target 绕转 CC 的位置，不会操作 CC 本身的旋转，CC 本身的旋转需要添加 RotationControl 来控制。

    - tilt/pitch：俯仰，绕着 X 轴的旋转
    - roll：翻滚、翻身，绕着 Z 轴的旋转
    - yaw：偏航，绕着 Y 轴的旋转

  - Lazy Follow

    Lazy Follow 模式在相机本地空间中解释偏移量和阻尼值。

    这个模式模拟了人类摄像师跟踪拍摄目标的行为，它会在一个世界空间的平面，以最小移动，带阻尼，保持和目标的常量距离。

    它的 Offset 的 Y 定义了世界空间中移动平面相对于 Target 的高度，Z 定义了平面上保持和 Target 常量距离的 Circle 的半径，CC 只会在这个 Circle 上移动。注意这个平面会随着 Target 的移动而移动。X 分量没有作用，被锁定，不可编辑。

    Target 的旋转对 CC 没有任何影响，只有 Target 的位置对 CC 有影响。注意它只是保持 CC 到 Target 的常量距离，只影响 CC 的位置。但是不会让 Target 总是瞄准 Target，瞄准需要添加 RotationControl 来操作 CC 的自身旋转.

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

所有的 Damping 值都定义的是时间，CC 到 Rest 位置（Target + Offset）的时间，Damping 越小，响应越快，Damping 越大，响应越慢越平滑。

注意当为 CinemachineCamera 切换 Target 的时候，会出现 CC 瞬移到某个位置，然后再平滑移动到新的 Target 的跟踪位置，而不是从 CC 当前位置平滑地移动到新 Target 的跟踪位置。这种画面的调整非常突兀。

使用 CinemachineCamera 跟踪不同目标，并在目标之间切换时有两种方式：

1. 使用一个 CinemachineCamera，然后修改 Tracking Target
2. 为每个目标创建一个 CC，然后通过优先级在不同的 CC 之间切换

事实证明，第一种方法在切换时非常突兀，第二种方法则是完全平滑的。Cinemachine 既然提供了丰富的在 CC 之间 Blend 的机制，似乎为每个目标单独设置 CC，然后在 CC 之间切换才是建议的使用方式。而且第一张方式不够灵活，直接切换 Tracking Target，只能是为每个 Target 都使用相同的 CC 设置（例如 Lens，FOV）相同的 Position Control 和 Rotation Control。而实际上每个目标的镜头需求可能都是不同的，因此为每个目标定制 CC，然后在 CC 之间切换才是主流的方式。

另外这也说明了为什么非 active 的 CC 也可能需要正常运行（只是不操控 Unity Camera），因为 CC 可能会在多个正常运行的 CC 之前切换来创建画面，因此非 active 的 CC 有时只是临时的，在非 active 的时候也需要正常运行（该跟随的跟随，该旋转的旋转）。

**注意：对于 Follow，Hard Lock To Target 这里基于点 point 的 binding mode，offset 偏移的是 CC 自身的位置，而对于 Orbital Follow 这里基于体积表面的 binding mode，偏移的是 Volume 的中心，即相对 Target 偏移 Volume，例如 Sphere 的球心**

