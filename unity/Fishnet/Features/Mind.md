# Fishnet

## 应用管理

### Fishnet

### 对标 Unity Application

## 场景管理

### Fishnet.SceneManager

### 对标 Unity SceneManager

## 网络对象

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
  - Spawn 不分配 ownership：owner=null 或不传递 owner 参数
  - Spawn 分配 ownership：owner 指定 connection
  - Despawn 和 spawn 类似访问，通过 NetworkBehaivour, NetworkObject, NetworkManager
  - Despawn 时可以 pool NetworkObject，而不是销毁
  - 通过 NetworkObject/NetworkBehaviour IsSpawned 检查对象是否是生成的
  - Scene object despawn 时 disable 而不是 destroy
- Spawn Payloads
  - Spawn NetworkObject 时附带传输额外信息
  - NetworkBehaviour 提供 WritePayload/ReadPayload 方法，每个 NetworkBehaviour 都可以读写自己的额外数据
  - 读写的顺序和数量必须完全一致
  - Server Spawn NetworkObject 可以写入一些动态信息，一起发给 client，用于 object 的初始化
- 预测生成
  - 类似预测运动，客户端预先执行，服务器后续确认
  - 客户端根据输入预先生成对象，同时向服务器发送输入
  - 有预测生成，隐含包括预测销毁（客户端预先销毁）
  - 全局设置
    - ServerManager 上设置，若场景中没有 ServerManager，则在 NetworkManager 上添加之
    - 勾选 Allow predicted spawning
    - 调整 Reserver Object Ids
  - Object 设置
    - 仍需每个 Object 设置预测生成
    - 为要预测生成的 Scene Object 或 Prefab 添加 PredictedSpawn 组件
    - 可以继承 PredictedSpawn 组件，自定义预测生成行为
  - 设置了全局设置、Object 之后，客户端就可以向服务器一样预测生成和销毁
- Object Pooling
  - Fishnet 内置了对象池功能
  - 同时用于客户端和服务器
  - 对象池可以预热，prewarm，预先放入一组对象以供使用
  - Scene 中的 NetworkObjects 不会添加到对象池中，despawn 时只禁用而非销毁
  - 启用了对象池后，仍然需要修改 NetworkObject 的默认回收行为或手动显示回收
  - Spawn 对象时，从 Pool 中取出可用对象

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

## 网络状态事件

- 全局网络事件，而非 NetworkBehaviour level 事件
- server 端事件，ServerManager
  - OnAuthenticationResult
  - OnServerConnectionState
  - OnRemoteConnectionState
- client 端事件，ClientManager
  - OnAuthenticated
  - OnClientConnectionState
  - OnRemoteConnectionState
- server 和 client 共享事件，TimeManager
  - OnPreTick：network tick 之前
  - OnTick：network tick，可以设置网络一定频率同步数据
  - OnPostTick：network tick 之后

## 网络通信

### Remote Procedure Calls

- 需求：
  - 必须在继承自NetworkBehaviour的脚本中调用。
  - Fish-Net框架会自动为类型生成序列化器（支持数组、列表）<br/>若无法生成则需手动实现自定义序列化器。
- ServerRpc
  - client 发送，在 server 上执行逻辑
  - 默认只有对象的所有者（client/connection）才能调用 ServerRpc
  - RequireOwnership = false 可以允许任何 client/conneciton 对 Object 调用 ServerRpc
  - ServerRpc 方法可以包含一个 NetworkConnection 参数<br/>Fishnet 自动添加调用者，用于 server 端识别哪个客户端在调用 Rpc
- ObserverRpc
  - server 发送，在 client 上执行
  - 只有一个 object 的 observer clients 执行 ObserverRpc
  - server 根据 NetworkObserver 设置的条件判断一个 object 的 observer clients
  - 观察者包含 owner，指定 ExcludeOwner = true 可以排除 observer
  - 可以通过 ObserverRpc 将最新数值同步到新加入观察者序列的客户端<br/>适合仅通过 RPC 变更的数值类型，对比是 SyncTypes
    - 指定 BufferLast 选项
    - 新加入观察者自动被 server 发送这个 ObserverRpc，同步一次
- TargetRpc
  - server 发送，在 client 上执行
  - 第一个参数是 NetworkConnection，指定在哪个 client 上执行 rpc
  - 对比 ObserverRpc
    - 相同点：都需要服务端手动发起，调用 TargetRpc/ObserverRpc 方法<br/>但是 ObserverRpc 可以通过 BufferLast 缓存最后一次 rpc<br/>当有新加入的 observer client，会自动为其发送最后一次缓存的 rpc
    - 不同点：TargetRpc 需要手动指定要执行逻辑的客户端<br/>ObserverRpc 则由 server 根据 NetworkObserver 设置的条件自动判断要执行 rpc 的客户端
- Multi-Purpose Rpc
  - 一个方法可以既是 TargetRpc，又是 ObserverRpc
  - 这样方法既可以作为观察者自动被 server 调用，又可以被 server 指定调用 rpc
- Channels
  - Rpc 可以通过 reliable 或 unreliable 通道调用
  - 在 Rpc 方法中添加一个 channel 参数
    - 对于发送者，指定发送的通道
    - 对于接收者，指定接收的通道
  - 每次 rpc 调用都可以指定不同的通道，即使是同一个方法的多次调用
- RunLocally
  - 默认 rpc 只会通过网络发送到目的地执行
  - 所有 rpc 都可以指定 RunLocally，尤其是 ServerRpc
  - 方法首先在本地调用(client/server)，同时发往目的地(server/client)
- Rpc 方向
  - ObserverRpc/TargetRpc：Server -> Client
  - ServerRpc：Client -> Server
  - Client 之间不能直接 Rpc
- DataLength：Rpc 参数可以指定潜在发送参数数据的最大数据 size<br/>使框架可以优化 rpc 内存分配

### SyncTypes

- 作为网络通信方法，rpc 对比 method，sync type 对比 field
- 方向：server -> client，服务端修改，改变发送到客户端
- 增量同步，仅传输变化数据，尤其是容器
- 为 custom type 自动生成序列化器
- OnStartServer 之前的修改只在客户端或服务器执行，其后的变化通过网络同步
- 可以设置 SendRate 网络同步频率，0f 表示每个 tick 发送一次 change
- Host Client 限制：当 asServer = false，prev value 是当前值或 null，否则才是真正的之前值
- 设置 SyncTypeSettings：和 rpc 一样，作为通信方式，都有各种设置
  - 在创建 SyncTypes 变量时指定设置
  - 在创建后可以修改设置
  - 同步频率
  - 发送通道：unreliable/reliable
  - SyncTypes 变量可以向普通变量一样在 Inspector 中显示
- SyncVar
  - 最简单的同步方案，可以同步一个变量
  - 支持所有数据类型：值、结构体、类
  - 它是一个模板，模板参数是要同步的类型
  - 同步设置：频率、变化通知回调
  - 回调函数参数：prev value，current value，asServer
  - 回调函数可以作为另一种 rpc 来使用<br/>触发方式就是改变 SyncVar，在回调函数中执行逻辑
  - 方向：只能 Server 修改，同步到客户端，客户端无法直接修改 SyncVar 的值来触发同步
  - 客户端要修改可以使用 ServerRpc，将 Property 方法实现为 ServerRpc，使得在 server 端修改 sync types
  - 后续可能实现客户端权威属性
  - ReadPermissions.ExcludeOwner 设置可以防止自身触发更新
  - WritePermissions.ClientUnsynchronized 允许客户端直接修改变量
  - 在 ServerRpc 中启用 RunLocally=true 可确保 RPC 逻辑同时在客户端和服务端执行
- 容器类型
  - SyncList
  - SyncDictionary
  - SyncHashSet
  - 只发生变化部分
  - 值类型可直接修改
  - 引用类型（class）必须手动标记 dirty，来触发同步
- 计时类型
  - SyncTimer
    - 服务器-客户端之间高效的定时器同步方案
    - 与 SyncVars 不同，SyncTimer 只同步定时器启动、停止等状态变化，而不是逐帧变化
    - 与 SyncVars 相同，修改只能在 server 触发
    - 方法
      - StartTimer
      - PauseTimer
      - UnpauseTimer
      - StopTimer
    - 更新
      - timer 必须在 server 和 client 都 udpate
      - 对于 host 模式，只需要其中一个 update
      - 可以在任何方法中 update，但应该在 MonoBehaviour.Update 中更新
    - 读取值
      - Paused
      - Remaining
    - 回调
      - 参数：SyncTimerOperation op, float prev, float current, bool asServer
      - SyncTimerOperation
        - Start
        - Pause
        - PauseUpdated
        - Unpause
        - Stop
        - StopUpdated
        - Finish
        - Complete
  - SyncStopwatch
    - 服务器-客户端高效的秒表同步方案
    - SyncTimer 基于 Tick，SyncStopwatch 基于毫秒
    - SyncTimer 与 FishNet 的 TimeManager 配合<br/>处理网络计时、服务器与客户端的时间同步<br/>以及对客户端预测计时的支持，用于维护整个网络的时间基准<br/>确保不同客户端和服务器的时间一致性<br/>通常用于需要严格时间同步的网络操作，例如同步游戏中的关键事件、状态更新
- 自定义 SyncType
  - SyncVar 同步整个变量（结构体、类）
  - 容器只同步变化的 item（仍然是整体同步）
  - 自定义 SyncType 可以向容器一样，只同步 struct/class 变化的部分
  - 适用于包含大量数据的复合类型（struct/class）

### Broadcasts

- Broadcasts 允许在多个 object 之间发送消息，而不需 object 具有 NetworkObject 组件
- 允许非联网对象之间通信，例如聊天系统
- 和 local message dispatcher 在单体应用中任意 objects 之间发送消息一样，只是它是在网络上发送
- Fishnet 框架负责接收网络消息，任意对象（非 NetworkObject）都可以注册监听网络消息
- 可通过 reliable 或 unreliable 通道发送
- 方向：既可以客户端向服务端发送，也可以服务端向客户端发送
- 通过 ClientManager/ServerManager 发送广播，和注册回调<br/>可在 NetworkBehaviour/NetworkManager/InstanceFinder 中找到其引用
- 消息必须是结构体，结构体类型同时作为消息名字、类型，通过结构体类型注册到相应的消息通道，以及在相应的消息通道发送广播
- 回调函数参数 NetworkConnection conn, ChatBroadcast msg, Channel channel
- 任何脚本都可以注册回调，不需要 NetworkBehaviour

### 数据序列化

- SyncTypes 负责数据同步逻辑，Data Serialization 负责数据序列化和反序列化<br/>SyncTypes 和 Broadcasts，以及 Rpc 调用 Data Serialization 传输数据。
- 无论是 SyncTypes，Broadcasts，还是 Rpc，在网络传输数据类型的时候<br/>Fishnet 自动寻找或创建该类型的序列化器
- Fishnet 序列化的字段跟 Unity 一样，只序列化 public 或 serialized 字段<br/>要排除字段，添加 System.NonSerialized 属性
- Fishnet 还支持继承序列化
- 自定义序列化器
  - 当自动序列化不可行时，或想定制时，可自定义序列化器
  - 按照约定实现，Fishnet 可自动识别类型的自定义序列化器
  - 自定义序列化器可以覆盖自动序列化器
  - 步骤
    - 方法必须是 static，并且在一个 static class
    - 写方法名字必须以 Write 开始
    - 读方法名字必须以 Read 开始
    - 第一个参数必须是 this Writer，或者 this Reader
    - Data 必须以和写入相同的顺序读取
    - Data 可以以任何逻辑写入，不一定全量写入<br/>例如可根据某个 bool 字段，只写入读取其中的几个字段
    - 可以将对象以接口或基类的方式序列化，首先写入一个枚举值，<br/>指示具体类型是什么，但返回时返回类型或基类的类型

## Ownership 管理

- 理解如何使用 ownership，以及它如何影响 clients 和 server 对任何 project 是至关重要的
- 所有权是 Fish-Net 的核心概念，用于确定哪个客户端拥有对某个对象的控制权
- 每个 NetworkObject 都可以被分配给一个客户端 Connection 作为其所有者，<br/>或者该对象也可以没有分配所有者
- 只有服务器有权限更改对象的所有权，不过服务器本身不能成为任何对象的所有者，<br/>Owner 是一个 Connection
- 当某个客户端拥有一个对象时，它就被视为该对象的合法使用者，<br/>可以执行诸如移动角色或使用武器等操作
- 所有权也可以临时授予，用于与世界对象的交互，比如操作炮塔。
- 所有权检查对于确保对对象的正确控制至关重要
  - 验证某个客户端是否有权操作某个对象
  - 检查玩家相关数值（如名称或分数）的所有权状态
  - 确保只有所有者才能执行特定的网络调用（例如 ServerRpc）
- 分配所有权
  - Spawn 时指定所有权，通过 NetworkConnection 参数指定
  - 改变或新指定所有权，通过 NetworkObject.GiveOwnership(newConnection)
  - 移除所有权：NetworkObject.RemoveOwnership()
- 检查所有权
  - 可以通过 NetworkObject/NetworkBehaviour 属性检查
  - base.IsOwner：如果 local client 拥有这个 object，返回 true
  - base.Owner：获取当前 owner 的 NetworkConnection
  - base.IsController：如果是 local client 并且拥有这个 object，<br/>或者是 server 并且没有指定任何 owner，返回 true
- 所有权转移
  - 只有 server 可以 assign，transfer，remove ownership。<br/>典型地，ownership 在 spawning object 时授予。
  - 自动分配所有权：PlayerSpawner 脚本（位于 NetworkManager 预制体中）<br/>会确保生成的玩家对象由其对应的客户端持有所有权。
  - 立即分配所有权：若客户端需要即时获得所有权（例如无延迟地控制炮塔），<br/>可使用 PredictedOwner 组件。该组件支持扩展以实现自定义逻辑。
- 通过 Connection 读取其他客户端的 values
  - 要求在 ServerManager 上启用共享 ID（Share Ids），<br/>这样客户端能知道其他客户端（Conneciton），<br/>然后可以通过 Connection 读取其他 player 的信息
  - 共享 ID 默认处于启用状态，且不会向客户端泄露任何敏感信息
  - 共享的 ID 就是 NetworkConnection，NetworkConnection 可以序列化并在网络上传递
  - 在 Server 上用 Sync 容器可以向所有客户端同步共享所有客户端的 NetConnection，<br/>Server 可以用 SyncDictionary 保存各个客户端的其他信息，这样 client 就能知道其他客户端的相关信息了

## Area of Interest(Observer System)

- 兴趣区域实现网络上的可见区域，用于精准控制哪个客户端能接收哪些对象的信息
- 某个对象的观察者 Observer 是指能够查看此对象，并能与之交互的客户端
- 可以通过 NetworkObserver/ObserverManager 组件来配置哪些客户端有权观察此对象，<br/>在 NetworkObject 上添加 NetworkObserver，其中配置观察条件，用来让 server 确定哪些 clients 是这个对象的观察者
- 如果客户端未被认为是一个对象的观察者，则该对象对其处以非激活状态
  - 客户端不会受到该对象的网络信息
  - 不会触发相关回调函数
  - 对于 Scene NetworkObject，它始终处于 disable 状态，直到这个客户端获得观察权限
  - 动态 spawn 的对象，客户端在获得观察权之前根本不会加载该对象
- 观察者系统（兴趣区域）专门为新手开发者提供了开箱即用的基础功能
- 系统还提供了高度灵活的扩展能力，可以自定义观察者规则
- NetworkManager 预制体已包含新项目开发所需的推荐基础组件，<br/>其中内置的 ObserverManager 组件配置了 Scene Condition。
- NetworkManager 中的 PlayerSpawner 会将 player 添加到当前场景，<br/>使得本客户端成为该场景内对象的观察者，但前提是玩家对象必须提前 Spawn
- 如果自行创建 NetworkManager（而不是使用预制体），或使用预制体并移除 PlayerSpawner，<br/>则需要手动将客户端加载到目标观察场景中
- 如果移除 PlayerSpawner 组件或未使用 SceneManager.AddOwnerToDefaultScene 方法，<br/>则必须通过 SceneManager 显式加载客户端场景。只有通过 Fishnet.SceneManager 加载的场景，<br/>其中的对象才会被认定为网络同步场景。客户端可通过全局场景加载或针对特定连接（客户端）的场景加载成为场景成员
- 修改条件
  - 运行时可以修改观察条件
  - 必须通过 NetworkObserver 组件访问条件<br/>```base.NetworkObserver.GetObserverCondition<DistanceCondition>().MaximumDistance = 10f;```
  - 所有条件都可以启用或禁用。禁用条件可以临时忽略条件<br/>```ObserverCondition.SetIsEnabled(false);```
- 自定义条件
  - 条件是 ScriptableObject，创建为资源
  - 继承 ObserverCondition
  - 重写 ```bool ConditionMet(NetworkConnection connection, bool currentlyAdded, out bool notProcessed)```
    - connection 是当前被检查的客户端，判断它是否是观察者
    - currentlyAdded 指示 connection 当前是否对 object 可见
    - notProcessed 是输出参数，返回 true 表示本次检查不被处理，<br/>仍然使用上一次条件检查的结果
  - 如果检查需要其他参数，例如 NetworkObject 甚至更多参数，<br/>可以作为 ScriptableObject 脚本的参数，并在运行时指定
