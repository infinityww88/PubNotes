# Network Room Player

Network Room Player 在 room 时为 Network Room Manager 存储 per-player 的状态.当使用这个组件，你需要编写一个 script，其允许 players 通过设置 ReadyToBegin 属性指示它们已经准备好开始。

一个具有 Network Room Player 组件的 gameobject 必须有一个 Network Identity 组件。当你在一个 gameobject 创建一个 Network Room Player 组件时，Unity 还会创建一个 Network Identity 组件，如果它上面还没有的话。

![NetworkRoomPlayer](../../Image/NetworkRoomPlayer.png)

- Show Room GUI

  在 room 中为 players 显式开发者 GUI。这个 UI 只是用来方便开发。默认开启

- Ready To Begin

  指示 player 已经准备好

- Index

  player 的 index，Player 1，Player 2，等等

- Network Sync Interval

  信息从 Network Room Player 发送到 server 的速率

## Methods

### Client Virtual Methods

```C#
public virtual void OnClientEnterRoom() {}

public virtual void OnClientExitRoom() {}

public virtual void OnClientReady(bool readyState) {}
```
