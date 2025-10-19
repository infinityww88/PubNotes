# SyncLists

SyncLists 是类似 C# List<T> 的基于 lists 的 array，它从 server 到 client 同步它的内容。

一个 SyncList 可以保护任何 Mirror 支持的类型。

## Usage

为你的特定类型创建一个从 SyncList 派生的 class。这是必要的，因为 Mirror 将会使用 weaver 为这个类添加方法。然后为你的 NetworkBehaviour class 添加一个 SyncList 字段。例如：

```C#
[System.Serializable]
public struct Item
{
    public string name;
    public int amount;
    public Color32 color;
}

[System.Serializable]
public class SyncListItem : SyncList<Item> {}

public class Player : NetworkBehaviour
{
    readonly SyncListItem inventory = new SyncListItem();

    public int coins = 100;

    [Command]
    public void CmdPurchase(string itemName)
    {
        if (coins > 10)
        {
            coins -= 10;
            Item item = new Item
            {
                name = "Sword",
                amount = 3,
                color = new Color32(125, 125, 125, 255)
            };

            // during next synchronization,  all clients will see the item
            inventory.Add(item);
        }
    }
}
```

有一些已经预制的 SyncLists 你可以直接使用：

- SyncListString
- SyncListFloat
- SyncListInt
- SyncListUInt
- SyncListBool

你还可以在 client 和 server 检测一个 SyncList 何时改变。这非常有用，可以在你添加装备时刷新你的 character，或者确定你何时更新数据库。

通常在 Start，OnClientStart，或 OnServerStart 期间订阅回调事件。

注意在你订阅时，list 以及初始化好了，因此将不会为 initial data 调用，只会为 updates 调用。

注意 SyncLists 必须在 constructor 初始化，不是在 StartXXX()。你可以使它们为 readonly 的来保证正确使用。

```C#
class Player : NetworkBehaviour {

    readonly SyncListItem inventory = new SyncListItem();

    // this will add the delegates on both server and client.
    // Use OnStartClient instead if you just want the client to act upon updates
    void Start()
    {
        inventory.Callback += OnInventoryUpdated;
    }

    void OnInventoryUpdated(SyncListItem.Operation op, int index, Item oldItem, Item newItem)
    {
        switch (op)
        {
            case SyncListItem.Operation.OP_ADD:
                // index is where it got added in the list
                // item is the new item
                break;
            case SyncListItem.Operation.OP_CLEAR:
                // list got cleared
                break;
            case SyncListItem.Operation.OP_INSERT:
                // index is where it got added in the list
                // item is the new item
                break;
            case SyncListItem.Operation.OP_REMOVEAT:
                // index is where it got removed in the list
                // item is the item that was removed
                break;
            case SyncListItem.Operation.OP_SET:
                // index is the index of the item that was updated
                // item is the previous item
                break;
        }
    }
}
```

默认地，SyncList 使用一个 List 来存储它的数据。如果你想使用一个不同的 list 实现，添加一个 constructor 并传递 list 实现到 parent constructor。

```C#
class SyncListItem : SyncList<Item>
{
    public SyncListItem() : base(new MyIList<Item>()) {}
}
```
