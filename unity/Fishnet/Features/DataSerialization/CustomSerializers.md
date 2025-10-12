自定义序列化器在以下场景中非常有用：当自动序列化不可行时，或者你需要以特定方式序列化数据时。

创建自定义序列化器时需要注意几个关键点：只要按照正确步骤操作，Fish-Networking 就能自动识别并使用你的自定义序列化器。你的自定义序列化器可以覆盖自动序列化器，但无法覆盖内置的序列化器。

- 方法必须是 static，并且在一个 static class
- 写方法名字必须以 Write 开始
- 读方法名字必须以 Read 开始
- 第一个参数必须是 this Writer，或者 this Reader
- Data 必须以和写入相同的顺序读取

尽管 Vector2 已经被支持，下面的例子使用 Vector2 进行展示：

```C#
// Write each axis of a Vector2.
public static void WriteVector2(this Writer writer, Vector2 value)
{
    writer.WriteSingle(value.x);
    writer.WriteSingle(value.y);
}

// Read and return a Vector2.
public static Vector2 ReadVector2(this Reader reader)
{
    return new Vector2()
    {
        x = reader.ReadSingle(),
        y = reader.ReadSingle()
    };
}
```

自定义序列化器通常用于条件性场景——即写入内容会根据数据值动态变化的情况。下面是一个更复杂的示例，展示如何仅在必要时写入特定数据。

```C#
/* This is the type we are going to write.
* We will save data and populate default values
* by not writing energy/energy regeneration if
* the enemy does not have energy. */
public struct Enemy
{
    public bool HasEnergy;
    public float Health;
    public float Energy;
    public float EnergyRegeneration;
}

public static void WriteEnemy(this Writer writer, Enemy value)
{
    writer.WriteBoolean(value.HasEnergy);
    writer.WriteSingle(value.Health);
    
    // Only need to write energy and energy regeneration if HasEnergy is true.
    if (value.HasEnergy)
    {
        writer.WriteSingle(value.Energy);
        writer.WriteSingle(value.EnergyRenegeration);
    }
}

public static Enemy ReadEnemy(this Reader reader)
{
    Enemy e = new Enemy();
    e.HasEnergy = reader.ReadBoolean();
    e.Health = reader.ReadSingle();
    
    // If there is energy also read energy values.
    if (e.HasEnergy)
    {
        e.Energy = reader.ReadSingle();
        e.EnergyRenegeration = reader.ReadSingle();
    }

    return e;
}
```

创建自定义序列化器时，若希望其在整个项目及所有程序集中通用，需注意：

默认情况下，自定义序列化器仅在其所属程序集中生效。

若需全局使用，只需为该序列化器所针对的类型添加 [UseGlobalCustomSerializer] 特性即可。

```C#
[UseGlobalCustomSerializer]
public struct Enemy
{
    public bool HasEnergy;
    public float Health;
    public float Energy;
    public float EnergyRegeneration;
}
```
