## Fields

- List<NetworkBehaviour> NetworkBehaviours
- NetworkObserver NetworkOberser：这个 object 上的 NetworkObserver（Conditions）
- Hashset<NetworkConnection> Observers：可以看见这个 NetworkObject 并接收其 message 的 clients 的 connections

## Properties

- ClientManager：这个 object 的 ClientManager
- HasAuthority：IsOwner or IsServerInitialized

---

- IsClientStarted

  client start 和认证之后设置为 true。
  
  在 Host Client 上，即使 object 还没有为 client 初始化，也返回 true。

  要检测 object 是否已经为 client 初始化，使用 IsClientInitialized。

- IsClientOnlyStarted

  client start 和认证之后设置为 true

---

- IsClientInitialized

  object 在客户端完成初始化后调用。

  在 client start callback 之前被设置为 true，在 stop callback 之后被设置为 false。

- IsClientOnlyInitialized

  object 只在 server 端初始化后调用。

  在 server start callback 之前被设置为 true，在 stop callback 之后被设置为 false。

- IsHostInitialzied

  当 object 在 server 和 client side 初始化后，设置为 true。

- IsHostStarted

  true: 当 client 和 server 都已启动。

---

- IsGlobal

  使 object 成为 global 的，并添加到 DontDestroyOnLoad scene。只能为 spawn object 设置，不可以对 scene object 设置。

  可以在开始时即设置，也可以生成后任何时间设置。

- IsHostInitialized

  true：object 在 server 和 client 上完成初始化

- IsHostStarted

  true：client 和 server started

- IsManagerReconciling
- IsObjectReconciling

- IsNested

- IsNetworked

  - true：如果 object 已经初始化为 networked object。
  - false：object 不会自动在网络上初始化。

  在一个 object 上使用 Spawn() 总是将那个 instance 设置为 networked。要检测 object 在 server 或 client 是否已经被初始化，IsXYZInitialized。

- IsOffline

  true：如果 client 或 server 没有启动。

- IsOwner

  本地 client 是否是这个 object 的 owner。
  
  它只在 IsClientInitialized（对象也完成初始化）也为 true 时才返回 true。

  可以使用 Owner.IsLocalClient 检测 ownership，无视 object 的初始化状态。

- IsOwnerOrServer

  IsOwern or IsServerInitialized(without Owner on Server)

- IsSceneObject

  如果 object 在 edit-time 时放在 scene 中，则为 true。

- IsServerInitialized

  如果 object 已经在 server side 上初始化，返回 true。

  它在 server start callbacks 之前被设置，在 stop callbacks 之后重置。

- IsServerOnlyInitialized

  非 Host 的 Server 的 IsServerInitialized。

- IsServerStarted

  server active 时返回 true。

  在 Host 模式下，即使 object 已经在 server 上 deinitialized，也返回 true。

  要检测 object 是否在 server 上初始化，使用 IsServerInitialized。

- IsServerOnlyStarted
  
  如果 server 已启动，返回 true。

- IsSpawnable

  如果 object 在运行时 spawn，返回 true。

  对 scene object 或没有 spawn 的 prefab，返回 false。

- IsSpawned

  如果 object 已经为 network 初始化，返回 true。

- LocalConnection

  object 所在的客户端的 connection。这不一定是 owner，因为一个 NetworkObject 可能在很多 client 上都有副本。

- Owner(NetworkConnection)

  Owner 才是对 object 具有 ownership 的 connection，不一定是本地 connection。

- NetworkManager
- ObserverManager
- OwnerId(int)
- PredictedOwner
- PredictedSpawn
- PredictedSpawner
- PredictionManager
- PredictionSmoother
- PrefabId(ushort)
- RigidbodyPauser
- RollbackManager
- SceneManager
- ServerManager
- SpawnableCollectionId(ushort)
- TimeManager
- TransportManager

## Methods

- void Broadcast<T>(T message, bool requireAuthenticated=true, Channel channel=Channel.Reliable)

---

Spawn 和 Despawn Object，只能在 server 上调用。

- void Spawn(NetworkObject nob, NetworkConection ownerConnection=null, Scene scene=default(scene))
- void Despawn(NetworkObject nob, DespawnType? despawnType=null)
- DespawnType GetDefaultDespawnType()
- void SetDefaultDespawnType(DespawnType despawnType)

---

- void SetGraphicalObject(Transform)
- Transform GetGraphicalObject()

---

- GetNetworkBehaviour(byte, bool)

---

- void RegisterInstance<T>(T component, bool replace=true)

  到 NetworkManager 的便捷调用。

- void UnregisterInstance<T>()
- T GetInstance<T>()
- bool HasInstance<T>()

---

- GiveOwnership(NetworkConnection, bool)

- RemoveOwnership(bool includeNested=false)

- SetLocalOwnership(NetworkConnection, bool)
  
  占有这个 object 和 child network objects 的 ownership，允许立即控制

  - NetworkConnection：赋予 ownership 的 Connection
  - includeNested

---

- SetGlobal(bool)

- SetIsNetworkObject(bool)：必须在 start 之前调用

---

- void SetParent(NetworkObject)
- void SetParent(NetworkBehaviour)
- UnsetParent()

---

- SetRenderersVisible(bool visible, bool force)

  为 Host client 设置 renderer 的可见性

- UpdateRenderers(bool)：更新 cached 用于管理 Host Client 可见性的 renderers
