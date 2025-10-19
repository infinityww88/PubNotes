# Attributes

Networking attributes 被添加到 NetworkBehaviours 脚本的成员函数，使它们或者运行在 client，或者允许在 server。

这些属性可以被用于 Unity game loop 方法，例如 Start 或 Update，以及其他实现方法。

当使用抽象或虚拟方法时，Attributes 也需要应用在 override 方法上。

- Server

  这个属性使得只有 server 可以调用这个方法。如果在一个 client 上调用，则抛出一个 warning 或 error。

- ServerCallback

  和 Server 一样，但是在 client 调用时不会抛出 warning。

- Client

  只有 client 可以调用这个方法。如果在一个 server 上调用，则抛出一个 warning 或 error。

- ClientCallback

  和 Client 一样，但是在 server 调用时不会抛出 error。

- ClientRpc

  Server 使用一个 RPC 在 clients 上调用这个函数。

- TargetRpc

  这个属性可以放在 NetworkBehaviours 类的方法上，允许它们从 server 在 clients 上被调用。不像 ClientRpc 属性，这些函数式在独立的 target client 上调用的，而不是所有准备好的 clients。

- Command

  从 client 在 server 上调用这个函数。确保有效输入等等。不可能从 server 上调用这个函数。使用这个作为其他 function 的 wrapper，如果你也想在 server 上调用这些函数。

  允许的参数类型是：

  - Basic type（byte，int，float，string，UInt64，等等）
  - Built-in Unity math type（Vector3，Quaternion，等等）
  - Arrays of basic types
  - Structs containing allowable types
  - NetworkIdentity
  - Game object with a NetworkIdentity component attached

- SyncVar

  SyncVars 用来自动从 server 到所有 clients 同步一个变量。

  不要在 client 对它们进行赋值。不要让它们为 null，否则会得到一个 error。

  可以使用 int，long，float，string，Vector3 等所有简单类型，NetworkIdentity 组件，以及拥有一个 NetworkIdentity 的 gameobject。

分类：

- 执行作用域：Client，Server，ClientCallback，ServerCallback
- Server 对 Clients 的调用：ClientRpc，TargetRpc
- Clients 对 Server 的调用：Command
- 变量同步（状态同步）：SyncVar

