# Network Identity

Network Identity 是 Unity networking high-level API。它控制一个 gameobject 在网络上的唯一的身份 identity，并且它使用那个 identity 使得 networking system 知晓这个 gameobject。它提供两个不同的互斥的配置选项，只能选择其中一个或者都不选：

- Server Only

  选择这个选项使得 Unity 只在 server 上生成这个 gameobject，而不是 clients

  ![NetworkIdentity](../../Image/NetworkIdentity.png)

## Instantiate Network Game Objects

使用 Mirror server-authoritative networking system，server 必须生成具有 NetworkIdentity 的 networked gameobjects，使用 NetworkServer.Spawn。这个自动在连接到 server 的 clients 上创建它们，并为它们赋予一个 netId。

你必须将一个 Network Identity 组件放在任何在运行时生成的 Prefabs，使得 network 系统可以使用它们。

## Scene-based Network Game Objects

你还可以使用保存为 Scene 一部分的 networked gameobjects（例如 environmental props）。Networking gameobjects 使它们的行为略有不同，因为你需要在 network 上生成它们。

当构建你的游戏的时候，Unity disables 所有带有 NetworkIdentity 组件的 Scene-based gameobjects。当一个 client 连接到 server 时，server 发送 spawn 消息来告诉 client 哪些 scene gameobjects 要被 enable，以及它们的最新状态是什么。这确保 client 的 game 在开始 playing 时，不包含位于错误位置上的 game objects，或者 Unity 不生成并且立即销毁 gameobjects（例如，如果在那个 client 连接之前一个事件移除了 gameobject）

## Preview Pane Information

这个组件包含 network 追踪信息，并在 preview pane 上显式信息。例如，已经被赋予 object 的 scene ID，network ID，和 asset ID。这允许你检查可以用于调查和 debugging 的信息。

![NetworkIdentityPreviewRuntime](../../Image/NetworkIdentityPreviewRuntime.png)

