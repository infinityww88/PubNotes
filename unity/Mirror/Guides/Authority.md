# Network Authority

Servers 和 Clients 都可以管理一个 gameobject 的行为。

Authority 指的是一个 gameobject 如何以及在哪里管理。

## Server Authority

使用 Mirror 的 networked games 的默认 authority 状态是 Server 对所有不表示 players 的 gameobjects 具有 authority。这意味着 server 将管理所有可收集 items，移动的 platforms，NPCs，以及游戏中 players 可以交互的任何其他部分，而 player gameobjects 在它们自己的 client 上具有 authority，意味着 client 管理他们的行为。

## Client Authority

Client authority 意味着 local client 可以控制一个 networked game object。默认只有 server 可以控制一个 networkded object。

在实践中，具有 client authority 意味着 client 可以调用 Command 方法，并且如果 client 断开连接，这个 object 会自动销毁。

Client 的 NetworkIdentity.hasAuthority 属性可以确定一个 gameobject 是否具有 local authority（方便起见，NetworkBehaviour 也可以访问）。

为一个 client 赋予一个 gameobject authority 将导致 Mirror 在这个 gameobject 的每个 NetworkBehaviour 上调用 OnStartAuthority()，并设置 hasAuthority 属性为 true。在其他 clients 上，hasAuthority 属性保持 false。

Player objects 总是具有 client authority。这对于控制移动和其他 player actions 是必须的。

不要将 Client Authority 和 client authoritative 架构混淆。Client Authority 中任何 action 仍然必须通过 Command 到达 server。只不过 action 的数据是有 authority client 提供的，最终仍然有 server 发送给所有 clients。Client authoritative 架构则通过 P2P 方式发送到所有 clients，并通过分布式算法在所有 clients 保持一致状态。

Client 不能直接修改 SyncVars 或者影响其他 client，必须通过向 Server 发送 Command。

- Server authority 由 server 管理所有 gameobject 的操作和数据，状态和动作总是有 server 发送给 clients。Server -> Clients。
- Client authority 由具有 authority 的 client 管理授予它管理的的 gameobject 的动作和状态。这个 gameobject 的操作和状态由 client 发送给 server，再由 server 发给其他 clients。Clients -> Server -> Clients。
- Client authoritative 架构由 client 管理所有自己生成的 gameobjects，通过 P2P 方式将它们的动作和状态发送给所有 clients。Clients -> Clients。

## Non-Player Game Objects

有两种方式为 non-player gameobjects 授权 client authority。

- 使用 NetworkServer.Spawn 生成 gameobject，并传递 client 的 network connection 来获得所有权
- 使用 NetworkIdentity.AssignClientAuthority 以及 client 的 network conneciton 来获得所有权

还有，有一个可选的参数 [Command] 可以跳过 authority 检查：[Command(ignoreAuthority = true)]，其允许他们被调用而不需 client 具有这个 object 的所有权。

下面的示例生成一个 gameobject，并向生成它的 player 的 client 授予 authority。

```C#
[Command]
void CmdSpawn() {
    GameObject go = Instantiate(otherPrefab, transform.position + new Vector3(0, 1, 0), Quaternion.identity);
    NetworkServer.Spawn(go, connecitonToClient);
}

[Command]
void GrantAuthority(GameObject target) {
    // target 必须拥有一个 NetworkIdentity 组件，来通过一个 Command 传递，并且同时存在于 server 和 client
    target.GetComponent<NetworkIdentity>().AssignClientAuthority(connectionToClient);
}
```

## Network Context Properties

NetworkBehaviour 类包含允许 scripts 在任何时候知晓一个 networked gameobject 上下文的属性，包括：

- isServer：如果 gameobject 是在 server 上，并且已经被生成
- isClient：如果 gameobject 是在 client 上，并且是被 server 创建的
- isLocalPlayer：如果 gameobject 是这个 client 的 player gameobject
- hasAuthority：如果 client 具有 gameobject 的所有权

在 server 上，NetworkIdentity 在 connectionToClient 保存拥有它的 client。

要查看这些属性，选择想要查看的 gameobject，在 inspector 窗口查看 NetworkBehaviour 脚本组件。你可以使用这些属性的值来基于 scripting 在哪个 context 中运行来执行代码。
