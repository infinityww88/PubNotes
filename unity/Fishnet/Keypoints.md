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

Fishnet 只是一个网络传输框架，在 GameObject 之间传递消息。本质上跟 scene 无关。scene 只是一堆 GameObject 的集合。只要 server 端和 client 端具有可以互通信息的 gameobject 副本，可以自洽运行，就没有问题，无关是否在相同的场景中。而且实际上，server 端和 clients 本来就可以具有不同的场景组合，每个 instance 上的 scene（gameobject 集合）都可能不同。甚至本质上只需要一个场景即可，一旦建立通信，就可以在这一个场景中不断创建、销毁可以相互通信的 gameobjects，例如可以使用 prefab 作为子场景进行管理。核心是可以相互通信的 gameobjects，scene 不是本质需要的。scene 只是 Unity/Fishnet 用来管理 gameobjects 集合的手段。
