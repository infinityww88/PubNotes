# Script Serialization

序列化是一个自动化过程，将数据结构或 GameObject states 转换为 Unity 可以存储和之后重构的格式。

在 Unity Project 中组织数据的格式影响 Unity 如何序列化数据，这对 Project 的性能有很大的影响。

## Serialization rules

Unity 的序列化器被特别设计以在运行时高效地运行，因此 Unity 的序列化机制和其他编程环境的序列化机制有所不同。

Unity 的序列化器直接作用于 C# 类的字段，而不是 properties，因此字段有一些必须遵守的规则以被序列化。

字段要被序列化，需要：

- public 或具有 SerializeField 属性
- 不是 static 的
- 不是常量的 const
- 不是只读的 readonly
- 具有可以序列化的字段类型：

  - 基本数据类型（int，float，double，bool，string 等）
  - 枚举类型（32 位或更少）
  - 固定大小的 buffers
  - Unity 内置类型，例如 Vector2，Vector3，Rect，Matrix4x4，Color，AnimationCurve
  - 具有 Serializable 属性的自定义结构体
  - 具有 Serializable 属性的自定义类
  - 到 UnityEngine.Object 派生类的引用
  - 以上类型的数组
  - 以上类型的 List<T>

注意 Unity 不支持 multilevel types 的序列化，例如多维数组（T[2,3]），参差数组 jagged arrays（T[][]），字典，嵌套的容器类型。如果想序列化这些类型，有两个选项：

- 在 class 或 struct 内部包装这些类型为可序列化的类型
- 实现 ISerializationCallbackReceiver，接受序列化回调，执行自定义序列化

## Serialization of custom classes

要使 Unity 序列化一个 custom class/struct，必须确保 class：

- 具有 Serializable 属性
- 不是 static class/struct

当把一个 UnityEngine.Object 派生类的实例赋予一个字段，并且 Unity 保存它时，Unity 序列化这个字段为到那个 instance 的引用。Unity 单独序列化那个 instance 自身，因此当多个字段引用同一个 instance 时，不会重复序列化它。但是对于不是派生自 UnityEngine.Object 的自定义 class/struct，Unity 直接在应用它们的 MonoBehaviour 或 ScriptableObject 的序列化数据中包含 instance 的状态。有两种方式可以出现此情景：

- inline serialization：默认地，如果在应用这个 class 的字段上不指定 [SerializeReference]，Unity inline（inplace）序列化自定义类。这意味着如果在不同的地方存储对同一个自定义 class 的实例的引用，当序列化时，它们将变成单独的 objects。之后，当 Unity 反序列化这些字段的时候，它们包含具有相同数据的完全不同的对象。
- [SerializeReference] serialization：如果指定 [SerializeReference]，Unity 将 object 处理为 managed reference。Host object 仍然在它的序列化数据中直接存储 objects，但是在一个专用的 registry section。

[SerializeReference] 增加了额外的 overhead，但是可以支持以下场景：

- Fields 可以是 null。Inline Serialization 不能表示 null，它将 null 表示为一个具有 unassigned fields 的 inline object
- 到同一个 object 的 multiple references，使得它不会被重复序列化
- 支持图状和循环的数据依赖（例如一个 object 引用它自身）。Inline class serialization 不支持 null 和共享 reference，因此任何循环数据依赖都会导致意外的结果，例如奇怪的 Inspector 行为，console errors 和 无限循环
- 支持多态。如果使用一个父类类型的变量引用一个子类的实例，不使用 SerializeReference，Unity 只会序列化属于父类的字段，并且反序列化只得到父类的实例
- 当 data structure 需要一个稳定的标识符 id 来指向特定的 object 而无需硬编码 object 的数组位置或搜索整个数组

Inline serialization 更高效，应尽量使用它，除非特别需要 [SerializeReference] 支持的特性。

## Properties 的序列化

Unity 正常不支持序列化 Properties，除非：

- 如果 property 有一个 backing field
- Unity 序列化带自生成字段的 Properties，仅限 hot reloading

  ```c#
  public int MyInt { get; set; }
  ```

如果你不想 Unity 序列化一个带自生成字段的 property，使用 [NonSerialized] 属性。

## 自定义序列化

有时可能需要序列化一些 Unity 序列化器不支持的数据（例如 C# 字典）。最佳的方式在你的类中实现 ISerializationCallbackReceiver 接口。这让你可以在序列化和反序列化期间接收回调：

- 当一个 object 将要被序列化时，Unity 调用 OnBeforeSerialize() 回调。回调内你可以将 Unity 不支持的数据类型转换为 Unity 支持的数据类型，并序列化后者。例如将自动转换为两个数组，分别对应 keys 和 values。
- OnBeforeSerialize() 回调完成后，Unity 序列化它支持的数据。
- 之后当 object 被反序列化时，Unity 调用 OnAfterDeserialize() 回调。回调内可以将数据转化为原来的类型，例如 C# 字典。

## Unity 如何使用序列化

### Saving 和 loading

Unity 使用 serialization 来加载和存储 scenes，Assets，和 AssetBundles 到设备内存中。这包括 MonoBehaviour 和 ScriptableObject 上存储的数据。

Unity Editor 的很多功能都基于核心的序列化系统。两个特别需要提到的是 Inspector widnow 和 Hot reloading。

- Inspector window

  Inspect window 显示检视对象（MonoBehaviour 或 ScriptableObject）的序列化字段。当你在 Inspector 中改变一个值时，Inspector 更新序列化数据，并触发一个反序列化来更新被监视的对象。

  Unity 不会调用任何 C# property 的 getter 和 setter，而是直接访问序列化的 bacing 字段。这和 Editor 脚本中的 SerializedObject/SerializedProperty 的使用是一样的，或这应该就是用这两个 api 实现的，通过路径直接找到底层数据的位置，然后更新，最后反序列化。

- Hot reloading

  Hot reloading 是指你可以在编辑器保持打开时，创建或编辑脚本，并立即应用脚本，而无需重启 Editor 来使改变生效。

  当你修改并保存一个脚本时，Unity hot reloads 所有的 script data。Unity 在所有加载的脚本（Scene 中引用的脚本）存储所有可序列化的变量，然后 reloads 那些脚本，并恢复所有序列化的变量。Hot reloading 丢弃所有不可序列化的数据（Unity 不支持的数据类型），因此它们将被重置。

  这影响 project 中所有 Editor windows 和 MonoBehaviour。和其他序列化场景不同，Unity 在 reloading 是默认序列化 private fields（但必须是 Unity 支持的序列化类型），即使它们没有 SerializeField 属性。

  当 Unity reloads 脚本时：

  - Unity 在所有加载的 scripts 中序列化并存储所有变量
  - Unity 将它们恢复到序列化前的初始值：

    Unity 恢复所有的变量（包括私有变量，即使没有 SerializeField 属性）。有时你需要阻止 Unity 恢复 private 变量，可以 [NonSerialized] 属性。

    Unity 从不恢复 static 变量。因此不要将 static 变量用于你需要 Unity reload scripts 后需要保持的状态，因为 reloading 过程会丢弃它们。

### Prefabs

Prefab 就是一个或多个 GameObject 或 components 的序列化数据。一个 Prefab instance 包含对 Prefab asset 的引用，和一个对它的修改的列表（override）。Prefab instance 是一个对象，它包含一个对 Prefab asset 的引用，以及一个 override 列表。因为 Prefab asset 也是 UnityEngine.Object，Scene 序列化时，会序列化这个引用本身。

### Instantiation

当在一个 scene 中的任何对象上调用 Instantiate 时，例如 Prefab 或 GameObject：

- Unity 先序列化它。这在 runtime 和 editor 中都会发生。Unity 可以序列化从 UnityEngine.Object 派生的任何对象
- Unity 创建一个新的 GameObject，然后反序列化数据到新的 GameObject 上
- Unity 以不同的变体运行相同的序列化 code，来报告它引用的其他 UnityEngine.Object。它检查所有引用的 UnityEngine.Object 来查看它们是否是 Unity instantiate 数据的一部分。如果这个引用执行外部的对象，例如一个 Texture，Unity 保持这个引用不变。如果这个引用指向内部的对象，例如一个 child GameObject，Unity 将引用指向相应的副本

### Unloading unused assets

EditorUtility.UnloadUnusedAssetsImmediate 是一个 native Unity 垃圾回收，与 C# 垃圾回收有不同的目的。它在你加载一个 scene 后运行，并检查它不再引用的对象（例如 Textures），并安全地卸载它们。Native Unity 垃圾回收以一个变体运行序列化器，使 objects 报告到所有对外部 UnityEngine.Objects 的引用。

### Differences between Editor and runtime serialization

绝大多数序列化发生在 Editor，而绝大多数反序列化发生在运行时。Unity 有一些特性只在 Editor 中序列化，而有一些特性同时在 Editor 和 Runtime 中序列化。\

| Feature | Editor | Runtime |
| --- | --- | --- |
| Assets in Binary Format | Read/write supported | Read supported |
| Assets in YAML format	| Read/write supported | Not supported |
| Saving scenes, prefabs and other assets | Supported, unless in Play mode | Not supported |
| Serialization of individual objects with JsonUtility | Read/write support with JsonUtility. Support for additional types of objects with EditorJsonUtility | Read/write support with JsonUtility |
| SerializeReference | Supported | Supported |
| ISerializationCallbackReceiver | Supported | Supported |
| FormerlySerializedAs | Supported | Not supported |
||||

Objects 可以有一些额外的字段只在 Editor 中序列化，例如在 UNITY_EDITOR 中声明字段：

```C#
public class SerializeRules : MonoBehaviour
{
#if UNITY_EDITOR
public int m_intEditorOnly;
#endif
}
```

这里 m_intEditorOnly 字段只子啊 editor 中序列化，并不包含在 build 中。这允许你在 build 中忽略只在 editor 中需要的数据来节省内存。任何使用这个字段的 code 也需要条件编译。

Editor 不支持只在 runtime 序列化的字段的 objects，例如声明在 UNITY_STANDALONE 中的条件编译。

MonoBehaviour 是脚本自定义组件的基类，但是 Unity 内置的组件不是 MonoBehaviour，而是 Component，MonoBehaviour 也是 Component 的子类。

