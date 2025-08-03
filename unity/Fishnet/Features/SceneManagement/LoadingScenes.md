## General

本指南将介绍如何设置和加载新场景、如何加载到现有场景中、如何替换场景，以及场景加载过程中底层运作的高级信息。

通过内置的DefaultScene组件，创建一个简单的 online 和 offline 场景非常容易。

若使用 ObserverManagers 的场景条件，以全局方式或按 connection 加载场景时，会将指定的客户端 connection 作为观察者添加到场景中。全局加载会将所有客户端都添加为观察者，而按连接加载则仅添加指定的连接。有关更多信息，请参阅“场景可见性”。

在以下示例中，所有的 SceneManager 调用都是在 NetworkBehaviour 类内部完成的，这就是为什么你可以通过 base.SceneManager 获取对 SceneManager 的引用。
如果你想在其他地方（非 NetworkBehaviour 类中）获取引用，可以考虑使用 FishNets 的 InstanceFinder.SceneManager。

## Setup

在调用 SceneManager 的加载场景函数之前，您需要先设置加载数据，以告知 SceneManager 您希望它如何处理场景加载。

- SceneLookupData（场景查找数据）

  SceneLookupData 是用于指定希望 SceneManager 加载哪个场景的类。您无需手动创建查找数据，而是使用 SceneLoadData 的构造函数，这些构造函数会自动为您创建 SceneLookupData。

- SceneLoadData（场景加载数据）

  无论以何种方式加载场景，您都必须将一个 SceneLoadData 类的实例传入加载方法中。该类为 SceneManager 提供了正确加载一个或多个场景所需的所有信息。

  SceneLoadData 提供的构造函数会根据您是加载新场景还是加载已有的场景实例，自动创建 SceneManager 所需的 SceneLookupData。

## Loading New Scenes

场景可以全局加载，也可以针对一组客户端连接进行加载。

**加载新场景时只能通过名称（Name）加载，不能使用句柄（Handle）或场景引用（Scene References）。**

### 全局场景（Global Scenes）

全局场景可以通过调用 `SceneManager` 中的 `LoadGlobalScenes()` 方法来加载。

当以全局方式加载时，场景将为所有当前已连接的客户端以及未来新连接的客户端加载。

```csharp
SceneLoadData sld = new SceneLoadData("Town");
base.SceneManager.LoadGlobalScenes(sld);
```

### 连接场景（Connection Scenes）

连接场景遵循相同的原理，但提供了几种不同的方法重载（overloads）。

您可以针对单个连接加载场景，也可以一次性为多个连接加载场景，或者仅在服务器端加载场景，为后续连接做准备。

当通过连接加载场景时，只有您指定的连接才会加载这些场景。

您还可以随时将额外的连接添加到已加载的场景中。

```csharp
SceneLoadData sld = new SceneLoadData("Main");

// 为单个连接加载场景
NetworkConnection conn = base.Owner;
base.SceneManager.LoadConnectionScenes(conn, sld);

// 一次性为多个连接加载场景
NetworkConnection[] conns = new NetworkConnection[] { connA, connB };
base.SceneManager.LoadConnectionScenes(conns, sld);

// 仅在服务器端加载场景。可用于预加载您不希望所有玩家都进入的场景
base.SceneManager.LoadConnectionScenes(sld);
```

### 加载多个场景（Loading Multiple Scenes）

无论是全局加载还是按连接加载，您都可以在单次方法调用中加载多个场景。

当您在单次调用中加载多个场景时，您放入 `Moved NetworkObjects` 中的网络对象（NetworkObjects）将被移动到您尝试加载的场景列表中的第一个有效场景。有关在场景之间保持网络对象的更多信息，请参阅“持久化网络对象（Persisting NetworkObjects）”。

```csharp
// 为多个连接加载多个场景
string[] scenesToLoad = new string[] { "Main", "Additive" };
NetworkConnection[] conns = new NetworkConnection[] { connA, connB, connC };

SceneLoadData sld = new SceneLoadData(scenesToLoad);
base.SceneManager.LoadConnectionScenes(conns, sld);
```

## Loading Existing Scenes

若场景已在服务器上加载，且你想将客户端加载到该场景实例中，建议通过场景引用（Scene Reference）或句柄（Handle）查找场景，以确保获取到准确的目标场景。

按名称加载场景时，系统会将连接加载到首个匹配名称的场景中。若启用了场景堆叠（Scene Stacking），可能存在多个同名场景，此时按名称加载需格外注意。

若利用场景缓存（Scene Caching）功能（即在所有客户端离开后仍保留场景及其当前状态），可向无其他客户端的场景中加载客户端。

以下是使用 FishNet 的 SceneManager 获取已加载场景引用的几种方法：

### By Event

```C#
// Manage your own collection of SceneRefernces/Handles
// Customize how you want to manage you scene references so its easy
// for you to find them later.
List<Scene> ScenesLoaded = new();

public void OnEnable()
{
    InstanceFinder.SceneManager.OnLoadEnd += RegisterScenes;
}

public void RegisterScenes(SceneLoadEndEventArgs args)
{
    //Only Register on Server
    if (!obj.QueueData.AsServer) return;
    
    //if you know you only loaded one scene you could just grab index [0]
    foreach(var scene in args.loadedScenes)
    {
        ScenesLoaded.Add(scene);
    }
}

public void OnDisable()
{
    InstanceFinder.SceneManager.OnLoadEnd -= RegisterScene;
}
```

### By Connection

```C#
//NetworkConnections have a list of Scenes they are currently in. 
int clientToLookup;
InstanceFinder.ServerManger.Clients[clientToLookup].Scenes;
```

### By SceneManager.SceneConnections

```C#
// SceneManager Keeps a Dictionary of All Connection Scenes as the Key
// and the client connections that are in that scene as the value.
NetworkConnection conn;
Scene sceneNeeded;

//Get the scene you need with foreach or use Linq to filter your conditions.
foreach(var pair in SceneManager.SceneConnections)
{
    if(pair.Value.Contains(conn))
    {
        sceneNeeded = pair.Key;
    }
}
```

### 使用 Reference 加载到现有 Instance

使用上述方法获取场景的引用或句柄，然后利用该引用或句柄将客户端加载到现有场景中。

```C#
scene sceneReference;
NetworkConnection[] conns = new(){connA,connB};

//by reference
SceneLoadData sld = new(sceneReference);
base.SceneManager.LoadConnectionScenes(conns,sld);

//by handle
SceneLoadData sld = new(sceneReference.handle);
base.SceneManager.LoadConnectionScenes(conns,sld);
```

## Replacing Scenes

Fishnet 提供了能力来用请求加载的 scenes 替换已经在 clients 上加载的 scenes。

要 Replace Scenes，你需要在 SceneLoadData 中设置 ReplaceScene 选项。

被替换的 scenes 在新 scenes 加载之前会被卸载。

要替换的 scenes 默认会将 server 和 clients 的 scenes 都替换。如果你想要 server 保持 scene 加载，只替换 clients 的 scene。

### Replace None

这是加载时的默认方法，它会忽略 replace options，并正常地加载 scenes。

### Replace All

这回替换当前加载到 Unity 中的所有 scenes，即使那些不是被 FishNet.SceneManager 管理的 scenes。

```C#
//Replace All Option.
SceneLoadData sld = new SceneLoadData("DungeonScene");
sld.ReplaceScenes = ReplaceOption.All;

//This will replace all Scenes loaded by FishNet or outside of FishNet like Unity,
//and load "DungeonScene"
SceneManager.LoadGlobalScenes(sld);
```

### Replace Online Only

这个选项只会替换 FishNet.SceneManager 管理的 scenes。

```C#
//Replace Online Only Option.
SceneLoadData sld = new SceneLoadData("DungeonScene");
sld.ReplaceScenes = ReplaceOption.OnlineOnly;

//This will replace only scenes managed by the SceneManager in FishNet.
SceneManager.LoadGlobalScenes(sld);
```

### Advanced Info

- Scenes 的幕后

  SceneManager 类有非常详细的 XML 注释，关于 load process 如何工作的详细细节。如果向调试 scene 加载的相关问题，这些注释会帮助你理解一个 scene 加载的流程。

- Events

  确保查看 Scene Events，可以订阅来更好地控制游戏。

## Automatic Online and Offline Scenes

使用 DefaultScene 组件自动化管理简单的 scene 设置。

如果你想寻找一种简单的方法在 network 开始或停止时管理 scene transitions，FishNet 有一个简单的方式来管理它，而无需任何 code。DefaultScene 组件是一个 ready-made solution，当 network 开始时，它自动加载你指定的 online scene，当 network 关闭时，自动卸载 offline scene。

这非常适合想要 plug-and-play 设置而不想编写代码的开发者。

## Setup Instructions

- 添加 DefaultScene 组件到 NetworkManager GameObject
- 在 Inspector 种，指定你的 Offline Scene 和 Online Scene
- 确保两个 Scene 时不同的。使用同一个 scene，会阻止组件正常工作
