SyncDictionary 是一种能让 Dictionary 集合在网络中自动保持同步的便捷方案。

它支持普通字典的所有功能，正如 SyncList 支持 List 的全部能力一样。

SyncDictionary 的回调机制与 SyncList 类似。与其他同步类型相同，数据变更会在回调触发前立即生效。

```C#
private readonly SyncDictionary<NetworkConnection, string> _playerNames = new();
    
private void Awake()
{
    _playerNames.OnChange += _playerNames_OnChange;
}

//SyncDictionaries also include the asServer parameter.
private void _playerNames_OnChange(SyncDictionaryOperation op,
    NetworkConnection key, string value, bool asServer)
{
    /* Key will be provided for
    * Add, Remove, and Set. */     
    switch (op)
    {
        //Adds key with value.
        case SyncDictionaryOperation.Add:
            break;
        //Removes key.
        case SyncDictionaryOperation.Remove:
            break;
        //Sets key to a new value.
        case SyncDictionaryOperation.Set:
            break;
        //Clears the dictionary.
        case SyncDictionaryOperation.Clear:
            break;
        //Like SyncList, indicates all operations are complete.
        case SyncDictionaryOperation.Complete:
            break;
    }
}
```

若将此 SyncType 用于类或结构体等容器类型，且需修改容器内的值，必须先将值标记为“脏”（dirty）。具体用法请参考下方示例。

```C#
[System.Serializable]
private struct MyContainer
{
    public string PlayerName;
    public int Level;
}

private readonly SyncDictionary<int, MyContainer> _containers = new();

private void Awake()
{
    MyContainer mc = new MyContainer
    {
        Level = 5
    };
    _containers[2] = mc;
}

[Server]
private void ModifyContainer()
{
    MyContainer mc = _containers[2];
    //This will change the value locally but it will not synchronize to clients.
    mc.Level = 10;
    //You may re-apply the value to the dictionary.
    _containers[2] = mc;
    //Or set dirty on the value or key. Using the key is often more performant.
    _containers.Dirty(2);
}
```