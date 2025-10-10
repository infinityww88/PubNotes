管理相机（Manager Camera）负责统筹多个CinemachineCamera，但从Cinemachine Brain和Timeline的角度来看，它表现得就像一个单一的CinemachineCamera。

Cinemachine 包含以下 manager cameras：

- Mixing Camera：使用最多 8 个 child CinemachineCameras 的加权平均值
- Sequencer Camaera：使用 child CinemachineCameras 执行一个的 blends 或 cuts 的 sequence
- Clear Slot Camera：采用对 target 具有最佳视角的 CinemachineCamera
- State-Driven Camera：改变 animation state 时，采用某个 child CinemachineCamera

因为 Manager cameras 表现地就像一个正常的 CinemachineCameras，因此可以嵌套它们。换句话说，可以联合正常 CinemachineCameras 和 Manager Cameras 来创建任意复杂的 camera rig（装置）。

# Making Your Own Custom Manager Camera

可以创建自己的管理相机，根据自定义的任意算法来选择当前活跃的子相机。

例如，如果正在制作一款2D平台游戏，并希望相机装置 camera rig 能根据角色是向右移动、向左移动、跳跃还是下落等不同状态来自行调整取景(frame)方式，那么编写一个自定义的CameraManager类可能就是个不错的解决方案。

要实现这一点，可以创建一个继承自CinemachineCameraManagerBase的新类。该基类已经实现了包含多个CinemachineCamera子对象的数组以及一个混合器（blender）。

接下来，需要实现抽象方法 ChooseCurrentCamera。每当管理器处于激活状态时，该方法会在每一帧被调用，其作用是返回本帧应当处于活跃状态的子相机。您的自定义类可以采用任意逻辑来做出这个决定。在示例中，该方法会检查玩家的状态（比如面向方向、是否处于跳跃或下落状态等），然后选择合适的子相机。

如果新需要的相机与上一帧的不同，CinemachineCameraManagerBase 将根据您在 DefaultBlend 和 CustomBlends 字段中设置的配置发起一次混合过渡。

当您为每种玩家状态添加了带有相应设置的子相机，并将它们连接至您的管理器实例后，您就拥有了一个会根据玩家状态自动调整的Cinemachine相机装置。该装置本身在系统其他部分看来就像一个普通的CinemachineCamera，因此可以像使用普通CinemachineCamera一样在任何地方使用它——包括嵌套在其他相机装置中。

Manager CC 和 Normal CC 每帧执行的方法、回调等等都一样，这就是为什么它可以 Normal CC 一样被使用。

# Managed Cameras need to be GameObject children of the manager

这主要是为了防止在嵌套管理器时可能出现的递归循环问题。强制要求被管理的相机必须作为子对象存在，从而彻底杜绝了递归的可能性。



