# Overview

## 简介

Mirror 是 deprecated Unity Networking API 最兼容的直接替换。

Mirror 几乎拥有来自 UNet 的全部组件和功能，使得联网更加容易，简洁，可维护。

Mirror 可以支持任何规模的游戏，从 LAN party games，到运行成百上千个 players 的 dedicated high-volume authoritative servers。

支持多个 Transports

- TCP（Telepathy，Apathy，Booster）
- UDP（ENet，LiteNetLib）
- WebGL（Secure Web Sockets）
- Steam（Steamwork.Net）
- Multiplexer
- Fallback

核心功能和组件

- Transports 是可互换的组件
- Additive Scene 处理
- Single 和 separated Unity 项目支持
- Network Authenticators 管理对游戏的访问
- Network Discovery 轻而易举地连接 LAN players 到一个 LAN server 或 host
- Network Manager 和 HUD
- Network Room Manager 和 Room Player
- Network Identity
- Network Transform 来带插值地同步 position，rotation，和 scale
- Network Animator 最多支持 64 个参数
- Network Proximity Checker 帮助 Area of interest（关注区域，战争迷雾？）
- Network Scene Checker 将 players 和 networked objects 于 Additive scene 实例隔离
- Network Match Checker 通过 Network Visibility 隔离 players 和 networked objects
- SyncVar，Sync List，SyncDictionary，和 SyncHashSet

集成

- Smooth Sync
- Steamworks Networking
- Master Audio Multiplayer

Mirror Multiplayer High Level API（HLAPI）是一个系统，用来构建 Unity Multiplayer Games。

它构建在 lower level transport real-time communication layer，并且处理多人游戏中很多常见任务。

虽然 Transport layer 支持任何种类的 network 拓扑，但 HLAPI 是一个 server authoritative system，尽管它允许一个参与者同时是 client 和 server，因此可以不需要专用的 server。可以和 internet services 一起工作，允许在 internet 上进行多人游戏，而几乎不需要开发者任何工作。

HLAPI 关注于简易使用和迭代开发，并为多人游戏提供有用的功能，例如：

- 消息处理
- 通用目的高性能序列化
- 分布式对象管理
- 状态同步
- Network classes：Server，Client，Connection

![NetworkLayers](../Image/NetworkLayers.jpg)

## Server 和 Host

在 Mirror High Level API（HLAPI）系统，multiplayer games 包括：
- Server
  Server 是一个 Game 实例，所有其他 players 连接到它。Server 管理游戏的各个方面，例如保存分数，向客户端传输数据。
- Clients
  Clients 是从不同的计算机连接到 server 的游戏实例。Clients 可以在局域网连接，或者 online

一个 server 可以是一个 dedicated server 或者 一个 host server。

- Dedicated server
  这是一个游戏实例，只用作 server
- Host server
  当没有 dedicated server 时，一个 client 可以扮演 server 的角色。这个 client 就是 host server。Host server 创建一个游戏实例，同时作为 server 和 client。这意味着 host server 本身是一个 local client。

![NetworkHost](../Image/NetworkHost.png)

Host 使用一个特殊 internal client 用于 local client 通信，对其他 clients 使用 remote clients。

Local client 和 Host 使用直接函数调用和 message queues 进行通信，因为它们在同一个进程。

无论是 Local Client 还是 Remote Client，Mirror HLAPI 自动为你处理一切。

Multiplayer 系统的一个目标是 local clients 和 remote clients 的 code 是相同的，使得你在开发时只需要考虑一种 client 就可以。绝大多数情况下，Mirror 自动处理这些区别。

## Instantiate 和 Spawn

当制作一个 single player game，通常使用 GameObject.Instantiate 方法来在运行时创建新的 gameobjects。但是在 multiplayer system，必须由 server 生成 gameobject 以使它们在网络中激活。当 server 生成新的 gameobjects，它在 connected clients 上触发 gameobjects 的创建。Spawning System 管理这些 gameobjects 的生命周期，并且基于你如何设置 gameobject 来同步 gameobject 的状态。

## Players 和 Local Players

Mirror multiplayer HLAPI system 对 player gameobject 的处理和 non-player gameobject（环境物体，NPC） 的处理不同。当一个 player 加入游戏时（一个新的 client 连接到 server），player 的 gameobject 在它的 client 上变成一个 local player gameobject，Mirror 将 player 的 connection 和 player gameobject 关联在一起。

Mirror 为每个参与游戏的 player 关联一个 gameobject，并且路由 networking commands 到这个 gameobject。一个 Player 不能在 player gameobject 上调用命令，只能用它们自己的。

## Authority

Servers 和 clients 都可以管理一个 game object 的行为。Authority 的概念指的是 game object 如何以及在哪里被管理。Mirror HLAPI 是基于 server authority，Server 对所有 game objects 上具有 authority。Player game objects 是一个特殊情景，被认为具有 local authority。你可以使用一个不同的 authority 系统构建你的游戏，见 Network Authority。

