# 数据类型

Client 和 server 可以通过 Remote methods，State Synchronization 或 Network Messages 彼此之间传递数据。

Mirror 支持很多 data types，你可以使用它们，包括：

- 基本 C# 类型 (byte, int, char, uint, UInt64, float, string, etc)
- 内置的 Unity 数据类型 (Vector3, Quaternion, Rect, Plane, Vector3Int, etc)
- NetworkIdentity
- 带有 NetworkIdentity 组件的 Game object 
- 包含任何上述类型的 Struct
  - 建议实现 IEquatable<T> 来避免 boxing，并且是 stuct 只读，因为修改一个字段不会导致一个 resync
- 每个字段都是受支持 data type 的 classes
  - 这将分配 garbage，并且它们每次被发送时，将会在接收者实例化一个新的
- 每个字段都是受支持 data type 的 ScriptableObject
  - 这将分配 garbage，并且它们每次被发送时，将会在接收者实例化一个新的
- 上述任何类型的数组
  - SyncVars 和 SyncLists 不支持。不支持数组同步变量
- 上述任何类型的 ArraySegments
  - SyncVars 和 SyncLists 不支持。不支持数组同步变量

## Game Objects

SyncVars，SyncLists，SyncDictionaries 中的 GameObjects 某些情况下是脆弱的，并且应当小心使用：
- 只要 gameobject 已经同时存在于 server 和 client，引用就没有问题

当 sync data 到达 client，被应用的 gameobject 在那个 client 上可能还不存在，导致 sync data 的 null values。这是因为在内部 Mirror 传递 NetworkIdentity 的 netId，然后尝试在 client 的 NetworkIdentity.spawned 字典中查找它。

如果 object 还没有在那个 client 上生成，就不会找到匹配。还可能因为来自一个 client 的 gameobject 由于 network visibility 被排除，例如 NetworkProximityChecker。

有时同步 NetworkIdentity.netID(uint) ，然后自己在 NetworkIdentity.spawned 中查找，更加鲁棒。

```C#
public GameObject target;

[SyncVar(hook = nameof(OnTargetChanged))]
public uint targetID;

void OnTargetChanged(uint _, uint newValue)
{
    if (NetworkIdentity.spawned.TryGetValue(targetID, out NetworkIdentity identity))
        target = identity.gameObject;
    else
        StartCoroutine(SetTarget());
}

IEnumerator SetTarget()
{
    while (target == null)
    {
        yield return null;
        if (NetworkIdentity.spawned.TryGetValue(targetID, out NetworkIdentity identity))
            target = identity.gameObject;
    }
}
```

## Custom Data Types

有时你不想 Mirror 为你自己的类型生成序列化。例如，相比于序列化 quest 数据，你可能想只序列化 quest id，然后 receiver 可以在预定义 list 通过 id 查找 quest。

有时你可能想序列化 Mirror 不支持的数据类型，例如 DateTime 或 System.Uri。你可以通过添加扩展方法到 NetworkWrite 和 NetworkReader 来支持任何类型。例如，在 project 中的某个地方添加下面代码片段，来支持 DateTime 序列化：

```C#
public static class DateTimeReaderWriter
{
      public static void WriteDateTime(this NetworkWriter writer, DateTime dateTime)
      {
          writer.WriteInt64(dateTime.Ticks);
      }
     
      public static DateTime ReadDateTime(this NetworkReader reader)
      {
          return new DateTime(reader.ReadInt64());
      }
}
```

然后你可以在你的[Command] 或 SyncList 使用 DateTime。

## 继承和多态

有时你可能想要发送一个多态数据类型到你的 commands。Mirror 出于安全原因不序列化类型名，因此 Mirror 不能通过查看 message 指出对象的类型。

下面的代码不能立即使用

```C#
class Item 
{
    public string name;
}

class Weapon : Item
{
    public int hitPoints;
}

class Armor : Item
{
    public int hitPoints;
    public int level;
}

class Player : NetworkBehaviour
{
    [Command]
    void CmdEquip(Item item)
    {
        // IMPORTANT: this does not work. Mirror will pass you an object of type item
        // even if you pass a weapon or an armor.
        if (item is Weapon weapon)
        {
            // The item is a weapon, 
            // maybe you need to equip it in the hand
        }
        else if (item is Armor armor)
        {
            // you might want to equip armor in the body
        }
    }

    [Command]
    void CmdEquipArmor(Armor armor)
    {
        // IMPORTANT: this does not work either, you will receive an armor, but 
        // the armor will not have a valid Item.name, even if you passed an armor with name
    }
}
```

只有你为 Item 类型提供一个定制 serializer，CmdEquip 才能工作，例如

```C#
public static class ItemSerializer 
{
    const byte WEAPON = 1;
    const byte ARMOR = 2;

    public static void WriteItem(this NetworkWriter writer, Item item)
    {
        if (item is Weapon weapon)
        {
            writer.WriteByte(WEAPON);
            writer.WriteString(weapon.name);
            writer.WritePackedInt32(weapon.hitPoints);
        }
        else if (item is Armor armor)
        {
            writer.WriteByte(ARMOR);
            writer.WriteString(armor.name);
            writer.WritePackedInt32(armor.hitPoints);
            writer.WritePackedInt32(armor.level);
        }
    }

    public static Item ReadItem(this NetworkReader reader)
    {
        byte type = reader.ReadByte();
        switch(type)
        {
            case WEAPON:
                return new Weapon
                {
                    name = reader.ReadString(),
                    hitPoints = reader.ReadPackedInt32()
                };
            case ARMOR:
                return new Armor
                {
                    name = reader.ReadString(),
                    hitPoints = reader.ReadPackedInt32(),
                    level = reader.ReadPackedInt32()
                };
            default:
                throw new Exception($"Invalid weapon type {type}");
        }
    }
}
```

## Scriptable Objects

人们经常想从 client 想 server 发送 scriptable objects。例如，你可能有一组创建为 scriptable object 的 swords，然后你想将 equipped sword 放在 syncvar。这是可以工作的，Mirror 将会为 scriptable objects 生成一个 reader 和 writer，通过调用 ScriptableObject.CreateInstance 并复制所有数据。

然而，生成的 reader 和 writer 不适用所有场景。Scriptable objects 经常引用其他 assets，例如 textures，prefabs，或其他不能序列化的类型。Scriptable objects 经常保存在 Resources 目录中。Scriptable objects 有时拥有大量数据。生成的 reader 和 writer 可能不能工作，或者不够高效。

相比于传递 scriptable object data，你可以传递 name，而另一端可以通过 name 查找同一个 object。这样，你可以在 scriptable object 中拥有任何种类的数据。你可以通过提供自定义 reader 和 writer 完成这个目的：

```C#
[CreateAssetMenu(fileName = "New Armor", menuName = "Armor Data")]
class Armor : ScriptableObject
{
    public int Hitpoints;
    public int Weight;
    public string Description;
    public Texture2D Icon;
    // ...
}

public static class ArmorSerializer 
{
    public static void WriteArmor(this NetworkWriter writer, Armor armor)
    {
       // no need to serialize the data, just the name of the armor
       writer.WriteString(armor.name);
    }

    public static Armor ReadArmor(this NetworkReader reader)
    {
        // load the same armor by name.  The data will come from the asset in Resources folder
        return Resources.Load<Armor>(reader.ReadString());
    }
}
```