通过自定义的SynType，您可以自主决定同步数据的方式与内容，并根据需求进行优化调整。

例如：当您拥有包含大量变量的数据容器时，可能不希望像SyncVar那样在修改时发送整个容器。通过创建自定义SyncType，您可以完全掌控同步行为——这正是其他SyncType的工作原理。

```C#
/* If one of these values change you
* probably don't want to send the
* entire container. A custom SyncType
* is perfect for only sending what is changed. */
[System.Serializable]
public struct MyContainer
{
    public int LeftArmHealth;
    public int RightArmHealth;
    public int LeftLegHealth;
    public int RightLeftHealth;            
}
```

自定义的 SyncType 遵循与其他 SyncType 相同的规则。从内部实现来看，其他 SyncType 都继承自 SyncBase，您的类型也必须如此。此外，您还必须实现 ICustomSync 接口。

```C#
public class SyncMyContainer : SyncBase, ICustomSync
{
    /* If you intend to serialize your type
    * as a whole at any point in your custom
    * SyncType and would like the automatic
    * serializers to include it then use
    * GetSerializedType() to return the type.
    * In this case, the type is MyContainer.
    * If you do not need a serializer generated
    * you may return null. */
    public object GetSerializedType() => typeof(MyContainer);
}

public class YourClass
{
    private readonly SyncMyContainer _myContainer = new();
}
```

由于自定义 SyncType 的灵活性极高，因此并不存在适用于所有场景的通用示例。您可以在 FishNet 导入目录下的 ​FishNet/Demos/CustomSyncType​ 中查看多个自定义示例。
