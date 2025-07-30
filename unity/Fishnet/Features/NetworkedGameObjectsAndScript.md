## NetworkObject

### NetworkObject

任何具有 NetworkObject 的 GameObject，被称为 NetworkObject。

当你添加一个 NetworkBehaviour 组件到 prefabs 或 scene objects 上，networkBehaviour 会在这个 object 或 parent objects 中搜索一个 NetworkObject。如果没有找到 NetworkObject，则会在 top-most object 上自动添加一个。

### Spawned NetworkObject

使用 ServerManager.Spawn() 方法 Instantiated 和 Spawned 的 NetworkObjects 称为 Spawned NetworkObject。在 NetworkObject 组件内部，IsSpawned 属性被标记为 True。

### Scene NetworkObject

任何作为 Scene 一部分的 NetworkObject（即不会在 scene 中 instantiated/spawned），称为 Scene NetworkObject。在 NetworkObject 组件内部，IsSceneObject 属性被标记为 True。

### Global NetworkObject

任何 IsGlobal 标记为 true 的 NetworkObject（无论是在 inspector 中还是在 code 中）都被称为 GlobalNetworkObject。

当在 server 上实例化以及在 clients 上 spawned 时，GlobalNetworkObjects 会自动放在 DontDestroyOnLoad scene 中。

Scene Objects 不能被标记为 global。所有 global objects 必须被标记为 instantiated 或 spawned。

### NestedNetworkObject

任何作为 NetworkObject child 的 NetworkObject，被称为 Nested NetworkObject，NetworkObject 组件内部 IsNested 属性被标记为 true。

Fishnet 允许在 scene 和 prefabs 中嵌入 NetworkObjects。

当 spawning 一个 root NetworkObject，任何 active 的 nested NetworkObjects 也会被 spawned。Nested NetworkObjects 会经历和 root 相同的 callbacks，以及共享相同信息，例如 IsOwner。

你可以在 Scene 或 Prefab 中有 deactivated 的 Nested NetworkObjects，稍后再 spawn 它们。

当 Nested NetworkObject 再 root 被 spawned 之后 spawned，owner 信息不会自动假设为 root 的 owner。你必须再调用 Spawn 时指示 client 是否应该获得 ownership。

在 Instantiating Prefab 和 Spawning Root Network Object 之间（这是两个步骤，第一个步骤先实例化 Prefab，然后调用 Server.Spawn 在网络上 Spawn 它），你可以改变 Nested NetworkObjects。这包括 SyncTypes，甚至 object 的 active 状态。这些修改在 root spawned 时自动同步。

Instantiating Prefab：是标准地在 Unity Scene 中实例化 Prefab 为 GameObject

Spawning NetworkObject：是调用 Server.Spawn 在网络上（所有客户端）生成这个 NetworkObject

NetworkObject 首先是普通的 GameObject，可以先存在于 Scene 或 Prefab 中，只有调用了 Server.Spawn 之后，它才会在其他 Clients 中生成。

```C#
//An example of changing the enabled state for NestedNob.
public GameObject MyPrefab;

private void SpawnPrefab()
{
    GameObject go = Instantiate(MyPrefab);
    GameObject nestedNob = go.transform.GetChild(0);
    nestedNob.SetActive(false);
    //MyPrefab will spawn with NestedNob disabled for server and all clients
    //until you spawn it at a later time.
    base.Spawn(go);
}
```

Nested NetworkObjects 可能被 spawned 或 despawned，但是它们不应该 detached。有一个例外是 nested scene NetworkObjects，它们可以被 detached。

## NetworkBehaviour

NetworkBehaviours 是 networking 的一个基础部分，它允许你很容易地同步数据，以及访问网络相关的信息。

当从 NetworkBehaviours 继承时，你就是在指示你的脚本会以某种方式利用网络。一旦 NetworkBehaviour 脚本添加到 object，NetworkObject 组件会自动 attached。

NetworkBehaviours 时 RPC，Sync 的基础，并且访问关键的网络信息。

### Properties

NetworkBehaviour 有一些 public 属性，其中很多你会经常使用。绝大部分属性只在 object 被初始化之后才可用。

- 如果作为 client，并且 network 已经被初始化，IsClientInitialized 为 true
- 如果作为 server 并且 network 已经被初始化，IsServerInitialized 为 true
- 如果作为 client 和 object 的 owner，IsOwner 为 true
- 如果作为 owner，或者作为 server 并且没有 owner，HasAuthority 为 true

### Callbacks

## Spawning and Despawning
