# NetworkBehaviour

包含网络功能的基类。

public abstract class NetworkBehaviour : MonoBehaviour

派生类

- NetworkLerpRigidbody
- NetworkRigidbody
- NetworkTransformBase
- NetworkAnimator
- NetworkRoomPlayer
- NetworkTransformBase
- NetworkVisibility

就像 MonoBehavior 一样，一个 GameObject 可以有很多 MonoBehaviour 组件，每个组件包含某一特定方面的逻辑。同样，一个 GameObject 也可以有很多 NetworkBehaviour 组件，每个 Behaviour 包含某一特定方面的网络逻辑。但不是每个 NetworkBehaviour 都自己和 server 通信，而是有 NetworkManager 统一为场景中所有的 GameObjects 的所有 NetworkBehaviour 组件完成网络通信。

这个组件允许调用网络 actions，接收各种 callbacks，自动从 server-to-client 同步状态。

NetworkBehaviour 组件需要一个 NetworkIdentity 组件。一个 GameObject 可以有多个 NetworkBehaviour，但是只能有一个 NetworkIdentity。包含 children gameobject 的 gameobject，NetworkIdentity 和 NetworkBehaviour 必须在 root gameobject。

## Fields

- syncInterval：public float

  OnSerialize 的 sync 频率（seconds）

- syncMode：public SyncMode 

  OnSerialize 的 sync 模式（Observers，Owner）

- syncObjects：protected readonly List<SyncObject> 

  可以同步自己的 objects，例如 synclists。Mirror 将所有 SyncVars 收集到这里，统一进行 sync。所有 SyncVars 继承 SyncObject

## Properties

- connectionToClient：public NetworkConnection 

  关联在 NetworkIdentity 上的 NetworkConnection，这对 Server 上的 Player Objects 有效。

- connectionToServer：public NetworkConnection

  关联在 NetworkIdentity 上的 NetworkConnection，这对 Client 上的 Player Objects 有效。 

- hasAuthority：public bool

  如果在分布式网络应用中，这个 object 是 authoritative version（副本），返回 true。

  NetworkIdentity 上的 hasAuthority 决定决定如何确定 authority。对于绝大多数 objects，authority 被 server 控制。对于 hasAuthority = true 的 client objects，authority 被这个 client 控制。

- isClient：public bool

  如果这个 NetworkBehaviour 所在的 object 是 Client version（副本），并且是被 server 生成的，返回 true。

  isClient => netIdentity.isClient

- isClientOnly：public bool

  如果这个 object 存在于 client 上，并且 client 不是 server（host），返回 true。

  isClientOnly => isClient && !isServer

- isLocalPlayer：public bool

  如果 object 在 local machine 上代表一个 player，返回 true。

  在 多人游戏 中，游戏是一个分布式系统，每个 build 实例都包含场景中的所有 objects。因此 client 上有多个 player object 实例（每个 player 一个）。Client 需要知道哪个 player object 是自己的，使得只有这个 player 处理 input 以及 camera。IsLocalPlayer 只对属于 client 上的代表其 player 的 object 返回 true。因此它可以用来对 non-local（remote player）过滤输入。

- isServer：public bool

  如果 object 在一个 active server 上 active，返回 true。

  只有 object 被 spawned 之后才为 true。这个 NetworkServer.active 不同，后者表示的是 server 的 active 状态，而不是 gameobject。

  （可以是 host)

  isServer => netIdentity.isServer

- isServerOnly：public bool

  不可以是 host

  isServerOnly => isServer && !isClient

- netId：public unit netId

  object 的唯一 network id。被 network server 在运行时赋值。

- netIdentity：public NetworkIdentity

  返回 object 的 NetworkIdentity

- syncVarDirtyBits：protected ulong

## Methods

- ClearAllDirtyBits()：public void

  清除使用 SetDirtyBits() 在这个 script 上设置的所有的 dirty bits。它在为 object 发送了一个 update 时自动调用。但是也可以手动调用。

- SerializeSyncVars(NetworkWriter, Boolean)：public virtual void

  Weaver 使用这个函数生成代码。
  
  用于覆盖的虚拟方法，以发送自定义 serialization data。

  initialState flag 用于区分第一次 object 被序列化，和增量更新。Object 第一次发送给 client 时，它必须包含全部 state snapshot，但是接下来 udpates 可以通过只包含增量改变来节约带宽。**SyncVar hook 函数在 initialState 为 true 时不被调用，它只在 incremental updates 时调用。对于 Client 初次获得 sync vars，在 OnStartClient 直接读取变量值**。

  如果一个 class 具有 SyncVars，它和对应的 OnDeserialize 被自动添加到这个类中。因此一个具有 SyncVars 的类不能还有自定义的序列化函数。

  OnSerialize 函数返回 true 指示应该发送一个 update。如果返回 true，则用于这个 script 的 dirty bits 被 set 为 0，否则 dirty bits 不改变。这允许一个 script 的多个 changes 可以累积，在准备好之后再发送，而不是每一帧都发送。

- DeserializeSyncVars(NetworkReader, Boolean)：public virtual void

  Weaver 使用这个函数生成代码

- isDirty()：public bool

  Sync Data 是否有更新

- OnStartAuthority()：public virtual void

  在具有 authority 的 behaviour 上被调用，基于 context 和 hasAuthority

  在 OnStartServer 之后 OnStartClient 之前调用。

  当在 server 上调用 AssignClientAuthority(NetworkConnection) 时，这将在拥有这个 object 的 client 上调用。如果 object 使用 Spawn(GameObject, Network Connection) 生成，这个函数在 NetworkConnection 对应的 client 上调用。

- OnStartClient()：public virtual void

  每一个 NetworkBehaviour 在 client 上 activate 时调用。

  在 Host 上的 object 也会调用，因为 host 上也有一个 local client。

  **当这个回调调用时，object 上的 sync vars 确保以及使用 server 的最新状态初始化了**。

- OnStartLocalPlayer()：public virtual void

  当代表 player 的 gameobject（local player object）被设置好后调用。在 OnStartClient 之后调用，被来自 server 的 ownership message 触发。这里适合放置激活用于 local player 的组件和功能，例如 cameras 和 input。

  当 NetworkBehaviour 所在的 GameObject 是 local player，这个 NetworkBehaviour 的 OnStartLocalPlayer 在 OnStartClient 之后调用。

- OnStartServer()：public virtual void

  当 NetworkBehaviour objects 在 server 上 active 时被调用。这个可以使用 NetworkServer.Listen() 为 scene 中的 objects 触发，或者使用 NetworkServer.Spawn() 为动态创建的 objects 触发。

  这为 host 上和 dedicated server 上的 objects 调用。

- OnStopAuthority()：public virtual void

  当 object authority 从 client 上移除时，在 NetworkBehaviour 上调用。

  当 NetworkId.RemoveClientAuthority 在 server 上被调用时，这将在拥有这个 object 的 client 上调用。

- OnStopClient()：public virtual void

  当 server 上销毁这个 object 时，在这个 object 的所有 clients version 上调用。
  
- OnStopClient()：public virtual void

  当 object 在 server 上 unspawned 时调用。可以用于在持久存储时保持 object data。
