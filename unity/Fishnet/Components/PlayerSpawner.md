# PlayerSpawner

Player Spawner 组件可以被用于在 client 连接到 game 时，自动 spawn gameobject，而不用手动生成并设置 owner。

FishNet 中的 ​​PlayerSpawner​​ 组件负责在客户端连接到服务器时为其生成玩家对象。

你可以通过 ​​Inspector（检视面板）​​ 或调用 ​​SetPlayerPrefab​​ 方法来设置玩家预制体。

此外，你还可以定义一个玩家生成点（Transform）数组（即 ​​Spawns​​ 数组）。如果没有设置生成点，则会使用预制体自身的位置和旋转。你还可以访问 ​​OnSpawned​​ 事件，该事件会在服务器上玩家生成时触发。

FishNet 足够灵活，不要求 client/condition 具有专有的 player object。但这是个常用实践，因此 PlayerSpawner 为此提供了预制脚本。

## Settings

- Player Prefab

  这个字段用于当 client 连接到 server 时，组件要为 clients 实例化的 prefab。

- Add to Default Scene

  当未通过 FishNet 的 SceneManager 指定全局场景时，此功能用于将客户端添加到活动场景中。这一点非常重要，因为 FishNet 不会强制客户端与服务器从同一场景开始运行，因此需要明确告知 FishNet：客户端是否应该观察特定场景，并接收该场景中网络对象（Network Objects）的相关信息。

- Spawns

  这是 PlayerSpawner 用来生成玩家对象的 GameObject 变换（Transform）位置列表。它会按照顺序逐个使用这些位置，到达最后一个后会循环回到第一个重新开始。如果没有指定任何生成点，则会使用预制体自身的基础位置。
