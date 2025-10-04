Cinemachine Brain 是 Unity 相机挂载的一个组件。它会监测场景中所有处于活动状态的 CinemachineCamera，选择下一个用于控制 Unity 相机的 CinemachineCamera，并控制从当前 CinemachineCamera 切换（或混合过渡）到下一个的过程。

带有 Cinemachine Brain 的对象在层级视图中会显示一个小小的 CinemachineCamera 图标。你可以在 Cinemachine 偏好设置面板中关闭该图标显示。

要为 Unity Camera 添加要给 Cinemachine Brain 组件，有两种方法：

- 使用 GameObject > Cinemachine 菜单为场景中添加一个 CinemachineCamera，这会让 Unity 同时为 Unity camera 添加一个 Cinemachine Brain 组件，如果 Unity camera 上还没有这个组件。
- 手动为 Unity Camera 添加一个 Cinemachine Brain 组件。

提示：你还可以在 Timeline 中控制 CinemachineCameras。Timeline 会覆盖 Cinemachine Brain 的决定。

Cinemachine Brain 控制以下关键属性：

- Blend Settings

  一个 定义如何从一个CinemachineCamera混合过渡到另一个的列表。例如，可以向列表中添加一个 item，实现从vcam1到vcam2的4秒混合过渡，再添加另一个 item 实现从vcam2返回vcam1的1秒混合过渡。如果两个相机之间的混合未被定义，Cinemachine Brain将使用其默认混合设置。

- Channel Filter

  Cinemachine Brain 只会使用那些 输出到通道掩码（Channel Mask）中所包含通道的 CinemachineCamera。你可以通过使用通道掩码来筛选通道，从而设置分屏环境。

- Event Dispatching

  当Cinemachine Brain切换镜头时会触发事件。当某个CinemachineCamera开始生效时，它会触发一个事件；当它从一个CinemachineCamera剪切切换到另一个时，也会触发一个事件。你可以使用后一种事件来重置时间类后期特效。

 ![CinemachineBrainInspector](../../Images/CinemachineBrainInspector.png)

# 属性

- Show Debug Text：勾选此项可在视图中显示当前活跃的CinemachineCamera及其混合状态的文本摘要。
- Show Camera Frustum：勾选此项可在场景视图中显示相机的视锥体。
- Ignore Time Scale：勾选此项可使CinemachineCamera即使在游戏慢动作运行时，也能实时响应用户输入和阻尼效果。
- World Up Overide：指定 GameObject 的Y轴将作为 CinemachineCamera 的世界空间上向量。此属性适用于俯视角游戏环境。设置为None将使用世界空间的Y轴。正确设置此属性对于避免极端上下视角情况下的万向节锁非常重要。
- Channel Mask：CinemachineBrain 会查找输出到所选任意通道中优先级最高的 CinemachineCamera。未输出到这些通道之一的 CinemachineCamera 将被忽略。通常情况下，此值应保持为“默认(Default)”。仅在需要多个 CinemachineBrain 的情况下（例如实现分屏功能时）才需更改此设置。
- Update Method：何时更新CinemachineCamera的位置和旋转。
  - Fixed Update：将CinemachineCamera的更新与物理模块同步，在FixedUpdate中进行更新。
  - Late Update：在 MonoBehaviour LateUpdate 中更新 Unity Camera。
  - Smart Update：根据每个CinemachineCamera的目标更新方式来更新相机。这是推荐的设置。
  - Manual Update：CinemachineCamera不会自动更新。您必须在游戏循环中的适当时机显式调用brain.ManualUpdate()。这应该在任何相机 LookAt 或 Follow 目标移动之后进行。这是一个高级功能。
- Blend Update Method：何时解析 blends 和 update main camera。
  - Late Update：建议设置
  - Fixed Update：仅在更新方法(Update Method)设置为FixedUpdate且混合时出现卡顿(judder)的情况下使用此设置。
- Lens Mode Override：启用后，Cinemachine相机将允许覆盖主相机的镜头模式（透视模式/Perspective、正交模式/Orthographic 或物理镜头模式/Physical）。
  - Default Mode：当启用镜头模式覆盖(Lens Mode Override)且没有CinemachineCamera正在主动覆盖镜头模式时，此镜头模式将被应用到主相机上。
    - None：如果启用了镜头覆盖模式(Lens Override Mode)且将默认模式(Default Mode)设置为"无(None)"，那么当CinemachineCamera未覆盖镜头模式时，将不会向相机推送任何默认模式。此设置不建议使用，因为它可能导致不可预测的结果。最佳做法是始终设置一个默认模式。
    - Orthographic：将 Projection 设置为 Orthographic。
    - Perspective：将 Projection 设置为 Perspective，关闭 Physical Camera 的功能和属性。
    - Physical：将 Projection 设置为 Perspective，开启 Physical Camera 的功能和属性
- Default Blend：当未明确定义两个CinemachineCamera之间的混合过渡时，将使用的默认混合方式。
  - Cut：Zero-length 混合
  - Ease In Out：S-shaped curve
  - Ease In
  - Ease Out
  - Hard In
  - Hard Out
  - Linear
  - Custom：自定义 blend curve，你自己绘制 curve。
- Custom Blends：包含场景中特定CinemachineCamera之间自定义混合设置的资源资产。
- Create Asset：创建一个包含CinemachineCamera之间自定义混合列表的资源资产。
- Camera Cut Event：当某个CinemachineCamera直接激活（无混合过渡）时触发此事件。
- Camera Activated Event：当某个CinemachineCamera开始生效时触发此事件。如果涉及混合过渡，则该事件会在混合的第一帧触发。

