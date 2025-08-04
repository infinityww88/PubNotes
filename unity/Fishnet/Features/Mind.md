# Fishnet

## 应用管理

### Fishnet

### 对标 Unity Application

## 场景管理

### Fishnet.SceneManager

### 对标 Unity SceneManager

## 对象标识

### NetworkObject

- 添加 NetworkBehaviour 到 prefabs 或 scene objects<br/>在object及以上自动搜索 NetworkObject<br/>没有则在 top-root 添加一个 NetworkObject
- Spawned NetworkObject
  - 运行时动态生成的 NetworkObject
  - 先本地实例化 Instantiate，在网络生成 Spawn
  - IsSpawned = true
- Scene NetworkObject
  - 作为 scene 的 NetworkObject
  - IsSceneObject = true
- Global NetworkObject
  - IsGlobal = true 的 NetworkObject
  - Server 上实例化，Client 上 Spawn
  - 自动放在 DontDestroyOnLoad
  - 在 server 和 client 上始终保持
  - 只能是 Spawned NetworkObject
  - Scene NetworkObject 不能是 Global 的
- NestedNetworkObject
  - NetworkObject 的 Child NetworkObject
  - IsNested = true
  - 可以在 Scene 和 Prefab 中嵌入 NetworkObject
  - Parent-Child 只是 GameObject 的组织方式（其实是 Transform 的父子关系）<br/>Parent-Child 的两个 Rigidbody 也是两个独立运动物体
  - Instantiate 实例化 Prefab 时会实例化 Nested GameObject<br/>Root NetworkObject Spawn 时，activated NestedNetworkObject 也会被 Spawn
  - Nested NetworkObject 经历 root 一样的 callbacks，共享相同的信息例如 owner
  - Scene 或 Prefab 中可以有 deactivated NetworkObject<br/>可以在稍后任何时候手动调用 Spawn 来生成
    - owner 不会自动假设为 root 的 owner<br/>必须在调用 Spawn 时指示 client 是否应该获得 ownership
  - 在 Instantiate GameObject 和 Server.Spawn NetworkObject 之间可以改变 NetworkObject
  - NetworkObject/NetworkBehaviour 都包含 Spawn 方法，但是只能在 server 端调用
  - Nest NetworkObjects 可以 spawn 或 despawn，但不可以 deatch
  - 就像嵌套的 rigidbody，嵌套的 NetworkObject 仍然是两个独立的 object<br/>指示它们的 transform 被设置为 parent-child
- Spawning/Despawning
  - 要在网络中生成对象存在
    - 该对象需要挂载 NetworkObject 组件
    - 必须通过服务器进行生成
      1. 先实例化对象 Insstantiate
      2. 调用 Spawn 方法将其生成，在 client 上生成对象
      3. 提供了多种 Spawn 方法可供选择

### 对标 Unity GameObject

### 所有权 ownership

## 行为组件

### NetworkBehaviour

- 负责网络通信部分
- 同步数据，访问网络相关信息
- 一旦从 NetworkBehaviour 继承，就意味着你要使用网络
- Rpc 和 SyncType 的基础
- 属性
  - IsClientInitialized = true：作为 client 并且 network 已初始化
  - IsServerInitialized = true：作为 server 并且 network 已初始化
  - IsOwner = true：如果 instance 是 client 并且是本 object 的 owner
  - HasAuthority：如果 instance 是 client 并且是本 object 的 owner，或者 instance 是 server 并 object 没有 owner
  - 当访问 NetworkBehaviour 的属性或方法，使用 base 明确显示你的意图，base.IsOwner
- 回调
  - 每个 NetworkObject 都经历这些 object，服务器、客户端略有不同
  - 服务端回调
    - OnStartNetwork
    - OnStartServer
    - OnOwnershipServer
    - OnSpawnServer
    - OnDespawnServer
    - OnStopServer
  - 客户端回调
    - OnStartClient
    - OnOwnershipClient
    - OnStopClient
    - OnStopNetwork

### 对标 Unity MonoBehaviour

## 客户端管理

### NetworkConnection

- 对客户端执行操作
- 获取客户端信息
- 重要的字段和属性
  - ClientId
  - FirstObject
    - 第一个拥有控制权的 Object
    - SetFirstObject
    - Fishnet 没有强制的 Player GameObject
  - Objects：Connection 拥有的所有权的 Object 的 hashset
  - Scenes：这个 Connection 所属所在的网络场景
  - CustomData：为 Connection 附加的自定义数据
- ClientManager.Connection
- NetworkBehaviour.LocalConnection
- ServerManager.Clients：为每个连接的客户端保存一个 NetworkConnection<br/>dict[ClientId]=NetworkConnection
- ClientManager.Clients
- Owner
  - 每个 NetworkObject 具有一个 owner，是一个 NetworkConnection
  - NetworkObject.Owner 或 NetworkBehaviour.Owner
- TargetRpcs：第一个参数提供 NetworkConnection，指示向哪个客户端发送 RPC

### 代表一个连接的客户端

### 所有权 ownership 和权威性检查

### 认证状态：客户端是否在连接、断开的过程中

### 跟踪客户端已加载的网络场景

### 提供事件

- 获取、失去 object 的所有权
- 加载 start scene
- 附加的自定义数据（不会同步）
- 让客户端可以断开连接

## code 环境检测

### 变量检测

- NetworkObject<br/>NetworkBehaviour<br/>NetworkManager
- NetworkObject/NetworkBehaviour 内直接检测成员变量
- 非 Network 脚本 InstanceFinder.NetworkManager 检测
- IsClientStarted：是否为客户端，或者 host 的客户端
- IsClientOnlyStarted：仅为客户端，排除 host
- IsServerStarted：是否为服务器，或者 host 的服务器
- IsServerOnlyStarted：仅为服务器，排除 host

### 方法属性

- \[Client\]：方法仅在客户端执行
  - Logging
  - RequireOwnership：是否仅限制对象所有者执行
  - UseIsStarted：是否检测 NetworkObject 初始化
    - true：忽略 NetworkObject 是否初始化完成，<br/>仅检测客户端是否初始化完成
    - false：检测 NetworkObject 是否初始化完成，<br/>只有对象初始化完成才可调用
- \[Server\]：方法仅在服务器执行

### 监听客户端、服务器专属事件
