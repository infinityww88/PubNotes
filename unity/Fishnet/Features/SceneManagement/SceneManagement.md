Fish-Networking 框架内置了一个强大的场景管理工具，它能让你以极低的成本实现网络场景同步，同时提供了大量高级功能选项。

SceneManager 组件提供了多种场景功能，以满足你的多人游戏需求。

Fishnet.SceneManager 和 Unity SceneManager 使用的是一样的 Scene，Fishnet.SceneManager 是建立在 Unity SceneManager 基础上的。

Fishnet.SceneManager 通过 name 查找的 Scene 就是 Unity 的 Scene。就像 Server Spawn 的 Object 就是 Unity GameObject 一样。

# SceneManager

## Scene 可以想象为一个 Prefab

- 加载卸载场景就是实例化、销毁 Destroy Prefab
- 加载卸载可以替换整个场景，或者替换、添加为场景的部分
- 但是这些 Prefab 是在网络上 spawn、despawn 的
- 实例化、销毁过程中发送百分比事件

## Scene Events

- OnClientLoadedStartScenes
  - 每次客户端首次加载 start scene 触发
  - start scene 可以是设置的任何 global scene
  - 若无 global scene，则为进入游戏时加载的场景<br/>（此时不需要加载场景，但是联网时还是会触发这个回调函数）
  - 参数：connection（指示客户端）和 asServer
  - 如果只想知道某个 connection 何时加载 start scene，<br/>使用 OnLoadedStartScenes
- OnQueueStart/OnQueueEnd
  - 每次场景加载卸载触发一个 queue，缓存后面的场景操作
  - queue 为空时触发 end
  - queue 为空并开始 load 时触发 start
- OnLoadStart/OnUnloadStart
  - Queue 中每处理一个 item 时触发
  - scene load 时触发 OnLoadStart
  - scene unload 时触发 OnUnloadStart
- OnLoadPercentChange
  - 场景加载时唯一可用的事件
  - 提供一个 float 指示加载的百分比
- OnLoadEnd/OnUnloadEnd
  - Queue 中每个 item 加载完或卸载完时触发
- OnClientPresenceChangeStart/OnClientPresenceChangeEnd
  - 仅在服务器可用
  - 指示客户端正在添加到某个场景中，或正在从某个场景移除
  - 只在客户端完全加载、卸载场景后触发
  - Start 变体（OnClientPresentStart）：会在客户端观察者状态更新之前被调用
  - End 变体（OnClientPresentEnd）：会在客户端观察者状态更新之后被调用

## Scene Data

- SceneManager 加载和卸载场景使用的数据（参数类型）
- SceneLookupData：如何查找一个场景
  - Handle(int)：通过句柄查找
  - Name(string)：通过名字查找
- SceneLoadData
  - PerferredActiveScene(PreferredScene)
    - 成员
      - Client(SceneLookupData)：Client perferred scene
      - Server(SceneLookupData)：Server perferred scene
    - 指定这个参数时，指示其中的 scenes 在加载后将作为 server 和 clients 的 active scene
    - Unity 游戏当前可以有多个场景，但是其中一个作为 Active Scene。<br/>意味着实例化对象都放在这个场景中，但是其他场景一样正常运行
  - SceneLookupDatas(SceneLookupData[])
    - 要加载的所有 scenes 的 SceneLookupData
    - 一次可以同时加载多个场景，但是可以在 PerferredActiveScene 中指定 active scene
  - MovedNetworkObjects(NetworkObject[])
    - 将当前一组 NetworkObjects 移动到 SceneLookupDatas 的第一个场景中
  - ReplaceScene(ReplaceOption)
    - 与 Unity 原生 SceneManager 加载场景类似，允许指定用场景替换当前场景或增量添加到当前场景中
    - 使用所有新的场景替换当前场景。当替换 scenes 时，第一个加载的场景作为 active scene，其他的作为 additive
  - Params(LoadParams)
    - 加载场景时设置的加载参数，为每个场景加载定义加载参数
    - ServerParams：用作服务器场景加载的加载参数
    - ClientParams：用作客户端场景加载的加载参数
  - Options(LoadOptions)：用于加载场景的额外选项
    - AutomaticallyUnload
      - true：当加载的 scenes 没有任何 clients 使用时，自动卸载场景
      - false：当连接意外离开（断开连接），该场景仍然留在内存中
      - 这个字段只应用于为 connections 加载的场景，而不是 globally loaded scenes
      - 全局场景 Global Scenes 只能通过 ReplaceScenes 或显示卸载方法来卸载
    - AllowStacking
      - true：一个 scene 可以加载多次（在 SceneLookupDatas 中多次指定同一个 scene），这称为场景堆叠 scene stacking
      - false：不允许同一个场景加载多次
      - 场景堆叠只在 server 发生，client 只会加载一个实例
      - Global scenes 不能堆叠
    - LocalPhysics(LocalPhysicsMode)
      - 一个场景的物理模模式
        - 物理场景和渲染场景是分离的。默认创建、加载一个场景时，其物理在默认物理场景 default physics scene 中模拟。<br/>但是可以为每个场景指定一个独立自有的物理场景（2D 或 3D）
        - None：不创建独立的物理场景
        - Physics2D：创建独立的 2D 物理场景
        - Physics3D：创建独立的 3D 物理场景
      - 如果堆叠多个场景，建议设置合适的 LocalPhysics 避免堆叠的场景之间发生不必要的碰撞
    - ReloadScenes
      - true：如果场景已经加载了，reload 它。现在还没有实现
    - Addressables
- SceneUnloadData
  - PreferredActiveScene：卸载后哪个场景变成 Active Scene（client & server）
  - SceneLookupDatas(SceneLookupData 数组)：指示哪些场景被卸载
  - Params(UnloadParams)：unload 时传递给 Unity Scene Unload 的参数
    - ServerParams
    - ClientParams
  - Options(UnloadOptions)
    - Mode：如何在 server 卸载 scenes
      - UnloadUnused 会卸载没有任何 clients 的场景
      - KeepUnused 即使场景中没有任何 client，server 仍然将场景保持在内存中
      - ForceUnload 无视 clients 是否还在场景中，仍然在 server 中卸载场景
    - Addressable

## Loading Scenes

- 与 SyncTypes 一样，加载场景只能在 Server 端执行
- DefaultScene 为实现一个简单的 online/offline scene 切换提供了一个简单的预制脚本
- 如果使用 ObserverManager 的 Scene Condition，<br/>以 Global 或按 connection 加载场景时，<br/>会将指定客户端的 connection 作为观察者添加到场景中
  - Globa Load 会将所有客户端都作为观察者添加到加载的场景中
  - By Connection Load 则仅将指定连接添加到加载的场景中
- 场景加载通过 SceneManager 实现
  - 其引用可以在 NetworkBehaviour 中获取(base.SceneManager)
  - 其他地方可以使用 InstanceFinder.SceneManager
- 设置
  - 调用 SceneManager 加载场景之前，需要先设置 loading data，以告知 SceneManager 应该如何加载场景
  - SceneLookupData：指定如何查找场景
  - SceneLoadData：无论以何种方式加载场景，必须为加载方法传递一个 SceneLoadData 对象
    - SceneLoadData 提供了正确加载一个或多个 scenes 所需的所有信息
    - SceneLoadData 的构造函数会根据加载新场景、还是加载已有的场景实例，<br/>自动创建 SceneManager 所需的 SceneLookupData
- Loading New Scenes
  - 场景可以全局加载（可认为对所有 client connections 加载），也可以针对部分客户端加载
  - 加载新场景只能通过名字 Name 加载，不能使用 Handle 或 Reference
  - 全局场景 Global Scenes
    - 全局场景加载通过 SceneManager.LoadGlobalScenes() 加载
    - 全局场景加载不需指定 connection，它为所有 connections 加载
    - ```base.SceneManager.LoadGlobalScenes(new SceneLoadData("Town"))```
  - 按客户端场景 Connection Scenes
    - 可对单个 connection 加载场景，可对多个 connection 加载场景，或仅在服务端加载场景
    - 通过连接加载场景时，只有指定的 connection（客户端）会加载这些场景
    - 还可以随时将额外的 connection 添加到已加载的场景中
    - 对单个客户端加载场景：```base.SceneManager.LoadConnectionScenes(base.Owner, new SceneLoadData("Main"))```
    - 对多个客户端加载场景：```base.SceneManager.LoadConnectionScenes(new NetworkConnection[]{connA, connB}, new SceneLoadData("Main"))```
    - 仅在服务端加载：```base.SceneManager.LoadConnectionScenes(new SceneLoadData("Main"))```
  - 加载多个场景 Loading Multiple Scenes
    - 无论是全局加载还是按连接加载，都可以在单次方法中加载多个场景，只需在 SceneLoadData 指定多个场景的名字或 handle
- Loading Existing Scenes
  - 如果场景已经在服务器上加载，可将客户端加载到该场景中
  - 通过场景引用 Reference 或句柄 Handle 查找场景，以确保获取到准确的目标场景
  - 按名称加载场景时，系统会将 connection 加载到首个匹配名称的场景中。<br/>若启用场景堆叠 scene stacking，可能存在多个同名场景，需要格外注意
  - 若利用场景缓存 scene caching 功能（所有客户端离开场景后，server 仍然保持 scene），<br/>可以向没有任何客户端的场景加载客户端
  - SceneManager 获取已加载场景引用的方法
    - 通过事件：SceneManager.OnLoadEnd 的事件回调参数包含 loadedScenes 的引用
    - 通过 Connection：NetworkConnections 有一个 Connections 所在的 Scene 列表<br/>可以通过客户端 Id 在 ServerManager.Clients[clientId].Scenes 获得
    - 通过 SceneManager.SceneConnections：SceneManager 保存了一个所有 Connection Scenes 的字典，<br/>Scene 的 Reference 为 key，其中所有的 Connections 集合为 value
  - 使用 Reference 加载 connection 到现有场景。<br/>只需要用上述方法获得场景引用，在 SceneLoadData 中传入 Reference 或 Reference.handle 即可。<br/>其他与用名字加载新场景一样，指定要加载的 connections。
- 替换场景 Replacing Scenes
  - Fishnet 提供能力用新请求加载的 scenes 替换 clients 上已加载的 scenes
  - 在 SceneLoadData 中设置 ReplaceScene 选项
  - 被替换的 scenes 在新场景加载前会先卸载
  - 请求替换的 scenes 默认会同时替换 server 和 clients 上已加载的 scenes。<br/>如果你希望 server 保持 scenes 加载，只替换 clients 上的 scenes，使用 Scene Caching 功能
  - 选项
    - Replace None：默认的加载选项，忽略 replace options 并正常加载 scene
    - Replace All：这会替换当前 Unity 加载的所有场景，即使不是被 Fishnet SceneManager 管理的那些
    - Replace Online Only：只替换被 Fishnet.SceneManager 管理的 scenes
- DefaultScene
  - Fishnet 提供了 DefaultScene 来支持最简单的 scene 管理
  - DefaultScene 是一个 ready-made solution，提供一个简单方法<br/>在 network 开始或停止时在一个 online scene 和一个 offline scene 之间转换，<br/>无需编写任何 code
  - 当 network start 时，它自动加载指定的 online scene，当 network stop 时自动加载 offline scene
  - 这适合想要 plug-and-play 解决方案的开发者，但是更复杂的应用还是需要手动加载卸载场景
  - 步骤
    - 添加 DefaultScene 到 NetworkManager 上
    - 在 Inspector 中，指定 online scene 和 offline scene
    - 确保两个场景是不同，否则组件不会正常工作

## Unloading Scenes

- 卸载和加载相同，只是调用 Unload 而不是 Load
- 可全局卸载（踢出所有 clients），也可以按 connection 卸载（踢出部分 clients）
- Global Scene
  - ```SceneManager.UnloadGlobalScenes()```
  - 不可以用 UnloadConnecitonScenes 卸载 Global Scenes
  - 用 SceneUnloadData 指定要卸载的场景和选项
- Connection Scenes
  - 可以指定一个或多个 connections
  - 如果所有 connections 都从一个 scene 卸载，Server 会从自身卸载那个 scene
  - 如果希望卸载一个 scene 和所有 connections
    - 获取 scene 中的所有 connections
    - 对每个 connection 调用 unload
    - SceneManager.SceneConnections 保存了所有 online scene 和其中的 connections
  - 如果想卸载所有 Connections 并保持 scene 在 server 上加载，使用 scene caching

## Scene Stacking

- Scene Stacking 是 server 或 host 的能力
- 加载同一个 scene 的多个实例，通常每个 scene 有不同的 clients(connecitons) 或 observers
- 加载到新的 Stacked Scene
  - 在 SceneLoadData 选项中设置 AllowStacking = true
  - SceneLookupData 必须使用 scene name 填充，以创建一个 stacked scene 的新实例
  - Global Scenes 不可 stacked
- 加载到现有 Stacked Scene：如果使用 Scene Reference 或 Handle 加载两个 connections 到一个 scene，它们会添加到同一个 scene 中，无论 AllowStacking 是 true 还是 false
- 分离物理模拟 Separating Physics
  - stacking scenes 时可以分离 physics，这确保 stacked scenes physics 不会彼此交互
  - 在 SceneLoadData 设置 LocalPhysics 选项
    - LocalPhysicsMode.None：使用默认 physics scene
    - LocalPhysicsMode.Physics2D：为 scene 创建一个本地 physics2d scene
    - LocalPhysicsMode.Physics3D：为 scene 创建一个本地 physics3d scene
  - 一旦使用了 separate physics scenes，必须手动进行模拟，这是有意设计的
    - 在 TimeManager.OnPrePhysicsSimulation 注册回调函数
    - 回调函数中调用 gameObject.scene.GetPhysicsScene().Simulate(delta)

## Scene Caching

- Scene Caching 是 server 的能力，保持 scene 在 server 端加载，<br/>而所有 clients 都已从那个 scene 卸载或停止观察它
- 加载 scene 时可以在 SceneLoadData 中指定所有 clients 卸载时是否自动卸载 scene，<br/>还是保留在 server 中
- 卸载 scene 时可以通过 ServerUnloadMode.KeepUnused 覆盖加载时的 AutomaticallyUnload 选项
- 无论加载还是卸载都是 server 执行的，不是在 client 端发起的，<br/>但是 client 会按照指令加载或卸载指定场景
- Host Mode
  - server 需要保持 scene 加载，client 却要求场景卸载
  - client 不会直接卸载 scene，而是通过观察者系统将 client 从场景中移除（通过 Scene Condition），然后更新场景可见性。
  - Scene 仍然在内存中，但是对 client disable renderer
  - 作为 host，服务器和客户端共享同一份已加载场景和游戏对象实例。<br/>如果 Host Client 真的执行场景的卸载操作，Host Server 的场景也会被卸载。<br/>因此必须在 ObserverManager 中通过 Scene Condition 使 server 保持 scene 加载，<br/>而 Host Client 看不见场景中的 Object（disable renderer）
  - 这通常意味着每个带有 mesh 的 GameObject 必须具有一个 NetworkObject 组件，<br/>使得其 renderer 被 Scene Caching 控制可见性

## Scene Visibility

- ObserverManager 配合 SceneCondition，在场景中管理观察者
- ObserverManager + SceneCondition 可以控制 client <br/>是否成为它们所在 scene 的 gameobjects 的 observer
- Scene Condition 确保 NetworkObjects（无论是 Scene 中还是 Spawned）<br/>只对该对象所在场景中的 connection 可见
- 绝大多数情况下，应该将具有 scene condition 的 NetworkObserver 添加到 networked objects。<br/>这也是 ObserverManager 默认添加的唯一条件
- 如果在场景切换时遇到找不到 NetworkObject 或 RPCLink 的错误，<br/>很可能是忘记添加 Scene Condition 了
- 管理 Visibility
  - 初始场景加载
    - client 首次加载到游戏中，第一个场景是被 Unity Scene Manager 加载的，而不是 Fishnet.SceneManager
    - 这意味着 clients 没有自动添加其 connection 到 scene 中（这需要 Fishnet.SceneManager）
    - 这也意味着 clients 没有这个场景的 visibility
    - Fishnet 提供了预制组件 PlayerSpawner，其中包含将 client 添加到 default scene 的逻辑
    - 如果你不想使用 PlayerSpawner，而是自己操作
      - 使用 Fishnet.SceneManager 将 client 添加到场景中
      - 在你赋予 ownership 的 object 上调用 SceneManager.AddOwnerToDefaultScene()
  - 添加 client connections 到 scenes
    - 当 globally 或按 connection 加载一个场景，<br/>ServerManager 会自动将那个 connection 放在加载的 scene 中
    - 添加后，客户端能够查看该场景的所有 NetworkObjects
    - 可以手动添加 Client Connection 到 Scenes 中。<br/>如果 scene 已经在 client 上加载了（比如通过 Unity Scene Manager 加载的第一个场景），<br/>可以通过 SceneManager.AddConnectionsToScene() 添加 Connection 到 Scene 中
    - 手动添加 client connection 只建议由高级开发者使用
  - 从 scenes 移除 client connections
    - 从 client 卸载一个场景时，server 从那个 scene 中移除 client connection
    - 对于 host，从一个 scene 卸载 client，只会从那个场景移除 client 的 connection，<br/>client 对场景失去可见性，但是场景仍然保持在内存中
    - 可以手动从一个加载的场景中移除一个 client connection<br/>```SceneManager.RemoveConnectionsFromScene()```
    - 无论是 Unity SceneManager 管理的场景，还是 Fishnet SceneManager 管理的场景，<br/>都是相同的 Unity Scene。实际上 Fishnet SceneManager 是建立在 Unity SceneManager 之上的逻辑，<br/>它仍然需要使用 Unity SceneManager 实际加载和卸载场景

## Persisting NetworkObjects

- 就像 Unity 的 Dont Destroy On Load 可以在场景切换之间保持 GameObject 一样
- Fishnet Persisting NetworkObject 也是基于 DDOL GameObject 实现的
- 在网络场景切换之间保持 NetworkObjects，它们保持对所有 clients 可见
- Spawned NetworkObjects
  - 加载场景时，SceneLoadData 可以指定一个 NetworkObjects 数组，<br/>它们会被移动到新加载的第一个场景中
- Scene NetworkObjects：无法实现跨场景持久化
  - 既不能标记为 Global
  - 也不能将其置于 DontDestroyOnLoad 场景中
  - 若需要跨场景持久化，不用作为 scene networked objects
- Global NetworkObjects
  - 类似普通 GameObject 放入 DDOL 场景的行为
  - 在场景加载和卸载过程中，Global NetworkObjects 始终保留在服务器和客户端 DDOL 场景中，<br/>维持其状态不变，无需额外操作（像 Spawned NetworkObject 那样显式指定才能持久化）
  - 若需将某个 NetworkObject 设置为全局对象，<br/>只需在其组件上将 IsGlobal 设置为 true
  - 通常客户端始终作为 DDOL 场景的观察者存在，<br/>因此 Global NetworkObjects 更适用于管理器类型的游戏对象，<br/>而非带有 mesh 渲染的实体对象
  - Scene NetworkObject 不能被标记为 Global，<br/>因此只能先 Spawn NetworkObject，然后将其标记为 IsGlobal=true
- Nested NetworkObjects
  - Unity 不允许将嵌套的 GameObject 移动到其他场景中，只能移动 root GameObject
  - Fishnet 只能移动 root NetworkObject