## 通过源代码查找问题

Fishnet 基础是开源的，通过分析 code 来掌握其使用方法。编写测试场景，用 Debug.Log 打印关键信息。

要调试 Server 问题，就将 Editor 以 server 启动，要调试 Client 问题，就将 Editor 以 Client 启动。

## Global Scenes 加载和 ReplaceOption

Fishnet 中有很多使用约定，并没有在文档中阐述，需要在实际应用中总结。

例如 Global Scene 每个 game 应该只有一个，即使后面可以通过 additive LoadGlobalScenes 也不应该加载 Additive Global Scenes。因为通过查看 SceneManager 代码可见，每次加载 Global Scene 就会把那次请求的 ReplaceOption 记录下来，仅记录最后一次加载的选项。每当 client 连接到 server 时，server 会将 SceneManager 管理（保存）的 global scenes 广播给这个 client，告诉它加载这些 scenes，同时传递 ReplaceOption。这样如果最后一次 global scenes 加载指定了 Additive，那么无论之前加载的 Global Scenes 是使用什么 ReplaceOption 加载的（All、Online），到了 client 都会使用 Additive 加载。集合 DefaultScene 使用时，就会出现这样的情况：

- client 还在 offline scene，server 通知以 additive 加载 global scenes
- client 以 additive 加载 global scenes
- offline 包含 Main Camera 和 EventSystem，而 Global Scenes 也包含它们，这样就导致游戏中同时存在两个 Main Camera 和 EventSystem，而这是不应该的，同时 Unity 会打印警告日志
- 后面 DefaultScene 会为了安全起见，卸载 offline scene。但是仍然存在一个窗口期，导致同时存在两个 Main Camera 和 EventSystem，并出现警告日志

从仅保存最后一次 Global Scenes 加载的 Replace Option 来看，Fishnet 应该是假设每个 Server instance 应该仅有一次 Global Scenes 加载的（但是其中可以同时加载多个 scenes），后续 scenes 应该仅为 NetworkConnection 加载。

## 多场景的使用和 Prefab

Scene 很大程度类似 Prefab，都是一组 GameObjects 的管理单元。

用 Scene 实现的功能绝大部分都可以同 Prefab 代替。

Unity 和 Fishnet 使用 Scene 作为明确的游戏场景划分和多场景管理。如果要使用多场景，游戏逻辑上必须也是多场景的，即每个场景的客户端都完全隔离。就相当于多个 server，每个 server 使用不同的 scenes 服务 clients，只不过这里可以用一个 server 逻辑上划分多个完全独立隔离的场景，就像一个物理机器上可以开启多个虚拟机或容器意义。

不用将多场景用于实现逻辑上本应该是同一个场景的功能，例如用 additive scene 向场景中添加更多的 GameObjects，这本来应该用 Prefab 很容易实现。Fishnet 和绝大部分框架一样，都有使用约定，同时并没有严格约束和限制用户按照约定使用，但是如果不按照约定使用，试图寻找一些非常规方法使用它们，会遇到各种问题而且不会获得好处，因为框架不是为此设计的，因此也不为此做保证。

同一个逻辑场景的 clients 必须共享相同的 scenes，同时要添加更多功能应该使用 prefab。

能使用 prefab 实现的尽量用 prefab 实现，它不仅简单，而且能避免各种问题。只有 prefab 不能实现的时候再使用多 scenes，而这也通常进入多 scenes 应该适用的情形。

## Scene 做场景分离

Scene 应该用于游戏逻辑上的场景分离情形，除此以外不应该使用多场景。

Global Scenes 用于存储对所有 clients 都必须存在的 GameObjects。Connection Scenes 用于对具体某些 connections 的 scenes，这就需要手动管理和分离 clients 了。

逻辑上在相同区域的 clients（即它们可以相互看见），必须在 server 和所有 clients 上共享相同的 scenes（即 scenes 必须同步），不应该让 server 或某些 clients 有更多的 scenes，而另一些没有。这就是 scenes 不同步。尽管 Fishnet 可以这样做，但是这样会很快遇到各种棘手的问题。这就属于没有按照约定使用，就会遇到被惩罚。

例如 Dota 游戏就只有一个场景，server 和 clients 共享相同的场景。通过各种 Observer Condition 来实现区域可见性的分离。不应该使用多场景，因为逻辑上所有单位（客户都）就是在一个场景中，而且不同区域可见性的分离是基于游戏逻辑（比如单位之间的距离）。而 scenes 是 editor 和 build 时固定的，不能在游戏中动态生成。

Scene 用于固定的游戏场景概念，不能用于基于游戏逻辑的 Prefab 实例化场景，使用的场景时在 Editor 和 Build 时固定的。

总之 Scene 不能用于游戏逻辑的场景。

- 尽量简单使用场景
- 多场景只用作多区域隔离，不同区域的 clients 完全相互隔离，看不见
- 同一个区域的 clients（可以彼此看见对方）必须在 server 和 clients 具有相同的 scenes(scenes 完全同步)。通过各种 observer conditions 实现兴趣区域分离
- 能使用 Prefab 就不用使用 Scene，Prefab 更简单，更符合游戏逻辑。除非只能用 Scene，那说明到了 Scene 适用的情景

## Spawnable Prefab List

所有在 Server 上 Spawn 的 NetworkObject 必须做成 Prefab，并填充到 NetworkManager 的 Spawnable Prefabs 的列表中。Spawnable Prefabs 是一个资源，可以创建自己的 Spawnable Prefabs 并设置到 NetworkManager 中。要 Spawn 的 NetworkObject 的 Prefab 可以手动放在 Spawnable Prefabs 中，也可以有 Editor 自动识别并添加。

要 Spawn 的 Prefab 必须挂载 NetworkObject，但不一定是 NetworkBehaviour。NetworkBehaviour 是需要进行网络通信才挂载的组件。但是通常在所有 clients 上 spawn 的 NetworkObject 都不是为了安静地存在于游戏中，而是为了和玩家交互，因此通常或多或少都具有网络通信的需求，因此一般都带有一个或几个 NetworkBehaviour，即使不是自己实现的，系统自带的 NetworkTransform 本身也是 NetworkBehaviour。

有一种情况 Spawn Prefab 可以只有 NetworkObject 而不需要 NetworkBehaviour。就是其作为一组 NetworkObject 的 root，用来在网络上生存一组新的 NetworkObject，就是用 Prefab 实现 Additive Scene 的功能。这样的 NetworkObject 下面会挂载多个 NetworkObject/NetworkBehaviour。这样它本身不需要网络通信功能，它的 NetworkObject 只是为了 Server Spawn，真正需要的是它下面的 NetworkBehaviours。这就是 Nested NetworkObject。

## 新加入的客户端

新加入的客户端会同步 server 上的最新信息，不仅包括初始 global scenes，还包括后续（在 client 连接之前）server 生成的 network objects。

对于 spawned network objects，销毁的就不会发送给 client。对于 scene network object，server 不会销毁，而是 disable 它们，对新加入的 client 也会告诉它 disable 这些 objects。

## LoadConnectionScene without connections

不指定 connections 加载 connection scenes，它们不会通知客户端加载，只在 server 端加载。这些场景在 server 上就是 existing scenes。

它们用于 scene caching（场景缓存）。后续可以将 connections 加载到这些 existing scenes。

加载场景不一定总是加载新场景，可以将 connections 加载到现有的场景中。

例如 server 上有两个 scene，每个 scene 代表一个房间。client 从一个房间进入另一个房间，就是从一个 existing scene 立刻，加入到另一个 existing scene。

这样来说，Global Scenes 可能并不是最常用的 scenes，基于 Connection Scenes 手动进行场景管理才是最常见的，尤其是游戏是存在多个 online room 的。每个 online room 都是始终存在的，client 只能从一个 room/scene 进入另一个 room/scene。

Global Scenes 只适合 Moba 或 CS 这样同时只有一个 online 场景的游戏。如果是多 online scenes 游戏，只能使用 Connection Scenes 进行场景管理。

UnloadConnectionScenes 可以只为指定几个 Connections 卸载指定几个 Scenes，这些 Scenes 不一定真正卸载，因为还可能有其他 connections 在其中，只是这些 connections 脱离这些 scenes。然后后面可以 LoadConnectionScenes 将这些 connections 加载到其他几个 scenes（也是正在运行的 existing scenes）。这样就实现了 clients 从一个 room 脱离，加入另一个 room 的功能。

对于始终 online 的 scenes，Fishnet 可以在加载时指定是否当所有 connections 都立刻时卸载它们，还是让它们仍然存在于内存中（例如等待后面新的 connections）。

## SceneProcessor

实际处理场景加载的是 SceneProcessor。不指定 SceneProcessor 时使用 Fishnet 内置的 DefaultSceneProcessor，它只是简单使用 Unity Scene Manager 从 Build Scenes 列表中查找和加载指定的 Scene。

如果使用 Addressable 或更高级的热更新系统（例如 YooAsset），就可以自定义 SceneProcessor，自定义加载场景的逻辑。SceneProcessor 被 SceneManager 请求加载场景时，会传递给它场景的名字和加载参数，自定义 SceneProcessor 就可以使用名字和场景参数确定如何加载场景。

场景加载提供的是异步 api，同时要提供加载的进度和是否完成的接口。

## Scene Condition

ObseverManager 是为场景中 Objects 可见性加更多限制条件的。默认 Objects 对所有 client 都可见。每新增一个条件，可见性就更受限制。

默认 ObserverManager 的条件为空。但是基于 Scene 的 Objects 可见性是基本的，通常应该首先添加一个 Scene Condition，否则其他场景的 Objects 也会被 Client 看到。Fishnet 提供的 NetworkManager Prefab 就配置了包含 Scene Condition 的 ObserverManager，如果你手动制作 NetworkManager 也应该这样做。

## NetworkManager Don't Destroy On Load

如果游戏存在跨 online scene 的情形，NetworkManager 不可再场景切换时销毁。因为它们上面挂载有各种 Manager（SceneManager，ClientManager，SceneManager，ObserverManager，Transport 等等），这些 Manager 也只能被 NetworkManager 管理，不能是独立的 GameObject，以为从代码中可以看见 NetworkManager 在 Awake 时在自身 GameObject 上查找或创建这些 Manager。而这些 Manager 分别管理游戏的方方面面的重要逻辑，其内存中保存着游戏的重要数据，例如 SceneManager 保存着当前游戏的各种场景和 Connections，以及运行时生成和销毁的 NetworkObjects，尤其是 Transport 它管理着 client 和 server 的底层网络通信信道。这些组件一旦销毁，就代表着整个游戏世界消失，而且客户端和服务器断开连接。 

这些 Manager 只能存在于 NetworkManager 之上，InstanceFinder 也是读取 NetworkManager 的这些 Manager 实例。而且即使单独保存也是没有意义的，因为那样它们自己就需要考虑切换场景时如何保持自己数据的能力，还不如放在 NetworkManager 上统一管理。

如果游戏有多个区域（room），client 在这些区域中跨越，有两种方式实现：

- 从网络上中断和 sever 的连接
  - 和 server 断开连接，会到 offline scene
  - 指定新区域的 online scene
  - 重新于 server 连接，进入指定的 scene
- 不与 server 断开连接，online 地切换 scene

第一种情况，NetworkManager 就可以不设置 Don't Destroy On Load，因为需要和 server 断开连接，并且新的 online scene 有新的 NetworkManger。

第二章情况，NetworkManager 就必须设置为 Don't Destroy On Load，因为要始终保持与 server 的连接。Server 通过广播和 Client 来同步 Scenes。

联合 DefaultScene 适用时，如果 NetworkManager 没有设置为 DDOL，当切换场景时，NetworkManager 被销毁，网络就断开了，client 不会收到 server 发送的 broadcast，无法加载后续场景，导致游戏空白一片。

## SceneId of XXX not found in SceneObjects

```
SceneId of 4294434555 not found in SceneObjects. For more information on the missing object add DebugManager to your NetworkManager and enable WriteSceneObjectDetails. This may occur if your scene differs between client and server, if client does not have the scene loaded, or if networked scene objects do not have a SceneCondition. See ObserverManager in the documentation for more on conditions.
```

同一个游戏区域中，Clients 和 Server 的场景必须保持同步，不能 server 或一部分 clients 包含额外的 scenes，另一些 clients 则没有，这会导致各种 scene 找不到的问题，尤其是指定了 SceneCondition 的时候。

## Predicition

TimeManager 以一定频率调用 OnTick，每个 OnTick 前有一个 OnPreTick，后面又一个 OnPostTick。对于 Fishnet 网络应用程序，涉及网络更新部分，必须在 TimeManager 的 Tick 中执行，它相当于 Unity 的 Update/FixedUpdate/LateUpdate 等。

例如，Replicate 方法通常在 OnTick 执行，Reconcile 通常在 OnPostTick 执行。

Fishnet 类似的网络框架并不会分开编写 server 和 client 的代码，而是作为共同体编写同一个脚本，同时用在服务器和客户端。至于如何区分服务端运行还是客户端运行：

- 通过标记识别，例如 IsServerStarted
- 通过方法属性 attribute

Replicate 用于执行动作（动画、特效、音效、各种 action），Reconcile 用于同步各种状态（生命值、子弹数量、耐力值、各种标记），Reconcile 不执行任何动作。

Replicate 类似 Rpc，Reconcile 类似 SyncVar。

Replicate 标记的方法既可以在 Server 运行，也可以在 client 运行。

- Controller 首先收集 Input data，执行它，并发送给 Server
- Server 执行收到的 Input data，并将 Input data 发送给其他 Clients
- 其他 Clients 收到 Server 发送的 Input data，并执行（这就是 replay）

执行 Replicate 方法都是使用相同的数据结构 ReplicateData,由 Controller 收集，然后在网络上传输，收到者用这个同样的 ReplicateData 执行 Replicate 方法。

可见 Replicate 在 Controller、Server、其他 Clients 上的逻辑都不相同，但是逻辑都写在同一个方法中，这些不同的逻辑都是被 Replicate 属性实现，包括 Server、Client 对 input data 的缓存，也是在其中实现的。

无论是 Controller 还是 Server，还是其他 Clients，Replicate 方法总是在 Tick 中实时在运行，无论有没有输入。但是当没有输入时？

状态同步和执行动作是分开的，可以视为异步执行，因此它们不需要严格保持同步，代码中也不能依赖于此。考虑状态时只考虑状态，考虑动作时只考虑动作即可。当收到 Reconcile，只需要将其中的 data 复制到本地即可。当收到 Replicate，只需要按照 Input data 执行动作即可。若要在 Reconcile 和 Replicate 实现某种同步，可以通过 data 所在的 Tick 确定先后顺序，完成同步，类似线程同步的同步变量。

