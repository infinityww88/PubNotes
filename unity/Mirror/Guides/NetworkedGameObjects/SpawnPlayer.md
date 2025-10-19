# Player Game Objects

Mirror multiplayer HLAPI 系统对 player gameobjects 和 non-player gameobjects 的处理不同。当一个 player 加入游戏（当一个新 client 连接到服务器），这个 player 的  gameobject 变成这个 player 的 client 上的一个 “local player” gameobject，并且 Unity 管理 player 的 connection 到这个 player gameobject 上。Unity 为每个 player 关联一个 player gameobject，并且路由网络命令到那个独立的 gameobject。一个 player 不能在另一个 player gameobject 上调用 Command。

NetworkBehaviour class（用来继承并创建你自己的 network scripts）具有一个 isLocalPlayer 属性。在每个 client player gameobject 上，Mirror 在 NetworkBehaviour 上设置这个 property 为 true，并调用 OnStartLocalPlayer() 回调函数。这意味着每个 client 都有一个不同的 gameobject 设置为这样，因为在每个 client 上，有一个不同的 gameobject 作为这个 local player 的代表。

![NetworkLocalPlayers](../../../Image/NetworkLocalPlayers.png)

只有属于你的 player gameobject 才会将 isLocalPlayer 设置为 true。通常应该检测这个标记，来决定是否处理输入，是否使摄像机追踪 gameobject，或者做任何其他只应发生在 client 上的 player gameobject 上的 client-side 的事情。

Player gameobjects 在 server 上代表这个 player（即 play 这个游戏的 person），并且具有能力执行来自这个 player client 的 Commands。这些命令是安全的 client-to-server 远程过程调用。在这个 server-authoritative 系统中，其他 non-player server-side gameobjects 不能直接从 client-side gameobjects 接受命令。这同时是为了安全性和降低构建游戏的复杂度。通过使用 player gameobject 来 routing 所有来自 incoming commands，你可以确保这些消息来自正确的地方，正确的客户端，并且可以在一个集中的地方处理。
