# NetworkConnection

## Fields

- ClientId(int)

  Connection 的 Id，可被其他客户端共享。

- CustomData(object)

  和 connection 关联的自定义数据，可以被 user 修改。这个字段的数据不会通过网络同步。

- Objects(HashSet<NetworkObject>)

  connection 拥有的 Objects。对 connection 和 server 可用。

## Properties

- Disconnecting

  connection 是否正在断开连接，只对 server 可用（监听连接）。

- FirstObject(NetworkObject)

  第一个拥有 ownership 的 NetworkObject。

- IsActive

  Connection IsValid and not Disconnecting。

- IsAuthenticated

  Connection 是否被认证。只对 server 可用。

- IsHost

  如果 connection 是 clientHost，返回 True。

- IsLocalClient

  如果 connection 是这个 client 的 connection，返回 true。

- IsValid

  如果 connection 是 valid 的返回 true

  一个 invalid connection 指示这个 connection 没有设置任何 client。

- LocalTick（EstimatedTick）

  近似 local tick，如同当前连接中的实际情况。其中还包含本地和远程的最后设置的值。

- NetworkManager

- PacketTick（EstimatedTick）

  从该连接接收到的最后一个未乱序数据包的计时器（滴答）值。此值仅在服务器端可用。

  有两种计时：

  - Time（seconds）
  - Tick（ticks）

  这与操作系统的具有两种时间标识是一样的，一个是滴答 tick 时间，一个是时钟时间（时分秒）。
  
  FishNet 提供了在 Tick 和 Time 之间的转换方法。

- ReplicateTick（EstimatedTick）

  ​​服务器端针对此连接的近似复制计时器（滴答）。其中还包含本地和远程的最后设置值。

- Scenes（HashSet<Scene>）

  connection 所在的 scenes。对 connection 和 server 可用。

- TransportIndex(int)

## Methods

- void Broadcast<T>(T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)

  对这个 connection 发送一个广播。

- void Disconnect(bool immediately)

  断开此连接。

- bool Equals(NetworkConnection nc)

- string GetAddress()

  返回 connection 的地址。

- void InitializeState()：用于 pool
- void ResetState()：用于 pool

- void Kick(KickReason kickReason, LoggingType loggingType = LoggingType.Common, string log = "")

  踢出这个 connection，同时调用 OnClientKick。

- void Kick(Reader reader, KickReason kickReason, LoggingType loggingType = LoggingType.Common, string log = "")

  Reader 是 kick 前需要清空的 reader。

- bool LoadedStartScenes()

  connection 是否已经加载 start scenes。可用于 connection 和 server。

- bool LoadedStartScenes(bool asServer)

- void SetFirstObject(NetworkObject nob)

  设置一个自定义 FirstObject。connection 必须是这个 nob 的 owner。
