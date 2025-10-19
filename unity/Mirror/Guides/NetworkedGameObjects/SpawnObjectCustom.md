# Custom Spawn Functions

你可以使用 spawn handler functions，在 client 创建 spawned gameobjects 时自定义默认行为。Spawn handler 函数确保你对如何生成 gameobject 具有全面的控制权，以及你如何销毁它。

使用 ClientScene.RegisterSpawnHandler 或 ClientScene.RegisterPrefab 来注册生成和销毁 client gameobjects 的函数。Server 直接创建 gameobjects，然后通过这个功能在 clients 上生成它们。这个 functions 使用 asset ID 或一个 prefab 和两个 function delegates：一个处理在 client 上创建 game objects，一个处理在 client 上销毁 gameobjects。assetID 可以是一个动态的，或者只是你想生成的 gameobject prefab 上找到的 asset ID。

Spawn / unspawn delegates 看起来像这样：

```C#
GameObject SpawnDelegate(Vector3 position, System.Guid assetId) 
{
    // do stuff here
}
```

或

```C#
GameObject SpawnDelegate(SpawnMessage msg) 
{
    // do stuff here
}
```

Unspawn delegates：

```C#
void UnSpawnDelegate(GameObject spawned) 
{
    // do stuff here，poll objects 而不是 destroy objects
}
```
 
当一个 prefab 被保存时，它的 assetId 字段将会被自动设置。如果你想在运行时创建 prefabs，你必须生成一个 GUID。

在运行时生成 prefab：

```C#
// generate a new unique assetId 
System.Guid creatureAssetId = System.Guid.NewGuid();

// register handlers for the new assetId
ClientScene.RegisterSpawnHandler(creatureAssetId, SpawnCreature, UnSpawnCreature);
```

使用现有 prefab：

```C#
// register prefab you'd like to custom spawn and pass in handlers
ClientScene.RegisterPrefab(coinAssetId, SpawnCoin, UnSpawnCoin);
```

Spawn on Server:

```C#
// spawn a coin - SpawnCoin is called on client
NetworkServer.Spawn(gameObject, coinAssetId);
```

Spawn 函数自己使用 delegate 签名来实现。下面是一个 coin spawner。SpawnCreature 看起来一样，但是具有不同的 spawn 逻辑：

```C#
public GameObject SpawnCoin(SpawnMessage msg)
{
    return Instantiate(m_CoinPrefab, msg.position, msg.rotation);
}
public void UnSpawnCoin(GameObject spawned)
{
    Destroy(spawned);
}
```

当使用自定义 spawn functions，有时能够 unspawn gameobjects 而不是 destroying 它们很有用。这可以通过调用 NetworkServer.UnSpawn 来完成。这导致 object 在 server 上被 Reset，并且发送一个 ObjectDestroyMessage 到 clients。这个 ObjectDestroyMessage 将会导致在 clients 上调用自定义 unspawn function。如果有没有自定义 unspawn function，这个 object 就会被销毁。

注意在 host 上，gameobjects 不对 local client 生成，因为它们已经存在于 server 上。这还意味着没有 spawn 或 unspawn handler 函数被调用。

## Setting Up a Game Object Pool with Custom Spawn Handlers

这是一个例子，你如何使用 custom spawn handlers 设置一个简单的 gameobject pooling 系统。然后 Spawning 和 unspawning 将 gameobject 放入或从 pool 取出。

```C#
using System.Collections.Generic;
using Mirror;
using UnityEngine;

namespace Mirror.Examples
{
    public class PrefabPoolManager : MonoBehaviour
    {
        [Header("Settings")]
        public int startSize = 5;
        public int maxSize = 20;
        public GameObject prefab;

        [Header("Debug")]
        [SerializeField] Queue<GameObject> pool;
        [SerializeField] int currentCount;


        void Start()
        {
            InitializePool();

            ClientScene.RegisterPrefab(prefab, SpawnHandler, UnspawnHandler);
        }

        void OnDestroy()
        {
            ClientScene.UnregisterPrefab(prefab);
        }

        private void InitializePool()
        {
            pool = new Queue<GameObject>();
            for (int i = 0; i < startSize; i++)
            {
                GameObject next = CreateNew();

                pool.Enqueue(next);
            }
        }

        GameObject CreateNew()
        {
            if (currentCount > maxSize)
            {
                Debug.LogError($"Pool has reached max size of {maxSize}");
                return null;
            }

            // use this object as parent so that objects dont crowd hierarchy
            GameObject next = Instantiate(prefab, transform);
            next.name = $"{prefab.name}_pooled_{currentCount}";
            next.SetActive(false);
            currentCount++;
            return next;
        }

        // used by ClientScene.RegisterPrefab
        GameObject SpawnHandler(SpawnMessage msg)
        {
            return GetFromPool(msg.position, msg.rotation);
        }

        // used by ClientScene.RegisterPrefab
        void UnspawnHandler(GameObject spawned)
        {
            PutBackInPool(spawned);
        }

        /// <summary>
        /// Used to take Object from Pool.
        /// <para>Should be used on server to get the next Object</para>
        /// <para>Used on client by ClientScene to spawn objects</para>
        /// </summary>
        /// <param name="position"></param>
        /// <param name="rotation"></param>
        /// <returns></returns>
        public GameObject GetFromPool(Vector3 position, Quaternion rotation)
        {
            GameObject next = pool.Count > 0
                ? pool.Dequeue() // take from pool
                : CreateNew(); // create new because pool is empty

            // CreateNew might return null if max size is reached
            if (next == null) { return null; }

            // set position/rotation and set active
            next.transform.position = position;
            next.transform.rotation = rotation;
            next.SetActive(true);
            return next;
        }

        /// <summary>
        /// Used to put object back into pool so they can b
        /// <para>Should be used on server after unspawning an object</para>
        /// <para>Used on client by ClientScene to unspawn objects</para>
        /// </summary>
        /// <param name="spawned"></param>
        public void PutBackInPool(GameObject spawned)
        {
            // disable object
            spawned.SetActive(false);

            // add back to pool
            pool.Enqueue(spawned);
        }
    }
}
```

要使用这个 manager，创建一个新的 empty gameobject 并且添加 PrefabPoolManager 组件（上面的代码）。接下来，多次拖拽一个你想 spawn 的 prefab 到 Prefab field，并设置 startSize 和 maxSize 字段。startSize 当游戏开始时有多少 instance 生成。maxSize 是可以生成的最大数量，如果达到这个最大数量再试图创建更多的 objects 则会给出一个 error。

最后，在你用于 player 移动的 script 中设置一个对 PrefabPoolManager 的引用：

```C#
PrefabPoolManager prefabPoolManager;

void Start()
{
    prefabPoolManager = FindObjectOfType<PrefabPoolManager>();
}
```

你的 player logic 可能包含想下面这些东西，当移动或发射 coins 时：

```C#
void Update()
{
    if (!isLocalPlayer)
        return;
    
    // move
    var x = Input.GetAxis("Horizontal") * 0.1f;
    var z = Input.GetAxis("Vertical") * 0.1f;
    transform.Translate(x, 0, z);

    // shoot
    if (Input.GetKeyDown(KeyCode.Space))
    {
        // Command function is called on the client, but invoked on the server
        CmdFire();
    }
}
```

在 player 的 fire logic 中，使它使用 gameobject pool：

```C#
[Command]
void CmdFire()
{
    // Set up bullet on server
    GameObject bullet = prefabPoolManager.GetFromPool(transform.position + transform.forward, Quaternion.identity);
    bullet.GetComponent<Rigidbody>().velocity = transform.forward * 4;

    // tell server to send SpawnMessage, which will call SpawnHandler on client
    NetworkServer.Spawn(bullet);

    // destroy bullet after 2 seconds
    StartCoroutine(Destroy(bullet, 2.0f));
}

public IEnumerator Destroy(GameObject go, float delay)
{
    yield return new WaitForSeconds(delay);

    // return object to pool on server
    prefabPoolManager.PutBackInPool(go);

    // tell server to send ObjectDestroyMessage, which will call UnspawnHandler on client
    NetworkServer.UnSpawn(go);
}
```

上面的 Destroy 方法显式如何返回 gameobjects 到 pool，使得它们可以在重新 fire 时重新使用。
