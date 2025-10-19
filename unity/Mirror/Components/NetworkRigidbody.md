# Network Rigidbody

Network Rigidbody 当前是 “Experimental” 的，小心使用。

NetworkRigidbody 组件在网络上同步一个 rigidbody 的 velocity 和其他属性。当你有一个 non-kinematic Rigidbody 并具有 constant forces 应用到它们上面（例如重力），但还想要在具有 authority 的 server 或 client 应用 forces 和改变 velocity 到这个 rigidbody 时，这个组件很有用。例如，使用带有重力的 rigidbody 进行 move 和 jump 的 objects。

具有一个 NetworkRigidbody 组件的 gameobject 必须还有一个 NetworkIdentity 组件。

NetworkRigidbody 在 object 上还有一个 NetworkTransform 组件保持 position 和 velocity 一样同步时工作的最好。

![NetworkRigidbody](../../Image/NetworkRigidbody.png)

默认地，Network Rigidbody 是 server-authoritative，除非你选中 Client Authority。

Client Authority 应用到 player objects 就像被明确赋予 client 的 non-player objects，当时只用于这个 component。开启这个选项之后，value 变化从 client 发送到 server。

Sensitivity 选项允许你设置一个在 value 发送到网路上之前的最小的阈值，只有 value 变化超过这个阈值才会发送到网络上。这可以帮助最小化变化非常小的网络流量。

对于一些 object，你可能不想要它们旋转并且不想同步 Angular Velocity。Clear Angular Velocity 每一帧将会设置 Angular Velocity 为 zero，最小化 object 的旋转。如果 Sync Angular Velocity 开启，则 clear 被忽略。Clear Velocity 也是一样。

通常，改变被发送给这个组件的 object 的所有 observers。设置 Sync Mode 为 Owner Only 使得改变在 Server 和 Client 之间是私密的。

你可以使用 Sync Interval 来指定多块 syncs（seconds）。它同时应用到 Client Authority 和 Server Authority。


