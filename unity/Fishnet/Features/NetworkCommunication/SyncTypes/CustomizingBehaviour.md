SyncTypes 具有专属的设置项和属性，支持通过多种方式自定义你的 SyncType。

## SyncTypeSettings

SyncTypeSettings 可以为任何 SyncType 初始化，来定义 SyncType 的默认设置。

```C#
//Custom settings are optional.
//This is an example of declaring a SyncVar without custom settings.
private readonly SyncVar<int> _myInt = new();

//Each SyncType has a different constructor to take settings.
//Here is an example for SyncVars. This will demonstrate how to use
//the unreliable channel for SyncVars, and send the value upon any change.
//There are many different ways to create SyncTypeSettings; you can even
//make a const settings and initialize with that!
private readonly SyncVar<int> _myInt = new(new SyncTypeSettings(0f, Channel.Unreliable));
```

这些设置还可在运行时动态调整。根据游戏机制需求灵活变更行为特性，或在玩家数量增加时降低数据发送频率，这种实时配置能力显得尤为实用。

```C#
//This example shows in Awake but this code
//can be used literally anywhere.
private void Awake()
{
    //You can change all settings at once.
    _myInt.UpdateSettings(new SyncTypeSettings(....));

    //Or update only specific things, such as SendRate.
    //Change send rate to once per second.
    _myInt.UpdateSendRate(1f);
}
```

## Showing In The Inspector

SyncTypes 还可以在 inspector 中显示。

如果 type 为容器，你必须首先确保你的 type 被标记为 serializable。这是一个 Unity 需求。

```C#
//SyncTypes can be virtually any data type. This example
//shows a container to demonstrate the serializable attribute.
[System.Serializable]
public struct MyType { }
```

接下来需要注意：​SyncType 禁止使用 readonly 标记。我们默认要求启用该标记，旨在强调 ​SyncType 不应在运行时初始化。

下面是错误示例：

```C#
private SyncVar<int> _myInt = new();

private void Awake()
{
    //This would result in errors at runtime.

    //Do not make a SyncType into a new instance
    _myInt = new();
    //Do not set a SyncType to another instance.
    _myInt = _someOtherDeclaredSyncVar.
}
```

上述代码会导致编辑器直接报错无法编译——因为我们的代码生成器会检测到你未添加 readonly 标记。若需移除该只读限制，必须在 SyncType 声明前添加 AllowMutableSyncType 特性。

```C#
//This will work and show your SyncType in the inspector!
[AllowMutableSyncType]
[SerializeField] //Be sure to serializeField if not public.
private SyncVar<int> _myInt = new();
```
