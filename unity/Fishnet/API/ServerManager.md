# ServerManager

## Fields

- Clients

  Dict<int, NetworkConnection>

  认证的和非认证的 connected clients。

## Properties

- NetworkManager

- Objects

- ShareIds

  如果设置为 true，与其他 clients 共享 clients 的 ids 和它们拥有的 objects。

  不会共享敏感信息。

- Started

  True：如果 server connection（listen socket）已经启动（server 已经开始监听指定通道）

## Method

- bool AnyServerStarted(int? excludedIndex = null)

  如果有任何 server socket 处于 started state，返回 true。

---

- void Broadcast<T>(T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  为所有客户端发送广播。

- void Broadcast<T>(NetworkConnection connection, T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  为指定 connection/client 发送广播。

- void Broadcast<T>(NetworkObject networkObject, T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  为指定 networkObject 的所有观察者发送广播。

- void Broadcast<T>(HashSet<NetworkConnection> connections, T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  为指定 connections 发送广播。

- void BroadcastExcept<T>(NetworkConnection excludedConnection, T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  为指定 connection 之外的所有连接发送广播。

- void BroadcastExcept<T>(HashSet<NetworkConnection> excludedConnections, T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  为指定 connections 之外的所有连接发送广播。

- void UnregisterBroadcast<T>(Action<NetworkConnection, T, Channel> handler)

---

Spawn 和 Despawn 只能在 sever 上执行。

- void Spawn(NetworkObject nob, NetworkConnection ownerConnection = null, Scene scene = default(Scene))

  在网络上 spawn 一个 object。可以指定 ownership connection。

- void Spawn(GameObject go, NetworkConnection ownerConnection = null, Scene scene = default(Scene))

- void Despawn(GameObject go, DespawnType? despawnType = null)

  在网络上 Despawn 一个 object。

- void Despawn(NetworkObject networkObject, DespawnType? despawnType = null)

---

- bool StartConnection()

  启动 local server connection。开始监听和完成客户端连接。

- bool StartConnection(ushort port)

- bool StopConnection(bool sendDisconnectMessage)

---

- void Kick(NetworkConnection conn, KickReason kickReason, LoggingType loggingType = LoggingType.Common, string log = "")
  立即踢出一个连接，同时调用 OnClientKick。

- void Kick(NetworkConnection conn, Reader reader, KickReason kickReason, LoggingType loggingType = LoggingType.Common, string log = "")

- void Kick(int clientId, KickReason kickReason, LoggingType loggingType = LoggingType.Common, string log = "")

--- 

- void SetRemoteClientTimeout(RemoteTimeoutType timeoutType, ushort duration)

- void SetFrameRate(ushort value)

- void SetAuthenticator(Authenticator value)
- Authenticator GetAuthenticator()

- bool GetStartOnHeadless()
- void SetStartOnHeadless(bool value)

- bool OneServerStarted()
  
  如果一个 server 启动，返回 true。


  