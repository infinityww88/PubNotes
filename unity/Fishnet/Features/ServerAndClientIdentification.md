确定 code 是在 server 还是在 client 上执行，以及如何彼此识别 clients。

## Executing on Server or Client

### Overview

在实际开发中，你的代码经常需要判断当前运行环境是服务器、客户端还是同时处于两者（如Host模式）。FishNet提供了多种环境检测方式：既可以通过监听仅限客户端/服务器触发的专属事件或调用特定方法来判断，也能通过编译指令识别当前构建版本类型，还可通过方法标记限制代码执行环境，甚至直接检测布尔值状态。

### 检测 boolean

你可以通过简单的布尔值检查来判断当前代码是否运行在服务器端。为此，FishNet的NetworkBehaviour和NetworkObject类专门提供了易用的属性供开发者调用，这些属性也能直接通过NetworkManager访问。

- 使用IsClientStarted可检测当前运行环境是否为客户端（但也可能是同时作为客户端的服务器）
- 通过IsClientOnlyStarted能明确判断当前是否仅为客户端运行环境（排除服务器情况）
- IsServerStarted用于检测当前是否为服务器运行环境（但需注意也可能同时是客户端）
- 最后，IsServerOnlyStarted可确切判断当前是否仅为服务器环境（排除客户端可能性）

若处于NetworkBehaviour中，直接使用IsServerStarted属性最简便，但需注意它会同时检查NetworkObject是否已在网络中生成。若需从MonoBehaviour或 non-spawned NetworkBehaviour中检测，可通过InstanceFinder获取NetworkManager实例来进行判断。

```C#
using FishNet.Object;

public class Player : NetworkBehaviour
{
    public void OnStruck()
    {
        if (!IsClientStarted)
            return;

        // Play visual effect and sounds only on a client.
    }
}
```

### Method Attributes

有很多属性可以用于确保一个 method 只运行在合适的 game instance 上。

这些方法还用于 Fish-Networking Pro 的自动化 code stripping。尤其重要的是，标记为 \[Server\] 属性的方法会使它们的 method body 从 non server builds 中剥离。

#### Client Method Attribute

在方法上方添加\[Client\]特性标注后，可确保该方法仅在本地客户端处于激活状态时（可选条件：当关联的NetworkObject完成初始化后）才能被调用。该特性还支持通过附加参数扩展更多功能。

```C#
[Client]
void ShowUI()
{
    // This code will only run on a client, otherwise it will print a warning.
}
```

这个例子中，ShowUI 方法不会在非 client 中运行。

这个属性还有一些属性。

若在无客户端激活时调用此方法，系统会打印警告且方法不执行。可通过Logging属性修改日志类型，控制是否记录警告（默认为LoggingType.Warning）。还可通过设置RequireOwnership为true，限制仅对象所有者能调用该方法（默认为false）。此外，使用UseIsStarted属性可忽略NetworkObject的初始化状态，仅检查客户端是否已启动。

```C#
// The server does not need to play VFX; only play VFX if the client is active.
[Client(Logging = LoggingType.Off, RequireOwnership = true, UseIsStarted = true)]
void PlayVFX() 
{ 
    // Play VFX here...
}
```

#### Server Method Attribute

\[Server\]特性标注提供与\[Client\]特性类似的功能，不同之处在于：若服务器未激活（或可选地，关联的NetworkObject未完成初始化），则禁止方法执行。

以下示例展示了如何通过\[Server\]特性确保代码仅在服务器端执行（禁止在客户端或其他环境运行）。
与\[Client\]特性类似，若在服务器未激活时调用该方法，系统会抛出警告提示。
开发者可通过调整Logging属性来修改或禁用该警告通知。
此外，启用UseIsStarted属性可跳过NetworkObject的初始化状态检查，仅验证服务器是否已启动。

```C#
// The server would validate hit results from a client.
[Server(Logging = LoggingType.Off, UseIsStarted = false)]
private void ValidateHit() 
{
    // Hit validation code here that will only run on the server.
}
```

## NetworkConnections

在FishNet框架中，NetworkConnection是一个核心对象，用于表示网络系统中单个已连接的客户端。每当有客户端与服务器建立连接时，系统就会创建对应的NetworkConnection实例，通过该实例可对该客户端执行操作并获取其特定信息。

### 目的

- 代表客户端

  每个已连接的玩家/客户端都对应一个独立的NetworkConnection实例。该对象负责追踪客户端的身份标识、连接状态及其所拥有的网络对象。

- Ownership and Authority

  NetworkConnection会记录客户端所拥有的网络对象（如玩家角色化身），从而支持权限验证与状态管理功能。

- Authentication and State

  它负责管理认证状态，并监测客户端是否处于断开连接过程中。

- Scene Tracking

  追踪客户端已加载的网络场景。

- Events

  为诸如获取、失去 objects 的 ownership 和加载 start scenes 的动作提供事件。

- Custom Data

  开发者可通过该连接关联自定义数据以支持游戏逻辑或服务器运算（注：此类数据不会自动进行网络同步）。

- Disconnection

  提供方法来断开客户端，立刻或者在发送 pending data 后。

### 重要的字段和属性

- ClientId
  
  一个重要的字段是 ClientId。这是用于 NetworkConnection 的唯一 ID，并用于 Fish-Networking 的其他一些地方。如果 ClientId 没有设置，默认为 -1。通常 ClientIds 通常从 0 增长，直到达到最大整数，然后才会从开始重用旧的 Id。

- FirstObject

  Fishnet 没有一个强制的 Player GameObject，但是你可以通过 FirstObject 属性得到 client 拥有的第一个 object。还可以通过 SetFirstObject 方法设置这个值，这可以用于使 object 销毁再重新实例化。

- Objects

  这个字段这个 connection 拥有的 network objects 的 HashSet。它对这个 connection 和 server 可用。

- Scenes

  这些是这个连接被认为所属于的 networked scenes。

- CustomData

  这是用户自定义 object，用于在 connection 上存储任意数据。它从不同步。

### 从哪里得到它们，在哪里使用它们

- 每个 client 有一个 NetworkConnection 代表它自己，这可以通过 ClientManager.Connection 或者 NetworkBehaviour 的 LocalConnection 来访问。
- server 为所有连接的 clients 维护一个 NetworkConnection instances 的字典。它可以通过 ServerManager.Clients 访问。在 clients 上它也可以通过 ClientManager.Clients 访问。如果 instance 运行在 server，应该使用 ServerManager 版本。字典的键是 Client ID，值是 NetworkConnection。
- NetworkObjects 可以有一个 owner，这是一个 NetworkConnection 对象，它对 object 具有权威。在 NetworkObject 或 NetworkBehaviour 中，可以通过 Owner 属性得到。
- 当调用 TargetRpcs，你需要提供 NetworkConnection 作为第一个参数，这代表 RPC 将要发送到哪个 client。
