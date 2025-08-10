- 网络启动停止
- 代码环境检测（client、server、host）
- 网络状态事件通知
- NetworkObject 生命周期
- Communication（Rpc，SyncTypes，Broadcast）
- 所有权管理
- 观察者系统
- NetworkObject 生成销毁
- 场景管理
- 数据序列化
- 预测（运动、对象生成）
- 延迟补偿
- Fishnet 大部分能力（场景管理、对象管理）都是 server 端的能力（服务端权威），只能服务端发起。<br/>客户端的能力只有 ServerRpc，预测移动和预测生成（客户端权威）
- 网络调用在 NetworkBehaviour 脚本中，通过 SceneManager、ServerManager、NetworkBehaviour 的 API。
- 每个 NetworkObject 在服务端和客户端都有副本，在 NetworkObject 的 server 端副本的 NetworkBehaviour 的 code 中进行调用（意味着要判断代码的执行环境）

## Scene 管理

Scene 可以本质上和 Prefab 差不多，都是 Game 中一组 GameObject 的管理单位，让 Unity 以一个集合一起处理一组 GameObjects（加载、卸载）。对于 Fishnet 也是一样，Scene 是其在网络上，在 Server 和 Clients 之间，以一组 GameObject 集合（Scene）一起加载、卸载一组 GameObject。甚至可以整个游戏中可以只有一个 Scene，然后仅以 Prefab 管理子场景（一组 GameObjects）。Fishnet 的场景就是 Unity 的场景，因此只需在网络上传递场景名字即可加载、卸载场景。但是 Fishnet 在 Unity 场景之上还管理了更多一些信息，因此 Fishnet Game Server 和 Clients 应该使用 Scene 管理和同步。Scene 管理（加载、卸载）只应该由 server 发起，客户端只能被动接收、同步。但是注意，场景可以作为 Additive 加载到当前游戏中，而无需替换游戏中的当前场景。

NetworkObject 可以有一个 owner（Connection），Connection 应在某个或某几个 Scenes 中。

SceneManager 只在 server 使用。Server 上 SceneManager 维护 NetworkConnection 和 Scene 的对应关系。操作 Scene 都是 Scene 对象，不是名字，说明是本地操作。Scene Condition。

- Global Scenes

  通过 ServerManager.LoadGlobalScenes 加载的 scenes。

  Server 记录作为 Global 加载的 scenes。

  每个 clients 都要加载这个 scene。

- Init Scenes

  Server 当前的 Global Scenes。它们是后续连接的 client 的 init scenes 或 start scenes。
  
  每次客户都连接并认证成功后，Server 会将 global scenes 的名字广播给它，通知其加载这些 scenes。

- Default Scene

  游戏的当前 Active Scene。新生成的 GameObject 总是在 Active Scene 中实例化。

  通过 GameObject.scene 可以得到其所在的 scene。

  ServerManager.AddOwnerToDefaultScene，就将 NetworkObject 的 owner 添加到 GameObject.scene 中

- NetworkConnection Scenes

  为 NetworkConnection 加载的 Scene。

  Server 会加载这些 scene，但是只有指定的客户端才会加载同样的 scene。


Server 端维护 Scene 和 Connection 的对应关系中，Scene 为对象类型（即 Unity 中的 Scene），说明是本地使用，网络使用应传递 scene 名字。从 Scene 类型中可以获取 Scene 的名字。

Server 加载为 Global 的 scenes 为所有客户都加载。为 Connection 加载的 scene 在 server 和指定的 clients 上加载。指定为空的 Connections 加载的 Connection Scene 只在 server 上加载，不会通知任何客户端加载，它们也不是 Global scenes，后续客户端也不会加载，因此它们将只在 server 存在（当然后续也可以卸载），scene 只是管理一组 GameObject 的单位，server 端会有需要只在服务端加载一组 gameobjects 而不需要任何 client 加载的情形。

Server 分别维护 Fishnet.ServerManager 加载的 scenes（Global Scenes/Connection Scenes）和 SceneConnections（Scene 与 Connection 的对应关系）。这就存在一种不一致的情况，ScenesConnection 中的 scene 不是 ServerManager 加载的 scene，例如游戏开始时，server 和 client 都处于一个由 Unity SceneManager 加载的场景，而不是 Fishnet SceneManager 加载的场景。

严格来说，Fishnet 网络通信不依赖 Scene。即使 Server 和 Client 都位于不同的 Scene，只要它们所有的 NetworkObject 都是同一个 Object 的副本（即运行时生成的）并且 Server 端将客户都的连接手动加入到 SceneConnections 中，理论上应该一样就像游戏。但是处理这样的例外，甚至基于它来开发，不仅棘手，而且没有任何意义和好处。这不仅涉及 Scene 和 Connection 对应关系的管理，还涉及观察者系统的管理，还有客户端的 scene 如果与服务端的 scene 不一致且包含 NetworkObject 会导致什么样的后果等等。网络编程是非常复杂和精密的任务，即使努力遵守一切约定，仍然可能出现各种意想不到的的错误。即使让 server 和 client 保持 scene 同步，也可能会出现意外情况。而且加载一个 scene 就如同实例化一个 Prefab 一样，从不会认为实例化一个 Prefab 是多么麻烦的一件事。因此从一开始就应该进入 Fishnet Manager 的世界，由 Fishnet 管理一切，确保 Server 和 Client 的 scene 始终保持同步。

- Server 和 Client 初始时都位于由 Unity SceneManager 加载的场景
- Server 应该立即加载一个 Global Scenes 作为自己和 Clients 的初始场景
- Client 在 offline scene 中（Unity SceneManager 加载的 scene 中）可以作为自己的房间或仓库，进行一些换装、组装等游戏操作
- Client 决定开始多人游戏，开始连接服务器
- Client 连接到服务器后，Server 会通知 Client 加载当前的 Globals scenes
- 此后 Server 和 Client 就可以正常同步了
- 这样操作后，就不需要手动添加 connection 到 scene 中了，因为 LoadGlobalScene/LoadConnectionScene 会自动将 connection 添加到 SceneConnections
- DefaultScene 组件就是做的这件事情，源代码很容易理解。这也是文档为什么建议不用使用 AddOwnerToDefaultScene 的原因

一旦解决了场景同步的问题，游戏逻辑只需要专注生成 NetworkObject 和分配、转移所有权，和兴趣区域管理。

## DefaultScene

- DefaultScene 是一个很好的起点，尽管简单，但是仍然可以很好地用于正式开发中

  因为它处理了 offline scene 和 online scene 直接的切换工作，完成 Server 和 Client 初始的同步工作，后续同步就简单多了。

  一旦进入 online scene，就可以以那个 online scene 为起点加载更多 network scenes。

  一旦回到 offline scene，既可以向普通 Unity Scene 加载各种 local scene。

  因此尽量使用 DefaultScene。

  其 code 很好理解，可以作为如何手动进行此工作的参考。即使你自己手动编写，大概也是如此而已。

## PlayerSpawner

和 DefaultScene 一样，PlayerSpawner 处理另一种场景需求，为客户端生成要给初始 NetworkObject，也是一个很好的起点。

这是一个很常见的需求，几乎是多人游戏的标准配置。但是 Fishnet 足够灵活，并没有强制每个 client 具有一个 Player Object，但是为此提供 PlayerSpawner 预制脚本。

关键点：

- Server 端脚本：只有 server 可以 Spawn Object
- Player Prefab：为所有客户端生成这个 prefab 的一个实例
- Spawn Positions：可以指定一组位置，为每个进入的 client 循环分配一个位置
- Add to Default Scene：FishNet 不会强制客户端与服务器从同一场景开始运行。如果不在 server LoadGlobalScene，需要明确告知 FishNet 客户端是否应该观察特定场景，并接收该场景中网络对象（Network Objects）的相关信息。这通常可用于开发和测试

## asServer

Fishnet 很多地方出现的 asServer 是泛指是否在 server 执行，不仅仅是 Host 模式的 server。很多 data 都包含 asServer 指示是为服务器执行，还是为客户端执行。

实际上 Fishnet 没有单独的 Host 模式，其 Host 模式是 Instance 同时启动了 ServerManager.StartConnection() 和 ClientManager.StartConnection()。

```C#
// True if running as client, while network server is active.
bool asHost = !asServer && NetworkManager.IsServerStarted;
```

对于应该在 server 上执行的操作，不需要每个操作都验证是否在 server 上执行。很多 API 只在 server 上有意义，只需要在调用的最顶层判断是否是 server 即可，下面的可以直接调用，无需再次判断。

胖服务端（权威）瘦客户端，绝大部分工作都是由服务端来做，注意服务器包含最全面的信息，客户端有的信息，服务端一定有，服务端有的信息，客户端不一定有。每个 NetworkObject 在服务端都有副本，在它们的脚本中执行绝大部分网络操作。这些工作包括，场景加载卸载、观察者系统控制、对象生成、网络通信（RPC，Broadcast，SyncTypes），而客户端只被动地接收服务端的消息，并跟随操作即可。客户端唯一能主动做的事情只有 ServerRpc 和预测（运动预测、对象生成预测）。因此 API 中绝大部分都是暴露给 Server 端的。因此编写 code 时首先假设 code 是在服务端执行的，是没有问题的，直到确定 code 应该在客户端执行。

Fishnet 框架所有 code 在客户端服务端都存在，都能访问，例如客户端也能访问到 NetworkManager.ServerManager，但不意味着客户端应该使用服务端的 API。客户端只应该访问客户端相关的 API，服务端应该访问服务端相关的 API。

SceneManager 的 LoadScene 同时为客户端和服务端加载场景，但是它暴露的 API（LoadScene 和 UnloadScene）只应该在 server 端访问。

Fisnnet 非常灵活，网络操作的每个步骤都是独立分离的。例如加载场景和将网络连接导入到场景就是两个独立的操作（LoadScene 和 AddConnecitonToScene），然后生成 Object 又是独立的操作。

很多对 Sever 有意义的工作对 client 是没有意义的。

Server 端需要维护 Scene 和 NetworkConnection 的对应关系，即哪个 scene 包含哪些 connections，哪个 connection 在哪些 scene 中。这是因为基于 Scene 管理和分离场景是最基本的客户端管理。Server 端可能同时存在多个区域，或同时服务多个房间，只有同一个场景（或同一个兴趣区域）的客户端才能看见彼此，这是所有网络游戏最基础的。这也是为什么 SceneCondition 作为基本的 ObserverCondition 添加到 ObserverManager 作为默认条件。Fishnet 只会将 NetworkObject 的状态发送给其观察者（最基本的就是同一个 Scene 中的客户都），Owner 只是让 Server 确认来自 NetworkObject 的 Rpc 请求是 Owner Connection 发送的。以上就是 Server 要维护 Scene 和 NetworkConnection 对应关系的原因。但是这对 Client 就是没意义的。Client 的所有 Scene 都是其 NetworkConnection 能看见和所在的，不需要维护 Scene 和 Connection 的对应关系。因此 SceneManager 中管理 Scene 和 Connection 对应关系的 API 对客户端也是没有意义，它们只应该在 server 端调用。

```C#
//查看 Fishnet 源码可知，AddConnectionToScene 内部间接调用了 ServerManager.Objects.RebuildObservers()
//这充分说明了将 connection 添加到 scene 是 server 操作，维护 connection 和 server 的对应关系也是 server 操作，只应该在 server 上调用
public void AddConnectionToScene(NetworkConnection conn, Scene scene)

 _serverManager.Objects.RebuildObservers(nob);
```

因此尽管所有 code 都存在与 Server 端和 Client 端，但不是所有 API 都可以在 Client 上调用。始终记住，绝大部分操作都是在 server 端执行，都是在 server 端才有意义的。Client 上只有 ServerRpc 和 Prediction 是有意义的。

查看 Fishnet 源码，可以看见，Server 端很多地方尤其是框架内部（不是 NetworkObject 的自定义 code）是通过 Broadcast 和 Client 通信的，通过发送特定类型的 Message（向 client connection）。例如客户端连接到服务器之后，Server 就向 Client 发送加载初始场景的 Broadcast，Client 收到 Broadcast 就可以调用 SceneManager 加载场景了，而通过其中注册  SceneProcessor 可以获得场景加载的百分比（这是完全的本地操作）。

每个 NetworkObject 在 Server 和 Client 都有副本，其 code 在 server 和 client 中都能执行，因此需要区分服务端环境和客户都环境。


## 能跟 ServerManager 一个代码块运行的 code，都是在 Server 上运行的。

```C#
private void SceneManager_OnClientLoadedStartScenes(NetworkConnection conn, bool asServer)
{
    if (!asServer)
        return;
    if (_playerPrefab == null)
    {
        NetworkManagerExtensions.LogWarning($"Player prefab is empty and cannot be spawned for connection {conn.ClientId}.");
        return;
    }

    Vector3 position;
    Quaternion rotation;
    SetSpawn(_playerPrefab.transform, out position, out rotation);

    NetworkObject nob = _networkManager.GetPooledInstantiated(_playerPrefab, position, rotation, true);
    _networkManager.ServerManager.Spawn(nob, conn);

    // If there are no global scenes 
    if (_addToDefaultScene)
        _networkManager.SceneManager.AddOwnerToDefaultScene(nob);

    OnSpawned?.Invoke(nob);
}
```

## Host 模式

查看 NetworkHudCanvases 如何将 Instance 启动为 Server、Client、Host。

很简单：

- Server：启动 ServerManager.StartConnection()
- Client：启动 ClientManager.StartConnection()
- Host：同时启动 ServerManager.StartConnection() 和 ClientManager.StartConnection()

NetworkManager 的 IsHostStarted 指示 Instance 是否启动为 Host。在代码中通过 asServer 判断是为 Server 端执行，还是为 Client 端执行.

```C#
public void OnClick_Server()
{
    if (_networkManager == null)
        return;

    if (_serverState != LocalConnectionState.Stopped)
        _networkManager.ServerManager.StopConnection(true);
    else
        _networkManager.ServerManager.StartConnection();

    DeselectButtons();
}

public void OnClick_Client()
{
    if (_networkManager == null)
        return;

    if (_clientState != LocalConnectionState.Stopped)
        _networkManager.ClientManager.StopConnection();
    else
        _networkManager.ClientManager.StartConnection();

    DeselectButtons();
}
```

## 判断代码执行环境

ServerManager 总是在 Server 端执行（包括回调），ClientManager 总是在 Client 端执行（包括回调）。

SceneManager 总是应该在 Server 执行。

NetworkObject、NetworkBehaviour 既在 server 执行，也在 client 执行。通过各种标记执行：

- NetworkObject/NetworkBehaviour

  - IsClientStarted
  - IsClientInitialized
  - IsClientOnlyInitialized

  - IsServerStarted
  - IsServerInitialized
  - IsServerOnlyInitialized

  - IsHostStarted：For both server and client side
  - IsHostInitialized：For both server and client side

  Started 指示客户端是否初始化，Initialized 指示 Object/Behaivour 是否初始化。

  Client 指示客户端（ClientOnly and Host），Server 指示服务端（ServerOnly and Host）。

  ClientOnly 指示仅客户端（不包括 Host），ServerOnly 指示仅服务器（不包括 Host）。

  Host 指示同时客户端和服务器。

- NetworkManager

  - IsClientStart
  - IsClientOnlyStart
  - IsServerStart
  - IsServerOnlyStart
  - IsHostStart

- 回调参数 asServer

  指示为服务端执行。

- ServerManager.Started 和 ClientManager.Started

  通过 ServerManager.Started 和 ClientManager.Started 判断是否在服务端和客户都执行。

一些类只在 Server 上使用（ServerManager），一些仅在 Client 上使用（ClientManager）。

一些既在 Server 上执行，也在 Client 上执行（NetworkManager，NetworkObject，NetworkBehaviour，SceneManager）。但是不意味着它们所有的 API、event 都可以在 Server 上或 Client 上调用。首先假设所有功能都应该在 server 端执行，直到确定它们应该在 client 端执行。
