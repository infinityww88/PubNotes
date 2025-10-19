# Spawning Game Objects

在 Unity 中，你通常使用 Instantiate 来 spawn（创建）新的 gameobjects。然而，在 Mirror 中，单词 spawn 意味着更 specific（特殊） 的东西。在 Mirror server-authoritative 模型中，在 server 上 “spawn” 一个 gameobject 意味着 gameobject 在连接到 server 的 clients 上创建，并且被 Spawning 系统管理。

一旦 gameobject 使用这个系统 spawn，任何时候在 server 上 gameobject 有所改变，状态更新被发送到 clients。当 Mirror 在 server 上销毁 gameobject 时，它还在 clients 上销毁它们。

Server 和所有其他 networked gameobjects 一起管理 spawned gameobjects，使得如果另一个 client 稍后加入游戏，server 可以在那个 client 上生成 gameobjects。这些 spawned gameobjects 有一个 unique network instance ID，称为 netId，对于每个 gameobject，它在 server 上和 clients 上都是相同的。这个 unique network instance ID 被用于在网络上路由消息到 gameobjects，以及标识一个 gameobjects。

一个 gameobject Prefab 在试图注册到 Network Manager 之前必须有一个 NetworkIdentity 组件。

要使用 NetworkManager 在 Editor 中注册一个 Prefab，选择 NetworkManager gameobject，在 Inspector 中，找到 NetworkManager 组件。点击 Spawn Info 旁边的三角箭头打开 setting，在 Registered Spawnable Prefabs 中，点击 + 按钮。拖拽 Prefabs 到 empty field 来将其赋予到 list。

## Spawning Without Network Manager

对于高级 users，你可能发现想要注册 Prefabs 并且 spawn gameobjects 而不使用 NetworkManager component。可以通过脚本自己处理 Prefab registration。使用 ClientScene.RegisterPrefab 方法来注册 Prefabs 到 NetworkManager。

```C#
using UnityEngine;
using Mirror;

public class MyNetworkManager : MonoBehaviour 
{
    public GameObject treePrefab;

    // Register prefab and connect to the server  
    public void ClientConnect()
    {
        ClientScene.RegisterPrefab(treePrefab);
        NetworkClient.RegisterHandler<ConnectMessage>(OnClientConnect);
        NetworkClient.Connect("localhost");
    }

    void OnClientConnect(NetworkConnection conn, ConnectMessage msg)
    {
        Debug.Log("Connected to server: " + conn);
    }
}
```

在这个例子中，你创建换一个 empty gameobject 来作为 NetworkManager，然后创建并附加 MyNetworkManager 脚本到这个 gameobject。创建一个附加 NetworkIdentity 组件的 prefab，然后拖拽到 MyNetworkManager 组件 Inspector 上的 treePrefab 槽位。这确保当 server spawns tree gameobject 时，它还在 clients 上创建相同的 gameobject。

Registerin prefabs 确保没有 stalling 或 loading 时间用于创建 Asset。

要使 script 工作，你还需要添加 code 到 server 上。添加这些 code 到 MyNetworkManager 脚本：

```C#
public void ServerListen()
{
    NetworkServer.RegisterHandler<ConnectMessage>(OnServerConnect);
    NetworkServer.RegisterHandler<ReadyMessage>(OnClientReady);

    // start listening, and allow up to 4 connections
    NetworkServer.Listen(4);
}

// When client is ready spawn a few trees  
void OnClientReady(NetworkConnection conn, ReadyMessage msg)
{
    Debug.Log("Client is ready to start: " + conn);
    NetworkServer.SetClientReady(conn);
    SpawnTrees();
}

void SpawnTrees()
{
    int x = 0;
    for (int i = 0; i < 5; ++i)
    {
        GameObject treeGo = Instantiate(treePrefab, new Vector3(x++, 0, 0), Quaternion.identity);
        NetworkServer.Spawn(treeGo);
    }
}

void OnServerConnect(NetworkConnection conn, ConnectMessage msg)
{
    Debug.Log("New client connected: " + conn);
}
```

Server 不需要注册任何东西，因为它知道什么 gameobject 被 spawned（asset ID 在 spawn message 中被发送）。Client 需要有能力查询 gameobject，因此它必须在 client 上被注册。

当编写你自己的 network manager，十分重要的是在 server 上调用 spawn command 之前使 client 准备好接受状态更新，否则它们不会被发送。如果你使用 Mirror 的 built-in NetworkManager 组件，这些自动完成。

对于高级使用，例如 object pools 或者动态创建的 Assets，你可以使用 ClientScene.RegisterSpawnHandler 方法，其允许为 client-side spawning 注册 callback 函数。

如果 gameobject 有一个 network state 诸如 synchronized variables，然后这个状态使用 spawn message 被同步。在下面的例子中，script 附加在 tree Prefab：

```C#
using UnityEngine;
using Mirror;

class Tree : NetworkBehaviour
{
    [SyncVar]
    public int numLeaves;

    public override void OnStartClient()
    {
        Debug.Log("Tree spawned with leaf count " + numLeaves);
    }
}
```

一旦这个 script 被挂载，就可以改变 numLeaves 变量，并修改 SpawnTrees 函数在来精确查看 client 上反映出的值。

```C#
void SpawnTrees()
{
    int x = 0;
    for (int i = 0; i < 5; ++i)
    {
        GameObject treeGo = Instantiate(treePrefab, new Vector3(x++, 0, 0), Quaternion.identity);
        Tree tree = treeGo.GetComponent<Tree>();
        tree.numLeaves = Random.Range(10,200);
        Debug.Log("Spawning leaf with leaf count " + tree.numLeaves);
        NetworkServer.Spawn(treeGo);
    }
}
```

### 约束

- 一个 NetworkIdentity 必须自一个 spawnable Prefab 的 root gameobject 上。没有这个组件，NetworkManager 不能注册 Prefab
- NetworkBehaviour 脚本必须和 NetworkIdentity 在同一个 GameObject 上，而不是在 child game objects

## GameObject Creation Flow

Spawning gameobjects 的内部发生的实际 flow 是：

- 具有 NetworkIdentity 组件的 Prefab 被注册为 spawnable
- gameobject 在 server 上从 Prefab 实例化
- Game code 在 instance 上设置初始值（注意 3D 物理 forces applied 在这里不会立即发生）
- NetworkServer.Spawn 被调用，使用这个 instance 作为参数
- Server 上的 instance 上的 SyncVars 的状态通过调用 [Network Behaviour] 组件上的 OnSerialize 被收集
- 一个 ObjectSpawn 消息被发送到连接的包含 SyncVars 数据的 clients
- OnStartServer 在 server 上的 instance 上被调用，isServer 被设置为 true
- Clients 接收 ObjectSpawn ObjectSpawn 消息，并从 registered Prefab 创建一个新的 instance
- SyncVar data 通过 NetworkBehaviour 的 OnDeserialize 方法被应用到 client 的新 instance 上
- OnStartClient 在每个 client 上的 instance 上调用，isClient 被设置为 true
- 在游戏进行过程中，对 SyncVar 值的修改被自动同步到 clients。这个过程持续不断，直到游戏结束
- NetworkServer.Destroy 在 server 上的 instance 上调用
- 一个 ObjectDestroy network message 被发送到 clients
- OnNetworkDestroy 在 clients 上的 instance 上调用，然后 instance 被销毁

### Player Game Objects

HLAPI 中的 Player gameobjects 和 non-player gameobject 的工作方式略有不同。使用 NetworkManager Spawning player gameobjects 的流程是：

- 具有 NetworkIdentity 的 Prefab 被注册为 PlayerPrefab
- Client 连接到 server
- Client 调用 AddPlayer，MsgType.AddPlayer network message 被发送到 server
- Server 接收消息，并调用 NetworkManager.OnServerAddPlayer
- 在 server 上，GameObject 从 Player Prefab 实例化
- NetworkManager.AppPlayer

## Spawning GameObjects with Client Authority

要生成 gameobjects 并将它们的 authority 赋予特定 client，使用 NetworkServer.Spawn，它使用一个 client 的 NetworkConnection 参数用来指定 authority。

对于这些 gameobjects，在 client 上 hasAuthority 为 true，并且 OnStartAuthority 在 authority client 上调用。然后这个 client 就可以为这个 gameobject 发送 Commands。在其他 client（以及 host）上，hasAuthority 为 false。

生成的具有 client authority 的 objects 必须在它们的 NetworkIdentity 中设置 LocalPlayerAuthority。

例如，tree spawn 例子可以像这样修改，允许 tree 具有 client authority：

```C#
void SpawnTrees(NetworkConnection conn)
{
    int x = 0;
    for (int i = 0; i < 5; ++i)
    {
        GameObject treeGo = Instantiate(treePrefab, new Vector3(x++, 0, 0), Quaternion.identity);
        Tree tree = treeGo.GetComponent<Tree>();
        tree.numLeaves = Random.Range(10,200);
        Debug.Log("Spawning leaf with leaf count " + tree.numLeaves);
        NetworkServer.Spawn(treeGo, conn);
    }
}
```

Tree script 现在可以被修改以向 server 发送一个 Command：

```C#
public override void OnStartAuthority()
{
    CmdMessageFromTree("Tree with " + numLeaves + " reporting in");
}

[Command]
void CmdMessageFromTree(string msg)
{
    Debug.Log("Client sent a tree message: " + msg);
}
```

注意你不能只是在 OnStartClient 上调用 CmdMessageFromTree，因为那时 authority 还没有被设置，因此调用将失败。
