# State Synchronization

状态同步指的是同步 values，例如 scripts 包含的 integers，floating point numbers，strings，和 booleans values。

状态同步从 server 到 clients 完成。Local client 没有数据序列化这些状态，它也不需要，因为它通过 server 共享 Scene。但是 SyncVar hooks 在 local clients 上被调用。

数据不会在相反方向上同步（从 client 到 server）。要实现这个功能，需要使用 Commands。

- SyncVars

  SyncVars 是继承自 NetworkBehaviour 的脚本的变量。它从 server 同步到 client。

- SyncEvent（Obsolete）

- SyncLists

  类似 redis，Mirror 提供了很多可同步的复合数据类型。

- SyncDictionary

- SyncHashSet

- SyncSortedSet

## Sync To Owner

经常地，你不想一些玩家数据对另外一些玩家可见。在 inspector 中将 Network Sync Mode 从 Observers（默认）改为 Owner，来让 Mirror 直到只向拥有它的 client 同步数据。

例如，假设你想制作一个 inventory 系统。假设 player A，B 和 C 在同一个 area。整个网络上一共有 12 个 objects

- Client A 有 Player A（自己），Player B，Player C
- Client B 有 Player A，Player B（自己），Player C
- Client C 有 Player A，Player B，Player C（自己）
- Server 有 Player A，Player B，Player C

它们中的每个都有一个 Inventory component。

假设 Player A 拿走了一些战利品。Server 添加战利品到 Player A 的 inventory 中，它将有一个 item 的 SyncLists。

默认地，Mirror 现在必须在所有地方同步 player A 的 inventory，这意味着发送一个 update message 到 client A，client B，和 client C，因为它们都有一个 Player A 的副本。这是不必要的，Client B 和 Client C 不需要知道 Player A 的 inventory，它们从不会在 screen 看到这些 inventory。这还是一个安全问题，一些人可以 hack client 并展示其他人的 inventory，并因此占据优势。

如果你设置 Network Sync Mode 为 Owner，则 Player A 的 inventory 只会向 Client A 同步。

这也对游戏的带宽有影响，假如不是3个而是50个 player 在同一个区域，并且它们中的一个拾取了一个战利品。这意味着你只发送一个消息，而不是50个。

其他典型应用包括道具，卡牌游戏中 player 手中的牌，技能，经验，或任何你不想和其他 players 共享的其他数据。

## 高级状态同步

绝大多数情况下，使用 SyncVars 对于游戏脚本已经足够序列化状态到客户端了。但是有时，你可能需要一些复杂的序列化代码。这只和需要定制序列化的高级开发者有关，为实现超出 Mirror 正常 SyncVar 功能的功能。

### 自定义序列化函数

要执行你自己的序列化，你必须实现用于 SyncVar 序列化的 NetworkBehaviour 上的虚拟函数。这些函数是：

```C#
public virtual bool OnSerialize(NetworkWriter writer, bool initialState);
public virtual bool OnDeserialize(NetworkReader reader, bool initialState);
```

使用 initialState flag 来区分第一次序列化 gameobject 和增量更新。Gameobject 第一次被发送给 client，它必须包含全部 state snapshot，但是接下来更新可以通过只包含增量改变来节省带宽。

OnSerialize 函数应该返回 true 来指示应该发送一个更新。如果它返回 true，那个 script 的 dirty bits 将被设置为 zero。否则，dirty bits 不会改变。这允许 script 的多个 changes 被累积并在系统准备好时以及发送，而不是每帧都发送。

OnSerialize 函数只在 NetworkBehaviour 变成 dirty 时调用。一个 NetworkBehaviour 只在一个 SyncVar 或 SyncObject（例如 SyncList）自上次 OnSerialize 调用之后有所修改时变成 dirty。数据被发送之后，NetworkBehaviour 将不再 dirty，直到下一个 syncInterval。一个 NetworkBehaviour 还可以通过调用 SetDirtyBit 被标记为 dirty（这并不会绕过 syncInterval 限制）。

尽管这是可以工作的，最好还是让 Mirror 生成这些方法，并为你的特定字段提供自定义 serializers。

## Serialization Flow

附加 NetworkIdentity 组件的 GameObjects 可以有很多从 NetworkBehaviour 派生的脚本（一个 GameObject 只能有一个 NetworkIdentity，但是可以有多个 NetworkBehaviour？）

在 server 上：

- 每个 NetworkBehaviour 有一个 dirty mask。这个 mask 在 OnSerialize 中是可用的，名字是 syncVarDirtyBits
- NetworkBehaviour 脚本中的每个 SyncVar 被赋予 dirty mask 中的一个 bit。
- 改变 SyncVars 的值导致那个 SyncVar 的 bit 在 dirty mask 中 被 set
- 或者，调用 SetDirtyBit 可以直接写 dirty mask
- NetworkIdentity gameobjects 在 server 上作为它的 Update loop 的一部分被检查
- 如果一个 NetworkIdentity 上的任何 NetworkBehaviour 是 dirty，则为这个 gameobject 创建一个 UpdateVars 数据包 packet
- UpdateVars packet 通过调用 gameobject 上的每个 NetworkBehaviour 的 OnSerialize 来填充
- 不是 dirty 的 NetworkBehaviour 为它们的 dirty bits 向 packet 写入 zero
- 是 dirty 的 NetworkBehaviour 写入它们的 dirty mask（每个 bit 表示一个 SyncVar），然后写入发生改变的 SyncVars
- 如果一个 NetworkBehaviour 的 OnSerialize 返回 true，这个 NetworkBehaviour 的 dirty mask 被重置，使得它不会重复发送，直到数据发生改变
- UpdateVars packet 被发送给观察这个 gameobject 的所有 clients

在 client 上：

- 接受到一个 gameobject 的 UpdateVars packet
- 调用这个 gameobject 上的每个 NetworkBehaviour 的 OnDeserialize 函数
- 这个 gameobject 上的每个 NetworkBehaviour 读取一个 dirty mask
- 如果用于这个 NetworkBehaviour 的 dirty mask 是 0，OnDeserialize 函数读取完 dirty mask 不在读任何字节，直接返回
- 如果 dirty mask 不是 0，则 OnDeserialize 函数读取 dirty mask 之后的数据，它们是对应 dirty bits 中设置的 SyncVars 的数据
- 如果有 SyncVar hook functions，它们将被调用，并传递从 stream 中读取的值

因此，对于这个脚本：

```C#
public class data : NetworkBehaviour
{
    [SyncVar(hook = nameof(OnInt1Changed))]
    public int int1 = 66;

    [SyncVar]
    public int int2 = 23487;

    [SyncVar]
    public string MyString = "Example string";

    void OnInt1Changed(int oldValue, int newValue)
    {
        // do something here
    }
}
```

下面的例子展示了 Mirror 为 SerializeSyncVars 函数生成的 code，它在 NetworkBehaviour.OnSerialize 中被调用：

```C#
public override bool SerializeSyncVars(NetworkWriter writer, bool initialState)
{
    // Write any SyncVars in base class
    bool written = base.SerializeSyncVars(writer, forceAll);

    if (initialState)
    {
        // The first time a game object is sent to a client, send all the data (and no dirty bits)
        writer.WritePackedUInt32((uint)this.int1);
        writer.WritePackedUInt32((uint)this.int2);
        writer.Write(this.MyString);
        return true;
    }
    else 
    {
        // Writes which SyncVars have changed
        writer.WritePackedUInt64(base.syncVarDirtyBits);

        if ((base.get_syncVarDirtyBits() & 1u) != 0u)
        {
            writer.WritePackedUInt32((uint)this.int1);
            written = true;
        }

        if ((base.get_syncVarDirtyBits() & 2u) != 0u)
        {
            writer.WritePackedUInt32((uint)this.int2);
            written = true;  
        }

        if ((base.get_syncVarDirtyBits() & 4u) != 0u)
        {
            writer.Write(this.MyString);
            written = true;     
        }

        return written;
    }
}
```

下面的例子展示了 Mirror 为 DeserializeSyncVars 函数生成的 code，它在 NetworkBehaviour.OnDeserialize 中调用：

```C#
public override void DeserializeSyncVars(NetworkReader reader, bool initialState)
{
    // Read any SyncVars in base class
    base.DeserializeSyncVars(reader, initialState);

    if (initialState)
    {
        // The first time a game object is sent to a client, read all the data (and no dirty bits)
        int oldInt1 = this.int1;
        this.int1 = (int)reader.ReadPackedUInt32();
        // if old and new values are not equal, call hook
        if (!base.SyncVarEqual<int>(num, ref this.int1))
        {
            this.OnInt1Changed(num, this.int1);
        }

        this.int2 = (int)reader.ReadPackedUInt32();
        this.MyString = reader.ReadString();
        return;
    }

    int dirtySyncVars = (int)reader.ReadPackedUInt32();
    // is 1st SyncVar dirty
    if ((dirtySyncVars & 1) != 0)
    {
        int oldInt1 = this.int1;
        this.int1 = (int)reader.ReadPackedUInt32();
        // if old and new values are not equal, call hook
        if (!base.SyncVarEqual<int>(num, ref this.int1))
        {
            this.OnInt1Changed(num, this.int1);
        }
    }

    // is 2nd SyncVar dirty
    if ((dirtySyncVars & 2) != 0)
    {
        this.int2 = (int)reader.ReadPackedUInt32();
    }

    // is 3rd SyncVar dirty
    if ((dirtySyncVars & 4) != 0)
    {
        this.MyString = reader.ReadString();
    }
}
```

如果一个 NetworkBehaviour 有一个 base class，它也有 serialization 函数，则 base class functions 也应该被调用。

注意，为 gameobject 状态更新创建的 UpdateVar packets，可能在发送给 client 之前被聚合，因此一个 transport layer packet 可能包含多个 gameobject 的更新。
