# Events And Callbacks

## 网络事件（框架全局）

### ServerManager

- OnAuthenticationResult(NetworkConnection, bool)

  - 当 server authenticator 得出 connection 的认证结果。Bool 指示认证是否通过。
  - 这个 event 可以用于存储以成功连接到服务器的 NetworkConnection，<br/>甚至发送一些消息到新连接的客户端

- OnClientKick(NetworkConnection, int, KickReason)

  - 当使用 Kick 将 client 从 server 移除时调用，在 client 断开连接之前调用。<br/>提供 NetworkConnection，ClientId，KickReason
  - KickReason
    - ExcessiveData：客户端发送了大量数据，可能是网络攻击
    - ExploitAttempt：客户端执行了一个仅在尝试压榨服务器的才会执行的操作
    - ExploitExcessiveData：客户端发送了超过它们应该发送的数据
    - MalformedData：接收到 client 发送过来的无法解析的 Data
    - UnexpectedProblem：服务器出现问题，唯一的选择是将该客户端踢出
    - Unset：未指示任何原因
    - UnusualActivity：客户端行为异常，例如提供了多个无效状态。这可能不是攻击行为，但无法完全确定

- OnRemoteConnectionState(NetworkConnection, RemoteConnectionStateArgs)
  - 当 remote client state 改变时调用
  - 当 client 连接 server 或断开时立即调用
  - 用途
    - 检测 client 何时断开连接
    - authentication 脚本处理发送的数据，进行认证（在认证器开始认证之前）
    - 在认证器认证之前检测 server 是否已满
  - 传递客户端连接 NetworkConnection
  - RemoteConnectionStateArgs
    - ConnectionId：状态发送改变的 client 的 ID。<br/>如果是 ConnectionState 用于 local server 的，Id 为 -1
    - ConnectionState（RemoteConnectionState）
     - Started：连接完成
     - Stopped：连接完全停止
    - TransportIndex：multiple transports 中使用的 transport 的索引

- OnServerConnectionState(ServerConnectionStateArgs)

  - 当 sever 的网络状态改变时调用（Socket 绑定本地端口和终止的过程）
  - 当 server 开始和停止时调用
  - ConnectionState(LocalConnectionState)
    - Started：连接已完成
    - Starting：连接正在构建，尚未完成
    - Stopped：连接已完全停止
    - Stopping：连接正在停止
  - TransportIndex：multiple transports 中使用的 transport 的索引

### ClientManager

- OnAuthenticated：client 被成功认证后调用，认证失败直接踢出。<br/>此时 Client 会有一个 ClientID，并添加到 ServerManager.Clients 和 ClientManager.Clients 中
- OnClientConnectionState(ClientConnectionStateArgs)
  - 当 client 到 sever 的连接状态改变时调用
  - 当 client 连接到 server 或断开连接时立即调用
  - 用途
    - 检测何时连接到服务器
    - 检测何时从服务器断开连接
    - 认证脚本 authentication scripts 会使用这个事件向 server 发送初始认证数据<br/>（用户名、密码等），使得 server 可以认证此客户端
  - ClientConnectionStateArgs
    - ConnectionState（LocalConnetionState）
    - TransportIndex
- OnRemoteConnectionState(RemoteConnectionStateArgs)
  - 当非自身的 client （其他 client）的连接状态改变时调用
  - 用于检测其他 player 连接到游戏或从游戏中断开<br/>（应由 server 发送的通知，因为 client 彼此之间不连接）
  - 只在 ServerManager.ShareIds 时可用
- OnClientTimeout
  - 本 client 到 server 的连接超时。超时后，断开连接之前立即调用
- OnConnectedClients(ConnectedClientArgs)
  - 当 server 发送当前所有连接的 clients 时调用。<br/>只在 ServerManager.ShareIds 时可用
  - ServerManager.ShareIds：True to share the Ids of clients and the objects they own with other clients. <br/>No sensitive information is shared.

## 场景事件(SceneManager)

- OnActiveSceneSet<bool>
  - scene 加载后，设置好 active scene 立即调用
  - Unity 游戏中有一个 active scene，其余 scene 时 additive scenes。<br/>GameObject 都只能生成在 active scene 中
  - 在 scene objects 的 NetworkBehaviour callbacks 之前运行
  - bool 指示 scene 时被用户指定为 active 的
- OnClientLoadedStartScenes<NetworkConnection, bool>
  - 连接后，client 加载初始 scene 时调用
  - bool -> asServer
  - 客户端 side 的 SceneManager 的回调
  - asServer 都是用于 Host 模式用来判断 server 还是 client 的
- OnClientPresenceChangeStart<ClientPresenceChangeEventArgs>
  - ClientPresenceChangeEventArgs
    - bool Added：如果是 client 添加到 scnee 为 true，如果是移除为 false
    - NetworkConnection connection
    - Scene scene
- OnClientPresenceChangedEnd<ClientPresenceChangeEventArgs>
  - 当客户端在场景中的呈现状态发生变化（且服务器已重建观察者列表）后触发此调用。
- OnLoadStart：当 scene 加载开始时调用
- OnLoadEnd：当 scene 加载结束时调用
- OnLoadPercentChange：加载 scene 时进度改变时调用，从 0f 到 1f，可用于绘制进度条
- OnQueueStart/OnQueueEnd
  - 场景加载卸载是耗时操作
  - 涉及网络
  - 可能同时处理多个场景操作
  - Fishnet 提供了一个操作队列，缓存并异步执行所有场景操作
  - 当队列为空并开始一个场景操作时，触发 QueueStart
  - 在队列非空的时候，任何接下来的场景操作都会入队，且不会触发 QueueStart
  - 队列中每个场景加载卸载会触发各自的事件（OnLoadStart/End, OnUnloadStart/End）
  - 当所有操作都处理完，队列为空时，触发 QueueEnd，下次再来新的场景操作，重新触发 QueueStart
- OnUnloadStart：当 scene 卸载开始时调用
- OnUnloadEnd：当 scene 卸载结束时调用

## 对象事件

### NetworkObject

- OnHostVisibilityUpdated
  - 用于 Host 模式，当 host 的 client 获得或失去 object 的 visibility 时调用
  - bool 指示 clientHost 获得 visibility
- OnObserversActive
  - 当 NetworkObject 失去所有观察者，或者之前没有任何观察者现在获得观察者时调用

### NetworkBehaviour

- OnDespawnServer(NetworkConnection)
  - object 的 despawn message 发送到 connection 之前，在 server 上调用
  - 可以用于在 despawn 之前向 clients 发送 rpc call 或 actions
- OnOwnershipClient(NetworkConnection)
  - 当 client 获得或失去这个对象的所有权时调用，在 client 上调用
  - NetworkConnection：之前拥有这个 object 的 owner
- OnOwnershipServer(NetworkConnection)
  - 当 NetworkConnection 获得或失去这个对象的所有权时调用，在 server 上调用
- OnSpawnServer(NetworkConnection)
  - object 的 spawn message 发送到 connection 之后，在 server 上调用
  - 用于在 object spawn 之后向 clients 发送 rpc 或数据
- OnStartClient()
  - 当 object 初始化之后，在 client 上调用
- OnStartNetwork()
  - 当 network 初始化这个 object 时调用
  - 可以为 server 和 client 调用，但是只会调用一次
  - 当作为 server 或 host，这个方法在 OnStartServer 之前执行
  - 当作为 client only（非 host client），这个方法在 OnStartClient 之前执行
- OnStartServer()
  - 在 network object 初始化只会，在 server 上调用
  - 这个方法之前或之中的 SyncTypes 修改，会在 spawn message 中发送给 clients
- OnStopClient()
  - object 反初始化之前，在 client 上调用
- OnStopNetwork()
  - 当 network 反初始化 object 时调用
  - 可以在 server 和 client 上调用，但只会调用一次
  - 当作为 host 或 server，这个方法在 OnStopServer 之后调用
  - 当作为 client only，这个方法在 OnStopClient 之后调用
- OnStopServer()
  - 反初始化 object 之前在 server 上调用

## 时间事件(TimeManager)

- OnFixedUpdate：MonoBehaviour 调用 FixedUpdate 时调用
- OnLateUpdate：MonoBehaviour 调用 LateUpdate 时调用
- OnPostPhysicsSimulation
  - 当使用 TimeManager 作为 physics timing 时，它在这个 tick 发生的 physics simulation 之后立刻调用
  - 当使用 Unity 作为 physics timing 时，它仅在存在物理帧的情况下于Update阶段被调用。
  - 如果你想对 stacked scenes 运行不同物理模拟，可以使用这个事件
- OnPostTick
  - tick 之后调用
  - 如果使用 PhysicsMode.TimeManager，physics 此时已经模拟
- OnPrePhysicsSimulation
  - 当使用 TimeManager 作为 physics timing 时，它在这个 tick 发生的 physics simulation 之前调用
  - 当使用 Unity 作为 physics timing 时，它在 FixedUpdate 期间调用。
  - 如果你想对 stacked scenes 运行不同物理模拟，可以使用这个事件
- OnPreTick：tick 之前调用，也在 data 之前
- OnRoundTripTimeUpdated：当 local clients ping 更新后调用
- OnTick：tick 时调用
- OnUpdate：MonoBehaviour 调用 Update 时调用

## 连接事件（NetworkConnection）

- OnLoadedStartScenes(NetworkConnection, bool asServer)：这个 connection 加载完 start scenes 时调用
- OnObjectAdd(NetworkObject)：connection 获得一个 object 的 ownership 时调用，并在 object 被添加到 Objects 之后调用。<br/>对这个 connection 和 server 可用
- OnObjectRemoved(NetworkObject)：connection 失去这个 object 的 ownership 时调用，并在 object 从 Objects 移除之后调用
