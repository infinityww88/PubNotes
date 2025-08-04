Scene Caching 是 Server 的能力，可以保持 scene 加载，而或者所有 clients 已经从那个 scene 卸载，或者停止观察那个 scene。

## General

当加载一个 scene，你可以在 SceneLoadData 指定当所有 clients 卸载时是否 AutomaticallyUnload scene，还是将 scene 留作 observer.

当卸载 Scene 时，你可以通过设置 ServerUnloadMode 来覆盖 AutomaticallyUnload 选项。

```C#
//When Loading Scenes.
SceneLoadData sld = new SceneLoadData("MainScene");
sld.Options.AutomaticallyUnload = false;

//When Manually Unloading Scenes.
//Whatever you set the ServerUnloadMode to here will override the AutomaticallyUnload
//setting you used when loading the scene earlier.
SceneUnloadData sud = new SceneUnloadData("MainScene");
sud.Options.Mode = ServerUnloadMode.KeepUnused;
```

## Host Behaviour

在 Hosts Server 需要保持场景加载，而 Hosts Client 却被要求卸载该场景的情况下，Hosts Client 不会直接卸载场景，而是通过观察者系统将其从场景中移除，并更新客户端的场景可见性。

作为 Host，服务器和客户端共享同一份已加载场景及游戏对象的实例。如果 Host Client 实际执行场景卸载操作，服务器端的对应场景也会被同步卸载。

必须在 ObserverManager 中设置 Scene Condition，以利用这个能力，来使 server 保持 scene 加载，并且 host client 不会看见场景中的 objects。

这通常意味着每个带有 mesh 的 GameObject 必须具有一个 NetworkObject 组件，如果你想要 Host Client 不会看见 scene。
