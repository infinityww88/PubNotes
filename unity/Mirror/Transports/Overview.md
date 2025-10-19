# Overview

Mirror 是一个 high level Networking Library，它使用一些不同的 low level transports。

要使用一个 transport，简单地将它作为组件添加到 NetworkManager GameObject 上，并拖放到 NetworkManager 的 Transport field。

- TCP - Telepahty：简单，基于消息，MMO 规模 TCP 网络 in C#。No magic。
- TCP - APahty：快速，轻量，allocation-free low level TCP 库，for Unity。以 native C 开发，用于最大 MMO 规模网络性能。
- TCP - Booster：Mirror Booster 大量提升 multiplayer game 性能，通过将 Networking load 移出 Unity。
- WebGL - WebSockets：用于 WebGL 客户端。
- Multiplexer：桥接 bridging transport，允许一个 server 同时处理不同 transports 上的 clients，例如使用 Telepathy 的 desktop clients 和使用 Websockets 的 WebGL clients。
- Fallback：兼容的 transport，用于不能在所有 platforms 上运行，需要 fallback 选项来覆盖所有其他 platforms 的 transports
- UDP - Ignorance：基于 ENet 实现一个可靠和不可靠的 sequenced UDP transport。
- UDP - LiteNetLib4Mirror：LiteNetLib4Mirror 基于 LiteNetLib 和 NetworkDiscovery，uPnP 实现一个 UDP transport。
- Steam - FizzySteamworks：利用 Steam P2P 网络的 Transport，构建在 Steamworks.NET 之上。
- Steam - FizzyFacepunch：利用 Steam P2P 网络的 Transport，构建在 Facepunch.Steamworks 之上。
