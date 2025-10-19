# Network Scene Checker

Network Scene Checker 组件控制 network clients 的 gameobjects 的可见性，基于它们在哪个 scene。

![NetworkSceneChecker](../../Image/NetworkSceneChecker.png)

- Force Hidden

  勾选这个选项为所有 players 隐藏这个 object

使用 Network Scene Checker，运行在一个 client 上的 game 没有关于不可见的 gameobjects 的信息。这又两个好处，它减少了在网络上发送的数据量，以及使游戏对于 hacking 更加安全。

这个组件通常地被用于当 server 有一些加载的 subscenes，并且需要隔离 networked objects 到它们所在的 subscene。

一个具有 Network Scene Checker 组件必须具有 Network Identity 组件。

具有一个 Network Scene Checker 组件的 Scene objects 如果不在同一个 scene 的话是 disabled 的，并且 spawned objects 如果不在同一个 scene 时将被销毁。

## Use with Additive Scenes

在 Mirror 中，Server 和 connected Clients 总是在相同的 main scene。然而 Server 和 Clients 可以有各种不同的额外加载的小 subscenes 的各种组合。Server 可能在开始时加载所有 subscenes，或者它可能动态加载和卸载 players 或其他活动将要发生的 subscenes。

所有 player objects 在 main scene 总是先 spawned，这可能有可能没有可视内容，networked objects 等等。使这个组件附加在所有 networked objects，无论何时 player object 被移动到一个 subscene（从 main 或者从另一个 subscene），在新 scene 和之前的 scene 的 observers 列表都会相应更新。

在 server 上加载 subscenes 是通过正常的 SceneManager 的过程：

```C#
SceneManager.LoadSceneAsync(subScene, LoadSceneMode.Additive);
```

接下来，你将发送一个 SceneMessage 到 client 告诉它也加载一个 subscene：

```C#
SceneMessage msg = new SceneMessage
{
    sceneName = subScene,
    sceneOperation = SceneOperation.LoadAdditive
};

connectionToClient.Send(msg);
```

然后，只在 server 上，你只移动 player object 到 subscene：

```C#
// Position the player object in world space first
// This assumes it has a NetworkTransform component that will update clients
player.transform.position = new Vector3(100, 1, 100);

// Then move the player object to the subscene
SceneManager.MoveGameObjectToScene(player, subScene);
```

可选地，你可以发送另一个 SceneMessage 到 client，带有 SceneOperation.UnloadAdditive 来移除任何之前的 client 不在需要的 additive scene。这将应用到一个在一个 level change 之后具有 levels 的游戏。在移除之前可能需要一个很短的延迟来允许  client 完全得到同步。

依赖于你的游戏的复杂性，你可能发现当在 subscenes 之间切换一个 player，来将一个 player object 首先移动到 main scene，yield 100 ms，re-position 它，最后将它移动到新的 subscene 非常有用。
