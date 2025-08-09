- 网络启动停止
- 代码环境检测（client、server、host）
- 网络状态事件通知
- NetworkObject 生命周期
- Communication（Rpc，SyncTypes，Broadcast）
- 所有权管理
- 观察者系统
- NetworkObject 生成销毁
- 场景管理
- 数据序列化
- 预测（运动、对象生成）
- 延迟补偿
- Fishnet 大部分能力（场景管理、对象管理）都是 server 端的能力（服务端权威），只能服务端发起。<br/>客户端的能力只有 ServerRpc，预测移动和预测生成（客户端权威）
- 网络调用在 NetworkBehaviour 脚本中，通过 SceneManager、ServerManager、NetworkBehaviour 的 API。
- 每个 NetworkObject 在服务端和客户端都有副本，在 NetworkObject 的 server 端副本的 NetworkBehaviour 的 code 中进行调用（意味着要判断代码的执行环境）

Scene 可以本质上和 Prefab 差不多，都是 Game 中一组 GameObject 的管理单位，让 Unity 以一个集合一起处理一组 GameObjects（加载、卸载）。对于 Fishnet 也是一样，Scene 是其在网络上，在 Server 和 Clients 之间，以一组 GameObject 集合（Scene）一起加载、卸载一组 GameObject。甚至可以整个游戏中可以只有一个 Scene，然后仅以 Prefab 管理子场景（一组 GameObjects）。Fishnet 的场景就是 Unity 的场景，因此只需在网络上传递场景名字即可加载、卸载场景。但是 Fishnet 在 Unity 场景之上还管理了更多一些信息，因此 Fishnet Game Server 和 Clients 应该使用 Scene 管理和同步。Scene 管理（加载、卸载）只应该由 server 发起，客户端只能被动接收、同步。但是注意，场景可以作为 Additive 加载到当前游戏中，而无需替换游戏中的当前场景。

Fishnet 应以 scene 管理 GameObjects 集合，然后再在运行时向场景中生成、销毁更多 Object。

Fishnet -> Scene -> Object。
