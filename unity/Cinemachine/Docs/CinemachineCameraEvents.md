当 Cinemachine 摄像机被激活时，全局事件会通过 CinemachineCore 发送。脚本可以向这些事件添加监听器，并根据它们采取行动。监听器将接收到所有摄像机的事件。

有时我们希望事件只针对特定的摄像机发送，这样脚本就可以根据该特定摄像机的活动得到通知，而无需编写代码来过滤事件。Cinemachine Events 组件正是为了满足这一需求而设计的。

如果你将它添加到一个 Cinemachine 摄像机上，它将暴露出基于该摄像机活动而触发的事件。当你为该摄像机添加的任何监听器，都会在该摄像机的相应事件发生时被调用。

如果你想获取针对特定 CinemachineBrain 触发的事件，请参见 Cinemachine Brain 事件。

如果你想获取针对特定 CinemachineCameraManager 触发的事件，请参见 Cinemachine 摄像机管理器事件。

# 属性

- Event Target

  这是正在监控其事件的对象。如果为 null，并且当前 GameObject 具有一个 CinemachineVirtualCameraBase 组件，则将使用该组件。

- Camera Activated Event

  这在混合开始时调用，当一个摄像机变为活跃状态时。参数包括：brain（大脑）、传入的摄像机。剪切（cut）被视为长度为零的混合。

- Camera Deactivated Event

  每当一个 Cinemachine 摄像机停止处于活跃状态时，此事件就会被触发。如果涉及到混合，则该事件会在混合的最后一帧之后触发。

- Blend Created Event

  每当创建新的 Cinemachine 混合时，此事件就会触发。处理程序可以修改混合的设置（但不能修改摄像机）。注意：对于时间线混合，不会发送 BlendCreatedEvents，因为这些混合预期完全由时间线控制。要修改时间线混合的混合算法，你可以为 CinemachineCore.GetCustomBlender 安装一个处理程序。

- Blend Finished Event

  每当一个 Cinemachine 摄像机完成混合进入时，此事件就会触发。如果混合长度为零，则不会触发此事件。

