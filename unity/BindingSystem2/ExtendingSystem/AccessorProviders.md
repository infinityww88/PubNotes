Accessor providers 适用于高级用户，当扩展系统时，提供了更大的灵活性。它们提供了一种方法，为 bindings 提供 custom values 和 paths。

默认情况下，系统会使用高度优化的反射和代码生成技术来提供绑定路径和值。不过，还存在另一种提供绑定的方式：IAccessorProvider。所有实现该接口的类都将被系统自动注册，并作为替代性绑定方法提供给用户。

下面是 IAccessorProvider 接口的简单实现：

```C#
public class MyProvider : IAccessorProvider
{
    public string Id => "Texture Data Provider";

    public IAccessor GetAccessor(Type sourceType, string pathId)
    {
        return pathId switch
        {
            "Width" => new ObjectAccessor<Texture2D, int>(t => ((Texture2D)t).width, null),
            "Height" => new ObjectAccessor<Texture2D, int>(t => ((Texture2D)t).height, null),
            _ => throw new ArgumentException(nameof(pathId)),
        };
    }

    public IEnumerable<AccessorPath> GetAvailablePaths(object source)
    {
        if(source is not Texture2D)
        {
            return Enumerable.Empty<AccessorPath>();
        }
        return new AccessorPath[]
        {
            new AccessorPath(this, "Width", BindMode.Read, typeof(int)),
            new AccessorPath(this, "Height", BindMode.Read, typeof(int)),
        };
    }

    public bool TryConvertIdToPath(string id, string separator, out string path)
    {
        path = id;
        return true;
    }
}
```
