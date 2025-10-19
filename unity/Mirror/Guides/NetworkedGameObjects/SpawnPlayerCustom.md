# Custom Character Spawning

很多游戏需要 character 自定义。你可能想定制 hair，eyes，skin，height，race 的颜色等等。

默认地，Mirror 会为你实例化 player。虽然这很方便，但是这阻止你去定制它。Mirror 提供了覆盖 player 创建和定制的选项。

1. 创建一个继承自 NetworkManager 的类，如果你还没有的话，并使用它作为你的 NetworkManager

   ```C#
   public class MMONetworkManager : NetworkManager
   {
       // ...
   }
   ```

2. 在Inspector 上打开你的 NetworkManager，关闭 “Auto Create Player” Boolean
3. 创建一个消息描述你的 player

   ```C#
    public class CreateMMOCharacterMessage : MessageBase
    {
        public Race race;
        public string name;
        public Color hairColor;
        public Color eyeColor;
    }

    public enum Race
    {
        None,
        Elvish,
        Dwarvish,
        Human
    }
   ```

4. 创建你的 player prefabs（想要多少创建多少），并且添加它们到你的 NetworkManager 上的 "Register Spawnable Prefabs"，或者添加一个 prefab 到 player prefab 字段。

5. 发送你的 message，并注册一个 player

   ```C#
    public class MMONetworkManager : NetworkManager
    {
        public override void OnStartServer()
        {
            base.OnStartServer();

            NetworkServer.RegisterHandler<CreateMMOCharacterMessage>(OnCreateCharacter);
        }

        public override void OnClientConnect(NetworkConnection conn)
        {
            base.OnClientConnect(conn);

            // you can send the message here, or wherever else you want
            CreateMMOCharacterMessage characterMessage = new CreateMMOCharacterMessage
            {
                race = Race.Elvish,
                name = "Joe Gaba Gaba",
                hairColor = Color.red,
                eyeColor = Color.green
            };

            conn.Send(characterMessage);
        }

        void OnCreateCharacter(NetworkConnection conn, CreateMMOCharacterMessage message)
        {
            // playerPrefab is the one assigned in the inspector in Network
            // Manager but you can use different prefabs per race for example
            GameObject gameobject = Instantiate(playerPrefab);

            // Apply data from the message however appropriate for your game
            // Typically Player would be a component you write with syncvars or properties
            Player player = gameobject.GetComponent<Player>();
            player.hairColor = message.hairColor;
            player.eyeColor = message.eyeColor;
            player.name = message.name;
            player.race = message.race;

            // call this to use this gameobject as the primary controller
            NetworkServer.AddPlayerForConnection(conn, gameobject);  // 指定作为 Player GameObject 的 gameobject
        }
    }
   ```

## Ready State

Client Connection 还有一个 “ready” state。Host 向已经准备好的 clients 发送有关 spawned gameobjects 和 状态同步更新的信息。没有准备好的 clients 不会发生这些更新。

但一个 clinet 初始链接一个 server 时，它还没有准备好。当处于 non-ready 状态时，client 可以做那些不需要与 server 上的 game state 实时交互的事情，例如加载 Scenes，允许 player 选择一个 avatar，或者填充 log-in boxes。一旦一个 client 已经完成了所有 pre-game 工作，并且它的 Assets 已经被加载。它可以调用 ClientScene.Ready 进入 ready 状态。上面这个简单例子展示了 ready states 的实现。因为使用 NetworkServer.AddPlayerForConnection 添加一个 player 也会将 client 设置到 ready state，如果它还不是 ready 的话。

Clients 可以在未 ready 时发送和接受 network 消息，这也意味着他们可以不需要有一个实际的 active player gameobject。因此一个在 menu 或者 selection screen 的 client 可以连接到游戏，并和它交互，尽管它们没有 player gameobject。即利用 low level network message 来通信。

## Switching Players

要为一个 connection 替换 player gameobject，使用 NetworkServer.ReplacePlayerForConnection。这对于限制特定时刻 player 可以发起的 commands 是非常有用的，例如在一个 pregame room screen 的时候。不同的 player gameobject 具有不同的 script，可以发送不同的 commands。

NetworkServer.ReplacePlayerForConnection 使用和 NetworkServer.AddPlayerForConnection 相同的参数，但是允许那个 connection 已经有一个 player gameobject 了。

Old player gameobject 不必须销毁。NetworkRoomManager 使用这个技术来从 NetworkRoomPlayer gameobject 切换到 game player gameobject（in game），在所有 player 准备好的时候。

你还可以使用 ReplacePlayerForConnection 来 respawn 一个 player 或者改变代表 player 的 gameobject。有些情况下，在 respawn 时只 disable 一个 gameobject 并重置它的 game 属性是更好的选择。

下面的例子展示如何使用一个新的 gameobject 实际替换 player gameobject：

```C#
public class MyNetworkManager : NetworkManager
{
    public void ReplacePlayer(NetworkConnection conn, GameObject newPrefab)
    {
        // Cache a reference to the current player object
        GameObject oldPlayer = conn.identity.gameObject;

        // Instantiate the new player object and broadcast to clients
        NetworkServer.ReplacePlayerForConnection(conn, Instantiate(newPrefab));

        // Remove the previous player object that's now been replaced
        NetworkServer.Destroy(oldPlayer);
    }
}
```

如果一个 connection 的 player gameobject 被销毁，则这个 client 不能执行 Commands。但是它们仍然可以使用 network messages 来发送消息。

要使用 ReplacePlayerForConnection，你必须有 player client 上的 NetworkConnection gameobject 来完成 gameobject 和 client 之间的关系。这通常是 NetworkBehaviour 的 connectionToClient 属性，但是如果旧的 player 已经被销毁，则它可能不可用。

要查找 connection，有一些可用的列表。如果使用 NetworkRoomManager，则 room players 在 roomSlots 可用。NetworkServer 还拥有 connections 列表。
