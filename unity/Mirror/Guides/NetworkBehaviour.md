# NetworkBehaviour

Network Behaviour 脚本和具有 NetworkIdentity 的对象一起工作。

这些脚本可以执行 high-level API 函数，诸如 Commands（Client-to-Server），ClientRpc（Server-to-Client）， SyncVars（Server-to-Client data）。

使用 Mirror server-authoritative 系统，server 必须使用 NetworkServer.Spawn 函数来生成带有 Network Identity 组件的 gameobjects。以这种方式生成的 gameobject 带有一个 netId，并且在 clients 上生成它们，并且连接到 server。这些 gameobject 是 non-player networked gameobjects。（每个 non-player networked gameobject 也要拥有 NetworkIdentity 组件）。

这不是一个你可以直接添加到 gameobject 的组件。相反，你必须创建一个脚本继承自 NetworkBehaviour（而不是 MonoBehaviour），然后你添加你的脚本到 gameobject 作为组件。

## Properties

- isServer

  如果 gameobject 运行在 server，并且以及被 spawned，返回 true

- isClient

  如果 gameobject 是在 client 上，并且已经被 server 生成，返回 true

- isLocalPlayer

  如果 gameobject 代表 为这个 client 创建的 player，返回 true

  说明还有不表示 player 的 networked gamobject，可能是代表其他 player 的 networked gameobject，以及 non-player networked gameobject。

- hasAuthority

  在 Client 上，如果 client 具有这个 gameobject 的 authority，返回 true。在 server context 中时无意义的。

- netId

  gameobject 的 unique network ID。Server 在运行时赋予这个 ID。在这个 network session 中每个 gameobject 都有不同的 ID。

- netIdentity

  返回这个 gameobject 的 NetworkIdentity。

- connectionToServer

  管理到 gameobject 上 NetworkIdentity 的 NetworkConnection。在 client 上只对  player gameobjects 有效。

- connectionToClient

  和 connectionToServer 一样，在 server 上只对 player gameobjects 有效。

NetworkBehaviour 脚本具有以下功能：

- Synchronized variables
- Network callbacks
- Server and Client functions
- Sending commands
- Client RPC calls
- Networked events

![UNetDirections](../../Image/UNetDirections.jpg)

## Network Callbacks

NetworkBehaviour 脚本有一些内置的 callback 函数，用于各种网络事件。

它们是一些 base class 的虚拟函数，因此你可以像这样才 override 它们

```C#
public class SpaceShip : NetworkBehaviour
{
    public override void OnStartServer()
    {
        // disable client stuff
    }

    public override void OnStartClient()
    {
        // register client events, enable effects
    }
}
```

built-in callbacks 是

- OnStartServer：在 server 上调用，当 gameobject 在 server 上生成时，或者当 server start 时
- OnStopServer：在 server 上调用，当 gameobject 在 server 上销毁时，或者当 server stop 时
- OnStartClient：在 clients 上调用，当 gameobject 在 client 上生成时，或者当 client 连接到 server 时
- OnStopClient：在 clients 上调用，当 server 销毁 gameobject 时
- OnStartLocalPlayer：在 clients 上调用，为 local client 的 player gameobjects（only）
- OnStartAuthority：在 clients 上为具有 authority 的 behaviour 调用，基于 context 和 hasAuthority
- OnStopAuthority：在 clients 上调用，当 behaviours 的 authority 被移除时

注意，在 peer-hosted 设置中，一个 client 同时作为 host 和 client，OnStartServer 和 OnStartClient 都会在同一个 same gameobject 上调用。这些 functions 对于特定于 client 或 server 的 action 非常有用，例如 server 上的 suppressing effects，或者设置 client-side events。

## Server and Client functions

你可以使用属性标记 NetworkBehaviour 脚本的成员函数来指定它们是 server-only 或 client-only 函数。如果 client 没有 active，Server 和 ServerCallback 立即返回。类似地，如果 server 没有 active，Client 和 ClientCallback 立即返回。

Server 和 Client 属性用于你自己自定义的回调函数。它们不生成编译时错误，但是如果在错误的 scope 中调用它们会发出一个 warning log message。

ServerCallback 和 ClientCallback 属性用于 built-in callback 函数（OnXXXX），这些回调函数被 Mirror 自动调用（MonoBehaviour 事件函数）。这些属性不会产生 warning。

## Commands

要在执行 server 上的 code，必须使用 commands。High-level API 是一个 server authoritative system，因此 commands 是一个 client 触发 server code 的唯一方法。

只有 player game objects 可以发送 commands。non-player networked gameobjects 不能发送 commands。

当一个 client player gameobject 发送一个 command 时，command 在 server 上相应的 player gameobject 上执行。这种 routing 自动发生，因此一个 client 不可能为另一个 player 发送一个 command。

要在 code 中定义一个 command，必须编写一个 function，其拥有：

- Cmd 开头的名字
- Command 属性

Commands 只需要在 client 像普通 function 一样调用，Mirror 在背后自动发送网络命令。但是命令中的代码不在 client 上执行，而是在 server 上的相应 player gameobject 上调用。

Commands 是 type-safe 的，具有内建的 security，并且 routing 给 player，使用一个高效的序列化机制，使调用更快。

## Client RPC Calls

Client RPC 调用 是 Server gameobjects 使得 client gameobjects 发生一些事情的方式。

Client RPC 调用不限制在 player gameobjects，而是可以在任何具有 NetworkIdentity 组件的 gameobject 上执行（non-player networked gameobjects）。

要在 code 中定义一个 Client RPC 调用，必须编写一个 function，其拥有：

- Rpc 开头的名字
- ClientRpc 属性

## Networked Events（Obsolete）

Client RPC
