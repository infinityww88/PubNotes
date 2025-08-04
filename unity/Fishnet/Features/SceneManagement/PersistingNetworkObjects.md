这里细介绍用户在场景加载和卸载过程中，用于持久化 ​NetworkObjects（网络对象）​​的可用选项。

类似 Unity DontDestroyOnLoad 场景在多个场景中持久化 GameObject，这里是在网络场景中持久化 NetworkObject。

## General

用户可选择的 ​NetworkObjects（网络对象）​​ 跨场景持久化方案，取决于该 NetworkObject 的类型。

## Spawned NetworkObjects

对于不属于下述其他类别的动态生成网络对象（Spawned NetworkObjects）​，可通过在加载下一场景时移动这些对象来实现跨场景持久化。

当调用 SceneManager ​的加载方法时，传入的场景加载数据（SceneLoadData）​包含一个数组，可你所有需要传送到新加载场景的动态生成网络对象（Spawned NetworkObjects）​填充至该数组中。

SceneManager ​会自动正确处理这些对象，若你尝试传送不允许的游戏对象（GameObject），系统还将触发调试警告。

若你在一次方法调用中加载多个场景，并通过 ​SceneLoadData​ 移动 NetworkObjects，则这些被移动的 NetworkObject 将仅进入首个有效请求的场景。

```C#
// Just Create an array of NetworkObjects 
// that are not a Scene, Global or Nested NetworkObjects.
NetworkObject[] objectsToMove = new NetworkObject[] { object1, object2, object3 }

// Assign this array to the SceneLoadData before you Load a Scene.
SceneLoadData sld = new SceneLoadData("NewScene");
sld.MovedNetworkObjects = objectsToMove;

// Fishnet will handle the rest after loading!
SceneManager.LoadGlobalScenes(sld);
```

## Scene NetworkObject

当前，​场景网络对象（Scene NetworkObjects）​​无法实现跨场景持久化——这是由 Unity 和 FishNet 的底层设计机制所决定的技术限制。你既不能将其标记为 ​全局对象（Global）​，也无法将其置于 ​​"不随场景销毁"（DontDestroyOnLoad）​​ 场景中。

若需实现跨场景持久 persist，建议移除该场景网络对象，并改用本页介绍的其他可行方案。

## Global NetworkObjects

全局网络对象（Global NetworkObjects）​的工作原理类似于普通 ​GameObject​ 被放入 ​​"不随场景销毁"（DontDestroyOnLoad，简称 DDOL）​​ 场景时的行为。

在场景加载和卸载过程中，​全局网络对象​ 会始终保留在服务器和客户端的 ​​(DDOL) 场景​ 中，并维持其状态不变，​无需额外操作。

若要将某个 ​NetworkObject​ 设为全局对象，只需在其组件上将 ​IsGlobal​ 布尔值设为 ​true​ 即可。

通常情况下，客户端始终作为 ​DDOL 场景​ 的观察者存在。因此，​全局网络对象（Global NetworkObjects）​​ 更适用于 ​管理器类型（Manager）​​ 的游戏对象，而非带有网格渲染的实体对象——但这并非强制限制，您仍可灵活选择。

## Nested NetworkObject

Unity 不允许将**嵌套游戏对象（Nested GameObjects）**移动到其他场景中。

不过，FishNet 会自动检测你是否尝试发送**嵌套网络对象（NestedNetworkObject）**，若检测到，将仅发送该对象的**根对象（root）**。
