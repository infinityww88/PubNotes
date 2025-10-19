# NetworkClient

public static class NetworkClient : object

被 networking system 使用。它包含一个 NetworkConnection，用于连接一个 network sever。

NetworkClient 处理 connection state，messages handlers，和 connection 配置。

同一时刻一个进程中可以有多个 NetworkClient，但只有一个可以连接一个 game server（NetworkServer）。

NetworkClient 有一个内部的 update 函数，它处理来自 transport layer 的事件。

这包含异步 connect / disconnect 事件，以及来自 server 的数据。

NetworkManager 有一个 NetworkClient 实例用于它启动的游戏，但是 NetworkClient 也可以被独立使用。

- 连接/断开连接 server/host
- 注册/反注册 消息处理器
- 发送消息
- Shutdown

## Properties

- active：public static bool

  当 client 正在连接或已经连接，则为 true（当 network 为 active）

- connection：public static NetworkConnection

  client 使用的 NetworkConnection

- isConnected

  client 是否已经连接

- isLocalClient：public static bool

  client 是否是 host mode 下的 local client

- serverIp：public static string

  client 连接的 server 的地址。当 client 还没有 connected，这个字段为空。

## Methods

- Connect(string address)

- Connect(Uri uri)

- ConnectHost()

- ConnectLocalServer()

  connect host mode

- Disconnect()

- DisconnectLocalServer()

  disconnect host mode。这也需要为 host client 调用 DisconnectMessage。

- RegisterHandler<T>(Action<T> hander, bool requireAuthentication = true)

- RegisterHandler<T>(Action<NetworkConnection, T> handler, bool requireAuthentication = true)

- ReplaceHandler<T>(Action<T> handler, bool requireAuthentication = true)

- ReplaceHandler<T>(Action<NetworkConnection, T> handler, bool requireAuthentication = true)

- Send<T>(T message, int channelId = null)

- UnregisterHandler<T>()

- Shutdown()

- Update()
