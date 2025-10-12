SyncVar 是服务端到客户端自动同步值，DataSerialization 是 Rpc 或 SyncVar 如何序列化数据（参数）。

为在网络间传输数据而进行的序列化与反序列化处理。

当你在通信过程中使用任何类型时，Fish-Networking 会自动识别该类型的序列化器（或为其创建一个）。FishNet 仅会尝试自动序列化公共字段和属性。此过程无需你执行任何额外操作，但若希望排除某些字段的序列化，请在该字段上方添加 [System.NonSerialized] 特性。

例如，Name 和 Level 字段会被发送到网络中，但 Victories 字段不会。

```C#
public class PlayerStat
{
    public string Name;
    public int Level;
    [System.NonSerialized]
    public int Victories;
}

[ServerRpc]
public void RpcPlayerStats(PlayerStat stats){}
```

Fish-Networking 还支持继承值的序列化。如下所示的 MonsterStat 类型中，Health（生命值）、Name（名称）和 Level（等级）字段将自动进行序列化处理。

```C#
public class Stat
{
    public float Health;
}
public class MonsterStat : Stat
{
    public string Name;
    public int Level;
}
```

在极少数情况下，某些数据类型无法自动序列化，例如 Sprite 类型。直接序列化其包含的实际图像数据并传输会非常困难且成本高昂。
替代方案包括：将精灵存储在集合中并发送集合索引，或自定义序列化器实现特定处理逻辑

FishNet 应该能够自动序列化许多基本的 C# 和 Unity 类型，以及由可序列化类型构成的类和结构体。

## NonSerialized Attribute

该属性属于 System 命名空间，可用于阻止字段在使用自定义类型时通过网络进行序列化。需注意，标记为 NonSerialized 的字段将无法在 Inspector 面板中显示，且无法被 JsonUtility 等其他序列化器处理

```C#
public class PlayerStats
{
    public float Health;
    public float MoveSpeed;
    /* In this example ControllerIndex is only used
     * for local multiplayer. This data does not need to be sent
     * over the network so it's been marked with NonSerialized. */
    [System.NonSerialized]
    public int ControllerIndex;
}
```

