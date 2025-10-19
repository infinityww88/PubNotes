# Network Manager

Network Manager 是一个组件，用来管理 multiplayer game 网络的方方面面。

Network Manager 功能包括：

- 游戏状态管理
- Spawn 管理
- Scene 管理
- 调试信息
- 自定义

## Geting Started with the Network Manager

Network Manager 是一个 multiplayer game 的核心控制组件。若要开始使用，在你的 starting scene 中创建一个 empty gameobject，然后添加 Network Manager 组件。新添加的 Network Manager 组件看起来像这样：

![NetworkManagerInspector](../../Image/NetworkManagerInspector.png)

注意：你在每个 scene 只能有一个 active Network Manager，因为它是一个单例。不要将 Network Manager 组件放在 networked gameobject（具有 NetworkIdentity Component）上，因为 Mirror在加载 scene 时会 disable 它们。

如果你已经非常熟悉 multiplayer 游戏开发，你可能发现知道 Network Manager 组件是完全通过 API 实现的是非常有用的，因此它做的每件事你都可以通过脚本来做。对于高级用户，如果你需要扩展 NetworkManager 组件的功能，你可以使用脚本从 Network Manager 派生自己的类并通过覆盖任何虚拟函数 hooks 来定制它。然而，Network Manager 组件包装了大量有用的功能在一个地方（在 NetworkManager 同时包含 client 和 server 代码），并且使 creating，running 和 debugging multiplayer 游戏尽可能简单。

## Transports

Mirror 使用单独的 component（从 Transport 类派生）来在网络上连接。默认地，它是 Telepathy Transport。这种将 transport 分离到自己的组件中的设计允许游戏开发者选择最适合其游戏需求的选择。改变 transports 只需要简单为 Network Manager Transport 字段赋值那样简单。

有效的 Transports 是 TCP，UDP，WebGL，和 Steam。此外，有一个 Multiplex transport 允许在 server 上同时使用两个 transports，例如 Telepathy 和 WeSockets，因此 desktop 和 browser players 可以在同一个 server 上无缝地 play。

## Game State Management

一个 Networking multiplayer game 可以运行在 3 个模式：

- client
- dedicated server
- host（同时作为 client 和 server）

如果你使用 Network Manager HUD，它自动告诉 Network Manager 从哪个 mode 开始，基于 player 点击哪个 button。如果你编写自己的 own UI 来允许 player 开始游戏，你需要从 code 中调用这些功能。这些方法是：

- NetworkManager.StartClient
- NetworkManager.StartServer
- NetworkManager.StartHost

无论从哪个模式开始，Network Address 和 Transport Port 属性都会被使用：

- 在 client 模式，游戏试图连接指定的 address 和 port specified。可以使用一个 fully-qualified domain name（FQDN）也可以用于 Network Address，例如“game.example.com”
- 在 server 或 host 模式，游戏监听指定端口上进入的连接，但是不绑定任何指定的 IP 地址，而是监听所有可用的地址

## Spawn Managerment

使用 Network Manager 来管理 spawning（networked instantiation），networked gameobject 从 prefab 生成。

![NetworkManagerSpawnInfo](../../Image/NetworkManagerSpawnInfo.png)

绝大多数游戏有一个 Prefab 代表 player，因此 Network Manager 有一个 Player Prefab slot。你可以将你的 player Prefab 赋予这个 slot。当你有一个 player Prefab 集合，对于每个进入游戏的 player，一个 player gameobject 自动从那个 Prefab 集合生成。这应用于 hosted server 上的 local player，和 remote clients 上的 remote players，server 上的 player 通过 client 向 server 发送 player spawn 消息来生成。你必须在将 Player Prefab 赋予到 field 之前附加一个 Network Identity 组件。

一旦你赋予一个 Player Prefab，你可以以 host 开始游戏，并观察这个 player gameobject 的生成。停止这个游戏将销毁 player game object。如果你构建和允许另一个游戏的副本，并连接它到 localhost 作为 client，NetworkManager 使另一个 player gameobject 出现。当你停止这个 client，它（host）销毁那个 player 的 gameobject。

除了 Player Prefab，你还必须注册其他的那些你想使用 Network Manager 在 game play 期间动态生成的 prefabs（装备，金币）。

你可以添加 prefabs 到 inspector 中的 Registered Spawnable Prefabs 的 list。你还可以通过 code 注册 prefabs，使用 ClientScene.RegisterPrefab 方法。

如果你有一个 Network Manager，它在 scenes 之间持久化，通过 Don't Destroy On Load（DDOL），你需要注册所有 prefabs 到它上面，它们可能在任何一个 scene 中生成。如果你在每个 scene 中有一个单独的 Network Manager，你只需要注册那个 scene 相关的 prefabs。

## Start Positions

Network Manager 默认将会在它们定义的 transform position 和 rotation 生成 Player Prefab，然而 Player Spawn Method 属性允许你控制如何联合 Network Start Position 组件来选择 start positions：

- Choose Random 来在随机选择的 startPosition 选项生成 players
- Choose Round Robin 来在 startPosition options 列表中循环

如果 Random 或 Round Robin 模式不满足你的游戏，你可以使用 code 定制如何选择 start position。你可以通过 NetworkManager.startPositions 列表访问可用的 Network Start Position 组件，你还可以使用 NetworkManager 上的 helper 方法 GetStartPosition，它可以被用于一个 OnServerAddPlayer 实现来发现一个 start position。

## Scene Management

绝大多数游戏有多个 scene。至少地，通常有一个 title screen 或 starting menu scene，以及游戏实际 played 的 scene。Network Manager 被设计以用于 multiplayer game 的方式自动管理 scene 状态和 scene 转换。

在 Network Manager inspector 上有两个 slots 用于 scenes：Offline Scene 和 Online Scene。拖放 scene assets 到这些 slots 激活 networked Scene Management。

当一个 server 或 host 开始时，Online Scene 被加载。然后它变成当前 network scene。任何连接到 server 的 client 被指示同样加载这个 scene。Scene 的名字保存到 networkSceneName 属性。

当 network 被停止时，通过停止 server 或 host，或者通过一个 client 断开连接，offline Scene 被加载。这允许游戏在从 multiplayer game 断开连接时自动回到 menu scene。

你还可以在游戏运行时改变 scenes，通过调用 ServerChangeScene。这使得所有当前连接的 clients 同样改变 Scene。通过设置 scenes，以及调用这些方法，你可以控制你的 multiplayer game 的流程。

注意 scene 改变导致前面scene 的所有 gameobjects 被销毁。

你通常应该确保 Network Manager 在 Scenes 之间持久，否则 network connection 在 scene 改变时断开。然而，还可能在每个 scene 有一个具有不同 settings 的单独 Network Manager，如果你希望控制增量 prefab 加载，或者不同的 scene transitions，这非常有用。

## Customization

在 NetworkManager 类上有虚拟方法，你可以通过创建继承自 NetworkManager 的自己的派生类来定制。当实现这些函数，确保注意默认实现提供的功能。例如，在 OnServerAddPlayer，函数 NetworkServer.AddPlayer 必须被调用来 activate connection 的 player game object。

## Properties

- dontDestroyOnLoad

  使用这个属性控制 Mirror 是否应该在 scene 改变时销毁具有 Network Manager 的 gameobject。勾选这个 checkbox 确保 Mirror 在 Scene 改变时不会销毁 NetworkManager gameobject。否则 Mirror 在 NetworkManager 所在的 scene 不在 active 时销毁 gameobject。如果你想在每个 scene 中管理单独的 Network Manager gameobject，这非常有用。默认是勾选的。

- runInBackground

  使用这个属性控制一个 networked game 是否在 window 失去焦点时仍然运行。默认勾选。如果你想在同一个机器上运行程序的多个实例，你需要勾选它，例如当使用 localhost 测试时。在部署到 mobile 平台上时，你应该 disable 它。当 enable 时，它在 NetworkManager 启动时设置 Application.runInBackground 为 true。你还可以在 Unity menu：Edit > Project Settings 上设置这个属性。

- startOnHeadless

  如果这个 box 被选中，并且运行程序的计算机没有 graphic device，程序将会以 server mode 启动。

- serverTickRate

  设置 server 的 target frame rate。默认 30.

- showDebugMessages

  控制 Mirror 输出到 console window 的信息的数量。

- offlineScene

  如果为这个字段赋予一个 scene，当一个 network session 停止时，Network Manager 自动切换到指定的 scene，例如，当 client 端口连接，或者当 server 关闭。

- onlineScene

  如果为这个字段赋予一个 scene，当一个 network session 停止时，Network Manager 自动切换到指定的 scene，例如，当 client 连接到 server，或者 server 开始监听连接时。

- Network Info

  - transport

    一个对 Transport 类对象的连接。默认地，TelepathyTransport 被创建并连接到这个字段。

  - networkAddress

    当前使用的 network address。对于客户端，这是可以连接到 server 的地址。对于 server，这是 local address，默认地，它被设置为 localhost。clients 可以使用 FQDN 地址。

  - maxConnections

    可以连接到 server 的最大客户端数量。注意 host 是一个 server 和 一个 client。Transports 对这个字段也可能有它们自己的设置，否则它们或者复制这个 value，或者将它留给 Mirror 来管理 limit。

- SpawnInfo

  - playerPrefab

    定义默认 Mirror 在 server 上应该用于创建 player gameobjects 的 prefab。Mirror 在 server 上的 AddPlayer 的默认 handler 中创建 Player gameobjects。实现 OnServerAddPlayer 来覆盖这个行为。

  - autoCreatePlayer

    勾选这个选项，如果你想 Mirror 在连接以及当 Scene 改变时自动创建 player gameobjects。默认勾选。

  - playerSpawnMethod

    定义 Mirror 应该如何决定在哪里生成新的 player game objects。默认是 Random。

    - random
    
      选择 Random 在随机选择的 startPositions 来生成 players 

    - roundRobin

      选择 RoundRobin 在 startPositions list 中循环

  - spawnPrefabs

    注册到 Network Manager 的 prefabs 列表

  - startPositions

    Transforms 列表，使用 scene 中所有具有 Network Start Position 组件的 gameobjects 构建

  - clientLoadedScene

    指示 client 已经加载当前的 scene

  - numPlayers

    返回 NetworkServer 的 active connections 数量，只在 server 上有效

  - networkSceneName

    当前加载和 active scene 的 名字

  - isNetworkActive

    指示 server 处于 online，或者 client 已经连接

  - client

    返回 NetworkClient.singleton

  - isHeadless

    指示 application 以 headless mode 启动

## Methods

### Unity Virtual Callbacks

```C#
public virtual void Awake() {}

public virtual void Start() {}
```

### Server Method

```C#
public bool StartServer() {}

public void StartClient() {}

public void StopHost() {}

public void StopServer() {}

public void StopClient() {}

public Transform GetStartPosition() {}
```

### Server Static Methods

```C#
public static void RegisterStartPosition(Transform start) {}

public static void UnRegisterStartPosition(Transform start) {}

public static void Shutdown() {}
```

### Server Virtual Methods

```C#
public virtual void ConfigureServerFrameRate() {}

public virtual void StartHost() {}

public virtual void ServerChangeScene(string newSceneName, LoadSceneMode sceneMode, LocalPhysicsMode physicsMode) {}

public virtual void OnServerConnect(NetworkConnection conn) {}

public virtual void OnServerDisconnect(NetworkConnection conn) {}

public virtual void OnServerReady(NetworkConnection conn) {}

public virtual void OnServerAddPlayer(NetworkConnection conn, AddPlayerMessage extraMessage) {}

public virtual void OnServerRemovePlayer(NetworkConnection conn, NetworkIdentity player) {}

public virtual void OnServerError(NetworkConnection conn, int errorCode) {}

public virtual void OnServerSceneChanged(string sceneName) {}

public virtual void OnStartHost() {}

public virtual void OnStartServer() {}

public virtual void OnStopServer() {}

public virtual void OnStopHost() {}

public virtual void OnDestroy() {}
```

### Client Virtual Methods

```C#
public virtual void OnStartClient() {}

public virtual void OnStopClient() {}

public virtual void OnClientConnect(NetworkConnection conn) {}

public virtual void OnClientDisconnect(NetworkConnection conn) {}

public virtual void OnClientError(NetworkConnection conn, int errorCode) {}

public virtual void OnClientNotReady(NetworkConnection conn) {}

public virtual void OnClientChangeScene(string newSceneName, LoadSceneMode sceneMode) {}

public virtual void OnClientSceneChanged(NetworkConnection conn) {}
```
