使用 Timeline 可激活、停用 Cinemachine 相机，并在它们之间进行混合。在 Timeline 中，可将 Cinemachine 与其他游戏对象和资源结合使用，以交互方式实现并调整丰富的过场动画，甚至支持交互式过场动画。

对于简单的 shot sequences，可以直接使用 Cinemachine Sequencer Camera，无需使用 Timeline。

Timeline 覆盖 Cinemachine Brain 决定的优先级。当 timeline 完成时，控制返回给 Cinemachine Brain，然后它选择具有最高优先级的 CinemachineCamera 来控制 Unity Camera。

在 Timeline 中，使用 Cinemachine Shot Clip 控制 CinemachineCameras。每个 shot clip 指向一个 CinemachineCamera，用以激活和关闭它。使用一个 shot clips 的序列来指定每个 shot 的顺序和 duration。

要在两个 CinemachineCameras 中进行剪辑（cut），将一个 clip 放在另一个后面。要在两个 CinemachineCameras 之间 blend，将 clip 首尾进行重叠。

![CinemachineTimelineShotClips](../../Images/CinemachineTimelineShotClips.png)

要为 Cinemachine 创建 Timeline：

- 创建一个 Empty GameObject，命名为 IntroTimeline
- 选中这个 GameObject，创建一个 Timeline Asset 和 instance
- 点击 Timeline window 的 lock 按钮，锁定 Timeline instance，使得更加容易地编辑 timeline
- 将一个 带 CinemachineBrain 的 Unity Camera 拖拽到 Timeline Editor 中，然后在下拉菜单中选择 Create Cinemachine Track
- 添加其他 tracks 到 Timeline 来控制场景中的其他东西，例如 Animation track 来活动 main character

提示：可删除引用你的 Timeline object 的默认 track。这个 track 对 Timeline 不是必须的。

要添加 Cinemachine Shot Clips 到 Cinemachine Track 中：
- 在 Cinemachine Track 中，右键单机，并选择 Add Cinemachine Shot Clip
- 使用以下两种方法之一添加 shot clip：

  - 将现有 CinemachineCamera 拖拽到 Cinemachine Shot 组件的 CinemachineCamera 属性中，来将现有CinemachineCamera 添加到 shot clip 中
  - 要创建新的 CinemachineCamera，并将其添加到 shot clip，点击 Cinemachine Shot 组件的 Create 按钮

- 在 Timeline editor 中，调整 shot clip 的 order，duration，cutting，和 blending
- 调整 CinemachineCamera 的属性以在场景中放置它，并指示它应该 aim 或 follow 什么
- 要动画 CinemachineCamera 的属性，为它创建 Animation Track，并向其他任意 GameObject 一样为其添加动画
- 组织你的 Timeline tracks，并精细调整场景

