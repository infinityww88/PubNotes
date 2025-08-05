SyncVars​ 是最简便的网络同步方案，可自动同步单个变量。

SyncVars​ 用于同步单个字段，支持几乎所有数据类型：值类型、结构体或类均可。若要使用 ​SyncVar，必须将你的类型实现为 ​SyncVar 类。

```C#
public class YourClass : NetworkBehaviour
{
    private readonly SyncVar<float> _health = new SyncVar<float>();
}
/* Any time _health is changed on the server the
 * new value will be sent to clients. 
 */
```

​SyncTypes​ 可通过以下方式自定义扩展选项：

​- 声明时初始化​：在 SyncType 声明时通过初始化器设置默认行为。
​- 运行时动态配置​：通过 UpdateSettings 方法调整同步策略，例如：
  - 启用值变更通知（如触发回调函数）。
  - 调整同步频率（如实时同步或定时批量同步）。
  - 其他高级选项（如冲突解决策略、批量大小等）。

具体可配置属性及方法请参考官方 API 文档。

以下示例演示如何以最长每1秒的间隔发送SyncType数据，并在数值变化时触发通知。

```C#
private readonly SyncVar<float> _health = new SyncVar<float>(new SyncTypeSettings(1f);
    
private void Awake()
{
    _health.OnChange += on_health;
}

//This is called when _health changes, for server and clients.
private void on_health(float prev, float next, bool asServer)
{
    /* Each callback for SyncVars must contain a parameter
    * for the previous value, the next value, and asServer.
    * The previous value will contain the value before the
    * change, while next contains the value after the change.
    * By the time the callback occurs the next value had
    * already been set to the field, eg: _health.
    * asServer indicates if the callback is occurring on the
    * server or on the client. Sometimes you may want to run
    * logic only on the server, or client. The asServer
    * allows you to make this distinction. */

    /*
    每个 ​SyncVar​ 回调函数必须包含三个参数：
    - ​previousValue​（变更前的旧值）
    - ​nextValue​（变更后的新值）
    - ​asServer​（标识回调触发方）

​    - 旧值（previousValue）​​：存储字段变更前的原始数据（例如修改前的角色血量）。
    ​- 新值（nextValue）​​：存储字段变更后的最新数据（例如修改后的角色血量）。
    - ​触发方标识（asServer）​​：布尔值，用于判断回调发生在服务端（true）还是客户端（false）。

    ​关键说明​：当回调触发时，新值（nextValue）​已同步写入目标字段​（例如 _health 字段已更新）。
    通过 asServer 参数，你可以精准控制逻辑仅在服务端或客户端执行（例如：仅服务端处理伤害计算，仅客户端播放特效）。
    */
}
```

另一个常见需求是实现客户端 Sync values。这可以通过 ServerRpc 实现。

SyncVar 是服务端修改，然后同步到客户端。这里要实现的是客户端直接修改变量，然后同步到其他 clients。

在客户端修改 ​SyncVar​ 时，每次赋值操作都会触发一次 RPC 调用。若你的 ​SyncVar​ 值会高频变更，建议通过限制客户端赋值频率来降低带宽消耗。

我们计划在后续版本中为所有 ​SyncType​ 新增客户端权威属性，届时将无需再采用此变通方案。

```C#
//A typical server-side SyncVar.
public readonly SyncVar<string> Name = new SyncVar<string>();
//Create a ServerRpc to allow owner to update the value on the server.
[ServerRpc] private void SetName(string value) => Name.Value = value;
```

在使用客户端 ​SyncVar​ 时（默认 SyncVar 只在 server 端使用），若需避免所有者（Owner）接收到自身触发的更新，可在 ​SyncVar​ 的 ReadPermissions 中设置 ExcludeOwner 权限。此外，将 WritePermission 设为 ClientUnsynchronized 能允许客户端在本地直接修改该值。最后，在 ServerRpc 中启用 RunLocally = true 可确保 RPC 逻辑同时在发送方（客户端）和服务端执行。
具体配置示例如下：

- ​SyncVar 权限设置​：ReadPermissions 选用 ExcludeOwner，WritePermissions 设为 ClientUnsynchronized
- ​RPC 行为控制​：在 ServerRpc 中设置 RunLocally = true，使调用方客户端本地同步更新数值

```C#
//Attributes shown in previous examples can stack but they were removed
//here for simplicity.
private readonly SyncVar<string> Name = new SyncVar<string>(new SyncTypeSettings(WritePermission.ClientUnsynchronized, ReadPermission.ExcludeOwner));
//Create a ServerRpc to allow owner to update the value on the server.
[ServerRpc(RunLocally = true)] private void SetName(string value) => Name.Value = value;
```
