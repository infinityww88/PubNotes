## General

就像 NetworkObject 对比 GameObject，NetworkBehaviour 对比 MonoBehaviour，Spawn 对比 Instantiate，都是用 Fishnet 联网版本代替 Unity 单机版本。同样，场景加载也是如此，用 Fishnet SceneManager 代替 Unity SceneManager 跨网络管理场景，即在 server 和多个 clients 之间管理场景的加载和卸载。

卸载 scenes 和加载 scenes 相同，只是调用 Unload 而不是 Load。Scenes 可以通过 connection 加载 Scenes，或者全局加载。卸载全局 scenes 会对所有 players 卸载。当按 connection 卸载时，只有指定的 connections 卸载 scenes。

## Unloading Scenes

### Global Scenes

- Global Scenes 可以通过调用 SceneManager.UnloadGlobalScenes() 卸载
- 不可以使用 UnloadConnectionScenes() 方法卸载 global scenes

```C#
SceneUnloadData sud = new SceneUnloadData("Town");
base.NetworkManager.SceneManager.UnloadGlobalScenes(sud);
```

### Connection Scenes

Connection Scenes 遵循相同的原则，但是有一些重载的方法。你可以为一个 connection，同时为多个 connections 卸载 scenes，或者在 server 上卸载 scenes。

- 如果所有 connections 都从一个 scene 卸载，Server 只会从自身上卸载那个 connection scene
- 如果你希望卸载一个 scene 和所有 connections，获取 scene 中的所有 connections，然后对那些 connections 调用 unload。SceneManager.SceneConnections 保存所有 online scenes 和其中的 connections
- 如果想卸载所有 Connections 时，保持 scene 在 server 上加载，使用 Scene Caching

```C#
SceneUnloadData sud = new SceneUnloadData(new string[] { "Main", "Additive") });

//Unload scenes for a single connection.
NetworkConnection conn = base.Owner;
base.NetworkManager.SceneManager.UnloadConnectionScenes(conn, sud);

//Unload scenes for several connections at once.
NetworkConnection[] conns = new NetworkConnection[] { connA, connB };
base.NetworkManager.SceneManager.UnloadConnectionScenes(conns, sud);

//Unload scenes only on the server.
//that you don't want all players in.
base.NetworkManager.SceneManager.UnloadConnectionScenes(sud);
```

### Advanced Info

- Scenes 的幕后

  SceneManager 类有非常详细的 XML 注释，关于 load process 如何工作的详细细节。如果向调试 scene 加载的相关问题，这些注释会帮助你理解一个 scene 加载的流程。

- Events

  确保查看 Scene Events，可以订阅来更好地控制游戏。
