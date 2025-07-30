Transport 控制数据如何在网络上发送，接收，和处理（加密-解密）。

Transport 是 low-level layer，负责在网络上发送、接收原始数据。它抽象掉 TCP/UDP sockets 的细节，处理数据包投递、可靠性、顺序性等等。

FishNet在内部通过事件机制接入传输层消息。虽然开发者通常无需直接访问这些底层消息，但FishNet仍为有需要的开发场景提供了相关接口。

有很多 transports 可用，一些被 Fish-Networking team 维护，其他被社区维护。

- Tugboat (LiteNetLib)
- Bayou (WebGL)
- Yak (For offline gameplay)
- Multipass (Multi-transport support)
- FishySteamworks (Steamworks.NET)
- FishyFacepunch (Facepunch for Steam)
- FishyEOS (Epic Online Services)
- FishyUnityTransport (Unity Transport)
- FishyRealtime (Photon Realtime)
- FishyWebRTC (WebRTC)
- CanoeWebRTC (WebRTC)
