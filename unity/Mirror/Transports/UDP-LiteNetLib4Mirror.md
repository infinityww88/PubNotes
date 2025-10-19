# LiteNetLib4Mirror Transport

用于 Mirror 的基于 LiteNetLib transport

## Usage

1. 下载 unity package，并 import 它到项目中
2. 将 LiteNetLib4MirrorTransport 组件放在 NetworkManager gameobjet 上并赋予到相应的字段上
3. （可选地）使你的 NetworkManager 继承 LiteNetLib4MirrorNetworkManager，并使用它的可选的 overloads

## Features

- UDP
- 内置的 Network Discovery and UPnP
- Fully managed code
- Small CPU and RAM usage
- Small packet size overhead（1个字节用于 unreliable，3个字节用于 reliable packets）
- 不同的发送机制
- Reliable with order
- Reliable without order
- Ordered but unreliable with duplication prevention
- Simple UDP packets without order and reliability
- Automatic small packets merging
- Automatic fragmentation of reliable packets
- Automatic MTU detection
- NTP time request
- Packet loss and latency simulation
- IPv6 support（dual mode）
- Connection statisitcs（需要 DEBUG 或 STATS_ENABLED flag）
- Multicasting（用于在 local network 发现 host）

## IL2CPP Warning！

使用 IL2CPP，IPv6 只支持 Unity 2018.3.6f1 和之后的版本。还有，socket Reuse Address 选项在 IL2CPP 不可用。

![LiteNetLibTransport](../../Image/LiteNetLibTransport.png)
