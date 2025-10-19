# Concept

## High level scripting API

Mirror networking 有一个 high-level script API，HLAPI。

这意味着你只需要使用 commands，commands 则处理绝大多数 multiplayer games 常见的需求，而不需关心 lower-level 实现细节。

HLAPI 允许你

- 使用一个 Network Manager 控制 game 的 networked state
- Operate “client hosted” games，即 host 也是一个 player client
- 使用一个通用目的序列化器序列化数据
- 发送和接受网络数据
- 从 clients 发送网络命令到 servers
- 从 servers 发起 remote procedure calls（RPCs）到 clients
- 从 servers 发送网络事件到 clients

## Engine 和 Editor integration

Mirror networking 被集成到 engine 和 editor，允许你操作 components 以及可视化辅助来构建你的 multiplayer game，它提供：

- 用于 networked objects 的 NetworkIdentity 组件
- 用于 networked scripts 的 NetworkBehaviour
- 可配置的 object transforms 的自动同步
- 脚本变量的自动同步
- 支持在 Unity scenes 中放置 networked object
- Network components
