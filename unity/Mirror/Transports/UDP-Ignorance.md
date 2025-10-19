# UDP Ignorance

Ignorance 是一个可靠 UDP transport layer，它通过一个 custom fork of ENet-CSharp 利用 native ENET C 网络库，为 64位 desktop 操作系统（Windows，Mac，Linux）和 Mobile OSes（iOS 和 Android）提供一个可靠和不可靠的 sequenced UDP transport。它还支持最多 255 个 channels 和 4096 个 clients 同时连接。

ENET 是一个坚实可靠的 UDP C++ 网络库，成熟而稳定。Unity LLAPI 需要一个替换（替换 Unity LLAPI）。Ignorance 设计时考虑了这个目标，填充了 gap，为 Mirror 并提供了一个高性能的 RUDP（可靠 UDP） transport。

## 为什么使用 Ignorance 替换 Unity LLAPI？

Unity 原有的 LLAPI 是恐怖低效的，大量测试已经显示在项目中使用 Unity LLAPI 将会损失大量性能。

## 为什么使用可靠 UDP 而不是 TCP

- 如果你需要快速可靠的实时通信（VoIP）
- 如果你需要 channels
- 如果你需要自定义 channel send types
- 如果你需要一个 data hose（软管）

## 为什么不想使用可靠 UDP，而使用 TCP？

- 如果你具有 mission critical 相关的东西（例如，data 必须从 A 发送到 B，没有异常）
- 如果你需要完全可靠的 network protocol
- 如果你是一个偏执狂
- 如果你正在制作一个 Minecraft-like 游戏，需要保持每个人都同步

## Sequencing 和 Reliable Delivery

Sequencing 基本上 tags packet 使它们知道在 dispatch 时的 number。这样如果你发送 packets 100，101，102 到 remote destination，另一端将会以那个顺序重构 pakcets ，而不是不同的顺序（比如 101，100，102）。如果一个 packet 丢失，它将会被跳过，但是网络库将会注意它丢失了并进行重发补偿。

Ignorance 包含两个 channels，Reliable 和 Unreliable mode。

## Misc

Ignorance 不支持 Websockets

从 GitHub 参考拉取最新 build。简单 import Unity Package 即可。
