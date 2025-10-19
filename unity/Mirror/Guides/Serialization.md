# Serialization

Mirror 使用 Weaver（C# 语言工具）为 types 创建序列化和反序列化。Weaver 在 unity 编译 dll 之后编辑它们。这允许 mirror 拥有许多复杂功能，例如 SyncVar，ClientRpc，和 Message Serialization，而不需要开发者手动设置方方面面。

## Rules and tips

关于 Weaver 可以做什么有一些规则和限制。一些功能增加了复杂性并且很难维护，因此还没有实现。这些功能不是不可能实现，并且如果非常需要的话可以添加：

- 你应该可以为任何类型编写自定义 Read/Write 函数，而 Weaver 将会使用它们。

  这意味着如果有一个不支持的类型例如 int\[][]，创建一个自定义 Read/Write 函数将允许你在 SyncVar/ClientRpc/等 同步 int\[][]

- 如果你有一个类型，它有一个字段不能被序列化，你可以标记这个字段为 [System.NonSerialized]，weaver 将会忽略它

### 不支持类型（需要编写自定义 reader writer）

- Jagged（不一致） 和 多维数据
- 继承自 UnityEngine.Component 的类型
- UnityEngine.Object
- UnityEngine.ScriptableObject
- 泛型类型 MyData<T>
  自定义 Reader/Writer 必须声明 T 的实际参数，例如 MyData<int>
- Interfaces
- 应用自身的 Types

## 内置 Reade Write Functions

Mirror 提供了一些内置 Read/Write Functions。它们可以在 NetworkReaderExtensions 和 NetworkWriterExtensions 找到。

下面是一个不完整的列表：

- 绝大多数 C# primitive 类型
- 常见 Unity 结构体
  - Vector3
  - Quaternion
  - Rect
  - Ray
  - Guid
- NetworkIdentity，GameObject，Transform

### NetworkIdentity，GameObject，Transform

对于这些类型，发送 netId，而不是 object 自身？

Object 的 netId 通过网络发送，具有相同 netId 的 Object 在另一侧被返回。如果 netId 是 0 或者 object 没有找到，则返回 null。

## Generated Read Write Functions

Weaver 将会为以下类型生成 Read Write 函数

- Classes 或 Structs
- Enums
- Arrays，例如 int[]
- ArraySegments，例如 ArraySegment\[int]
- Lists，例如 List<int>

### Classes and Structs

Weaver 将会 Read/Write 这个类型的每个 public 字段，除非它被标记为 [System.NonSerialized]。如果 class 或 struct 中有不支持的类型，Weaver 为它生成 Read/Write 函数将会失败。

Weaver 不会检查 properties（get，set）。

### Enums

Weaver 将会使用一个 enum 的底层类型来 Read 和 Write 它们。默认底层类似是 int。例如，Switch 将会使用 byte 的 Read/Write 函数来序列化：

```C#
public enum Switch : byte
{
    Left,
    Middle,
    Right,
}
```

### Collections

Weaver 将会为上述类型的 collections 生成 Read/Write。Weaver 将使用 collections 的 elements 的 Read/Write 函数。元素必须具有 Read/Write 函数来称为受支持类型，或具有自定义 Read/Write 函数。

例如：

- float[] 是一个受支持类型，因为 Mirror 对于 float 有内置的 Read/Write 函数
- MyData[] 是一个受支持类型，因为 Weaver 可以为 MyData 生成 Read/Write 函数

```C#
public struct MyData
{
    public int someValue;
    public float anotherValue;
}
```

## Adding Custom Read Write functions

以下面的形式编写 Read/Write 函数为静态方法：

```C#
public static void WriteMyType(this NetworkWriter writer, MyType value)
{
    // write MyType data here
}

public static MyType ReadMyType(this NetworkReader reader)
{
    // read MyType data here
}
```

最佳实践是使 Read/Write 函数成为 extension methods，使得它们可以像 writer.WriteMyType(value) 调用，并且命名它们为 ReadMyType 和 WriteMyType，使得可以直观地看出它们是什么类型。但是函数的名字并不重要，weaver 有能力找到它们，无论它们被称为什么。

### Properties Example

Weaver 不会写入 properties（get、set），但是一个自定义 writer 可以将它们通过发送发送。

如果你一个私有集合的属性，这非常有用。

```C#
public struct MyData
{
    public int someValue { get; private set; }
    public float anotherValue { get; private set; }

    public MyData(int someValue, float anotherValue)
    {
        this.someValue = someValue;
        this.anotherValue = anotherValue;
    }
}

public static class CustomReadWriteFunctions 
{
    public static void WriteMyType(this NetworkWriter writer, MyData value)
    {
        writer.WriteInt32(value.someValue);
        writer.WriteSingle(value.anotherValue);
    }

    public static MyData ReadMyType(this NetworkReader reader)
    {
        return new MyData(reader.ReadInt32(), reader.ReadSingle());
    }
}
```

### Unsupported type Example

Rigidbody 是一个不被支持的类型，因为它继承自 Component（MonoBehavior）。但是可以添加一个自定义 writer，如果 gameobject 上附加有一个 NetworkIdentity，则它可以通过 NetworkIdentity 同步。

```C#
public struct MyCollision
{
    public Vector3 force;
    public Rigidbody rigidbody;
}

public static class CustomReadWriteFunctions
{
    public static void WriteMyCollision(this NetworkWriter writer, MyCollision value)
    {
        writer.WriteVector3(value.force);

        NetworkIdentity networkIdentity = value.rigidbody.GetComponent<NetworkIdentity>();
        writer.WriteNetworkIdentity(networkIdentity);
    }

    public static MyCollision ReadMyCollision(this NetworkReader reader)
    {
        Vector3 force = reader.ReadVector3();

        NetworkIdentity networkIdentity = reader.ReadNetworkIdentity();
        Rigidbody rigidBody = networkIdentity != null
            ? networkIdentity.GetComponent<Rigidbody>()
            : null;

        return new MyCollision
        {
            force = force,
            rigidbody = rigidBody,
        };
    }
}
```

上面的函数用于 MyCollision，但是你还可以为 Rigidbody 添加 functions，然后让 weaver 为 MyCollision 生成一个 writer。

```C#
public static class CustomReadWriteFunctions
{
    public static void WriteRigidbody(this NetworkWriter writer, Rigidbody rigidbody)
    {
        NetworkIdentity networkIdentity = rigidbody.GetComponent<NetworkIdentity>();
        writer.WriteNetworkIdentity(networkIdentity);
    }

    public static Rigidbody ReadRigidbody(this NetworkReader reader)
    {
        NetworkIdentity networkIdentity = reader.ReadNetworkIdentity();
        Rigidbody rigidBody = networkIdentity != null
            ? networkIdentity.GetComponent<Rigidbody>()
            : null;

        return rigidBody;
    }
}
```

NetworkIdentity == netId

## Debugging

你可以使用 dnSpy 等工具来查看 weaver 修改之后的编译代码。这可以帮助理解和调试 Mirror 和 Weaver 做了什么。
