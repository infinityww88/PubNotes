远程过程调用（RPC）是一种通信方式，接收方是和发送方相同的 object，只是分布在不同的机器上。RPC主要分为以下3类：

RPC使用简单，类似本地方法调用，但需注意：

1. 必须在继承自NetworkBehaviour的脚本中调用。
2. Fish-Net框架会自动为类型生成序列化器（支持数组、列表），若无法生成则需手动实现自定义序列化器。

RPC 不需要示例中的那样带有 Rpc 前缀，但是加上它是很好的实践。

## ServerRpc

ServerRpc 允许 client 在 server 上执行逻辑。Client 调用一个 ServerRpc 方法，方法执行的参数 data 发送到 server。要使用一个 ServerRpc，client 必须 active，方法必须有 ServerRpc 属性。

```C#
private void Update()
{
    //If owner and space bar is pressed.
    if (base.IsOwner && Input.GetKeyDown(KeyCode.Space))
        RpcSendChat("Hello world, from owner!");        
}

[ServerRpc]
private void RpcSendChat(string msg)
{
    Debug.Log($"Received {msg} on the server.");
}
```

默认情况下，只有对象的所有者（Owner）才能调用ServerRpc方法。但通过设置ServerRpc特性的RequireOwnership属性为false，可以允许任何客户端（无论是否为所有者）调用该RPC。

若需识别调用来源，可在RPC方法参数列表末尾添加一个默认值为null的NetworkConnection类型参数。系统会自动填充当前发起调用的客户端连接信息，开发者无需手动传递连接参数。

```C#
[ServerRpc(RequireOwnership = false)]
private void RpcSendChat(string msg, NetworkConnection conn = null)
{
    Debug.Log($"Received {msg} on the server from connection {conn.ClientId}.");
}
```

## ObserverRpc

ObserversRpc允许服务器在客户端上运行逻辑，仅被观察的客户端会接收并执行该逻辑。

通过添加Network Observer组件可设置观察者，需在被调用的方法上添加ObserversRpc特性标记。

```C#
private void FixedUpdate()
{
    RpcSetNumber(Time.frameCount);
}

[ObserversRpc]
private void RpcSetNumber(int next)
{
    Debug.Log($"Received number {next} from the server.");
}
```

在某些情况下，您可能需要让对象的所有者忽略接收到的ObserversRpc调用。为实现这一需求，只需在ObserversRpc特性中将ExcludeOwner属性设置为true即可。

```C#
[ObserversRpc(ExcludeOwner = true)]
private void RpcSetNumber(int next)
{
    //This won't run on owner.
    Debug.Log($"Received number {next} from the server.");
}
```

还可以通过ObserversRpc自动将最新数值同步至新加入的客户端。该功能特别适用于仅通过RPC变更的数值类型。

实现方式：在ObserversRpc特性中将BufferLast属性设为true。

如下所示的示例代码既不会向所有者发送数据，又能确保新加入的客户端自动获取最新数值。

```C#
[ObserversRpc(ExcludeOwner = true, BufferLast = true)]
private void RpcSetNumber(int next)
{
    //This won't run on owner and will send to new clients.
    Debug.Log($"Received number {next} from the server.");
}
```

## TargetRpc

TargetRpc 是服务端发起，在指定客户端上运行逻辑，需通过添加\[TargetRpc\]特性实现。

调用时，方法的第一个参数必须为NetworkConnection类型，该参数指定数据发送的目标连接（即目标客户端的连接对象）

```C#
private void UpdateOwnersAmmo()
{
    /* Even though this example passes in owner, you can send to
    * any connection that is an observer. */
    RpcSetAmmo(base.Owner, 10);
}

[TargetRpc]
private void RpcSetAmmo(NetworkConnection conn, int newAmmo)
{
    //This might be something you only want the owner to be aware of.
    _myAmmo = newAmmo;
}
```

## Multi-Purpose Rpc

方法可同时标记为TargetRpc和ObserversRpc特性。

这种设计在需要灵活切换通信范围时非常实用——既可向特定客户端发送数据，也能广播至所有观察者客户端。

典型应用场景如聊天消息系统：既支持私聊（定向发送），也支持群聊（广播发送）。

```C#
[ObserversRpc][TargetRpc]
private void DisplayChat(NetworkConnection target, string sender, string message)
{
    Debug.Log($"{sender}: {message}."); //Display a message from sender.
}

[Server]
private void SendChatMessage()
{
    //Send to only the owner.
    DisplayChat(base.Owner, "Bob", "Hello world");
    //Send to everyone.
    DisplayChat(null, "Bob", "Hello world");
}
```

## Channels

远程过程调用（RPC）可设置为可靠或不可靠传输。

需在RPC方法中添加Channel类型参数​（作为最后一个参数），以实现该功能；还可通过该参数判断数据来自哪个通道。

```C#
private bool _reliable;
private void FixedUpdate()
{
    //Reliable or unreliable can be switched at runtime!
    _reliable = !_reliable;
    
    Channel channel = (_reliable) ? Channel.Reliable : Channel.Unreliable;

    //同一个RPC 调用每次不同调用都可以选择不同的 Channel
    RpcTest("Anything", channel);
}

/* This example uses ServerRpc, but any RPC will work.
* Although this example shows a default value for the channel,
* you do not need to include it. */
[ServerRpc]
private void RpcTest(string txt, Channel channel = Channel.Reliable)
{
    if (channel == Channel.Reliable)
        Debug.Log("Message received! I never doubted you.");
    else if (channel == Channel.Unreliable)
        Debug.Log($"Glad you got here, I wasn't sure you'd make it.");
}
```

若RPC是ServerRpc类型，且方法参数中已包含默认值为null的NetworkConnection参数，则Channel参数必须紧邻该连接参数之前添加（即倒数第二个参数位置）。

```C#
/* Example of using Channel with a ServerRpc that
* also provides the calling connection. */
[ServerRpc(RequireOwnership = false)]
private void RpcTest(string txt, Channel channel = Channel.Reliable, NetworkConnection sender = null)
{
    Debug.Log($"Received on channel {channel} from {sender.ClientId}.");
}
```

## RunLocally

所有类型的RPC均可使用RPC特性中的RunLocally字段。当该字段设置为true时，方法不仅会被发送到目标端执行，还会在调用方本地同步执行。例如：当客户端调用一个设置了RunLocally=true的ServerRpc时，该RPC会被放入客户端的发送缓冲区，同时客户端会立即在本地执行该方法逻辑。

```C#
//Keeping in mind all RPC types can use RunLocally.
[ServerRpc(RunLocally = true)]
private void RpcTest()
{
    //This debug will print on the server and the client calling the RPC.
    Debug.Log("Rpc Test!");
}
```

只有支持 unreliable messages 的 transports 可以以 unreliable 发送 Rpcs。如果 transports 不支持 unreliable 而试图以 unreliable 发送 rpc，rpc 默认会以 reliable 通道发送。

## DataLength

若需传输超大规模数据，可在RPC特性中声明数据的最大潜在容量。该操作将启用专用序列化器来避免内存重分配，从而提升性能表现。所有类型的RPC均支持此功能。

```C#
//This implies we know the data will never be larger than 3500 bytes.
//If the data is larger then a resize will occur resulting in garbage collection.
[ServerRpc(DataLength = 3500)]
private void ServerSendBytes(byte[] data) {}
```
