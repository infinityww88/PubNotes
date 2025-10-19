# Pooling

Object pooling is used to decrease the load on the garbage collector.

Object pooling 被用于降低 GC 的负载。

Pooling 是对于重度使用 system 或运行在低端硬件（例如移动平台）最大化性能非常好的方法。Mono GC 可以很好收集那些不在使用的 object，但是一个主要的问题是每次 GC 运行时，它需要冻结 freeze 游戏。你可能注意到游戏中每几秒就会出现一个小跳到（hiccups）。尤其是在 ram 和 处理器能力 受限的移动平台上，这将是一个问题。

一个解决方案是 pool 大多数 objects。使用 pools 将会降低 GC 的负载，因此减少游戏的 hiccups 的次数。

## Path Pooling

Pooling 几乎总是和 A* Pathfinding Project 的 Paths 和 lists 一起使用，因为它们是最经常分配的东西。添加 pooling 逻辑到你的脚本中需要非常少的 code，但是如果没有正确使用，会很容易出错。

A* Pathfinding Project 的 pooling 是基于一种手动引用计数。当你开始使用一个 path object，你应该调用它上面的特殊函数 Claim，然后当你停止使用它时，例如因为它被一个更新的 path 替换，你应该使用特殊的 Release 函数来释放它。当在一个 path 上调用 Release 函数，并且没有其他脚本使用它，它可以在任何时间被回收。这意味着它的变量也可以在任何时间被重置，因此当你在 path 上调用 release，你应该从不保持对它的引用（或者至少确保不再重新使用它）。还要注意 path class 的 vectorPath 和 path 列表 在 path 被回收时也被回收。因此你必须确保不再使用它们。如果你真的想要只使用 vectorPath/path 变量，但是回收 path，你可以将它存储为一个局部变量，并设置 path object 上的 vectorPath/path 变量为 null，然后 release path。因为 variable 是 null，path object 不能回收它，因此你可以继续安全地使用它。

如果你不在一个 path 上调用 claim 或者 release，它就简单地不被 pooled。因此如果你不需要操心 pooling，你就不需要。如果你在 path 上只调用 Claim，但是忘记调用 Release，然后所有 references 被移除了，它将会被垃圾回收，但它不会被放回到 pool。如果你在 path 上调用 Release 而没有之前在它上面调用 Claim，或简单地调用 Release 多次，将会打印一个 error。

一个典型的 path pooling 用法：

```C#
public class SomeAI : MonoBehaviour {
    ABPath path;

    public IEnumerator Start () {
        while (true) {
            GetComponent<Seeker>().StartPath(transform.position, transform.position + transform.forward*10, OnPathComplete);
        }
    }

    void OnPathComplete (Path p) {
        //Release any previous paths
        if (path != null) path.Release(this);

        path = p as ABPath;

        //Claim the new path
        path.Claim(this);
    }

    void Update () {
        //Draw the path in the editor
        if (path != null && path.vectorPath != null) {
            for (int i = 0; i < path.vectorPath.Count-1; i++) {
                Debug.DrawLine(path.vectorPath[i], path.vectorPath[i+1], Color.green);
            }
        }
    }
}
```

还要注意当一个 path 被回收，例如当它被 release 之后放回到 pool 中，它上面的 vectorPath 和 path 变量也会被回收。因此从 path 对象获取 vectorPath，然后回收 path object 但继续使用 vectorPath 是不安全的。

Claim 和 Release 函数使用一个 object reference，它主要用于减少出错的可能性。错误检查会被执行，使得一个 path 不会被 release 多次，或 claim 多次。

## List Pooling

或许对大多数 users 不是很重要，但是对于高级 users 很重要。这个 project 还包含一个泛型 lists 的 list pooling。它被系统内部用来避免每次重新分配新的 lists。这些 list pooling 类使用起来很简单，只需要使用 Pathfinding.Util.ListPool.Cliam 获得一个引用，然后当你用完它时，使用 Pathfinding.Util.ListPool.Release 释放它。ListPool 类使用一个类型参数，因此你可以使用任何 list 类型。

```C#
// Get a reference to a list
List<int> myList = Pathfinding.Util.ListPool<int>.Claim();

// Do something with it
for (int i = 0; i < 100; i++) myList.Add(i);
int fiftytwo = myList[52];

// Release it
Pathfinding.Util.ListPool<int>.Release(ref myList);
// The 'ref' parameter in the Release call is used to set the myList variable
// to null at the same time to avoid using the list again by mistake.
```

## Debugging

A* Pathfinding Project 内置了一个 pooling 调试器。添加 Components > Pathfinding > Debugger 到任何 GameObject 上。

另一个非常有用的事情是开启 Optimizations tab 下定义的 ASTAR_POOL_DEBUG，然后每个被销毁的 path 将会打印信息，关于 path 是否被 pooled 或 pooling 是否被错误地使用。
