# JsonUtility

## T FromJson(string json) / object FromJson(string json, Type type)

从 json 内容中创建一个 object。Unity 内部使用 Unity 反序列化器，因此创建的 object 类型必须支持 Unity 序列化。它必须是一个 plain class/struct，并使用 Serializable 属性标记。注意不能是 root 必须是 object，不能是基本类型或数组，必须将数据包装到 class/struct 中，同样 Json 最外层必须是 {}。被反序列化的类型必须是被 serializer 支持的类型。不被支持的类型，私有字段，被 NonSerialized 属性标记的字段，将被忽略。

创建的 object 必须是 plain class/struct 持，UnityEngine.Object 的子类（例如 MonoBehaviour 或 ScriptableObject）不支持。

如果 Json 表示缺失一些字段，它们将被赋予默认值，default(T)，而不会被赋予 field initializer 指定的值，也不执行构造函数。

json = null，返回 null。

json 可以是 string，也可以是 TextAsset。string 版本可以在 background thread 中调用，TextAsset 必须在 main thread 中调用。

## void FromJsonOverwrite(string json, object objectToOverride)

使用 json 内容覆写一个 object 的数据。

这个方法类似 FromJson，只是它不创建新的 object，而是 json 内容加载到现有 object 上。

objct 必须是标记为 Serializable 的 plain class/struct，或者 MonoBehaviour，ScriptableObject，其他类型包括 Unity built-in 类型不支持。要覆写的类型必须支持序列化。

## string ToJson(object obj) / string ToJson(object obj, bool prettyPrint)

生成一个 object public fields 的 JSON 表示。

object 必须是标记为 Serializable 的 plain class/struct，MonoBehaviour，ScriptableObject。你想要包含的字段必须是支持序列化的。

如果 object 包含对其他 Unity object 的引用，那些引用通过记录每个引用的 object 的 InstanceID 来序列化。因为 InstanceID 就像 object instance 的内存 handle，因此 JSON string 只能在同一个运行时 session 被反序列化。

## EditorJsonUtility.FromJsonOverwrite

类似 JsonUtility.FromJsonOverwrite，但是它支持任何 engine object，而不仅仅是 plain class/struct，MonoBehaviour，ScriptableObject。但是对于 struct，结果可能并非你所预期，因为传递的 struct 是按值的而不是按引用的。这意味着相比于这个方法覆写你原始的 struct，这个 struct 的一个 box copy 被传递到方法并覆写。你可以通过创建自己的 struct box copy 来避免，然后再方法返回时 unbox 出 values。即使如此，Unity built-in 的结构体（例如 Vector3，Bounds）也不能直接传递到这个方法中，因此你必须将 Unity built-in struct 包装到 class 或 struct 中。

