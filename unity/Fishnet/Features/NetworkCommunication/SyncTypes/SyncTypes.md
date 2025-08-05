RPC 对比 method（cross network，云方法），SyncTypes 对比 field（cross network，云属性）。

与远程过程调用（RPC）类似，SyncType是另一种网络通信机制。这类字段会在**服务器端**数值变更时，自动同步至所有客户端。目前支持的SyncType包括：SyncVar、SyncDictionary、SyncList、自定义SyncType等多种类型。

其核心优势在于增量同步机制——当SyncType发生变更时，仅传输变化部分的数据。例如：当一个包含10个元素的SyncList新增元素时，系统只会同步最新添加的条目而非整个列表。

SyncVar的值会在对象的OnDestroy方法运行之前被重置，因此在该方法中无法获取到它们的值。

SyncTypes 还会为 custom types 自动生成序列化器。

在Awake阶段，对SyncType的修改会直接在服务器和客户端执行，无需额外同步操作。此阶段适合用于向列表或字典添加初始数据。若需在初始化后同步数据，建议使用OnStartServer方法

设置 SendRate 为 0f 会允许 SyncTypes 每个 network tick 发送 changes.

## Host Client Limitations

当在单一构建中同时运行客户端和服务器时，所有SyncTypes都存在一个小限制。

作为 host client 时，如果 asServer 参数为 false，callbacks 中，prev value 将是当前值或者 null。否则 prev value 是真正的之前值。

```C#
// This example assumes you are acting as the host client.
// We will imagine previous value was 10, and next is 20.
private void _mySyncVar_OnChange(int prev, int next, bool asServer)
{
    // If asServer if true then the prev value will correctly be 10,
    // with the next being 20.
    
    // If asServer is false then the prev value will be 20, as well the
    // next being 20. This is because the value has already been changed
    // on the server, and the previous value is no longer stored.
    
    DoSomething(prev, next);
}
```

如果你计划在游戏中使用 clientHost，则有一种相当简单的方法可以应对这种情况。

```C#
// This example assumes you are acting as the host client.
// We will imagine previous value was 10, and next is 20.
private void _mySyncVar_OnChange(int prev, int next, bool asServer)
{
    // Only run the logic using the previous value if being called
    // with asServer true, or if only the client is started.
    if (asServer || base.IsClientOnlyStarted)
        DoSomething(prev, next);
}
```
