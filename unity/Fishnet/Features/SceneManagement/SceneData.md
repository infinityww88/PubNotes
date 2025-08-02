**场景数据（Scene Data）** 是在使用 **SceneManager** 时，用户将会交互使用的数据类型。

## SceneLookupData

### General

**SceneLookupData** 是服务器用来确定将客户端加载到新场景实例中，还是加载到服务器已加载的场景中的数据。

在创建 **SceneLoadData** 或 **SceneUnloadData** 时，系统提供了自动为您生成 **SceneLookupData** 的构造函数。在大多数情况下，您将直接使用这些构造函数，而无需单独创建 **SceneLookupData**。

当您通过场景引用或场景句柄指定场景时，​SceneManager​ 会优先使用场景句柄来查找该场景。这一机制在场景堆叠（Scene Stacking）​场景下尤为重要:

- 若通过句柄查找场景，连接（connections）会被直接载入指定的已有场景；
- 若通过场景名称查找，则服务器会为指定连接创建一个新的场景实例，并将它们载入该新实例。

需要注意的是，上述行为仅在使用多次加载调用​（multiple Load calls）时生效。例如：当您连续两次调用 LoadConnectionScene，且每次传入不同的连接时，系统就会为每个连接创建独立的新场景实例。

### Default Values

```C#
//SceneLookupData Default values
SceneLookupData slud = new SceneLookupData()
{ 
    //If Handle is greater than 0 then it will ignore Name and use Handle
    //to look up the scene.
    Handle = 0,
    //If Handle is set to 0, then Name is used to lookup the scene instead.
    Name = null 
}; 
```

## SceneLoadData

这是 **SceneManager** 用来判断如何加载某个场景所需的**数据类**。

### General

所有类型的场景加载都依赖于 **SceneLoadData**。  
**SceneLoadData** 类包含场景加载所需的关键信息，例如：  
- 需要加载的场景标识  
- 加载方式（如覆盖、叠加等）  
- 需要转移至新场景的对象列表  
- 其他加载配置参数  

您可通过[官方API文档](具体链接)查看其详细接口定义。

### Default Values

```C#
//Default Values
SceneLoadData sld = new SceneLoadData()
{
    PreferredActiveScene = null,
    SceneLookupDatas = new SceneLookupData[0],
    MovedNetworkObjects = new NetworkObject[0],
    ReplaceScenes = ReplaceOption.None,
    Params = new LoadParams()
    {
        ServerParams = new object[0],
        ClientParams = new byte[0]
    },
    Options = new LoadOptions()
    {
        AutomaticallyUnload = true,
        AllowStacking = false,
        LocalPhysics = LocalPhysicsMode.None,
        ReloadScenes = false, //Obsolete, Comming Soon.
        Addressables = false
    }
};
```

- PreferredActiveScene

  **首选活动场景（Preferred Active Scene）** 允许您指定在服务器和客户端上激活哪个场景。目前，该设置会将客户端和服务器都定向到您提供的 **SceneLookupData** 所对应的场景。

  如果将其保留为默认值 **null**，则第一个成功加载的有效场景将成为 **ActiveScene（活动场景）**。

- SceneLookupDatas

  该数组包含您希望加载的场景，具体内容取决于您在构造 **SceneLoadData** 时传入的参数。

- MovedNetworkObjects

  在加载新场景时，可以移动 **NetworkObjects（网络对象）**，例如在加载新场景时将玩家移动到另一个场景。您可以提供一个 **NetworkObjects 数组**，指定需要迁移到新场景中的对象。该数组中的所有网络对象将被移动到 **SceneLookupData** 中指定的第一个场景内。

- ReplaceScenes

  与 Unity 原生 SceneManager 在加载单个场景时的行为类似，​ReplaceScenes​ 功能允许您用新场景替换当前已加载的场景。该功能提供了多种使用选项，可根据需求灵活配置。

- Params

  参数（Params）​​ 是一种可选方式，用于为场景加载/卸载操作附加自定义数据。这些数据将在场景事件中可用，存储在参数中的信息可用于记录场景加载/卸载的相关信息，并在加载/卸载完成后进行引用。

​  - 服务器参数（ServerParams）​​

    ​ServerParams​ 仅在服务器端有效，且不会通过网络传输。它是一个对象数组，这意味着您可以发送任意类型的数据。不过，当通过事件参数访问这些数据时，您需要将对象强制转换为您期望的数据类型。

​  - 客户端参数（ClientParams）​​

    ​ClientParams​ 是一个字节数组，可以包含任意数据，并会在客户端收到场景加载指令时一并发送给客户端。客户端可以在场景切换事件中访问这些 ​ClientParams​ 数据。

- Options

  您可以通过 ​Options（选项）​​ 进一步优化场景的加载与卸载行为。

  - ​AutomaticallyUnload（自动卸载）​​
    - 当设置为 ​true​ 时，如果某个场景在服务器上不再有任何连接存在，该场景将被自动卸载。这是默认行为。
    - 当设置为 ​false​ 时，即使连接意外离开（例如断开连接），该场景仍将保留在内存中。
    - 注意：如 ​UnloadSceneData​ 章节所述，此行为可以通过 ​UnloadSceneData​ 中的 ​UnloadOptions​ 进行覆盖。
    - 仅针对为连接（客户端）加载的场景，在没有连接使用时才会自动卸载。
    - 全局场景（Global Scenes）只能通过 ​ReplaceScenes​ 或显式调用卸载方法来卸载。

  - ​AllowStacking（允许堆叠）​​
    - 当 ​AllowStacking​ 为 ​false​ 时，​SceneManager​ 不会将 ​SceneLoadData​ 中的场景进行堆叠（即不允许同一场景多次加载）。
    - 当设置为 ​true​ 时，允许场景被多次加载（即支持场景堆叠）。
    - 在 ​SceneLookupData​ 章节中我们提到，如果指定了场景引用或场景句柄，​SceneManager​ 会优先使用场景句柄来加载场景。但如果您希望通过多次加载调用，将连接（客户端）载入同一个堆叠场景中，那么您应该在 ​SceneLookupData​ 中使用场景引用或场景句柄来指定该场景。

  - ​LocalPhysics（本地物理）​​
    - ​LocalPhysics​ 是 Unity 提供的一个属性，用于控制场景中的物理模拟方式。
    - 通常情况下，如果您要堆叠多个场景，建议设置合适的 ​LocalPhysics 模式，以避免堆叠的场景之间发生不必要的物理碰撞。

  - ​Addressables（资源地址系统）​​
    - ​Addressables​ 仅作为标识信息使用，本身并不提供额外功能。
    - 您可以设置此值，以便在不创建 ​Params​ 的情况下，知晓某个场景是否是通过 Unity 的 ​Addressables 系统​ 进行加载的。

## SceneUnloadData

SceneManager 知道如何处理卸载 scene 需要的数据类。

### General

在卸载场景时，​SceneUnloadData​ 类用于构建卸载所需的信息，其结构与 ​SceneLoadData​ 类高度相似。

### Default Values

```C#
//Default Values
SceneUnloadData sud = new SceneUnloadData()
{
    SceneLookupDatas = new SceneLookupData[0],
    Params = new UnloadParams()
    {
        ServerParams = new object[0],
        ClientParams = new byte[0]
    },
    Options = new UnloadOptions()
    {
        Mode = ServerUnloadMode.UnloadUnused,
        Addressables = false
    }
};
```

- SceneLookupDatas

  该数组包含您需要卸载的场景列表，具体内容取决于您在构造 ​SceneUnloadData​ 时传入的参数配置。

- Params

  参数（Params）​​ 是一种可选机制，用于为场景加载/卸载操作附加自定义数据。这些数据将在场景事件中可用，存储在参数中的信息可用于记录场景加载/卸载的相关信息，并在加载/卸载完成后进行引用。

  - ​服务器参数（ServerParams）​​

    ​ServerParams​ 仅在服务器端有效，且不会通过网络传输。它是一个对象数组，这意味着您可以发送任意类型的数据。不过，当通过事件参数访问这些数据时，您需要将对象强制转换为您期望的数据类型。

  - ​客户端参数（ClientParams）​​

    ​ClientParams​ 是一个字节数组，可以包含任意数据，并会在客户端收到场景加载指令时一并发送给客户端。客户端可以在场景切换事件中访问这些 ​ClientParams​ 数据。

- Options

  与加载时的 **Options** 类似，**UnloadOptions** 在卸载场景时提供额外设置：  

  - Mode
    这些设置将覆盖场景加载时使用的 ​AutomaticallyUnload（自动卸载）​​ 选项。
    例如，若您在加载场景时将 ​AutomaticallyUnload​ 设为 ​false​（禁止自动卸载），但同时指定了 ​ServerUnloadModes.UnloadUnused​（卸载未使用场景模式），则当该场景不再有任何连接使用时，系统仍会自动将其卸载。
  - ServerUnloadModes.UnloadUnused
    仅卸载不再被使用的场景的默认设置
  - ServerUnloadModes.KeepUnused
    即使所有客户端断开连接，仍保留场景在服务器内存中