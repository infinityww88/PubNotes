# Network Transform

Network Transform 组件在网络上同步 networked gameobjects 的 position，rotation，scale。

具有 Network Transform 组件的 gameobject 必须具有一个 Network Identity 组件。

![NetworkTransform](../../Image/NetworkTransform.png)

默认地，Network Transform 是 server-authoritative，除非你选中 Client Authority。

Client Authority 应用到被指定赋予一个 client 的 player objects 以及 non-player objects，但是只对于这个组件（Client authority 只用于这个组件的属性）。当开启时，position 改变被从 client 发送到 server。

在 Sensitivity 下，可以设置产生 network message 的 transform values 变化的最小阈值。这帮助最小化网络 “noise”，最小化 twitch 和 jitter。

通常，改变被发送到组件所在的 object 的所有 observers。设置 Sync Mode 到 Owner Only 使得改变在 Server 和 object 的所有者 Client 之间是私有的。

使用 Sync Interval 指定同步的速率（seconds）。
