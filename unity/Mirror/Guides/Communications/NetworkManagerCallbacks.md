# Network Manager Callbacks

在一个 multiplayer 游戏中的正常操作中将会有大量事件发生，例如 host starting up，一个 player joining，或者一个 player leaving。

这些可能的事件的每一个有一个关联的 callback，你可以在自己的 code 中实现，在事件发生时执行动作。

要做到这一点，创建自己的脚本，继承自 NetworkManager。然后，你可以覆盖 NetworkManager 上的虚拟方法为自己的实现，定义当事件发生时执行什么行为。

不同 mode 下的 game 发生的事件和它们发生的顺序略有不同。游戏可以运行在 host，client，server-only 中的一种。

## Host Mode

当 StartHost 时

- OnStartServer
- OnStartHost
- OnServerConnect
- OnStartClient
- OnClientConnect
- OnServerSceneChanged
- OnServerReady
- OnServerAddPlayer
- OnClientChangeScene
- OnClientSceneChanged

当 StopHost 时

- OnStopHost
- OnServerDisconnect
- OnStopClient
- OnStopServer

当一个 client 连接时

- OnServerConnect
- OnServerReady
- OnServerAddPlayer

当一个 client 断开连接时

- OnClientDisconnect

## Client Mode

当 client start 时

- OnStartClient
- OnClientConnect
- OnClientChangeScene
- OnClientSceneChanged

当 client stop 时

- OnStopClient
- OnClientDisconnect

## Server Mode

当 server start 时

- OnStartServer
- OnServerSceneChanged

当一个 client 连接时

- OnServerConnect
- OnServerReady
- OnServerAddPlayer

当一个 client 断开连接时

- OnClientDisconnect

当一个 server 停止时

- OnStopServer
