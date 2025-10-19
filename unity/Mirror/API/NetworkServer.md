# Network Server

public static class NetworkServer : object

NetworkServer（以及 NetworkClient） 不是组件，而是一个单例的类。因此它不会在 scene 切换过程中销毁（例如 NetworkManager）。它一旦连接上，就在整个游戏进程中执行网络操作。NetworkManager 是使用 NetworkServer（NetworkClient）实现的高级管理器组件，而不是自己执行网络操作。完全可以使用 NetworkServer/NetworkClient 自己实现 NetworkManager。NetworkServer 和 NetworkClient 是底层的网络工具类。

Client Player 网络连接是全局维护的（NetworkServer，NetworkClient），而 NetworkManager 是对当前 scene 的 networked gameobjects 的管理组件，尽管它可以使用 DontDestroyOnLoad 在多个 scenes 之间共享，但本质上仍然是 scene scope 的，即 SceneNetworkedManager。当切换 scene 时，需要重构 scene 的 networked gameobjects，但是 player 的连接不会被影响。

NetworServer/NetworkClient 是全局的底层网络连接管理类，NetworkManager 是调用 NetworkServer/NetworkClient 实现的常用的 networked scene 管理组件。可以自己使用 NetworkServer/NetworkClient 实现 networked scene 管理器，但是也将会和 NetworkManager 类似。

NetworkServer 通过一个 NetworkServerSimple 实例 处理来自 remote clients 的 remote connections，并且对一个 local client 也具有一个 local connection（host）。

NetworkServer 是一个 singleton。它拥有静态便捷函数诸如 NetworkServer.SendToAll()，NetworkServer.Spawn()，它们自动使用这个 singleton instance。

NetworkManager 使用 NetworkServer，但是 NetworkServer 可以独立于 NetworkManager 使用。

以及生成的 networked objects 集合被 NetworkServer 管理。Objects 是通过 NetworkServer.Spawn() 生成，并将它们添加到这个集合中，并使它们在 clients 上创建。Spawned objects 在它们销毁时自动移除，或者它们可以通过调用 NetworkServer.UnSpawn() 来从 spawned set 中移除，这并不销毁 object，只是不再同步。

NetworkServer 内部使用大量的 internal messages，它们在调用 NetworkServer.Listen() 时被设置（注册消息和对应的回调函数）。

NetworkManager 使用 NetworkServer 的 API 提供了更高级的功能，NetworkManager 做的事情都可以使用 NetworkServer API 完成。

主要方法：

- 为连接添加/替换/移除/销毁 Player GameObject
- 注册/替换/反注册/清理 message handler
- 监听（Listen）/ 启动 server，断开连接，关闭 server
- 发送网络消息
- 生成 Spawn/UnSpawn Objects
- 标记 client ready 或 not ready

## Fields

- connections：public static Dictionary<int, NetworkConnectionToClient>

- disconnectInactiveConnections：public static bool

  Server 是否应该断开那些静默时间超过 Server Idle Timeout 的 remote connections

- disconnectInactiveTimeout：public static float

  从最后一条消息到 server 自动断开连接之间的 Timetout 时间（seconds）。

  这个最初从 NetworkManager 中设置，并可以在运行时修改。

  默认地，clients 至少每 2s 发送一个 Ping 消息。

  Host 的 local client 不会自动断开连接。

  默认为 60s。

- dontListen：public static bool

  如果开启这个选项，server 将不会监听网络端口进入的连接

  这可以用于游戏运行于 host mode，而且不想 external players 来连接它，即使它成为 single-player 游戏。在使用 AddExternalConnection 时也很有用。

## Properties

- active：public static bool

  检查 server 是否启动了。

  当 NetworkServer.Listen() 被调用之后为 true。

- localClientActive：public static void

  如果 Host Server 上 local client active 则为 true

- localConnection：public static NetworkConnectionToClient

  Host mode 下 local client 的 connection

## Methods

- ActivateHostScene()：public static void

  对于所有 spawned object，如果 isClient 为 false，调用其 OnStartClient

- AddConnection(NetworkConnectionToClient conn)：public static bool

  接受一个 network connection，并将它添加到 server。

  这个 connection 将使用注册在 server 的 callbacks。

- AddPlayerForConnection(NetworkConneciton conn, GameObject player)：public static bool

  当一个 AddPlayer 消息 handler 接收到一个 player 的请求，server 调用这个方法将 player object 关联到 connection。

  当为一个 connection 添加一个 player，这个 connection 的 client 就自动 ready 了。Player object 是自动生成的，因此你不需要为那个 object 调用 NetworkServer.Spawn。这个 function 用于添加一个 player，而不是替换那个连接的 player。如果那个 connection 以及有了 player，调用将会失败。

- AddPlayerForConnection(NetworkConneciton conn, GameObject player, Guid assetId)：public static bool

  为 player object 的 NetworkIdentity 设置 assetId

- ReplacePlayerForConnection(NetworkConnection conn, GameObject player, bool keepAuthority)

  替换 connection 的 player object 为另一个 play object。旧的 player object 不销毁（例如在一个 race game 中，player 可以从一个 car 跳到另一个 car，原来的 car 需要继续 running）。

  这不改变 connection 的 ready state，因此它在 changing scenes 时可以安全地使用。
  
- ReplacePlayerForConnection(NetworkConnection conn, GameObject player, Guid assetId, bool keepAuthority)

- Destroy(GameObject)：public static void

  销毁这个 object 和所有 clients 上的对应 objects 版本。

  一些情况下，从 spawned list 移除一个 object（不再同步） 而不是从 server 上删除它很有用，为此，使用 NetworkServer.UnSpawn() 而不是 NetworkServer.Destroy()

- DestroyPlayerForConnection(NetworkConnection conn)：public static void

  在一个 server 上销毁 NetworkConnection 关联的所有 player objects。

  这用于当 client 断开连接时，移除这个 client 的 player，以及销毁在这个 connection 上设置 authority 的 non-player objects。

- DisconnectAll()：public static void

  断开当前连接的所有 clients，除了 local connection。

  这能在 server 上调用。Clients 将收到 Disconnect message。

- Listen(Int32 maxConns)：public static void

  启动 server，设置连接的数量。

- Shutdown()

  关闭 server 并断开所有 clients 的连接

- NoConnections()：public static bool

  如果 connections 为空，或者只有 host。

- RegisterHandler<T>(Action<T> handler, bool requireAuthentication = true) where T : NetworMessage

  为特定 message type（T）注册一个 handler。

  有一些 system message types，你可以添加 handlers。你还可以添加自己的 message types。

  requireAuthentication：如果 message 需要一个 authenticated connection 则为 true

- RegisterHandler<T>(Action<NetworkConnection, T> Boolean) 

  handler 包含一个 NetworkConnection 参数。

- RemoveConnection(Int32 connectionId)：public static bool

  移除一个 AddExternalConnection 添加的一个 external connection，connectionId 是要移除的 connection 的 id。

- RemovePlayerForConnection(NetworkConnection conn, Boolean destroyServerObject)

  从 connection 移除 player object

- ReplaceHander<T>(Action<T> handler, bool requireAuthentication = true)

  替换指定消息类型的 handler

- ReplaceHandler<T>(Action<NetworkConnection, T> handler, bool requireAuthentication = true)

- UnregisterHandler<T>()

  反注册一个特定 message type 的 handler

- ClearHandlers()：public static void

  清理所有注册的 callback handlers

- Reset()

  重置 NetworkServer singleton

- SendToAll<T>(T msg, int channelId = null, bool sendToReadyOnly = false)

  想所有 connected clients 发送一个消息，无论是 ready 还是 not-ready 的。

- SendToClientOfPlayer<T>(NetworkIdentity identity, T msg, int channelId = null)

  指向指定 player 发送消息，可以指定一个 channelId，这样一个 player 和 server 可以有多个 channel，每个用于传递不同类型的消息。

- SendToReady<T>(T msg, int channelId = null)

  只向准备好的 clients 发送消息。这样可以让 room 内准备好的 clients 发送房间内更新消息。

- SendToReady<T>(NetworkIdentity identity, T msg, bool includeOwner = true, int channelId = null)

  只向准备好的 clients 以及可选地包含一个 object（identity） 的所有者（client）发送消息。

- SendToReady<T>(NetworkIdentity identity, T msg, int channelId)

  调用上面的 SendToReady，并且 includeOwner = true

- SetAllClientsNotReady()

  标记所有连接的 clients 不再 ready。所有 clients 不在发送状态同步更新。Player's clients 可以调用 ClientMananger.Ready() 重新进入 ready 状态。这可以用于切换 scenes。

- SetAllClientNOtReady(NetworkConnection conn)

  标记指定 client 不再 ready。

- SetClientReady(NetworkConnection conn)

  标记指定 client ready。当一个 client 通知它已经准备好了，这个方法告诉 server 这个 client 已经准备好接受 spawned objects 和 state synchronization 更新了。这通常在 SYSTEM_READY 消息的 handler 中调用。如果游戏没有要采取的特殊的 action，则依赖默认的 ready handler 函数也没问题，因此这个调用不是必须的。

- Spawn（GameObject obj，NetworkConnection ownerConnection = null）：public static void

  在所有的 ready clients 上生成给定的 gameobject。

  这将导致从 registered prefab 生成一个新的 object，或者从一个自定义 spawn 函数。

  obj 是带有 NetworkIdentity 的要生成的 gameobject。
  
  ownerConnection：赋予 object 的 authority 的 connection。

- Spawn（GameObject obj，Guid assetId，NetworkConnection ownerConnection = null）

  obj：要生成的 obj

  assetId：要生成的 object 的 assetId，用于自定义 spawn handlers

  ownerConnection： 具有 object 的 authority 的 connection

- Spawn（GameObject obj，GameObject ownerPlayer）

  obj：要生成的 object

  ownerPlayer：设置 Client Authority 的 player object

- SpawnObjects()：public static bool

  这个导致 scene 中 NetworkIdentity 在 server 上生成。

  一个 scene 中的 NetworkIdentity objects 默认是 disabled。调用 SpawnObjects() 导致这些 scene objects enabled 并 spawned。它就好像对 scene 中每一个 NetworkIdentity GameObject 调用 NetworkServer.Spawn()。可以预先在 Scene 中保存一些 Networked GameObject。调用这个方法使得所有 clients 上同步 enable 这些 objects。就像 GameObject 既可以作为 prefab 保存在 project 中，在运行时动态生成，也可以预先保存在 scene 中。

- UnSpawn(GameObject)

  un-spawn 已经 spawned object。

  这个 object 将会从生成它的所有 clients 上移除，或者为这个 object 调用 client 上的自定义 unspawn handler 函数。

  不像调用 NetworkServer.Destroy()，在 server 上这个 object 不会销毁。这允许 server 重用 这个 object，或者之后重新 spawn 它。

- Update()

  在 LateUpdate 中，有 NetworkManager 调用。

  