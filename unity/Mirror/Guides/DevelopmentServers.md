# Development Servers

这个指南将设置一个 dedicated server，并将 project 的 server build（server 版本构建）放在 dedicated server 上。

## Introduction

当你使用 Mirror 开发时，你将需要测试你的项目同时作为一个 client 和一个 server。

下面是一些测试你的项目的可能的方式：

- Default build：Host/Client 作为一个 build，并且连接另一个 build/editor，在一个计算机本地测试
- Server Build：Server 是一个单独的 executable。你可以将它放在你的计算机上并运行它，然后作为一个 client 连接它
- Dedicated Server：和 server build 相同，当时将 server executable 放在外部机器，你使用 server 的 IP 地址来连接它

这个指南关注 Dedicated Server 选项。有许多提供商提供虚拟计算服务，例如 Microsoft Azure，Amazon AWS 等等。所有可选项都执行相同的过程来确保客户端的连接性。

对 dedicated server 的一些需求：

- 端口转发 port forwarding（不严格必须，但是使所有事情都变得非常简单，而不需要 NAT 穿越
- Firewall 例外（允许端口）
- Computer/machine 保持在线，并且在任何时候保持可连接

## Amazon Web Services

### 使用 EC2 Management Console 设置一个 Windows instance

选择距离你最近的 region，进入 EC2 instance dashboard，准备 launch 你的 instance。

- 选择 Amazon Machine Image（AMI）

  Microsoft Windows Server 2019 Base

- 选择 Instance Type
- 配置 Instance
- 添加 Storage
- 添加 Tags
- 配置 Security Group

  这一步非常重要，它确保从外部连接 instance 的可能性。 

  创建一个新的 security group，给它一个名字和描述，添加一些规则：

  - RDP with source = Anywhere，描述可以是 Remote Desktop Program
  - 定制 TCP Rule，开放 7777 端口，source = Anywhere，描述可以是 Mirror
  - SSH with source = Anywhere，描述可以是 SSH

  SSH 不是必须的，但是可以使用其他方式用来远程连接 Instance，而不是使用 RDP。

- Review and Launch

  
还有一件事，Launch 之前会弹出一个窗口，请求 key pair。只需要创建一个新的就可以，通过选择 "Create a new key pair"，并给它一个名字，点击 "Download Key Pair"。

在一个安全的地方保存这个 key file (.PEM 文件)。没有这个 key 无法访问创建的 instance。

### 通过 RDP 配置 server（Remote Desktop）

使用 RDP 连接 instance 需要：

- 添加了 key pair 的 RDP 文件

  Get the password before clicking Download

  ![ConnectRDP](../../Image/ConnectRDP.png)

  复制 Password 为之后使用。然后点击 "Download Remote Desktop File"，下载 RDP 文件。

- 下载之后，配置 RDP 文件来允许从 C: 驱动或其他驱动器获得文件（这样你可以很容易地获得你的 zip project）

  找到刚下载的 RDP 文件，右键点击它选择 Edit。

  在 Local sources tab 中点击 more。在新的窗口中选择你的 C: 驱动或其他驱动，这是你自己用来连接的电脑，用来方便文件交互。

  现在可以运行 RDP 文件了。

- 启动 RDP 文件，输入 windows Admin password

  启动 RDP 文件后，将会请求一个 password。如果你忘记了密码，在 instance 上右键点击 "Get Windows Password" 获得。你将会被请求重新输入你的 key-pair (.PEM) 文件来解密消息。之后就可以复制 password 了。

  现在 Remote Desktop 将会显式你登录进入 dedicated server 了。

- 设置防火墙来允许连接进入

  在 windows firewall 设置中，找到 advanced firewall 设置，然后找到 inbound rules。

  添加一个新的 rule，并选择端口类型。选择 Tcp 并输入 7777 端口（或者任何其他你想要 Mirror 使用的端口，这个规则允许使用 Mirror 的 game client 连接 game server）。然后点击 next 并保持默认。

  ![WindowsFirewallException](../../Image/WindowsFirewallException.png)

### 测试连接

在你最终测试你的 server build 之前，需要将它放在 dedicated server。

将你的（zipped）server build 放在你添加的驱动器（C:）的更目录下，使它更容易被找到。

打开 My Computer，因为前面对 RDP 文件的修改，我们应该可以在 Devices and Drives 下面看见你的 local dirve。

![DriveOnTheDedicatedHost](../../Image/DriveOnTheDedicatedHost.png)

双击它，因为你将你的 zipped server build 放在那个驱动下，当加载完成时，你应该能立刻看见它。

现在 unzip 这个 project 到一个 dedicated server desktop 上的新的目录，并运行它。

如果想要在 Mirror Server 开启后，测试 7777 端口是否打开，在 EC2 Management Console 获得 Instance 的 public IPv4 地址。然后用你的 client 连接这个 IP 地址。
