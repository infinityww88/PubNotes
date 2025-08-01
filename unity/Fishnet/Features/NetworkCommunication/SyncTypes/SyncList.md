SyncList 是一种让 List 集合在网络中自动保持同步的简便方法。

使用 SyncList 的方式与普通 List 完全相同。

SyncList 的网络回调比 SyncVars 提供了更多信息。其他非 SyncVar 的 SyncTypes 也各自拥有独特的回调机制。以下示例演示了一个 SyncList 回调。

```C#
private readonly SyncList<int> _myCollection = new();

private void Awake()
{
    /* Listening to SyncList callbacks are a
    * little different from SyncVars. */
    _myCollection.OnChange += _myCollection_OnChange;
}
private void Update()
{
    //You can modify a synclist as you would any other list.
    _myCollection.Add(10);
    _myCollection.RemoveAt(0);
    //ect.
}

/* Like SyncVars the callback offers an asServer option
 * to indicate if the callback is occurring on the server
 * or the client. As SyncVars do, changes have already been
 * made to the collection before the callback occurs. */
private void _myCollection_OnChange(SyncListOperation op, int index,
    int oldItem, int newItem, bool asServer)
{
    switch (op)
    {
        /* An object was added to the list. Index
        * will be where it was added, which will be the end
        * of the list, while newItem is the value added. */
        case SyncListOperation.Add:
            break;
        /* An object was removed from the list. Index
        * is from where the object was removed. oldItem
        * will contain the removed item. */
        case SyncListOperation.RemoveAt:
            break;
        /* An object was inserted into the list. Index
        * is where the obejct was inserted. newItem
        * contains the item inserted. */
        case SyncListOperation.Insert:
            break;
        /* An object replaced another. Index
        * is where the object was replaced. oldItem
        * is the item that was replaced, while
        * newItem is the item which now has it's place. */
        case SyncListOperation.Set:
            break;
        /* All objects have been cleared. Index, oldValue,
        * and newValue are default. */
        case SyncListOperation.Clear:
            break;
        /* When complete calls all changes have been
        * made to the collection. You may use this
        * to refresh information in relation to
        * the list changes, rather than doing so
        * after every entry change. Like Clear
        * Index, oldItem, and newItem are all default. */
        case SyncListOperation.Complete:
            break;
    }
}
```

若将此 SyncType 用于类等容器类型，并需要修改容器内的值，则必须将该值标记为“脏”（dirty）。具体用法请参见下方示例。

```C#
private class MyClass
{
    public string PlayerName;
    public int Level;
}

private readonly SyncList<MyClass> _players = new SyncList<MyClass>();

//Call dirty on an index after modifying an entries field to force a synchronize. 
[Server] 
private void ModifyPlayer()
{
    _players[0].Level = 10;
    //Dirty the 0 index.
    _players.Dirty(0);
}
```

当结构体存放在集合中时，其内部值无法直接修改。您需要先为待修改的集合索引创建一个局部变量，在本地副本上进行数值变更，最后再将修改后的本地副本重新赋值回集合。

```C#
/* . */
[System.Serializable]
private struct MyStruct
{
    public string PlayerName;
    public int Level;
}

private readonly SyncList<MyStruct> _players = new();

[Server] 
private void ModifyPlayer()
{
    MyStruct ms = _players[0];
    ms.Level = 10;
    _players[0] = ms;
}
```