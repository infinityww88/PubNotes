# Actions and Communication

当你制作一个 multiplayer game，除了同步 networked gameobjects 的属性，你还可能需要发送，接收，响应其他信息片段。例如当匹配开始时，当一个 player 加入或离开 match 时，或特定于你游戏类型的其他信息，例如占旗风格游戏中，对所有 players 的一个通知，一个旗帜被占领了。

在 Mirror networking High-Level API 中，有 3 种方法来传达这种类型的信息。

## Remote Actions

Remote actions 允许你在网络上调用你脚本中的一个函数。你可以在所有 clients 上或特定某个的 client 上发起这个 server 方法调用。你还可以在 server 上发起 clients 方法调用。使用 remote actions，你可以传递数据作为参数到方法中，就像你调用一个本地方法一样，但实际上 Mirror 生成并发送一个消息到 server 上，在 server 上调用这个函数，作为参数的数据也被传递到 server 上的方法调用。

## Networking Callbacks

Networking callbacks 允许你 hook Mirror 内置事件（类似 OnCollisionEnter，OnTriggerEnter），它们在游戏过程中发生，例如当 player 加入或离开时，当 gameobjects 被创建或销毁时，或者当一个 Scene 加载时。

## Network Messages

Network Messages 是一种发送消息的 lower level 方法（尽管它们被归类为 networking "High Level API"）。它们允许你在 client 和 server 之间使用脚本直接发送消息。你可以发送基本数据类型（int，string，等待），以及绝大部分常见的 Unity types（例如 Vector3）。既然你自己实现它们，这些消息不与任何特定的 gameobjects 和 Unity Events 关联，由你来直接定义它们的目的和实现它们。

