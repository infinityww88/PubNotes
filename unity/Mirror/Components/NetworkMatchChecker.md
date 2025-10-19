# Network Match Checker

Network Match Checker 组件基于 match id 控制 networked objects 的可见性。

![NetworkMatchChecker](../../Image/NetworkMatchChecker.png)

任何具有这个 component 的 object 只会对在相同 match 的其他 objects 可见。

这可以用于在一个单个 game server 实例上隔离 players 到它们各自的匹配中（即同一个 game server 上可以同时运行多个匹配）。

当你创建一个匹配时，使用 System.Guid.NewGuid() 生成和存储一个新的 match id，并赋予同一个 match id 到 Network Match Checker，通过 GetComponent<NetworkMatchChecker>().matchId。

Mirror 的内置 Observers 系统将会隔离 networked objects 的 SyncVar 和 ClientRpc，只发送 udpate 到具有相同 match id 的 clients。
