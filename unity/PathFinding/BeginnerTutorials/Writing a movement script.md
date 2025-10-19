# Writing a movement script

首先需要做的是计算一个path。使用Seeker组件的StartPath方法

Path StartPath(Vector3 start, Vector3 end, OnPathDelegate callback = null)

```C#
using UnityEngine;
using System.Collections;
using Pathfinding;

public class AstarAI : MonoBehaviour {
    public void Start() {
        Seeker seeker = GetComponent<Seeker>();
        seeker.StartPath(transform.position, targetPosition.position, OnPathComplete);
    }

    public void OnPathComplete(Path p) {
        Debug.Log("find a path");
    }
}
```

StartPath是异步执行（在其他线程），在回调函数中返回结果。何时返回依赖执行的时间，通常会在下一帧返回结果。

Seeker组件使用Gizmos绘制最后一次计算的路径。

Seeker计算得到的path会执行modifier定义的post process，然后回调。

Callback还会调用注册的Seeker.pathCallback，这样就不必在每次调用StartPath时都指定回调了。

```C#
seeker.pathCallback += OnPathComplete;

seeker.StartPath(transform.position, targetPosition);

// 当disable或destroy脚本时，pathCallback引用没有移除，因此在OnDisable时移除回调函数
public void OnDisable() {
    seeker.pathCallback -= OnPathComplete;
}
```

Path实例包含两个list。Path.vectorPath是一个Vector3 list，其保存path，如果存在任何modifier，这个list将被修改。这是建议使用的获取path的方式。另一种方式是Path.path list，它包含一组GraphNode元素，它保存所有path访问的nodes。可以用来获得遍历路径上的附加信息。

首先一点，总是检查path.error。如果它是true，表示path因为某个原因失败了。Path.errorLog包含很多的错误信息。
