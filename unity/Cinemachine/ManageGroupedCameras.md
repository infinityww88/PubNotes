管理成组的 cameras。

一个 Manager Camera 监视很多 CinemachineCameras 但是从 Cinemachine Brain 和 Timeline 的视角看，表现地就像一个 CinamachineCamera。

Cinemachine 包含这些 manager cameras：

- Sequencer Camera：执行一个在其 child CinemachineCameras 进行 blends/cuts 的 sequence
- Clear Shot Camera：选择 child CinemachineCamera 中对 target 视角最好的一个
- State-Driven Camera：根据 animation state 的变化选择要给 child CinemachineCamera
- Mixing Camera：在最多8个 child CinemachineCameras 中，使用平均权重创建一个连续的 blend

因为 manager cameras 表现地像一个正常的 CinemachineCameras，你可以嵌套它。换句话说，联合使用 CinemachineCameras 和 Manager Cameras 可以创建任意复杂的 camera rigs。

### 创建自己的自定义 Manager Camera

可以创建你自己的 Manager Camera，并根据你提供的算法选择当前 active child CinamachineCamera。例如，如果正在制作一个 2D 平台游戏，想要一个根据角色是否向左移动、向右移动、跳跃、跌落来分别 frame 角色的 camera rig，自定义 CameraManager class 是最好的选择。

为此，创建一个继承 CinemachineCameraManagerBase 的类。这个基类实现一个 CinemachineCamera children 数组，和一个 blender。

然后，实现 abstract ChooseCurrentCamera 方法。当 manager 激活时，这个方法会在每帧进行调用，并且返回当前帧应该 active 的 camera。你的类可以以任意算法决定返回哪个 camera。例如，可以根据 player 的 state 来选择合适的 child camera。

如果新的 camera 和上一帧的不同，CinemachineCameraManagerBase 将会开始一个 blend，根据你在它的 DefaultBlend 和 CustomBlends 字段的设置。

一旦为每个 play state 添加带合适 setting 的 child cameras，并使它们在 manager camera instance 中正确配置，就得到一个 Cinemachine rig，它会根据 player state 调整自己。这个 rig 对系统其他地方看起来就像一个正常的 CinemachineCamera（就是要给 Camera Group），并可以用在任何 CinemachineCameras 可以使用的任何地方，包括嵌套在其他 rigs 中。

注意开箱提供的 State-Driven Camera，它实现了这样类似的功能，相关的 player state 被编码进了一个 Animation Controller State-Machine 中。如果 state 不是从 Animation Controller 中读取，你可以实现自己的 Manager。

Managed Cameras 需要作为 Manager Camera 的 GameObject children。这注意使放置出现依赖循环，强制作为 children 可以确保不会出现依赖循环。
