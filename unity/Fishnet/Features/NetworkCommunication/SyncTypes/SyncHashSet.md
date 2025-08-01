SyncHashSet 是一种能让 HashSet 集合在网络中自动保持同步的便捷方案。

其回调机制与 SyncList 类似。与其他同步类型相同，数据变更会在回调触发前立即生效。

```C#
private readonly SyncHashSet<int> _myCollection = new SyncHashSet<int>();

private void Awake()
{
    _myCollection.OnChange += _myCollection_OnChange;
}

private void FixedUpdate()
{
    //You can modify a synchashset as you would any other hashset.
    _myCollection.Add(Time.frameCount);
}

/* Like SyncVars the callback offers an asServer option
 * to indicate if the callback is occurring on the server
 * or the client. As SyncVars do, changes have already been
 * made to the collection before the callback occurs. */
private void _myCollection_OnChange(SyncHashSetOperation op, int item, bool asServer)
{
    switch (op)
    {
        /* An object was added to the hashset. Item is
         * is the added object. */
        case SyncHashSetOperation.Add:
            break;
        /* An object has been removed from the hashset. Item
         * is the removed object. */
        case SyncHashSetOperation.Remove:
            break;
        /* The hashset has been cleared. 
         * Item will be default. */
        case SyncHashSetOperation.Clear:
            break;
        /* An entry in the hashset has been updated. 
         * When this occurs the item is removed
         * and added. Item will be the new value.
         * Item will likely need a custom comparer
         * for this to function properly. */
        case SyncHashSetOperation.Update:
            break;            
        /* When complete calls all changes have been
        * made to the collection. You may use this
        * to refresh information in relation to
        * the changes, rather than doing so
        * after every entry change. All values are
        * default for this operation. */
        case SyncHashSetOperation.Complete:
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

private readonly SyncHashSet<MyContainer> _containers = new();
private MyContainer _containerReference = new();

private void Awake()
{
    _containerReference.Level = 5;
    _containers.Add(_containerReference);
}

[Server]
private void ModifyPlayer()
{
    
    //This will change the value locally but it will not synchronize to clients.
    _containerReference.Level = 10;
    //The value must be set dirty to force a synchronization.
    _containers.Dirty(_containerReference);
}
```