# SceneManager

## Properties

- NetworkManager

- SceneConnections

  Dict<Scene, HashSet<NetworkConnection>> SceneConnections

  每个 scene 包含的 connections。

## 方法

- void AddConnectionToScene(NetworkConnection conn, Scene scene)

  将一个 connection 添加到 scene。

  这个方法每次调用只处理一个 connection。因为 connections 只有在单独验证加载场景成功后才会被添加。

  这个功能只建议高级用户使用，谨慎使用。

  注意 Fishnet.SceneManager 和 Unity.SceneManager 管理和使用的 scene 是一样的 scene。在网络上（Server-Client）之间同步加载 scene 时，只需要传递 scene 名字，然后各个 instance 在本地寻找相应的 scene，各自加载。

- AddOwnerToDefaultScene(NetworkObject)

  如果没有 global scenes，添加 NetworkObject 的 owner 到其所在的 scene 中。

- static Scene GetScene(int sceneHandle)

  根据 handle 返回一个 scnee。

- static Scene GetScene(string sceneName, NetworkManager nm = null, bool warnIfDuplicates = true)

- void LoadConnectionScenes(NetworkConnection, SceneLoadData)

  在 server 上加载 scenes，告诉 connections 也一样加载它们。为指定的 connections 不会加载指定的 scenes。

- LoadConnectionScenes(NetworkConnection[], SceneLoadData)

- LoadConnectionScenes(SceneLoadData)

  只在 server 加载 scene，不告诉 clients 同样进行加载。

- LoadGlobalScenes

  为 server 和所有 clients 加载场景。未来的 clients 会自动加载这些 scenes。Server 上记录这些 global scenes，clients 连接到 server 时，server 告诉 clients 加载这些 scenes。只需要传递场景 names，所有 scenes 在每个 instance 上都有相同的副本。

  注意 scenes 和 prefab 一样（或就认为是 prefab 即可，只是可以通过名字加载）。

- void RemoveAllConnectionsFromScene(Scene scene)

  从一个 scene 移除所有 connections。

  参数是 UnityEngine.SceneManagement.Scene。

- void RemoveConnectionsFromNonGlobalScenes(NetworkConnection[] conns)

  从任何不是 global 的 scene 移除 connections。只建议高级用户使用，谨慎使用。

- void RemoveConnectionsFromScene(NetworkConnection[] conns, Scene scene)

  未指定 scene 移除 connections。

- void UnloadConnectionScenes(NetworkConnection connection, SceneUnloadData sceneUnloadData)

  在 server 上卸载 scenes，并通知指定 connection 一样卸载它们。其他 connections 不会卸载它们。

- void UnloadConnectionScenes(NetworkConnection[] connections, SceneUnloadData sceneUnloadData)

- void UnloadConnectionScenes(SceneUnloadData sceneUnloadData)

- void UnloadGlobalScenes(SceneUnloadData sceneUnloadData)
