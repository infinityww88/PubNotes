# ServerSpawner

一个简单工具，辅助当 server starts 时立即 spawn 特定 objects。

ServerSpawner 组件是 FishNet 提供的实用工具，可用于在服务器成功启动时（或按需手动触发）选择性地实例化并生成对象。

它常用于创建全局网络对象（Global Network Objects），这类对象需在运行时动态生成，而非直接存在于场景中。

## 设置

- Automatically Spawn

  该选项决定了组件是在服务器启动时立即实例化并生成对象，还是仅在您手动调用 ServerSpawner 组件的 Spawn 方法后执行。

  如果您希望手动控制这些对象的生成时机，可以禁用此选项。

- Network Objects

  该列表包含服务器启动时组件将实例化的网络对象（Network Objects）。
  
  实例化时会按照列表中的顺序进行，并且如果这些对象已添加到对象池中，组件会尝试使用 FishNet 的对象池系统进行实例化。
