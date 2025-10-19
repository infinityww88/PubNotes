# Client Scene

一个 client manager，包含静态 client 信息和函数。Client Scene 不是组件，是一个全局单例。它用在 Client Build 上。

这个 manager 包含被追踪的 static local objects 的引用，例如 spawner registrations。它还具有 clients 使用的默认的 message handlers，如果它们没有被注册的话。在 client connection 准备好之后，这个 Manager 用于向 game 添加和移除 player objects。

NetworkManager（client） = ClientScene + NetworkClient

ClientScene 是一个单例，它拥有静态便捷函数，例如 ClientScene.Ready()。

ClientScene 被 NetworkManager 使用，但是它可以自己独立使用。

因为 ClientScene 管理着 client 上的 player objects，它是 clients 请求添加 players 的地方。当 autoAddPlayer 被设置，NetworkManager 通过 ClientScene 自动完成这件事，但是它也可以通过在 code 中使用 ClientScene.AddPlayer() 来添加。这发送 AddPlayer 消息到 server，并导致为这个 client 创建一个 player object。

就像 NetworkServer，ClientScene 理解 local client（host mode）的概念。ClientScene.ConnectLocalServer() 用于成为一个 host，通过开启一个 local client（当 server 以及开始运行了）。

Server 向 Client Spawn Prefab，使用 Prefab 的 assetId 通信，指定要生成的 Prefab。但是 assetId 只能在 Editor 时才能得到，Unity 无法在运行时使用 assetId 查找 Prefab。所有 Networked GameObject 都具有一个 NetworkIdentity。NetworkIdentity 在 Editor 的时候就读取并保存了 Prefab 的 assetId。因此 Server 可以直接指定 Spawn 任何一个 NetworkIdentity GameObject（它里面包含 assetId）。但是当 assetId 传送到 client 时，Unity 不能使用 assetId 在运行时查找 Prefab，也无法遍历 Project 中所有的 Prefab。因此 client 只能预先构建好 assetId 和 Prefab 的映射，这样当 server 发送 assetId 到 client，就可以找到要 spawn 的 prefab。这就是为什么 Client 上必须需要预先注册 spawnable prefabs。ClientScene（NetworkManager 使用 ClientScene）提供 assetId 到 Prefab 的映射。此外，还可以注册 assetId 到 spawnHandler 的映射，当找不到 assetId 对应的 prefab 时，可以调用 handler 来获得一个 GameObject，这样可以自定义 spawn gameobject 的逻辑。

NetworkManager(Client) -> ClientScene -> NetworkConneciton

## Fields

- prefabs：public static readonly Dictionary<System.Guid, GameObject>

  这是使用 ClientScene.RegisterPrefab() 注册到 client 上的 prefabs 的 dictionary，key 是 prefab asset Id。

- spawnableObjects：public static readonly Dictionary<ulong, NetworkIdentity>

  这是 scene 中 disabled NetworkIdentity objects 的 dictionary，它们可以通过 server 的 message 被生成。

  key 是 NetworkIdentity sceneId。sceneId 是 NetworkIdentity 在 scene 中的 id，因为 Unity GameObject 在 scene 中没有可以唯一标识的 id（GameObject 只有名字，而且名字是可以重复的）。

  如果在 scene 中预先放置一些 NetworkIdentity GameObject。但是它们默认都是 disabled 的，因为它们在 scene 加载就生成，必须通过 server 通过 spawn message 在所有 clients 上同步 enable，即 spawn。

## Properties

- localPlayer：public static NetworkIdentity

  localPlayer 的 NetworkIdentity

- ready：public static bool

  当一个 client 的 connection 被设置为 ready 时，返回 true。

  一个 ready 的 client 从 server 接收状态更新，没有 ready 的 client 则不能。当游戏的状态不是 normal 的，例如 scene 改变，或者 游戏结束，这很有用（即改变 client 的 ready 状态）。

  这是只读的。要改变 client 的 ready 状态，使用 ClientScene.Ready()。Server 能够使用 NetworkServer.SetClientReady()，NetworkServer.SetClientNotReady()，和 NetworkServer.SetAllClientsNotReady() 设置 clients 的 ready state。

- readyConnection：public static NetworkConnection

  当前 ready 的 NetworkConnection。这是到 objects 生成所在的 server 的连接。

  这个 connection 可以用于向 server 发送消息。同一时刻只能有一个 ClientScene 和 ready connection。

## Methods

- AddPlayer（NetworkConnection readyConn）：public static void

  为 client 添加一个 player gameobject。这导致发送一个 AddPlayer 消息到 server，而且 NetworkManager.OnServerAddPlayer 被调用。如果一个向 AddPlayer 传递一个额外消息，则 OnServerAddPlayer 将被调用，并包含一个 NetworkReader 参数，它包含消息的内容。extraMessage 可以包含 character selection。

- ClearSpawner()

  清空这个 client 注册的 spawn prefabs，spawn handler functions。

- DestroyAllClientObjects()

  销毁 client 上的所有 networked objects。

  可以在 network connection 关闭时用于清理。

- GetPrefab(System.Guid assetId, out GameObject prefab)：public static bool

  查找这个 assetId 对应的注册 prefab。

- PrepareToSpawnSceneObjects()

  连接会后，在 client loading/unloading 一个 scene 后调用，来注册 spawnable objects。

  这是用来处理保存在 scene 中的 Networked GameObject，而不是 Prefab。Scene 中的 NetworkIdentity 使用 sceneId 标识。加载 scene 之后，调用这个方法，将 scene 中保存的 NetworkIdentity GameObjects 收集起来，使得当 server 可以想 clients 发送 SpawnSceneObject，但传递的是 sceneId 而不是 assetId。

- Ready（NetworkConnection conn）

  发送 client connection 以及准备好进入游戏的信号。

  例如，当一个 client 进入一个正在进行的游戏，并且已经完成加载当前 scene 了，就可以发送此信号（event）。Server 应该以合适的 handler 响应 SYSTEM_READY 事件，它是为这个 client 生成 player object。

- RegisterPrefab（GameObject prefab）

  向 spawning system 注册一个 prefab。

  当一个 NetworkIdentity object 在 server 使用 NetworkServer.SpawnObject() 生成时，并且那个 object 的 prefab 使用 RegisterPrefab（）注册过，client 将会使用那个 prefab 使用相同的 netId 来实例化相应的 client object。

  Prefab 在 Editor 阶段获得 assetId，但是需要在 Editor 阶段或者运行时阶段注册为 assetId-Prefab 的映射。这可以通过 NetworkManager 的 Spawnable Prefab 字段注册，也可以在 code 中使用 RegisterPrefab 注册。实际上 NetworkManager 也是在运行时将 Spawnable Prefab list 中的 prafab 依次调用 RegisterPrefab 注册的。

  NetworkManager 有一个 spawnable prefab 列表，它使用这个函数向 ClientScene 注册 prefabs。

  当前 spawnable object 集合可以通过 ClientScene.prefabs 访问。

- RegisterPrefab（GameObject prefab，SpawnDelegate spawnHandler，UnSpawnDelegate unspawnHandler）

  注册 prefab.assetId - spawnHander/unspawnHander。为一个 assetId 注册自定义 spawning methods。这应该用于不存在 spawned objects 的 prefab 的情景，例如如果它们是运行时从配置数据动态生成的。

  key 是 prefab.NetworkIdentity 的 assetId。如果已经注册过 Prefab，则不会再调用 handler，因此只应该为没有注册 prefab 的情景注册 spawn/unspawn handler。如果 prefab 没有 NetworkIdentity，则不会注册。如果 NetworkIdentity 的 sceneId != 0，说明它是保存在 scene 中，应该有 server 同步 enable，不能用于动态 spawn，因此也不会注册。

  public delegate GameObject SpawnDelegate(Vector3 position, Guid assetId);

- public static void RegisterPrefab(GameObject prefab, SpawnHandlerDelegate spawnHandler, UnSpawnDelegate unspawnHandler)
 
  public delegate GameObject SpawnHandlerDelegate(SpawnMessage msg);

  注册 spawnHandler 有两种格式：SpawnDelegate 和 SpawnHandlerDelegate。

  SpawnHandlerDelegate 直接使用 SpawnMessage 作为参数，SpawnDelegate 是一种简化回调格式，只使用 message 的 position 和 assetId 作为参数。

  UnspawnHandle 只有一个，UnSpawnDelegate，只使用 GameObject 作为参数。

以上 RegisterPrefab 还接受一个 System.Guid 参数版本。Guid 参数被用作 Prefab 的 assetId，但是 GameObjects 不能已经具有 assetId。

- RegisterSpawnHandler(System.Guid, SpawnDelegate, UnSpawnDelegate)
- RegisterSpawnHandler(System.Guid, SpawnHandlerDelegate, UnSpawnDelegate)
  直接注册指定 Guid 的 spawnhandler 和 unspawnhandler，不需要 GameObject。
  此时 Guid 只用作 id 标识，和 asset 无关。

- UnregisterSpawnHandler(GameObject prefab)

  反注册 ClientScene.RegisterPrefab 注册的 prefab

- UnregisterSpawnHandler(System.Guid)

  反注册 ClientScene.RegisterHandler 注册 handler

## Events

- onLoadPlayerChanged

  public delegate void LocalplayerChanged(NetworkIdentity oldPlayer, NetworkIdentity newPlayer);
