# Network Identity

NetworkIdentity 在网络上（分布式游戏应用）标识 objects。它的主要数据是一个 NetworkIdentityId，由 Server 分配，然后设置到 clients 上。用于在网络通信中在不同的机器上查找 gameobjects。

public sealed class NetworkIdentity : MonoBehaviour

NetworkIdentity 用于在网络上同步 object 中的信息。只有 server 应该创建具有 NetworkIdentity object 的实例（需要分配 netId），因为不然的话它们将不能正确地连接到系统中。

对于复杂的 object（具有 hierarchy），NetworkIdentity 必须放置 root gameobject 上。不支持在 hierarchy 下面的 object 上附加 NetworkIdentity。

NetworkIdentity 管理 object 的 NetworkBehaviours 的 dirty state。当它发现 NetworkBehaviours 是 dirty 的，它将导致创建一个 update packet 并发送到 clients。

## Fields

- clientAuthorityCallback：public static NetworkIdentity.ClientAuthorityCallback

  可以放置一个回调函数，当 objects 的 client-authority 状态改变时，被通知

  无论何时一个 object 带有 authority 被生成时，或者 object 的 client authority status 被 AssignClientAuthority 或 RemoveClientAuthority 改变时，这个回调将会被调用。

  这个回调只在 server 上调用。

- observers：public Dictionary<int, NetworkConnection>

  可以看见这个 object 的 network connections（players）。

  在 OnStartServer 调用之前为 null。这对于 server-only 模式下的 SendToXXX 能正确工作是必须的。

- sceneId：public ulong

  在 scene 中 NetworkIdentity object 的唯一标识符（scene scope），它用于在 clients 上生成 scene objects。

- serverOnly：public bool

  使这个 object 只在 game 以 server（或 host）运行时存在的的标记。
  
  只在 server 上生成，不在 client 上生成。例如只和逻辑有关，不涉及显式，因此只需要在 server 上存在，使得 server 可以执行相关的计算，而不需要在 client 上出现。

- spawned：public static readonly Dictionary<uint, NetworkIdentity>

  所有生成的 networked objects，在 server 和 client 上都具有。

## Properties

- assetId：public Guid

  当 server spawns 这个 objects 时用于查找 source assets 的 guid（assert id）

- connectionToClient：NetworkConnectionToClient

  和 NetworkIdentity 关联的 NetworkConnection。

  只对 server 上的 player objects 有效

  使用它返回诸如 connection identity，IP address 和 ready status 等细节。

- connectionToServer：public NetworkConnection

  只对 local client 上的 player objects 有效
  
- hasAuthority：public bool

  如果这个 object 是 client 上的 authoritative player object，返回 true。

  这个 value 在运行时确定。对于绝大多数 objects，authority 被 server 保持。

  对于那些在 server 上使用 AssignClientAuthority 设置 authority 的 objects，它将在拥有它的 client 上返回 true，在其他 clients 上返回 false。

- isClient：public bool isClient

  如果运行为 client 并且这个 object 是被 server 生成的，返回 true。

- isLocalPlayer：public bool

  如果这个 object 在 local machine 上表示 player，返回 true。

  这在当 server 为这个 client 生成一个 player object 时设置。

- isServer

  如果 NetworkServer.active 并且 server 没有停止时返回 true。

- netId：public uint

  一个特定 object instance 的唯一标识符，用来在 networked clients 和 server 之间追踪 objects

- NetworkBehaviours：public NetworkBehaviour[]

  这个 GameObject 上所有的 NetworkBehaviour

- SpawnedFromInstantiate：public bool

- visibility：public NetworkVisibility

  返回 NetworkVisibility 组件

## Methods

- AssignClientAuthority(NetworkConnection)：public bool

  将一个 object 的控制权赋予 NetworkConnection 对应的 client

  这将导致 hasAuthority 在拥有 object 的 client 上设置，并且 NetworkBehaviour.OnStartAuthority 将在那个 client 上被调用。然后这个 object 将会在那个 connection 的 NetworkConnection.clientOwnedObjects 列表中。

  Authority 可以使用 RemoveClientAuthority 移除。任何时候，只有一个 client 可以拥有一个 object。不需要为 player objects 调用此方法，它们的 Authority 自动被设置。即 Player Objects 自动在 client 上设置 Authority，而 Non-Player Objects 的 Authority 默认在 server，只对它们才有必要调用 AssignClientAuthority。
  
- GetSceneIdentity(UInt64)：public static NetworkIdentity

  使用指定 id 在 sceneIds dictionary 返回 NetworkIdentity

- RebuildObservers(Boolean initialize)：public void

  这个导致重构可以看见 object 的 players 的集合。OnRebuildObservers 回调函数将在每个 NetworkBehaviour 上调用

- RemoveClientAuthority()：public void

  移除一个 object 的 ownership。这应用到使用 AssignClientAuthority 设置 authority 的 objects，或者带有 NetworkConnection 参数的 Spawn(GameObject, NetworkConnection) 函数生成的 objects。

- ResetNextNetworkId()：public static void

  Resets nextNetworkId = 1
