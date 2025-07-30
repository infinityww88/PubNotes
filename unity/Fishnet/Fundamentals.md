## 网络游戏

Fishnet 多人游戏的魔法在于在不同机器之间同步游戏状态，和发送自定义消息触发动作或更新信息的能力。这些确保了所有玩家能体验一个一致和交互的世界。

你编写的 code 行为就像常规游戏一样，Update 中的 code 每帧运行，Awake 在 script 被加载时触发。但是 Fishnet 添加了额外的功能，例如 Sync Variables，它可以让你在作为 server 的 game instance 上设置，并自动同步它们的值到所有连接的 client game instances。

Fishnet 还支持 Remote Procedure Calls，这些方法在一个 game instance 上调用，Fishnet 会在另一个 game instance 上调用，而不是在本地调用。

要开启这些功能，Fishnet 需要能够跨网络识别 game objects 和 scripts，使得它可以知道调用 RPC 或改变 SyncVar 的 game object 和其上的特定组件（NetworkBehaviour，因为一个 gameobject 上可以有多个 NetworkBehaviour，每个都需要标识）。

Fishnet 通过为带有 NetworkObject 的 GameObject 分配一个 ID 来实现对 gameobject 的标识。它还为任何继承自 NetworkBehaviour的组件分配 ID（一个 GameObject 上可以有多个 NetworkBehaviour，每个都需要标识）。NetworkBehaviour 是一个 MonoBehaviour，支持 RPC，SyncVar，和有用的 network methods 和 properties。

对于运行时生成的 NetworkObjects，Fishnet 需要存储一个它们的 Prefab，并为 prefab 分配要给 ID，使得它可以跨网络实例化 prefab（当你在 server 上生成它的时候）。因为 Fishnet 只会在网络上传输一个 ID 数字，然后在客户端实例上根据 prefab 的 ID 找到 prefab，然后实例化它。这是通过要给称为 Spawnable Prefabs 的 prefab 集合 scripable object 完成的。

## Server and Client

Fishnet 可以运行为 server 或 client，它们可以彼此独立的启动和停止。当启动一个 server 时，Fishnet 会设置各种字段，例如在运行为 server 的 game instance 上将 IsServerStarted 设置为 true。作为 client 启动也是类似的。当同时作为 server 和 client 启动时，还会设置诸如 IsHostStarted 等值。这些字段可以用来决定 code 是否作为 server，client，host（server+client）运行。

## 关键概念

### NetworkManager

这是 Fishnet application 的核心部分。它管理 networking 的 lifecycle，包括启动、停止 server 和 client，处理网络连接，监视 networked objects 的生成。

### NetworkObject

Scene 中任何需要通过网络连接的 GameObject 必须有一个 NetworkObject 组件。这个组件为 object 分配一个唯一 ID，并管理 object 的 networked lifecycle，确保它的存在和状态在所有连接的 client 上一致。

### NetworkBehaviour

类似 Unity 的 MonoBehaviour，NetworkBehaviour 是所有需要直接包含 RPC，SyncType 的脚本的基类。继承 NetworkBehaviour 的脚本可以访问 NetworkManager，IsServerStartersd，IsSpawned，IsOwner 等有用信息，以及被跨网络直接引用。

NetworkObject 负责 GameObject 的对象识别和生存周期相关，NetworkBehaviour 负责网络命令相关。

### Ownership and Observers

Fishnet 提供了一个清晰的系统，来定义 NetworkObjects 的所有权 ownership。通常所有权赋予创建或控制 object 的 client。Observers 是观察一个特定 NetworkObject 的 clients，意味着 client 可以接收这些 NetworkObjects 状态的更新。这允许高效的数据传输，仅发送相关 clients 的更新。

### Remote Procedure Call（RPCs）

RPC 是 clients 和 server 通信的核心机制。它允许你在特定 NetworkBehaviour instance 上调用方法，其在一个远程机器上执行。

任何脚本都可以调用一个 RPC，甚至是正常的 MonoBehaviour，ScriptableObjects，或其他普通 C# 类。

### SyncVars

这是一个强大的功能，可以在网络上自动同步变量和复杂的数据结构（例如 list 或 dict）。当 SyncVar 的值在 server 上改变时，它自动将变量复制到所有观察这个 NetworkObject 的 clients。

