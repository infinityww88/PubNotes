## Client-Server 架构

client-server 模型是多人游戏最常用的机制。这个模型中：

- Server：游戏的权威实例。它管理游戏的逻辑，同步游戏的 state，验证 player 的动作，处理 client 直接的通信
- Client：游戏的 player 实例。它发送输入到 server，并接收游戏状态的更新

有两种主要的 server 类型：

- Dedicated Server

  server 作为它自己的进程运行，和任何 player 分离开来。它更安全，并可缩放，通常用于竞技或大规模玩家的游戏。

  所有 clients 都连接服务器，并且通过服务器彼此通信。

- Host（Listen Server）

  Server 和 Local Client 在同一个进程运行。游戏实例即作为 server，也作为一个 player。这通常用于小型游戏，或者开发环境。

## Peer-to-Peer(P2P)

在 P2P 网络模型中，每个 player（或 peer）与其他 player（peer）直接相连，而不需要中心服务器。这可以减少延迟和服务器开销，但是会带来以下挑战：

- 低安全性和更容易作弊
- 很难可靠地同步游戏状态
- NAT 穿透问题

因为这些缺陷，P2P 很少在现代实时多人游戏中使用，尤其是竞技性游戏。Fishnet 不使用 P2P，因为它围绕着 client-server 模型来设计，来追求可靠性和安全性。

## Relay Servers

有时因为 NAT 问题或防火墙限制，clients 不能直接连接 server。Relay server 可以作为中间人，在 server 和 client 之间转发流量。

Relay Servers:

- 当直连失败时，允许连接
- 引入额外的延迟
- 可以用作 fallback，或用于 web-based games

## Host Migration

当使用 listen server 时，host 离开 game would 会导致所有 players 离开游戏；Host migration 是一个功能，当当前 host 断开连接或出现网络问题时，可以维护 game sessions。它允许从剩余连接的 players 中选择一个新的 host，最小化中断并确保 game session 可以无缝继续。

Fish-Networking 还没有内置的 host migration，但是它是一个可能在未来添加的功能。
