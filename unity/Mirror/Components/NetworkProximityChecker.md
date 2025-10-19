# Network Proximity Checker

Network Proximity Checker 组件为 network clients 的 gameobjects 的可见性，基于到 players 的邻近距离。

![NetworkProximityCheck](../../Image/NetworkProximityCheck.png)

- Vis Range

  定义 gameobject 对 observers 可见的距离

- Vis Update Interval

  定义 gameobject 应该检测 observers 进入可见范围的频率

- Check Method

  定义用于 proximity 检查的物理类型（2D，3D）

- Force Hidden

  点击这个 checkbox 对所有 players 隐藏 object

使用 Network Proximity Checker，运行在一个 client 的 game 没有关于不可见的 gameobjects 的信息。这又两个好处：它减少通过网络发送的数据的数量，并且它使你的游戏对于 hacking 更加安全。

这个组件依赖于物理来计算可见性，因此 observers gameobjects 必须还有一个 collider 组件。

一个具有 NetworkProximityChecker 组件的 gameobject 还必须有一个 NetworkIdentity 组件。当你在一个 gameobject 上创建一个 NetworkProximityChecker 组件，如果它上面没有 NetworkIdentity 组件，Mirror 会自动创建一个。

具有 NetworkProximityChecker 组件的 scene objects 在它们离开可见范围时被 disable，spawned objects 在它们离开可见距离时销毁。
