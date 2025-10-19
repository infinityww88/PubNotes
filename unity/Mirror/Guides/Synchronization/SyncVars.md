# SyncVars

SyncVars 是继承自 NetworkBehaviour 的 classes 的属性，它们从 server 到 clients 同步。当一个 gameobject 被生成时，或者一个新的 player 在游戏进行时加入游戏，它们被发送以 player 可见的 networked gameobjects 的所有 SyncVars 的最新状态。使用 SyncVar 自定义属性来指定你想要同步脚本中哪个 variables。

SyncVars 的状态在 OnStartClient() 被调用之前应用到 clients 上的 gameobjects。因此 object 的状态在 OnStartClient 中总是 up-to-date 的。

SyncVars 可以使用任何 Mirror 支持的类型。你在一个 NetworkBehaviour Script 中最多可以有 64 个 SyncVars，包括 SyncList。因为每个 NetworkBehaviour 有一个 dirty mask，每个 SyncVar 使用一个 bit 标记是否 dirty。因此这个 mask 是一个 long，一共 64 个 bits。

Server 在一个 SyncVar 改变时自动发送 SyncVar 更新，因此你不需要追踪它们何时改变，或者自己发送信息变化。在 inspector 中改变一个 value 不会触发更新。

SyncVar hook 属性可以用于指定一个方法，在 SyncVar 改变时在 client 上调用。

## SyncVar Example

比如说我们有一个 networked object，它有一个称为 Enemy 脚本：

```C#
public class Enemy : NetworkBehaviour
{
    [SyncVar]
    public int health = 100;

    void OnMouseUp()
    {
        NetworkIdentity ni = NetworkClient.connection.identity;
        PlayerController pc = ni.GetComponent<PlayerController>();
        pc.currentTarget = gameObject;
    }
}
```

PlayerController 看起来可能是这样：

```C#
public class PlayerController : NetworkBehaviour
{
    public GameObject currentTarget;

    void Update()
    {
        if (isLocalPlayer)
            if (currentTarget != null)
                if (currentTarget.tag == "Enemy")
                    if (Input.GetKeyDown(KeyCode.X))
                        CmdShoot(currentTarget);
    }

    // Command 函数只在 server 上执行，由 client 发起，client 使用普通的函数调用发起调用请求
    [Command]
    public void CmdShoot(GameObject enemy)
    {
        // Do your own shot validation here because this runs on the server
        enemy.GetComponent<Enemy>().health -= 5;
    }
}
```

在这个例子中，当 Player 点击一个 Enemey，这个 networked enemy gameobject 被赋予 PlayerController.currentTarget。当 player 按下 X，target 被通过 Command 传递 到 server 上执行，递减 health SyncVar。所有 clients 将会更新为这个新值。然后你可以在 enemy 上有一个 UI 显示当前值。

## Class inheritance

SyncVars 在类继承中也可以工作。

```C#
class Pet : NetworkBehaviour
{
    [SyncVar] 
    String name;
}

class Cat : Pet
{
    [SyncVar]
    public Color32 color;
}
```

你可以附加一个 Cat component 到你的 cat prefab，它将会同时同步 name 和 color。

注意 Both Cat 和 Pet 应该在同一个 assembly。如果它们在分离的 assemblies，确保不要在 Cat 内部直接修改 name，而是在 Pet 添加一个方法来修改它。
