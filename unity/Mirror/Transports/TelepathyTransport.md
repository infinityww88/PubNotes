# Telepathy Transport

简单，基于消息，MMO 规模的 C# TCP 网络库（不是专门针对 Unity 设计的）。No magic。

- Telepathy 以 KISS 原则设计
- 快速，极其可靠，为 MMO 规模网络设计
- 使用 framing，任何发送的东西都可以以相同的方式接收
- 原始的 C#，可直接被用于 Unity3D
- GitHub available

## 特殊的地方

原本为 uMMORPG 设计，在经历了 3 年的 UDP hell。

我们需要一个 library，其：

- 稳定和 Bug free：Telepathy 只使用 400 行代码。没有魔法。
- 高性能：可以处理成千上万个连接和 packages。
- 并行：每个 connection 使用一个线程。可以重度使用多核处理器。
- 简单：考虑了所有事情，你所做的一起只是调用 Connect/GetNextMessage/Disconect。
- Message based：如果发送 10 个字节，然后发送 2 个字节，则另一端先接收 10 个字节，然后接收 2 个字节，绝不会以下接收 12 个字节。

MMORPGs 极其难于制作，创建了 Telepathy 使得再也不用担心 low level Networking 了。

## What about ...

- Async Sockets：在我们的基准测试中并没有表现的更好。
- ConcurrentQuene：.NET 3.5 兼容性对 Unity 非常重要。不在比我们的 SafeQueue 快。
- UDP vs TCP：Minecraft 和 World of WarCraft 是两个最大的 multiplayer 游戏，它们都使用 TCP 网络，这是有原因的。
