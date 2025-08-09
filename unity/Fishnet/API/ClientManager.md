# ClientManager

## Fields

- Clients

  Dict<int, NetworkConnection>

  当前所有连接到 server 的 clients。

  注意这是保存在客户端上的。因此这个字段只在 ServerManager.ShareIds 开启时才包含数据。

  即只有 ServerManager.ShareIds 开启后，Server 才会将所有客户端的 Id + Connection 发送给所有客户端保存。除此以外不向客户端透露任何敏感信息。

  如果想要客户端查看其他客户端的信息，需要服务器将客户端信息保存在 sync 容器，以 clientId 或 connection 为键，通过 SyncTypes 将这些信息发送给所有客户端，然后客户端通过 clientId 或 connection 查找相关信息。

- NetworkConnection

  用于向 server 发送数据的本地客户端 connection。

  对应 NetworkObject/NetworkBehaviour 的 LocalConnection。

## 属性

- IsServerDevelopment
- NetworkManager

- Objects

  本地客户端已知对象的处理及信息。

- Started

  如果 client connection 已经连接到 server，返回 true。

## 方法

- void Broadcast<T>(T message, Channel channel = Channel.Reliable)

- void RegisterBroadcast<T>(Action<T, Channel> handler)

  为广播消息类型注册一个回调。

- void UnregisterBroadcast<T>(Action<T, Channel> handler)

- void SetRemoteServerTimeout(RemoteTimeoutType timeoutType, ushort duration)

- bool StartConnection()

  启动 local client（本地客户端）到 server 的 connection。

- bool StartConnection(string address)

  设置 transport address，并启动 local client connection。

- bool StartConnection(string address, ushort port)

  设置 transport address，并启动 local client connection，连接指定端口。

- StopConnection()

  关闭 local client connection。

- void SetFrameRate(ushort value)
