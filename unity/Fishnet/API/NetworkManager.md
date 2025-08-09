# NetworkManager

## Properties

以下方法是 NetworkObject/NetworkBehaviour 对应属性访问的信息。针对的是网络框架是否启动（Client、Server、Host）

- IsClientOnlyStarted
- IsClientStarted
- IsHost
- IsHostStarted
- IsServerStarted
- IsServerOnlyStarted

因为 NetworkManager 处理的是整个网络框架。除了这些属性，NetworkObject/NetworkBehaviour 还包含 Initialized 版本，指示的是 Object 是否初始化，而不是框架是否初始化。

除此以外，以下属性在 NetworkObject/NetworkBehaviour 也有对应的属性，访问的都是 NetworkManager 的信息：

- IsOffline

- ClientManager

- ServerManager

- DebugManager

- bool Initialized

  NetworkManager 实例是否已初始化。

- SceneManager

- ServerManager

- TimeManager

- TransportManager

- ObserverManager

- RollbackManager

- StaticsticsManager

下面的属性是 NetworkManager 的专用属性，NetworkObject 和 NetworkBehaviour 没有提供相应的访问属性：

- ObjectPool
- SpawnablePrefabs

## 方法

### Pool 操作

- void CacheObjects(NetworkObject prefab, int count, bool asServer)

  预热一组 objects 并添加到 pool 中

- NetworkObject GetPooledInstantiated(NetworkObject prefab, Transform parent, bool asServer)

### Spawnable Prefab 操作

- NetworkObject GetPrefab(int prefabId, bool asServer)

- int GetPrefabIndex(GameObject prefab, bool asServer)

- PrefabObjects GetPrefabObjects<T>(ushort spawnableCollectionId, bool createIfMissing)

### 注册全局实例

- bool HasInstance<T>()
- T GetInstance<T>()
- void RegisterInstance<T>(T component, bool replace = true)
- void RegisterInvokeOnInstance<T>(Action<Component> handler)
- void UnregisterInstance<T>()
- void UnregisterInvokeOnInstance<T>(Action<Component> handler)
