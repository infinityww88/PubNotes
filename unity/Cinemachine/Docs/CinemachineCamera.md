Cinemachine 是开源的，有问题可以直接查看源码分析。

CinemachineCamera 是一个组件，可以添加到一个空的 GameObject 上。它在 Scene 中表示一个 CinemachineCamera。

任何时候，每个 CinemachineCamera 属于以下状态之一：

- Live：CinemachineCamera 主动控制一个带有 Cinemachine Brain 的 Unity 相机。当 Cinemachine Brain 在两个 CinemachineCamera 之间进行混合时，这两个 CinemachineCameras 都处于活跃状态。当混合完成后，只有一个 CinemachineCamera 处于活跃状态。
- Standby：CinemachineCamera 不会控制 Unity 相机。然而，它仍然会跟随并瞄准其目标，并进行更新。处于此状态的 CinemachineCamera 已被激活，但其优先级与当前活跃的 CinemachineCamera 相同或更低。
- Disabled：CinemachineCamera 不会控制 Unity 相机，也不会主动跟随或瞄准其目标。处于此状态的 CinemachineCamera 不会消耗处理能力。要禁用 CinemachineCamera，只需停用其 GameObject。此时 CinemachineCamera 虽然存在于场景中但处于禁用状态。不过，即使 GameObject 被停用，如果该 CinemachineCamera 正在参与混合过程，或者被 Timeline 调用，它仍然可以控制 Unity 相机。

# Passive Cameras

CinemachineCamera 本身是一个被动对象，这意味着它的变换（transform）可以被控制或作为其他对象的父级，就像任何其他 GameObject 一样。它充当真实相机的占位符：当它处于 Live 状态时，Unity 相机会被定位以匹配 CinemachineCamera 的变换，并且其镜头设置也会与之匹配。此外，作为 Cinemachine 生态系统的一部分，它可以参与混合（blend），并且可以通过 Timeline 中的 Cinemachine 轨道进行控制。你还可以添加诸如冲击力（impulse）、后期处理（post-processing）、噪声（noise）以及其他扩展效果，以增强镜头的表现力。

当 CinemachineCamera 激活工作时，它的 Transform （position，rotation）完全被跟踪算法组件控制，其他组件对 Transform 的修改将无效。

# Going Procedural

然而真正的魔力在于当你添加程序化组件（Procedural Components）让摄像机活起来时，它能稳健地追踪目标并 compose 它的 shots。为此，你可以添加位置控制（Position Control）、旋转控制（Rotation Control）和噪声行为（Noise behaviors）来驱动 CinemachineCamera 的位置、旋转和镜头参数。当 Cinemachine Brain 或 Timeline 将 Unity 相机的控制权转移给 CinemachineCamera 时，这些设置就会被应用到Unity Camera上。

![CmCameraInspector](../Images/CmCameraInspector.png)

# 属性

- Solo

  toggle CinemachineCamera 是否临时处于活跃状态。使用此属性可在 Game View 中立即获得视觉反馈，以便调整CinemachineCamera。

- Game View Guides

  切换 Game View 中 compositional 辅助线的可见性。当"追踪目标"指定了一个游戏对象，并且 CinemachineCamera 具有 screen-composition 行为（如Position Composer 或 Rotation Composer）时，这些辅助线就会显示。此设置对所有 CinemachineCameras 共享。

  - Disabled：Game View Guides 不显示
  - Passive：Game View Guides 在相关 components 选中时显示
  - Interactive：Game View Guides 在相关 components 选中时显示，并可以在 Game View 中用鼠标拖拽来改变 settings

- Save During Play

  勾选此项可在游戏运行模式下应用更改。使用此功能可以精细调整CinemachineCamera，无需记住哪些属性需要复制粘贴。此设置对所有CinemachineCameras通用。

- Priority And Channel

  此设置控制 CinemachineBrain 如何使用该 CinemachineCamera 的输出。启用此选项可使用优先级或自定义CM输出通道。

  - Channel

    此设置用于控制哪个CinemachineBrain将由该摄像机驱动。当场景中存在多个CinemachineBrain时（例如实现分屏功能时）需要使用此功能。

  - Priority

    此设置用于控制在未受Timeline控制时，多个活跃的CinemachineCameras中哪一个应该处于活跃状态。默认情况下，优先级为0。使用此设置可以指定自定义的优先级值。数值越高表示优先级越高。也允许使用负值。当没有使用Timeline时，Cinemachine Brain会从所有已激活且具有与当前活跃CinemachineCamera相同或更高优先级的CinemachineCameras中选择下一个活跃的CinemachineCamera。在使用Timeline配合CinemachineCamera时，此属性无效。

- Tracking Target

  CinemachineCamera程序化跟随的目标游戏对象。程序化算法在更新Unity相机的位置和旋转时，会将该目标作为输入使用。

- Look At Target

  如果启用，这将指定一个不同的目标游戏对象，Unity相机将瞄准该目标。Rotation Control 属性使用此目标来更新Unity相机的旋转。

- Standby Update

  控制当 CinemachineCamera 不处于活跃状态时，其更新频率。

  - Always：保持每帧更新 virtual camera，即使它不是 live 的相机
  - Never：只在 virtual camera 是 Live 时，才更新相机
  - RoundRobin：偶尔更新 virtual camera，精确地频率依赖于有多少 virtual cameras 时 standby 的。轮转算法，每次（每帧）更新一个 standby 相机

- Lens

  以下这些属性是 Unity camera 相应属性的镜像。

  - Field Of View
  - Presets
  - Orthographic Size
  - Near Clip Plane
  - Far Clip Plane
  - Dutch
  - GateFit
  - SensorSize
  - LensShift
  - FocusDistance
  - Iso
  - ShutterSpeed
  - Aperture
  - BladeCount
  - Curvature
  - BarrelClipping
  - Anamorphism

- Mode Override

  允许你选择不同的相机模式，在Cinemachine激活此CinemachineCamera时应用到Unity相机组件上。

  重要提示：要使此覆盖设置生效，你必须在CinemachineBrain检查器中启用"镜头模式覆盖"选项，并在那里指定一个默认镜头模式。

  - None：保持相机中的投影（Projection）和物理相机（Physical Camera）属性不变。

  - Orthographic：将 Unity Camera 的 Projection 属性设置为 Orthographic。

  - Perspective：将 Unity Camera 的 Projection 属性设置为 Perspective，并开启 Physical Camera 的功能和属性。

  - Physical：将 Unity Camera 的 Projection 属性设置为 Perspective，并开启 Physical Camera 的功能和属性。

- Blend Hint

  为进出此 CinemachineCamera 时的位置混合提供提示。这些值可以组合使用。

  - Spherical Position

    在混合过程中，相机会沿着围绕追踪目标的球形路径移动。

  - Cylindrical Position

    在混合过程中，相机会沿着追踪目标周围的圆柱形路径移动（垂直坐标采用线性插值）。

  - Screen Space Aim When Targets Differ

    在混合过程中，追踪目标的位置将在屏幕空间中进行插值，而不是在世界空间中。

  - Inherit Position

    当此 CinemachineCamera 变为活跃状态时，尽可能强制将初始位置设为 Unity Camera 的当前位置。

  - Ignore Target

    在旋转混合时不要考虑追踪目标，仅进行球面插值。

  - Freeze When Blending Out

    通常情况下，相机在混合过程中会保持活跃状态，因为这样能产生最平滑的过渡效果。如果启用了此提示，则相机在淡出混合时不会更新；相反，它会创建其状态的快照，然后基于该快照进行混合。

    即将混合目标冻结为其淡出时刻的状态。淡出过程中，相机不会继续更新。

    所谓的状态就是相机的各种参数：位置、旋转、Lens，FOV 等等。

- Position Control

  用于快速设置 CinemachineCamera 程序化 positioning behaviour 的 short cut。

  选择一个位置跟踪算法，会为 GameObject 添加相应的组件。

- Rotation Control

  用于快速设置 CinemachineCamera 程序化 rotation behaviour 的 short cut。

- Noise

  用于快速设置 CinemachineCamera 程序化 noise 的 short cut。

- Add Extension

  用于快速设置 CinemachineCamera 添加过程化 extension 行为的 short cut。
  

