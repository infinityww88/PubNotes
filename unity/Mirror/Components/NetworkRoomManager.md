# Network Room Manager

Network Room Manager 是 Network Manager 的特定类型，提供一个用于进入 game play scene 之前的 multiplayer room。它允许你设置一个 network，包括：

- 一个 maximum player limit
- 当所有 players 准备好时自动开始
- 防止 players 在游戏过程中加入游戏的选项
- players 在 room 中时选择选项的可定制方式

有两种类型的带有 Network Room Manager 的 player objects：

- Room Player Prefab

  - 每个 player 一个
  - 当 client 连接或者 player 被添加时创建
  - 持久化直到 client 端口连接
  - 保存 ready flag 和配置数据
  - 处理 room 的 commands
  - 必须使用 Network Room Player 组件

- Player Prefab

  - 每个 player 一个
  - 当 game scene 开始时创建
  - 当离开 game scene 时销毁
  - 处理 game 中的 commands

![NetworkRoomManager](../../Image/NetworkRoomManager.png)

# Properties

- Show Room GUI

  为 room 显式默认 OnGUI 控件

- Min Players

  开始游戏需要的最小玩家数量

- Room Player Prefab

  当 player 进入 room 时为 players 创建的 prefab（需要 Network Room Player 组件）

- Room Scene

  用于 room 的 scene

- Gameplay Scene

  用于 main game play 的 scene

- pendingPlayers

  保存已经准备好开始的 players 的列表 List<NetworkRoomPlayer>

- allPlayersReady

  bool，指示所有玩家是否准备好开始 playing。这个 value 随着 players 调用 CmdChangeReadyState（指定 true 或 false）而改变，并在一个新 client 连接时设置为 false。

## Methods

### Server Virtual Methods

```C#
public virtual void OnRoomStartHost() {}

public virtual void OnRoomStopHost() {}

public virtual void OnRoomStartServer() {}

public virtual void OnRoomServerConnect(NetworkConnection conn) {}

public virtual void OnRoomServerDisconnect(NetworkConnection conn) {}

public virtual void OnRoomServerSceneChanged(string sceneName) {}

public virtual GameObject OnRoomServerCreateRoomPlayer(NetworkConnection conn)
{
    return null;
}

public virtual GameObject OnRoomServerCreateGamePlayer(NetworkConnection conn)
{
    return null;
}

public virtual bool OnRoomServerSceneLoadedForPlayer(GameObject roomPlayer, GameObject gamePlayer)
{
    return true;
}

public virtual void OnRoomServerPlayersReady()
{
    ServerChangeScene(GameplayScene);
}
```

### Client Virtual Methods

```C#
public virtual void OnRoomClientEnter() {}

public virtual void OnRoomClientExit() {}

public virtual void OnRoomClientConnect(NetworkConnection conn) {}

public virtual void OnRoomClientDisconnect(NetworkConnection conn) {}

public virtual void OnRoomStartClient() {}

public virtual void OnRoomStopClient() {}

public virtual void OnRoomClientSceneChanged(NetworkConnection conn) {}

public virtual void OnRoomClientAddPlayerFailed() {}
```