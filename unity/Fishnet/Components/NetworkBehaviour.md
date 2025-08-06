# NetworkBehaviour

NetworkBehaviour 允许脚本执行网络操作
- SyncTypes
- Rpc
- Broadcast

NetworkBehaviour 不能直接添加到 objects 上，<br/>必须要自定义脚本继承 NetworkBehaviour 再添加到 objects。

每个 NetworkBehaviour 必须挂载到它自身或其 parent 具有 NetworkObject 的 GameObject 上。

运行时动态添加 NetworkBehaviour 派生类现在还不支持。