SceneManager 在 server 和 clients 之间处理 networking scenes，包括更新 active scenes，addressable scenes，提供有用的 callbacks 等等。

SceneManager 为 networked Unity game 提供了强健的，同步的，事件驱动的 scene management，确保所有 clients 和 server 在复杂的场景操作中保持同步。

它负责协调哪些场景在所有 clients 和 server 上加载和卸载，确保同步，并为场景加载暴露很多选项。

SceneManager 中的 callbacks 的描述性很强，非常有用，值得仔细研究。

## 设置

- Scene Processor

  确定 scene 加载如何执行。如不设置，使用默认的 scene processor。

- Light Probe Updating

  控制 light probes 在 scenes 加载后如何更新。

- Move Client Host Objects

  如果开启，当场景卸载时，Host CLient 可见的对象不会被销毁，而是会被移动到一个临时场景中。
  
  随后，这些对象将在主机客户端的下一个帧周期被销毁。此机制确保了服务器和客户端回调函数在对象移动后仍能正常工作。

- Set Active Scene

  该功能允许场景管理器（SceneManager）在加载和卸载场景时，自主选择将哪个场景设置为活动场景。
  
  默认情况下会优先使用全局场景（global scenes），若未设置全局场景，则使用客户端当前的单个场景。
