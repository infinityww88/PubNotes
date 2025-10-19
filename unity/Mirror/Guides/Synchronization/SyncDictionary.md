# SyncDictionary

一个 SyncDictionary 是一个关联数组，包含无序的 key value pair list。Keys 和 values 可以是以下类型：

- Basic type（byte，int，float，string，UInt64 等）
- Built-in Unity math type（Vector3，Quaternion 等）
- NetworkIdentity
- 附加 NetworkIdentity 的 GameObject 
- 上述类型的结构体

SyncDictionary 和 SyncLists 工作类似，当在 server 上做出改变时，改变被传播到所有的 clients 上，并且 Callback 被调用。

要使用它，为你的特定类型创建一个从 SyncDictionary 派生的类。这是必要的，因为 Weaver 将会为这些类添加方法。然后添加字段到 NetworkBehaviour 类。

注意在你订阅 callback 时，dictionary 以及初始化好了，因此你不会为初始化数据获得调用，只会在更新时得到调用。

注意 SyncDictionary 必须在 constructor 中初始化，不是在 StartXXX()。你可以将它设置为 readonly 来确保正确使用。

## 简单的例子

```C#
using UnityEngine;
using Mirror;

[System.Serializable]
public struct Item
{
    public string name;
    public int hitPoints;
    public int durability;
}

[System.Serializable]
public class SyncDictionaryStringItem : SyncDictionary<string, Item> {}

public class ExamplePlayer : NetworkBehaviour
{
    [SerializeField]
    public readonly SyncDictionaryStringItem Equipment = new SyncDictionaryStringItem();

    public override void OnStartServer()
    {
        Equipment.Add("head", new Item { name = "Helmet", hitPoints = 10, durability = 20 });
        Equipment.Add("body", new Item { name = "Epic Armor", hitPoints = 50, durability = 50 });
        Equipment.Add("feet", new Item { name = "Sneakers", hitPoints = 3, durability = 40 });
        Equipment.Add("hands", new Item { name = "Sword", hitPoints = 30, durability = 15 });
    }

    public override void OnStartClient()
    {
        // Equipment is already populated with anything the server set up
        // but we can subscribe to the callback in case it is updated later on
        Equipment.Callback += OnEquipmentChange;
    }

    void OnEquipmentChange(SyncDictionaryStringItem.Operation op, string key, Item item)
    {
        // equipment changed,  perhaps update the gameobject
        Debug.Log(op + " - " + key);
    }
}
```

默认地，SyncDictionary 使用 Dictionary 来存储它的数据。如果你想使用一个不同的 IDictionary 实现，例如 SortedList 和 SortedDictionary，为你的 SyncDictionary 实现添加一个构造器，并传递一个 dictionary 到 base class。

```C#
[System.Serializable]
public class SyncDictionaryStringItem : SyncDictionary<string, Item> 
{
    public SyncDictionaryStringItem() : base (new SortedList<string,Item>()) {}
}
    
public class ExamplePlayer : NetworkBehaviour
{
    [SerializeField]
    public readonly SyncDictionaryStringItem Equipment = new SyncDictionaryStringItem();
}
```
