另一个常见问题是如何处理被多个其他类继承的基类的序列化问题。这类基类通常用于让RPC能够以基类作为参数类型，同时允许派生类作为实际参数传入。这种设计思路与接口序列化的实现方式颇为相似。

## Class Example

下面的例子是一个你可以序列化的类，并有两个类型继承它。

```C#
public class Item : ItemBase
{
    public string ItemName;
}

public class Weapon : Item
{
    public int Damage;
}

public class Currency : Item
{
    public byte StackSize;
}

/* This is a wrapper to prevent endless loops in
* your serializer. Why this is used is explained
* further down. */
public abstract class ItemBase {}
```

使用一个采用上面所有类型的 RPC 看起来如下所示：

```C#
public void DoThing()
{
    Weapon wp = new Weapon()
    {
        Itemname = "Dagger",
        Damage = 50,
    };
    ObsSendItem(wp);
}

[ObserversRpc]
private void ObsSendItem(ItemBase ib)
{
    /* You could check for other types or just convert it without checks
    *  if you know it will be Weapon.
    *  EG: Weapon wp = (Weapon)ib; */
    if (ib is Weapon wp)
        Debug.Log($"Recv: Item name {wp.ItemName}, damage value {wp.Damage}.");
}
```

### Creating The Writer

由于RPC接收的是ItemBase基类参数，因此必须处理可能传入的不同派生类情况。下方展示的序列化器正是为此设计的解决方案。

采用这种处理方式时，必须优先检查最底层的子类类型，这一点至关重要。

举例说明：Weapon（武器）类要排在Item（物品）类之前，Currency（货币）类同理——这两个类型会优先被检测。这就好比存在Melee（近战武器）: Weapon（武器）的继承关系时，Melee类型就会优先于Weapon类型被检查，以此类推。

```C#
public static void WriteItembase(this Writer writer, ItemBase ib)
{
    if (ib is Weapon wp)
    {
        // 1 will be the identifer for the reader that this is Weapon.
        writer.WriteByte(1); 
        writer.Write(wp);
    }
    else if (ib is Currency cc)
    {
        writer.WriteByte(2)
        writer.Write(cc);
    }
    else if (ib is Item it)
    {
        writer.WriteByte(3)
        writer.Write(it);
    }
}

public static ItemBase ReadItembase(this Reader reader)
{
    byte clsType = reader.ReadByte();
    /* These are still in order like the write method, for
    *  readability, but since we are using a clsType indicator
    *  the type is known so we can just compare against the clsType. */
    if (clsType == 1)
        return reader.Read<Weapon>();
    else if (clsType == 2)
        return reader.Read<Currency>();
    else if (clsType == 3)
        return reader.Read<Item>();
    // Unhandled, this would probably result in read errors.
    else
        return null;
}
```

除了封装处理通用情况之外，您仍然可以为单个类创建自定义序列化器！举个例子，如果您为Currency类编写了专属序列化器，那么上述代码在执行时就会优先调用您自定义的Currency序列化器，而不会使用Fish-Networking自动生成的版本。

最后，我们来说明设计ItemBase基类的原因。该类的唯一作用就是防止读取器陷入无限循环。试想一下，如果我们只返回Item类型，并且同时将其作为基类使用，那么您的读取器代码可能会变成这样...

```C#
public static Item ReadItem(this Reader reader)
{
    byte clsType = reader.ReadByte();
    /* These are still in order like the write method, for
    *  readability, but since we are using a clsType indicator
    *  the type is known so we can just compare against the clsType. */
    if (clsType == 1)
        return reader.Read<Weapon>();
    else if (clsType == 2)
        return reader.Read<Currency>();
    else if (clsType == 3)
        return reader.Read<Item>();
    // Unhandled, this would probably result in read errors.
    else
        return null;
}
```

问题就出在 return reader.Read<Item>(); 这行代码上。当你在同一个序列化器中调用相同类型的读取方法时，会导致系统反复执行 ReadItem 方法——先执行一次 return reader.Read<Item>();，接着再次调用 ReadItem，然后又是 return reader.Read<Item>();... 如此循环往复，相信您已经明白问题所在了。

而通过引入 ItemBase 这样的基类（该基类本身不能作为返回类型），我们就能从根本上杜绝这种无限循环的情况发生。