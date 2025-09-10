# ScriptableObject

ScriptableObject 是一个数据容器，可以用来存储大量数据。

SO 的一个主要用途是通过避免复制数据来减少项目的内存使用。

如果 Prefab 在挂载的 MonoBehaviour 脚本中存储了不会改变的数据，SO 就很有用。

每次实例化一个 Prefab，instance 都会得到 Prefab 上的数据副本。可以用一个 SO 来存储这些数据，然后让所有 prefab 都引用这个 SO，这意味着数据在内存中只有一份。

和 MonoBehaviour 一样，ScriptableObject 继承自 Unity Object，但不同的是，它不可挂载到 GameObject 上，相反你需要将它们以 asset 保存到硬盘上。

当使用 Editor 时，你可以既在 editing mode 存储数据，也可以在 play mode 存储数据，因为 ScriptableObject 使用 Editor namespace 和 Editor scripting。但是在部署构建时，你不能使用 ScriptableObjects 来存储数据（runtime 时不可以写入数据到磁盘的 ScriptableObject asset。但是在 runtime 时可以使用你在开发时存储到 SO asset 中的数据。

在 Editor 中存储到 SO asset 中数据会实时写入到硬盘，因此在 session 之间是持久的。

## 使用 ScriptableObject

主要用途：

- 在 Editor session 之间存储数据
- 在开发时存储数据到 asset 中，在运行时使用

```C#
using UnityEngine;

[CreateAssetMenu(fileName = "Data", menuName = "ScriptableObjects/SpawnManagerScriptableObject", order = 1)]
public class SpawnManagerScriptableObject : ScriptableObject
{
    public string prefabName;

    public int numberOfPrefabsToCreate;
    public Vector3[] spawnPoints;
}
```

使用 ScriptableObject 作为中心化数据。

使用 ScriptableObject.CreateInstance<T>() 创建一个内存 SO，使用 Editor Menu（CreateAssetMenuAttribute）或者 AssetDatabase.CreateAsset 脚本 API 将 SO 保存到硬盘上的 asset。

ScriptableObject 只能在 Editor（开发期间）创建。在运行时只能被读取。运行时脚本只能引用硬盘上的 SO asset。

如果一个 ScriptableObject 没有被保存到 asset，并被 scene 中的 object 引用，Unity 会将它直接序列化到 Scene 文件。对于在 project 中只有一个持久实例 persistent instance 的 ScriptableObjects，使用 ScriptableSingletont<T0>。

使用 AssetDatabase 访问之前存储的 SO asset，例如 AssetDatabase.LoadAssetAtPath。如果 MonoBehaviour 的一个字段引用一个 SO asset，SO 被自动加载，脚本可以直接使用字段来访问它。

SO 字段的序列号和 MonoBehaviour 的序列化完全一样，参考脚本序列化。

包含大数组，或其他潜在大的数据，应该以 PreferBinarySerialization 属性声明，因为 YAML 对这类数据不能很高效地表示这类数据。

当 ScriptableObject 被销毁时，C# Object 仍然保留在内存中，直到垃圾回收被执行。出于此状态的 SO 表现的就像 null，例如对 obj == null 返回 true。

SO 的生命周期函数：

- Awake
- OnEnable
- OnValidate
- OnDisable
- OnDestroy

Awake 和 OnEnable 在 object 被加载时调用，这包括：

- 创建一个 SO asset 时（此时 Editor 需要加载 asset 以在 Inspector 中显示它的内容）
- 加载一个包含对 SO 的引用的 Scene 时（包括 editor）
- 在 code 改变后，reloading domain，重新加载最近引用的 SO
- 在 Project 中或 reference selector 控件上点击 SO asset 时，如果 Editor 还没有加载它，则进行加载

执行加载的时机不确定，SO asset 可能已经被 Editor 加载，也可能没有被 Editor 加载。如果已被 Editor 加载则不会执行 Awake 和 OnEnable。在不需要时，Editor 会解除对 SO 的引用。如果点击 SO asset 查看 Inspector 时，Editor 会再次加载它，此时就会调用 Awake 和 OnEnable

总之，就是只要 SO 需要被加载时，就会调用 Awake 和 OnEnable，使其可以执行初始化逻辑。这个时机不确定，但是总会执行，保证 SO 的生命周期是完整的。

因此 Awake 和 OnEnable 不是只在创建 SO asset 时被调用，而是在后面的任何时候都有可能调用，只要 SO 需要被 loadding。

1. Launch Unity editor and open a scene referencing the object, or select the object in the inspector

   Awake -> OnEnable

2. Enter Play Mode

  -> OnDisable -> OnEnable

3. Load a different scene that does not reference this object

  -> OnDisable

OnValidate 是 Editor-only 的函数，Unity 在 script 被加载，或者在 Inspector 中改变一个值的时候调用它。在 Inspector 中改变一个值之后，可以使用这个函数来执行校验，确保数据完整性。无论是改变普通字段，还是数组中的元素。

OnValidate 不支持 SO 脚本修改不是它自身的其他脚本的 values。

You cannot reliably perform Camera rendering operations here. Instead, you should add a listener to EditorApplication.update, and perform the rendering during the next Editor Update call.

SO 在运行时不可被已修改，因此不能作为 PlayerPrefs 一样的数据库，它是只读数据。

# ScriptableObjectArchitecture

上面说的 SO 不能在运行时修改，指的是在 Build 中，硬盘上的 SO 文件不能被修改，它们的角色是只读的配置文件。但是：

- 运行时，存在于内存中的 SO，就是普通的内存对象，它们可以像普通的内存对象一样被修改
- 在 Editor 中，即使在 Play Mode，修改内存的 SO 对象，同样可以同步到硬盘上的 SO 文件，看起来似乎是修改内存 SO 对象可以同样修改硬盘上的 SO 文件，但这只适用于 Editor 的 Play Mode。对于 Build，运行时修改内存 SO 对象，是不会同步到硬盘上的 SO 文件的，每次重新启动 Build，SO 都是相同的
- 编辑时，不同的 Scene GameObject 或 Prefab 引用的同一个 SO 文件，在运行时仍然会引用相同的 SO 内存对象。SO 内存对象是区别 GameObject 存在的另一种对象，GameObject 引用 SO 对象，就像引用另一个 GameObject 一样
- SO 内存对象和 SO 文件的关系，就像 GameObject 和 Prefab 的关系。Prefab 就是 GameObject 的内存文件。修改 Prefab 会立即同步到 GameObject，就像修改 SO 文件会立即同步到 SO 内存对象。

在运行时（无论是 Play Mode 还是 Build），是可以修改 SO 内存对象的，只是 Editor 中，修改可以同步到硬盘上的 SO 文件，而 Build 中，修改在退出程序后就被丢弃了。

ScriptableObjectArchitecture 在 SO 基础上创建了一个框架。变量本身还提供了事件机制，引用者可以监听运行时对其的修改。有两种方法修改

- 为 Var.Value 赋值，这在 Editor 时还会同步修改到硬盘上
- 调用 Var.SetValue() 方法，这只修改内存对象，不会同步到硬盘上

SOA 框架不仅仅是将 SO 作为配置数据，更重要是实现了一套消息机制，为程序解耦。当运行时，程序的不同部分引用同一个 SO，其中一个修改了 SO 内存对象，另一个可以看见其修改。但是内置 SO 只能通过轮询感知修改，而 SOA 提供了事件，可以监听对 SO 的修改。

总而言之：SO 的本质角色是只读的配置文件，但是在运行时还可以作为一个数据中心和消息总线，用于不同组件之间的解耦。
