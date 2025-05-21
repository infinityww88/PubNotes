Cinemachine 在 cameras 激活和失活时，在 blend 开始和完成时，产生 events。更进一步，当 camera cut 发生时，即 active Cinemachine Camera 改变而不 blending 时，也会触发事件。

当 Cinemachine 发送一个事件，它被 CinemachineCore 全局发送。Scripts 可以添加 listeners 到这些事件，并基于它们采取行动。Listeners 为所有 cameras 接收事件。

Events 在每个 manages blends 的 context 中生成。这包括 CinemachineBrain，它在最高等级处理 blends，这还应用到 Cinemachine Manager Cameras 上，它们自己管理其 child cameras 之间的 blends。

有时只想对特定 camera 发送事件，这样脚本可以基于特定 camera 活动收到通知，而不需要通过 code 来 filter events。Cinemachine 提供以下 behaviours 来执行 filtering logic：

- 可以通过添加 Cinemachine Camera Events behaviour 到 CinemachineCamera 来过滤对特定 CinemachineCamera 的 activating 或 deactivating 相关的事件。
- 可以通过添加 Cinemachine Camera Manager Events 到 ManagerCamera 来过滤 ManagerCamera 产生的事件
- 可以通过添加 Cinemachine Brain Events 到 CinemachineBrain 来过滤 CinemachineBrain 产生的事件