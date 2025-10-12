广播功能允许你向一个或多个对象发送消息，而无需这些对象具备NetworkObject组件。这在需要实现非联网对象间通信的场景中尤为实用，比如聊天系统。

与远程过程调用(RPC)类似，广播既可可靠传输也可非可靠传输。通过广播发送的数据既可以从客户端传送到服务器，也可以从服务器广播至一个或多个客户端。系统同样会为广播自动生成序列化器。

广播必须定义为结构体，并实现IBroadcast接口。以下示例展示了聊天广播可能包含的数据字段。

```C#
public struct ChatBroadcast : IBroadcast
{
    public string Username;
    public string Message;
    public Color FontColor;
}
```

由于广播消息不与任何特定对象绑定，因此必须通过ServerManager或ClientManager进行发送。当需要向服务器发送广播时，请使用ClientManager；而当需要向客户端发送广播时，则应使用ServerManager。

以下示例通过 InstanceFinder 获取 ClientManager 和 ServerManager 的引用，但你也可以自行存储引用，或使用 NetworkManager 提供的公共引用，以及 NetworkBehaviour 中的引用。

下面是一个示例，从 client 向 server 发送一个 chat message。

```C#
public void OnKeyDown_Enter(string text)
{
    // Client won't send their username, server will already know it.
    ChatBroadcast msg = new ChatBroadcast()
    {
        Message = text,
        FontColor = Color.white
    };
    
    InstanceFinder.ClientManager.Broadcast(msg);
}
```

服务器向客户端发送广播的方式与客户端向服务器发送非常相似，但你会拥有更多可选参数。如需查看完整的选项列表，建议查阅API文档。以下示例演示如何向所有能观察到特定客户端的玩家广播消息——这模拟了clientA向服务器发送聊天信息，再由服务器转发给所有能看到clientA的其他客户端的场景。需要注意的是，在这个示例中clientA自身也会收到这条广播。

```C#
// When receiving broadcast on the server which connection
// sent the broadcast will always be available.
public void OnChatBroadcast(NetworkConnection conn, ChatBroadcast msg, Channel channel)
{
    // For the sake of simplicity we are using observers
    // on conn's first object.
    NetworkObject nob = conn.FirstObject;
    
    // The FirstObject can be null if the client
    // does not have any objects spawned.
    if (nob == null)
        return;
        
    // Populate the username field in the received msg.
    // Let us assume GetClientUsername actually does something.
    msg.Username = GetClientUsername(conn);
        
    // If you were to view the available Broadcast methods
    // you will find we are using the one with this signature...
    // NetworkObject nob, T message, bool requireAuthenticated = true, Channel channel = Channel.Reliable)
    //
    // This will send the message to all Observers on nob,
    // and require those observers to be authenticated with the server.
    InstanceFinder.ServerManager.Broadcast(nob, msg, true);
}
```

由于广播消息不会自动被发送方对象接收，你必须明确指定哪些脚本或对象可以接收广播。如前所述，这一特性不仅支持在非联网对象上接收广播，还能让同一条广播同时被多个对象接收。

虽然我们的示例仅使用了一个对象，但该特性非常适合需要批量修改游戏状态的场景——例如无需将每个灯光对象设为联网对象，就能统一控制它们的开关状态。

监听广播的方式类似于使用事件机制。以下示例展示了客户端如何接收来自服务器的广播数据。

```C#
private void OnEnable()
{
    // Begins listening for any ChatBroadcast from the server.
    // When one is received the OnChatBroadcast method will be
    // called with the broadcast data.
    InstanceFinder.ClientManager.RegisterBroadcast<ChatBroadcast>(OnChatBroadcast);
}

// When receiving on clients broadcast callbacks will only have
// the message. In a future release they will also include the
// channel they came in on.
private void OnChatBroadcast(ChatBroadcast msg, Channel channel)
{
    // Pretend to print to a chat window.
    Chat.Print(msg.Username, msg.Message, msg.FontColor);
}

private void OnDisable()
{
    // Like with events it is VERY important to unregister broadcasts
    // When the object is being destroyed(in this case disabled), or when
    // you no longer wish to receive the broadcasts on that object.
    InstanceFinder.ClientManager.UnregisterBroadcast<ChatBroadcast>(OnChatBroadcast);
}
```

需要提醒的是，上文已演示了服务器端的接收方法，其方法签名如下所示。

```C#
public void OnChatBroadcast(NetworkConnection conn, ChatBroadcast msg)
```

基于以上内容，接下来我们来看服务器如何监听来自客户端的广播。

```C#
private void OnEnable()
{
    // Registering for the server is exactly the same as for clients.
    // Note there is an optional parameter not shown, requireAuthentication.
    // The value of requireAuthentication is default to true.
    // Should a client send this broadcast without being authenticated
    // the server would kick them.
    InstanceFinder.ServerManager.RegisterBroadcast<ChatBroadcast>(OnChatBroadcast);
}

private void OnDisable()
{
    // There are no differences in unregistering.
    InstanceFinder.ServerManager.UnregisterBroadcast<ChatBroadcast>(OnChatBroadcast);
}
```

若想查看广播功能的具体应用示例，可打开Demos/Authenticator/Scripts文件夹中的PasswordAuthenticator.cs文件进行参考。
