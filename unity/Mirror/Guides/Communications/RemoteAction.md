# Remote Action

Mirror 网络系统拥有在 network 上执行 actions 的方法。这些 actions 类型有时称为 Remote Procedure Calls（远程过程调用）。

Network system 有两种类型的 RPCs：

- Commands：在 client 上调用，运行在 server 上
- ClientRpc：在 server 上调用，运行在 clients 上

![UNetDirections](../../../Image/UNetDirections.jpg)

## Commands

Commands 从 client 上的 player objects 发送到 server 上的 player objects。安全起见，Commands 默认只能从你的 player object 上发送，因此你不能控制其他 players 的 gameobjects。你可以使用 [Command(ignoreAuthority = true)] 绕过这个检查。

要是一个 function 成为 command，为它添加 [Command] 属性，并且为函数名添加 Cmd 前缀。现在，在 client 调用这个函数，Mirror 将会发送网络命令到 server 并在 server 上调用，任何允许的数据类型的参数都会被自动跟随 command 传递到 server。

Command 函数必须具有 Cmd 前缀，而且不能是静态的。这是一个提示，即这个 function 是特殊的而且不能像普通函数一样调用。

```C#
public class Player : NetworkBehaviour
{
    void Update()
    {
        if (!isLocalPlayer) return;

        if (Input.GetKey(KeyCode.X))
            CmdDropCube();
    }

    // assigned in inspector
    public GameObject cubePrefab;

    [Command]
    void CmdDropCube()
    {
        if (cubePrefab != null)
        {
            Vector3 spawnPos = transform.position + transform.forward * 2;
            Quaternion spawnRot = transform.rotation;
            GameObject cube = Instantiate(cubePrefab, spawnPos, spawnRot);
            NetworkServer.Spawn(cube);
        }
    }
}
```

注意上面每一帧从 client 发送 commands！这将导致大量的网络传输。

### Commands and Authority

如果以下任何条件为 true，可以在一个 non-player 上调用 commands（在 server 上执行命令）：

- object 是在这个 client 上生成，默认 这个 client 具有 authority
- object 具有 NetworkIdentity.AssignClientAuthority 设置的 client authority
- Command 具有为 true 的 ignoreAuthority
  - 你可以在命令方法签名中包含一个可选的 NetworkConnectionToClient sender = null 参数，而 Mirror 将会为你填充这个（发送 commands 的） sending client。这是因为任何 player 都可以发送这个命令，这个参数用来确定发送命令的 client。
  - 不要试图为这个可选参数设置一个 value，它会被忽略，简单来说，它是为 Mirror 提供的占位符

从这些 objects 上发送的 Commands 运行在 object 的 server 实例上，而不是在 client 的 server 上的 player gameobject。

```C#
public enum DoorState : byte
{
    Open, Closed
}

public class Door : NetworkBehaviour
{
    [SyncVar]
    public DoorState doorState;

    [Command(ignoreAuthority = true)]
    public void CmdSetDoorState(DoorState newDoorState, NetworkConnectionToClient sender = null)
    {
        if (sender.identity.GetComponent<Player>().hasDoorKey)
            doorState = newDoorState;
    }
}
```

## ClientRpc Calls

ClientRpc 调用从 server 上的 gameobjects 发送到 clients 上的 objects。它们可以任何生成的带有 NetworkIdentity 组件的 server gameobjects 上发出。因为 server 具有 authority，因此 server objects 发送这些调用不会有安全问题。

要使一个函数成为一个 ClientRpc 调用，添加 [ClientRpc] 属性到它上面，并添加 Rpc 前缀。

现在这个函数在 server 上调用时，它将会运行在 clients 上。任何允许的数据类型的参数都自动被传递到 clients。

ClientRpc 函数必须具有 Rpc 前缀，并且不能是静态的。这是一个提示，这个函数是特殊的，不能像普通函数一样调用。

ClientRpc 消息只被发送到 object 的 observers 上，根据 Network Visibility。Player objects 总是它们自己的 observers。有些情况下，你可能想要在调用一个 ClientRpc 时排除 owner client。这通过 excludeOwner 选项完成：[ClientRpc(excludeOwner = true)]。

```C#
public class Player : NetworkBehaviour
{
    int health;

    public void TakeDamage(int amount)
    {
        if (!isServer) return;

        health -= amount;
        RpcDamage(amount);
    }

    [ClientRpc]
    void RpcDamage(int amount)
    {
        Debug.Log("Took damage:" + amount);
    }
}
```

当一个游戏作为具有 local client 的 host 时，ClientRpc 调用将会在 local client 上被调用，尽管它和 server 是在同一个进程的。因此 local 和 remote clients 的行为对于 ClientRpc 调用是一样的。

## TargetRpc Calls

TargetRpc 调用被 server 上的 user code 调用，然后在指定的 NetworkConnection 的 client 上的相应 client gameobject 上调用。RPC 调用的参数在网络上序列化，因此 client function 使用和 server function 相同的参数被调用。

这些 functions 必须以 Target 开头，并且不能是静态的。

Context Matters：

- 如果 TargetRpc 方法的第一个参数是一个 NetworkConnection，则这就是将会收到消息的 client 而不管 context
- 如果第一个参数是任何其他类型，则 object 的 owner client 将会收到消息，并且在其脚本中的 TargetRpc 上调用

下面这个例子显示了一个 client 使用 Command 完成一个 server request (CmdMagic)，包含它自己的 connectionToClient 作为 TargetRpc 的第一个参数，在 Command 中直接调用：

```C#
public class Player : NetworkBehaviour
{
    int health;

    [Command]
    void CmdMagic(GameObject target, int damage)
    {
        target.GetComponent<Player>().health -= damage;

        NetworkIdentity opponentIdentity = target.GetComponent<NetworkIdentity>();
        TargetDoMagic(opponentIdentity.connectionToClient, damage);
    }

    [TargetRpc]
    public void TargetDoMagic(NetworkConnection target, int damage)
    {
        // This will appear on the opponent's client, not the attacking player's
        Debug.Log($"Magic Damage = {damage}");
    }

    [Command]
    void CmdHealMe()
    {
        health += 10;
        TargetHealed(10);
    }

    [TargetRpc]
    public void TargetHealed(int amount)
    {
        // No NetworkConnection parameter, so it goes to owner
        Debug.Log($"Health increased by {amount}");
    }
}
```

## Arguments to Remote Actions

传递给 Commands 和 ClientRpc 调用的参数被序列化并在网络上发送。你可以使用任何 Mirror 支持的类型。

Remote Actions 的参数不能是 gameobjects 的 sub-components，例如 script 实例，或 Transforms。