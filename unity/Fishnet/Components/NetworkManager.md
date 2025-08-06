# NetworkManager

NetworkManager 对运行 client 和 server 是一个基本组件。它在核心组件之间作为桥梁，并配置网络。

管理 networking lifecycle
- 建立连接
- hosting sessions
- 处理 client-server 通信

NetworkManager 自己不应该是 NetworkObject，必须不能包含 NetworkObject 在自身或 parent 或 child。

NetworkManager 还提供了一个注册、获取全局组件的能力（全局单例）。

NetworkManager 利用一些 sub-manager 组件。如果这些组件不在 object 上，它们会在运行时添加。

## 设置

- Run In Background：如果为 true 允许应用程序在后台允许。<br/>后台运行对 clients 尤其是 server 通常非常重要
- Dont Destroy On Load：确保 NetworkManager 在 scene 改变时保持。<br/>如果你只使用一个 NetworkManager，最好将它设置为 true
- Persistence：这个选项指示当游戏中存在多个 NetworkManagers 时的行为
- Logging
  - 指示对 builds，editor，headless 模式打印哪些 actions 的日志
  - 如果为空，使用默认 logging settings
  - 要创建一个自定义 logging settings，创建一个 Logging Configuation 资源
- Spawnable Prefabs
  - 指示哪些 prefabs 用作 Networked Objects
  - 默认对任何保存的 scene，这个字段自动设置为 DefaultPrefabObjects
  - 可以使用自定义规则创建你自己的 PrefabObjects
- Object Pool
  - 要使用的 object pooling 脚本
  - 为空时，运行时自动添加 DefaultObjectPool
  - 可以从 ObjectPool 继承创建自己的 Pool
- Refresh Default Prefabs
  - true：每次进入 play mode 时刷新 DefaultPrefabCollection
  - 通常不需要 enable，但是如果你的 prefab collection <br/>由于符号连接而频繁损坏，这个选项会有所帮助