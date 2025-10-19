# Components Overview

这些是 Mirror 包含的核心组件：

- Network Animator

  Network Animator 同步 networked objects 的 animation states。它同步一个 Animator Controller 的状态和参数。

- Network Authenticator

  Network Authenticators 设施集成 user accounts 和 credentials 到你的应用程序中。

- Network Discovery

  Network Discovery 使用一个 UDP broadcast 在 LAN 上允许 clients 查找运行的 running server 并连接它

- Network Identity

  Network Identity 组件是 Mirror networking high-level API 的核心。它控制一个 GameObject 在网络上的唯一身份，它使用这个 Identity 使 networking 系统知晓这个 GameObject。它提供了两个不同的配置选项，而且它们是互斥的，这意味着它们中只有一个可以选中或都不选中

- Network Headless Logger

  Network Headless Logger 在 headless 模式时为 log 添加颜色

- Network Log Settings

  Network Log Settings 组件允许你配置 logging level，并加载一个 build 中的设置

- Network Manager HUD

  Network Manager HUD 是一个快速开始工具来帮助你立刻开始构建你的 multiplayer game，而不需要先为 game creation/connection/joining 构建一个 user interface。它允许你直接跳到 gameplay 编程，并且意味着你可以在你的开发计划中逐渐构建这些控件的自己的版本

- Network Match Checker

  基于 match id 控制 networked objects 的可见性

- Network Ping Display

  使用 OnGUI 显式 clients 的 Ping time

- Network Proximity Checker

  基于到 players 的邻近距离控制 network clients 的 gameobjects 的可见性

- Network Rigidbody

  在网络上同步一个 rigidbody 的 velocity 和其他属性

- Network Room Manager

  Network Manager 的扩展组件，提供基本的 room 功能

- Network Room Player

  需要附加在用于具有 Network Room Manager 的 Room Scene 的 Player prefabs 上

- Network Scene Checker

  在两个 scenes 之间控制 networked objects 的可见性

- Network Start Position

  当创建 player objects 时 Network Manager 使用。Network Start Position 的 position 和 rotation 被用于放置新创建的 player objecs

- Network Transform

  在网络上同步 gameobjects movement 和 rotation。注意 Network Transform 组件只同步 spawned networked gameobjects

- Network Transform Child

  同步具有 Network Transform 组件的 gameobject 的 child gameobject 的 position 和 rotation


  