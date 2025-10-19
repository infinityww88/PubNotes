# ScriptableObject

ScriptableObject 是一个数据容器，你可以用来保存大量的数据，独立于 class 实例。ScriptableObjects 的一个主要应用场景是降低你的 Project 内存使用，通过避免复制 values。

如果你的 Project 有一个 Prefab，它在挂载的 MonoBehavior 脚本中存储不会修改的数据，这很有用。

每次你实例化这个 Prefab，它将会得到那个数据自己的副本。相比于使用方法，和存储重复的数据，你可以使用一个 ScriptableObject 来存储数据，然后在所有的 Prefabs 中通过引用来访问它。这意味着在内存中，数据只有一个拷贝。

就像 MonoBehaviors，ScriptableObjects 从 base Unity object 派生，但是不像 MonoBehavior，你不能附加 ScriptableObject 到 GameObject。相反，你需要保存它们为 Project 的 Assets。

当你使用 Edito 时，你可以在编辑时和运行时保存数据到 ScriptableObject，因为 ScriptableObjects 使用 Editor namespace 和 Editor scripting。但是在部署后的 build 中，你不能使用 ScriptableObjects 来保存数据（不能将它作为运行时数据库，它们只能在 editor 时编辑，作为数据配置），但是你可以使用开发时为它们设置的数据。

你在 Editor Tools 中保存到 ScriptableObjects 被作为 asset 写入到 disk，因此在 sessions 之间是持久化的。任何对它的修改都是写入到磁盘的。因此可以保存 Play Mode 中的编辑的数据。

有很多在 Unity 中使用 ScriptableObject 的原因。它们可以改进你的工作流，减少内存使用，甚至解耦你的 code architecture。另一个主要的好处是，作为配置文件，同一个 ScriptableObject 可以有多个实例，使得切换配置非常容易。

## Using a ScriptableObject

ScriptableObjects 的主要用法是：

- 在 Editor session 期间保存和存储数据
- 将数据保存为 asset 并在运行时使用

要使用一个 ScriptableObjects，创建一个 script，继承 ScriptableObjects 类。你可以使用 CreateAssetMenu 属性以方便的创建这个 assets。

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

编写完这个脚本后，就可以通过 Assets > Create > ScriptableObject > SpawnManagerScriptableObject 来创建这个 ScriptableObject 的一个实例。

为你的 asset 一个有意义的名字，然后修改它的 values。要使用这些 values，你需要创建一个新的 script，它引用你的 ScriptableObject，SpawnManagerScriptableObject。

```C#
using UnityEngine;

public class Spawner : MonoBehaviour
{
    // The GameObject to instantiate.
    public GameObject entityToSpawn;

    // An instance of the ScriptableObject defined above.
    public SpawnManagerScriptableObject spawnManagerValues;

    // This will be appended to the name of the created entities and increment when each is created.
    int instanceNumber = 1;

    void Start()
    {
        SpawnEntities();
    }

    void SpawnEntities()
    {
        int currentSpawnPointIndex = 0;

        for (int i = 0; i < spawnManagerValues.numberOfPrefabsToCreate; i++)
        {
            // Creates an instance of the prefab at the current spawn point.
            GameObject currentEntity = Instantiate(entityToSpawn, spawnManagerValues.spawnPoints[currentSpawnPointIndex], Quaternion.identity);

            // Sets the name of the instantiated entity to be the string defined in the ScriptableObject and then appends it with a unique number. 
            currentEntity.name = spawnManagerValues.prefabName + instanceNumber;

            // Moves to the next spawn point index. If it goes out of range, it wraps back to the start.
            currentSpawnPointIndex = (currentSpawnPointIndex + 1) % spawnManagerValues.spawnPoints.Length;

            instanceNumber++;
        }
    }
}
```

挂载上面的脚本到场景中的 GameObject。然后，在 Inspector 中，设置 Spawn Manager Values 字段为 SpawnManagerScriptableObject asset。

如果你在 Inspector 中使用 ScriptableObject 引用，你可以双击 reference field 来打开 ScriptableObject 的 Inspector。你还可以创建一个自定义 Editor 来定义 ScriptableObject Inspector 的展现数据的形式

ScriptableObject 用来派生一个 class，它只用来保存数据，不需要挂载到 gameobjects。

## 静态方法

- CreateInstance(string className)：ScriptableObject

- CreateInstance(Type type)：ScriptableObject

- CreateInstance(): T

创建一个 ScriptableObject 实例。

使用 CreateAssetMenuAttribute 更加容易地创建一个 ScriptableObject 实例，并绑定到一个 .asset file 中。


## 实例方法

- Awake()

  当 ScriptableObject 脚本开始时调用。类似 MonoBehavior.Awake，生命周期中只有一次。

- OnDestroy()

  ScriptableObject 被销毁时调用。

- OnDisable()

  ScriptableObject 离开 scope 时调用。当 object 被销毁时也会调用，可以用于 cleanup code。当 scripts 在编译后重新加载，OnDisable 也会被调用，后面跟着一个 OnEnable（当 script 被加载后）。

- OnEnable()

  当 object 被加载时调用。
