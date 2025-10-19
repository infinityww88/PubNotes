# Searching for paths

这个文档是有关于要编写自己的移动脚本或者因为其他原因需要计算路径的情景。如果使用内置的移动脚本，只需要设置destination属性就可以了。

路径查询失败时查看错误码确定问题。

## 使用Seeker搜索路径

有很多方式可以查询路径。最简单的方式是给要查询路径的GameObject添加一个Seeker component，然后调用Seeker.StartPath()。Seeker自动处理modifiers。

一个Seeker每次只执行一个pathfinding。如果在上一个查询还没有结束的时候发起一个新的请求，上一个请求将被取消。

```C#
using Pathfinding;

public void Start() {
    var seeker = GetComponent<Seeker>();
    seeker.StartPath(transform.position, transform.position + transform.forward * 10, OnPathComplete);
}

public void OnPathComplete(Path) {
    if (p.error) {
        // 未发现可用路径，检查error是什么问题
    }
    else {
        // 得到可用路径，使用p.vectorPath
    }
}
```

常见的错误是认为path在调用StartPath之后立即可用。StartPath只是将请求放在queue中，之所以这样做是因为当有很多单位同时要计算它们的路径时，期望的是在多个frames中分散路径计算的压力，避免FPS drops。如果multithreading开启，还会在其他线程中计算路径。如果需要立即得到路径，使用Pathfinding.BlockUntilCalculated方法。

```C#
Path p = seeker.StartPath(transform.position, transform.position + Vector3.forward * 10);
p.BlockUntilCalculated();
// 现在path可用了
```

还可以在一个coroutine中使用Pathfinding.Path.WaitForPath

```C#
IEnumerator Start() {
    Path p = seeker.StartPath(transform.position, transform.position + Vector3.forward * 10);
    yield return StartCoroutine(path.WaitForPath());
}
```

还可以调用Seeker方法时使用自定义的path objects。这可以在计算路径之前改变path object上的设置。

```C#
// 创建一个新path object，最后一个参数时回调函数。上面StartPath返回的就是一个path object。但是它在StartPath内部已经创建好了，没法再修改设置了。因此可以自己创建一个path object
// 使用静态方法创建path object可以利用path pool，避免GC尖峰
Path p = ABPath.Construct(transform.position, transform.position + Vector3.forward * 10, null);
// 默认如果target point不可到达时，搜索距离它最近的可到达node。但是对于turn based游戏，可能不希望如此。因此设置NNConstraint.None关闭最近walkable node的搜索
// 这个设置不能在上面的StartPath方法中指定
p.nnConstraint = NNConstraint.None;
// 将自己创建的path object传递给seeker
seeker.StartPath(p, OnPathComplete);
```

Seeker的pathCallBack事件在每次pathfinding之后都会调用，这样就不必每次StartPath都指定一个回调函数了。

```C#
seeker.pathCallback += OnPathComplete;
seeker.StartPath(transform.position, transform.position + Vector3.forward * 10);
```

pathCallback是持久的，因此好的习惯是在OnDisable时取消callback。

```C#
seeker.pathCallback -= OnPathComplete;
```

Seeker组件是用来对单个character执行pathfinding的。因此它同时只处理一个request。要显式取消一个request，调用Seeker.CancelCurrentPathRequest()。

如果要并行计算多个path，直接使用AstarPath类

## 其他类型路径

MultiTargetPath

Path path = seeker.StartMultiTargetPath(transform.position, endPoints, true);

最后一个参数指定是要搜索一条能到达endPoints(Vector3[])的path，还是只到最近的一个point。

返回Path，但是可以转换成MultiTargetpath

通用type pathfinding查询

```C#
Path p = MyPathType.Construct(...); // MyPathType = MultiTargetPath or ABPath or ...
seeker.StartPath(p, OnPathComplete)
```

使用Construct方法而不是构造函数，使得可以使用path polling

## 直接使用AstarPath类

最全面的控制：AstarPath.StartPath。

可以同一时间计算很多paths。Seeker同一时间只能计算一个path。

使用AstarPath.StarPath计算的paths不会被后期处理。但是可以在得到一个path后调用Seeker.PostProcess，使用Seeker上挂载的modifiers后期处理它

AstarPath就是全局Astar对象上的组件

```C#
// scene中必须有一个AstarPath实例
if (AstarPath.active == null) return;

// 并行异步计算多个paths
for (int i = 0; i < 10; i++) {
    // 没有seeker跟踪callbacks，需要每次重新指定callback
    var p = ABPath.Construct(transform.position, transform.position + transform.forward * i * 10, OnPathComplete);
    // 在AstarPath.active上计算路径
    AstarPath.StartPath(p);
}

```

游戏程序也是普通程序，只是调用的图形API而已，和调用网络API的网络程序没有区别。所有程序设计的方法在这里都使用。Unity中的scene就是一组GameObjects而已，切换scene就是销毁当前GameObject，加载另一个scene asset定义的gameobject。scene和prefab一样，只是普通的资源文件，作为加载的模板。如果将一个scene所有的gameobjects都挂载到一个gameobject，称之为root，则scene就是project中的prefab而已，其中包含一组初始的gameobjects，而切换scene，就是销毁当前的root，实例化另一个scene的root。
