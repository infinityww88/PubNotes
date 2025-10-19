# Network Discovery

假设你坐在一个朋友的旁边。他以 host mode 开始一个游戏，而你想加入它。你的手机如何定位他的呢？

Network Discovery 可以解决这个问题。当你的游戏开始时，它在你当前 network 发送一个消息询问 “是否有任何 server 可用？”。同一个网络上的 任何 server 将会响应并提供如何连接它的信息。

Mirror 带有一个简单的 Network Discovery 的实现，你可以在你的游戏中使用。它还为你提供一个方法来扩展它，使得你可以在 discovery phase 传递额外数据。

NetworkDiscovery 和 NetworkDiscoveryHUD 组件被包含，或者你可以从 ScriptTemplate 创建自己的。

NetworkDiscovery 在 LAN 上使用一个 UDP 广播，允许 clients 来发现运行的 server 并连接它。

当 server 启动时，它监听 UDP Broadcast Listen Port 上来自 clients 的 requests，并放回一个 connection URI，clients 可以将其应用到它们的 transport。

你可以调整 clients 发送它们请求的频率，Active Discovery Interval（seconds）。

Server Found event 必须被赋予一个 handler method，例如 NetworkDiscoveryHUD 的 OnDiscoveredServer 方法。

在 NetworkDiscoveryHUD 中，NetworkDiscovery 组件应该被赋值。

## Quick Start

1. 创建一个具有 NetworkManager 的 gameobject
2. 不要添加 NetworkManagerHUD。Discovery有一个不同的 UI 组件
3. 添加一个 NetworkDiscoveryHUD 组件到 NetworkManager gameobject 上

   一个 NetworkDiscovery 组件将会自动被添加并 wired up 到你的 HUD

4. 添加一个 player 到 NetworkManager
5. Build 并运行一个 standalone version
6. 点击 Start Host
7. 在 editor 中开始 play mode，并点击 Find Servers
8. 然后 Editor 将会发现 standalone version，并显示一个 button
9. 点击 button 来连接它

NetworkDiscoveryHUD 提供用来作为简单快速的方式开始，但是你可能想要替换它为自己的 interface。

## Custom Network Discovery

你可以通过添加你自己的 interface 完全替换 user interface，而不是使用 NetworkDiscoveryHUD 默认的。你仍然需要 NetworkDiscovery 组件来做重量的事情。

有时你想在 discovery messages 中提供更多的信息。一些用例包括：

- client 可以显式 server 是否是 PvP 或 PvE 模式
- client 可以显示 server 有多拥挤
- client 可以显示对每一个 server 的 ping，使得 player 可以选择最快的 server
- client 可以显示语言
- client 可以显示 server 是否被密码保护

为此，在 Assets menu，点击 Create > Mirror > Network Discovery。这将创建一个 script，它具有两个 empty message classes，以及一个自定义 NetworkDiscovery 类，继承自 NetworkDiscoveryBase。

Message classes 定义在 client 和 server 之间发送什么。只要你保持你的 message 简单地只使用 Mirror 可以序列化的数据类型，你将不需要为它们编写自定义 serializers。

```C#
public class DiscoveryRequest : MessageBase
{
    public string language="en";

    // Add properties for whatever information you want sent by clients
    // in their broadcast messages that servers will consume.
}

public class DiscoveryResponse : MessageBase
{
    enum GameMode {PvP, PvE};

    // you probably want uri so clients know how to connect to the server
    public Uri uri;

    public GameMode GameMode;
    public int TotalPlayers;
    public int HostPlayerName;

    // Add properties for whatever information you want the server to return to
    // clients for them to display or consume for establishing a connection.
}
```

自定义 NetworkDiscovery 类包含 overrides 方法来处理上面的消息。

你可以参考 NetworkDiscovery 脚本来查看它们是如何实现的。

```C#
public class NewNetworkDiscovery: NetworkDiscoveryBase<DiscoveryRequest, DiscoveryResponse> 
{
    #region Server

    protected override void ProcessClientRequest(DiscoveryRequest request, IPEndPoint endpoint)
    {
        base.ProcessClientRequest(request, endpoint);
    }

    protected override DiscoveryResponse ProcessRequest(DiscoveryRequest request, IPEndPoint endpoint) 
    {
        // TODO: Create your response and return it   
        return new DiscoveryResponse();
    }

    #endregion

    #region Client

    protected override DiscoveryRequest GetRequest()
    {
        return new DiscoveryRequest();
    }

    protected override void ProcessResponse(DiscoveryResponse response, IPEndPoint endpoint)
    {
        // TODO: a server replied,  do something with the response such as invoking a unityevent
    }

    #endregion
}
```
