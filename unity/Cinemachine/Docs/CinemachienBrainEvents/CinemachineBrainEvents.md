当 Cinemachine 摄像机被激活时，全局事件会通过 CinemachineCore 发送。脚本可以向这些事件添加监听器，并根据它们采取行动。监听器将接收到所有摄像机以及所有大脑（CinemachineBrain）的事件。

有时我们希望事件只针对特定的 Cinemachine Brain 或 Cinemachine Camera Manager 发送，这样脚本就可以根据这些特定对象的活动得到通知，而无需编写代码来过滤事件。Cinemachine Brain Events 组件正是为了满足这一需求而设计的。

它将暴露出基于目标对象活动而触发的事件。你添加的任何监听器都会在该对象发生相应事件时被调用。目标对象可以在 Brain 字段中明确指定，或者你可以将其留空并将此脚本直接添加到带有 CinemachineBrain 组件的对象上。

如果你想获取针对特定 CinemachineCamera 触发的事件，请参见 Cinemachine 摄像机事件。

如果你想获取针对特定 CinemachineCameraManager 触发的事件，请参见 Cinemachine 摄像机管理器事件。

# 属性

- Brain

  这是发出事件的 CinemachineBrain。如果为 null，并且当前 GameObject 具有 CinemachineBrain 组件，则将使用该组件。

以下 4 个事件见 CinemachineCameraEvents.

- Camera Activated Event
- Camera Deactivated Event
- Blend Created Event
- Blend Finish Event

Brain 专有事件：

- Camera Cut Event

  当发生 0 程度 blend 时调用。

- Brain Updated Event

  此事件在 Brain 处理完所有 Cinemachine 摄像机并更新主摄像机后立即发送。依赖主摄像机位置或想要修改它的代码可以从这个事件处理程序中执行。

