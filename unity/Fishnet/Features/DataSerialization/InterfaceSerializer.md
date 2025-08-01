## General

接口在大多数Unity项目中非常常用。由于接口不是类，即使接口仅使用可序列化字段，仍需要自定义序列化器，才能使SyncTypes和RPC正确地通过网络序列化它们。

## Serializing the Interface Entrie Class

在大多数情况下，您需要将接口解析为其实际所属的类类型，并对整个类进行网络序列化。这样做的好处是：接收方客户端/服务器后续可以通过接口查询到完整数据，确保接收到的数据与发送方发送时的状态完全一致。

若该接口实际是NetworkBehaviour类型，更推荐直接将其作为NetworkBehaviour进行传输——因为网络序列化时仅会发送一个ID供接收端查表匹配。这种方式几乎不产生网络流量，却能完整保留所有数据！

### Creating The Writer

由于接口本身并非类类型，您必须设计写入器具备以下能力：首先识别接口背后的实际类类型，再对该具体类进行网络序列化。若某个接口可能对应多种不同的类实现，则需逐一处理接口可能关联的每一种类类型。

```C#
public static void WriteISomething(this Writer writer, ISomething som)
{
    if(som is ClassA c1)
    {
        // 1 will be the identifer for the reader that this is a ClassA.
        writer.WriteByte(1); 
        writer.Write(c1);
    }
    else if(som is ClassB c2)
    {
        // 2 will be the identifier for the reader that this is a ClassB.
        writer.WriteByte(2)
        writer.Write(c2);
    }
}  
```

### Creating The Reader

读取接口数据时，我们需要先读取用于标识接口实际所属类类型的字节信息，然后通过读取器解析该具体类的数据，最后将其强制转换为所需的接口类型。

```C#
public static ISomething ReadISomething(this Reader reader)
{   
    // Gets the byte of what class type we should be reading the next bit of data as.
    byte clsType = reader.ReadByte();
    
    // Remember we assigned 1 to be ClassA.
    if(clsType == 1)
        return reader.Read<ClassA>();
    // And 2 for ClassB.
    else if(clsType == 2)
        return reader.Read<ClassB>();

    // Fall through, unhandled. This would be bad.
    return default;
}
```

## Serializing Only The interfaces Properties

有时您可能只需要序列化接口属性，通过网络传输，但请注意：如果在接收端将其强制转换回实际类型，那些不属于接口的字段值将会是其默认值！

### Creating The Writer

您仍需使用标识符来指明接口的实际类类型，但此时我们只会通过网络发送接口属性，而不会传输整个类的完整数据。

```C#
public interface ISomething
{
    string Name;
    int Health;
    ushort Level;
}

public static void WriteISomething(this Writer writer, ISomething som)
{
    // Defining a blank Class Type Indentifier
    byte clsType = 0; // Default
    
    if(som is CustomClass1 cc1)
        writer.WriteByte(1);    
    else if(som is CustomClass2 cc2)
        writer.WriteByte(2);
    // Fall through, indicating unknown type.
    else
        writer.WriteByte(0);
    
    // Remember the order the data is written, is the order it must be read.
    writer.WriteString(som.Name);
    writer.WriteInt32(som.Health);
    writer.WriteUInt16(som.Level);
}
```

### Creating The Reader

读取时，我们会先从标识符中获取类类型，然后创建该类的新实例，将其强制转换为对应的接口类型，最后将自定义序列化的值赋给该接口！

```C#
public static ISomething ReadISomething(this Reader reader)
{
    /* Getting the Class Type Indentifier.
     * Read all values first. to clear out the
     * reader. */
    byte clsType = reader.ReadByte();
    string name = reader.ReadString();
    int health = reader.ReadInt32();
    ushort level = reader.ReadUInt16();
    
    ISomething som = default;
    // Check to see what class the interface is
    if(clsType == 1)
        som = new CustomClass1();
    else if(clasType == 2)
        som = new CustomClass2();
    
    // Value was not set, so we cannot populate it.
    if(som == default(ISomething))
        return null;
    
    som.Name = name;
    som.Health = health;
    som.Level = level;
    
    return som;

}
```

