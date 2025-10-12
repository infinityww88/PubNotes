使用 Cinemachine 需要一种全新的相机操作思维方式。例如，你可能此前投入了大量精力来精心编写相机行为脚本。但有了 Cinemachine，即便不能实现更好的效果，也能在更短的时间内达成相同的结果。

# Cinemachine Cameras

Cinemachine 并不会创建新的相机。相反，它通过一个单一的 Unity 相机来实现多个镜头的拍摄效果。你可以通过 Cinemachine 相机（有时也被称为虚拟相机）来编排这些镜头。Cinemachine 相机会移动和旋转 Unity 相机，并控制其各项设置。

CinemachineCameras 是与 Unity Camera 分开的 GameObject，它们独立运行。它们之间并不相互嵌套。例如，一个场景可能看起来是这样的：

![CinemachineSceneHierarchy](../Images/CinemachineSceneHierarchy.png)

这个 CinemachineCamera 的主要任务是：

- 在 Scene 中放置 Unity Camera
- 将 Unity Camera 瞄准一些东西
- 为 Unity Camera 添加过程化噪声。噪声模拟类似手持摄像机或车辆振动的效果

Cinemachine 鼓励你创建许多 CinemachineCameras。CinemachineCamera 被设计为消耗很少的处理能力。如果你的场景对性能敏感，在任何给定时刻停用除必要的 CinemachineCameras 之外的所有摄像机，以获得最佳性能。

建议为单个镜头片段(shot)使用一个 CinemachineCamera。利用这一点来创建戏剧性的或微妙的剪辑或混合。例如：

- 对于两个角色交换对话的过场动画，使用三个 CinemachineCameras：一个摄像机用于两个角色的中景，以及分别为每个角色设置单独的 CinemachineCameras 用于特写。使用 Timeline 将音频与 CinemachineCameras 同步。
- 复制一个现有的 CinemachineCamera，使两个 CinemachineCameras 在场景中的位置相同。对于第二个 CinemachineCamera，更改其视野（FOV）或构图。当玩家进入触发体积时，Cinemachine 会从第一个 CinemachineCamera 混合到第二个 CinemachineCamera，以强调动作的变化。

在任何时间点，都有一个 CinemachineCamera 控制着 Unity 相机。这就是当前的活跃 CinemachineCamera。唯一的例外情况是在一个 CinemachineCamera 到下一个 CinemachineCamera 的混合过程中。在混合期间，两个 CinemachineCameras 都是活跃的。

# Cinemachine Brain

Cinemachine Brain 是 Unity Camera 上的一个组件。Cinemachine Brain 会监控场景中所有活跃的 CinemachineCameras。要指定下一个活跃的 CinemachineCamera，你可以激活或停用所需的 CinemachineCamera 的游戏对象。然后 Cinemachine Brain 会选择最近被激活的、具有与当前活跃 CinemachineCamera 相同或更高优先级的 CinemachineCamera。它会在前一个和新的 CinemachineCameras 之间执行剪切或混合。

使用 Cinemachine Brain 可以实时响应动态的游戏事件。它允许你的游戏逻辑通过操控优先级来控制相机。这在实时游戏中特别有用，因为游戏中的行动并不总是可以预测的。在可预测的情境中（比如过场动画），可以使用 Timeline 来编排相机。Timeline 会覆盖 Cinemachine Brain 的优先级系统，从而为你提供精确到帧的相机控制。

# Positioning and Aiming

使用 CinemachineCamera 中的 Position Control 属性来指定如何在场景中移动它。使用 Rotation Control 属性来指定如何瞄准它。

默认，一个 CinemachineCamera 有一个 Tracking Target，它用于两个目的：

- 为 CinemachineCamera 指定了一个 GameObject 跟随移动（position control）
- 为 CinemachineCamera 指定了 LookAt target，即 CinemachineCamera 指定了瞄准的目标（rotation control）

如果你想要为这些目的使用两个不同的 GameObjects，可以在 CinemachineCamera 的 inspector 上开启 Separate LookAt Target 选项。

**Cinemachine 包含多种程序化算法来控制定位和瞄准**。每种算法都解决一个特定问题，并暴露出属性以便根据你的具体需求自定义该算法。Cinemachine 将这些算法实现为 CinemachineComponent 对象。使用 CinemachineComponentBase 类来实现自定义的移动或瞄准行为。

Position Control 属性提供了以下过程化算法，在场景中移动 CinemachineCamera：

- Tracking：以固定的关系向 Tracking target 移动，以及可选的 damping（阻尼）
- Position Composer：以固定的 screen-space 关系向 Tracking target 移动，以及可选的 damping（阻尼）
- Orbital Follow：以可变化的关系向 Tracking target 移动，可选地被 player input 移动
- Spline Dolly：以预定义的 Spline path 移动
- Hard Lock to Target：使用与追踪目标相同的位置
- Third Person Follow：将 camera 放在一个可配置的，挂载到 Tracking target 的 rigid rig 上。rig 随着 target 旋转。这非常适合用于 TPS（第三人称射击）和 POV（Point Of View）相机
- Do Nothing：不对 CinemachineCamera 进行任何过程化移动。Position 直接被 CinemachineCamera 的 transform 控制，而 CinemrachineCamera 的 transform 可以被脚本控制

Rotation Control 属性提供以下过程化算法来旋转一个 CinemachineCamera 面向 Look At target：

- Rotation Composer：使用组合约束，将 Look At 目标保持在 camera frame（视口）内
- Pan Tilt：基于用户输入旋转 CinemachineCamera
- Same As Follow Target：将 camera 的 rotation 设置为 Tracking target 的 rotation 
- Hard Look At：保持 Look At target 在 camera frame 的中心
- Do Nothing：不对 CinemachineCamera 进行任何过程化旋转。Rotation 直接被 CinemachineCamera transform 控制，它可以被脚本控制

上面的算法中有三个元素：Unity Camera -> CinemachineCamera -> Target（要观察追踪的对象）。

# Composing a shot

Position Composer 和 Rotation Composer 算法定义了 camera frame（视口） 中的区域，让你 compose 一个 shot：

- Dead zone：frame 中的区域，在其中 Cinemachine 保持 target。Target 可以在 region 中移动，Cinemachine Camera 不会调整进行 reframe target，直到 target 离开 dead zone 
- Soft zone：如果 target 进入了 frame 中的这个区域，camera 会调整并将它放回 dead zone。它可以缓慢或快速地完成，快慢根据 Damping settings 中指定的时间。
- Screen position：dead zone 的中心在屏幕上位置。0 是 screen 的中心，+1 和 -1 是 edges
- Damping：模拟当操作要给很重的物理相机时产生的延迟。Damping 指示当 target 进入 soft zone 时 camera 反应的快慢。使用小数值来模拟更加响应的相机，快速移动和瞄准，将 target 保持在 dead zone 内。较大的数值模拟更重的摄像机，数值越大，Cinemachine 允许目标穿越软区域的范围就越大。

Game View Guides 给出这些区域的一个交互的，可视化指示。

![CinemachineGameWindowGuides](../Images/CinemachineGameWindowGuides.png)

中间清空的区域指示 dead zone（target 在这个区域运动，Cinemachine 不会 reframe）。蓝色的区域指示 soft zone。Screen Position 是 Dead Zone 的中心。红色区域指示不可穿越的区域，相机会阻止 target 进入这个区域。黄色的方块指示 target 自身（在屏幕的位置）。

调整这些区域可以获得广泛的摄像机行为。为此，可以在游戏视图中拖动它们的边缘，或者在检视器窗口中编辑它们的属性。例如，对于快速移动的目标，可以使用更大的软区域；或者扩大死区，以在摄像机画面的中央创建一个不受目标运动影响的区域。利用这个功能可以处理诸如动画循环之类的情况，即当目标只是轻微移动时，你不希望摄像机对其进行跟踪。

# Using noise to simulate camera shake

现实世界中的物理摄像机通常沉重且笨拙。它们由摄像师手持或安装在诸如移动车辆等不稳定物体上。使用噪声属性可以为电影效果模拟这些现实世界的特性。例如，在跟随奔跑的角色时添加摄像机抖动，可以让玩家更沉浸于动作场景中。

在每一帧更新时，Cinemachine 会独立于相机的目标跟随运动额外添加噪声。噪声不会影响相机在后续帧中的位置。这种分离确保了 damping 等属性能按预期工作。

# Setting up CinemachineCameras

在工程中，组织 Scene Hierarchy 包含一个带 CinemachineBrain 组件的 Unity Camera，多个 CinemachineCameras。

要添加一个跟随和观察一个 target 的 CinemachineCamera：

- 在 Unity 菜单中，选择 GameObject > Cinemachine > Follow Camera

  Unity 会添加一个新的带 CinemachineCamera 组件的 GameObject。如果需要，Unity 还会添加一个 Cinemachine Brain 组件到 Unity Camera Object 上

- 用 Tracking Target 属性指定一个要跟踪和观察的 GameObject

  CinemachineCamera 总是相对 GameObject 自动放置 Unity Camera，并旋转 camera 来观察这个 GameObject，即使你在 scene 中移动这个 GameObject。

- 按需定制 CinemachineCamera

  选择 following 和 looking at 的算法，调整设置，例如 follow offset、follow damping、screen composition、和 re-aiming camera 时使用的 damping。

要添加一个 passive CinemachineCamera：

- 在 Unity 菜单中，选择 GameObject > Cinemachine > Cinemachine Camera

  Unity 会添加一个新的带 CinemachineCamera 组件的 GameObject。如果需要，Unity 还会添加一个 Cinemachine Brain 组件到 Unity Camera Object 上

- CinemachineCamera 默认创建匹配 Scene view camera。你可以设置 CinemachineCamera 的 transform 和 lens 属性

