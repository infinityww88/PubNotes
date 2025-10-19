# Network Manager HUD
Network Manager HUD (heads-up display) 是一个快速开始的工具，帮助你立即开始构建 multiplayer game，不需要先构建 user interface 用于 creation/connection/joining。它允许你直接开始 game play 编程，并意味着你之后在可以在开发计划中构建自己的 version。

然后它不是用于最终的游戏。这里的想法是这些控件用于让你快速开始，但是你应该之后创建自己的 UI，允许你的 players 以符合你的游戏的方式来发现和加入游戏。例如，你可能想要风格化 screen，buttons，可用游戏的列表的设计来匹配你整个游戏的风格。

要使用 Network Manager HUD，或者添加组件到具有 Network Manager 组件的 scene object，或者在你的 scene 创建一个 empty gameobject（menu：game object > Create Empty），并且 Network Manager HUD 组件到新的 gameobject。

![NetworkManagerHUDComponent](../../Image/NetworkManagerHUDComponent.png)

- Show GUI

  勾选这个 checkbox 在运行时显式 HUD GUI。这允许你显式或隐藏它来快速 debuging

- Offset X

  设置 HUD GUI 的水平 pixel offset，从 screen 的左边缘测量

- Offset Y

  设置 HUD GUI 的垂直 pixel offset，从 screen 的上边缘测量

NetworkManager HUD 提供基本的功能使得玩你的游戏的人们可以开始 hosting 一个 networked game，或者发现和加入一个现有 networked game。Unity 显式 Network Manager HUD 为 Game View 中一个 简单 UI 按钮的列表（IMGUI）。

![NetworkManagerHUDUI](../../Image/NetworkManagerHUDUI.png)

## Using the HUD

Network Manager HUD 开始以 Server + Client mode，并显示有关 hosting 和加入 multiplayer 游戏的按钮。

### Host（Server + Client）

点击 Host（Server + Client）按钮在 local network 上以 host 开始一个游戏。这个 client 在游戏中同时是 host 和 一个 player。它使用 inspector 中的 Network Info section 的信息来 host 游戏。

当点击在这个 button，HUD 切换到 network details 的简单显式，并且一个 Stop button 允许你停止 hosting game，并返回到 main HUD menu。

![NetworkManagerHUDHostingLAN](../../Image/NetworkManagerHUDHostingLAN.png)

当你以 host 开始一个游戏时，然后游戏的其他 players 可以连接这个 host 来加入游戏。

点击 Stop 按钮断开 host 连接，并返回 main HUD 菜单。

### Client

要在 internet 上连接 host 使用 Client 按钮右边的 text field 来指定 host 的地址。默认地址是 localhost，这意味着 client 在它自己的电脑上查找 game host。除了 localhost，你可以指定 IPv4 地址，和 IPv6 地址，或者一个 fully-qualified domain name（FQDN），例如 game.example.com。点击 Client 来尝试连接你指定的 host address。

使用这个字段的默认 localhost，你可以在一个计算机上允许游戏的多个 instances，交互地测试 multiplayer。为此，你可以创建一个你的游戏 standalone build，然后在你的计算机上 launch 多次。这是一个常用的方式来快速测试你的 networked game 像你的期望的那样工作，而不需要你在多个计算机或设备上部署你的游戏。

![NetworkGame3Instances](../../Image/NetworkGame3Instances.jpg)

当你想要在多个机器上测试你的游戏，你需要将作为 host 的计算机的地址放在 address text field。

作为 host 的计算机需要向每个运行 clients 告诉它的 address，因此你可以在输入框中输入这个地址。对于一个 LAN 上的 local clients，这是 local IP 地址。对于 remote clients，这是 host 的路由的 WAN IP 地址。对于作为 host 的 计算机，Firewall 规则和端口转发通常是必须的，以接受其他计算机的连接，无论它们是在 LAN 或 internet。

点击 IP 地址，点击 Client 来尝试连接 host。

### Server Only

点击 Server Onlyh 来开始一个作为 server 的游戏实例，其他 clients 可以连接它，但是它自己不作为游戏的 client。这种游戏类型通常称为 dedicated server。Player 不能在这个游戏的特殊实例上 play 游戏。所有 players 必须作为 clients 连接。

一个 dedicated server 对于所有连接的 players 可以得到更好的性能，因为 server 不需要在作为 server 运行的同时还处理一个 local player game play。

你还可以为在 internet 上 play 的游戏选择这个选项（而不是在一个 local network），但是想要维护 server 自身的控制。例如，要防止一个 client 的作弊，因为只有 server 具有对游戏的 authority。为此，你需要以 Server Only mode 在一个 public IP 地址运行游戏。
