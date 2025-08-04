Scene Visibility​ 详细介绍了如何使用 ​ObserverManager​ 配合 ​​"场景条件"（Scene Condition）​，以及如何在场景中管理观察者（Observers）。

## General

你可以控制 clients 是否变成它们所在 scene 的 gameobjects 的 Observer。这是可能的，如果你设置 ObserverManager 包含一个 Scene Condition。

Scene Condition 确保 NetworkObjects（无论是 Scene 中还是 Spawned 的）只对与该对象处于同一个 scene 中的 players 可见。绝大多数情况下，你会想要添加一个具有 scene condition 的 NetworkObserver 组件到 networked objects。

如果在场景切换时遇到 ​找不到 NetworkObject 或 RPCLink​ 的错误，你很可能 ​忘记添加场景条件（Scene Condition）​​ 了。

## Managing Visibility

### Initial Scene Load

当一个 client 首次加载到游戏中，第一个加载的 scene/offline-scene 是通过 Unity Scene Manager 完成的。这意味着当连接时，clients 不是自动添加到 scene 中的（因为网络场景需要 Fishnet.SceneManager 管理）。这也意味着它们没有那个场景的 visibility。

一旦 client 连接到 host 或 server，如果你使用 NetworkManager 上 Fishnet 提供的 PlayerSpawner 组件，这个组件中具有添加 client 到 Player Objects 生成的 default scene 的逻辑。

如果你决定不使用 NetworkManager 上的 PlayerSpawner 组件，你或者需要使用 Fishnets SceneManager 将 client 添加到场景中，或者在你赋予 client ownership 的 Object 上调用 SceneManager.AddOwnerToDefaultScene()。

### Adding Client Connections To Scenes

- 当全局或按 connection 加载一个场景，ServerManager 会自动将那个 connection 放在 scene 中
- 添加后，该客户端将能够查看属于该场景的所有 ​NetworkObjects（网络对象）​。
- 你可以手动添加 Client Connections 到 Scenes 中，如果 scene 已经在 client 上加载了，通过 SceneManager.AddConnectionsToScene()

手动添加和移除 client connections 只建议 Power Users 使用。

### Removing Client Connections From Scenes

- 当从 client 卸载一个场景，server 会从那个 scene 中移除 client connection
- 如果你是 host，并且你从一个 scene 卸载 hosts client，它只会从那个场景中移除 host，并且 hosts client 失去可见性
- 你可以手动从一个加载的场景中移除一个 client，通过使用 SceneManager.RemoveConnectionsFromScene()
