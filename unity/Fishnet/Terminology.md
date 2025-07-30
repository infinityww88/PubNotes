## Server, Client, Host

### Ownership and Controller

Ownership 是指一个特定 client 拥有 own 一个 object，而 controller 是指哪个实体控制这个 object。

拥有 object 的实体和控制 object 的实体并不一定相同。

当一个 client 拥有一个 object，它是这个 object 的 controller，并能够发送 RPC 而不需要关闭 authority checks（权威性检查），以及其他一些任务，例如生成预测数据。

如果 object 不被任何 client owned，controller 是 server，但是当 client own 这个 object 时，它就变成了 controller。

### Server

Server 是一个 Game 实例，client 可以连接到其上。Server 允许 clients 彼此交互，并且经常负责游戏的重要方面，例如 score keeping，world spawning，以及更多。

- Local Server

  当 server 开启后，运行 server 的 build 或 instance 被称为 local server。

- Remote Client

  remote client 是仅当作为 server 运行时的术语。它是一个到 server 的 player connection。Remote client 有可能和 local client 是相同的。主要区别是 local client 指的是 player-side logic，而 remote client 指的是 server 到 client 的连接。

### Client

Client 连接到服务器，无论 server 是 local 还是 online。Client 是游戏的 player。Client 体验 game-play，而 server 在 clients 之间同步数据。

- Local Client

  Local Client 指的是 client 控制其游戏。如果你作为 player 加入 server，你就是 local client。

- Remote Server

  当 local client 连接到 server，它们是连接到一个 remote server。Remote server 有可能也是 local server，如果 client 作为 host 运行。

### Host

当作为 host 运行时，你同时是 client 和 server。一个独立实例可以变成 host，无需额外的编译可执行程序，也无需提供对计算机额外的访问。即一个 Fishnet 可执行程序可以直接以 host 运行，无需任何额外操作。

Host 非常适合快速开发。

## Communicating

有很多方法可以在 server 和 clients 之间通信。

### SyncTypes

SyncTypes（同步类型）依附于对象存在，是数据驱动的变量或集合。SyncTypes以可调节的时间间隔进行同步。当对象上的SyncType被修改时，变更会自动从服务器发送至客户端。客户端将在同一对象上本地接收这些变更。一个典型的应用示例就是生命值变量——当玩家受到伤害时更新该变量，新数值便会同步发送给所有客户端。

```C#
using FishNet.Object;
using FishNet.Object.Synchronizing;

public class Player : NetworkBehaviour
{
    readonly SyncVar<int> _health = new SyncVar<int>(100);

    public void StepOnLego()
    {
        if (!IsServerInitialized)
            return;

        _health. Value -= 10;
    }
}
```

### Remote Procedure Calls

远程过程调用（RPC）是另一种基于对象的通信方式。与用于同步变量的SyncTypes不同，RPC允许在服务器和客户端上执行逻辑。RPC不受固定时间间隔限制，可立即在下个网络周期或尽可能快地发送。且RPC必须在NetworkBehaviour类中使用。

```C#
using FishNet.Object;

public class Player : NetworkBehaviour
{
    [ServerRpc]
    void UpdatePlayerName(string newName)
    {
        print($"Player {OwnerId} has updated their name to {newname}");
    }
}
```

### Broadcasts

广播（Broadcasts）与状态（States）不同，不绑定特定对象。广播可用于多种任务，但更常用于服务器与客户端间的数据组通信。广播可在代码的任何位置接收和发送，无需像RPC那样必须位于NetworkBehaviour类中。

```C#
using FishNet;
using UnityEngine;

public class ChatSystem : MonoBehaviour
{
    public void SendChatMessage(string text)
    {
        ChatBroadcast msg = new ChatBroadcast()
        {
            Message = text,
            FontColor = Color.white
        };

        InstanceFinder.ClientManager.Broadcast(msg);
    }
}
```

### 注意

上述所有通信方式均支持两种传输通道：​​可靠传输（Reliable）​​与​​不可靠传输（Unreliable）​​。

- ​​可靠传输​​能确保数据按发送顺序完整抵达并处理；
​- ​不可靠传输​​占用带宽更少，但可能出现乱序或丢包现象。

Fish-Networking框架的部分功能采用了​​最终一致性​​机制，例如基于不可靠信道传输的SyncVars变量或NetworkTransform组件。这些功能通过不可靠通道发送数据以节省带宽并提升性能，即便出现数据丢失或乱序的情况，系统仍能自动最终同步，开发者可以放心使用。

## Miscellaneous

### Scene Object

场景对象（Scene Object）是指在编辑阶段就被放置在场景层级（Hierarchy）中的物体。这类对象虽然可以通过网络进行生成（Spawn），但由于它们已预先存在于场景中，因此不需要额外的实例化（Instantiation）过程。

### Instantiated Object

Instantiated object 是在运行时实例化的 object，不是 scene object，例如 Instantiate(prefab)。

### Predicted Object

Predicted Object 是利用 prediction system 的 object。Predicted 功能通常同时运行在 client 和 server 上，允许实时的 gameplay interactions。这些 behaviours 的类型需要更多工作，但是一个正确的 prediction 设置会防止作弊。

### Client Authoritative

通常指对象由客户端直接控制，其操作结果未经服务器验证便直接同步。客户端权威（Client Authoritative）模式虽然更易实现，但可能增加作弊风险。例如将NetworkTransform组件的"客户端权威"设为true时，客户端可本地直接操控对象，而服务器仅被动接收并同步客户端传来的数值。

### Server Authoritative

Values 被 server 控制和验证，例如 SyncTypes。Predicted objects 是 server authoritative。