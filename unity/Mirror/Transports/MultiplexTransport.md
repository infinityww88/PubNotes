# Multiplex Transport

Multiplex Transport 自身不是一个 transport，但是它允许你组合其他 transports，使得你的 clients 可以通过它们中的一个来连接 servers。

一个常见的情景是 server 同时监听 websockets 和 TCP。你的 webgl clients 可以使用 websockets 连接到 server，而你的 mobile 或 desktop clients 使用 TCP 连接到 server。在 HLAPI，你必须在 websockets 和 UDP 之间进行选择，但你不能同时使用它们。你可以在 Multiplex Transport 中配置任何数量的 transports。

要使用 Multiplex Transport：

1. 在 scene 中添加一个带有 NetworkManager 组件的 gameobject
2. 默认地，Unity 将会在 NetworkManager gameobject 上添加 TelepathyTransport
3. 添加一个 MultiplexTransport 组件到 gameobject 上
4. 将 MultiplexTransport 组件赋予到 NetworkManager 的 transport 上
5. 添加一个 WebsocketTransport 组件到 gameobject 上
6. 添加 TelepathyTransport 组件到 MultiplexTransport 作为第一个 transport
7. 添加 WebsocketTransport 组件到 MultiplexTransport 作为第二个 transport

请注意：Telepathy 和 WebsocketTransport 不可以连接同一个端口。默认地，Telepathy 监听 7777 端口，websocket transport 监听 7778 端口。

如果你构建游戏作为一个 webgl 游戏，TelepathyTransport 将会被跳过，你的 client 将使用 websocket transport。如果你构建游戏作为一个 mobile 或 desktop app，它将选择 TelepathyTransport。Server 可以同时接收来自二者的连接。

![MultiplexSample](../../Image/MultiplexSample.png)
