# Searching for path

## Searching for paths using a Seeker

有很多方法可以查询路径。最近的方法是将一个 Seeker 组件挂载到你想要查询路径的 GameObject 上，然后调用 seeker.StartPath()。

注意 Seeker 每次只能进行一个 pathfinding。如果在前一个完成之前发送了一个新的查询，前一个会被取消。Seeker 还自动处理 path modifiers。

```C#
using Pathfinding;
public void Start () {
    // Get the seeker component attached to this GameObject
    var seeker = GetComponent<Seeker>();
    // Start a new path request from the current position to a position 10 units forward.
    // When the path has been calculated, it will be returned to the function OnPathComplete unless it was canceled by another path request
    seeker.StartPath (transform.position, transform.position+transform.forward*10, OnPathComplete);
    // Note that the path is NOT calculated at this stage
    // It has just been queued for calculation
}
public void OnPathComplete (Path p) {
    // We got our path back
    if (p.error) {
        // Nooo, a valid path couldn't be found
    } else {
        // Yay, now we can get a Vector3 representation of the path
        // from p.vectorPath
    }
}
```

一个常见的错误是假设 StartPath 调用完之后 path 就被计算出来。实际上 StartPath 只将 path 请求放在 queue 中就返回了。因为当有很多 units 同时计算 paths 时，需要将计算分散在多个帧中以避免掉帧。当开启多线程后，还可以在其他线程中计算路径。有一些情景需要立即计算路径，则可以使用 Pathfinding.Path.BlockUntilCalcualted 方法。

```C#
Path p = seeker.StartPath (transform.position, transform.position + Vector3.forward * 10);
p.BlockUntilCalculated();
// The path is calculated now
```
还可以再 coroutine 中使用 Pathfinding.Path.WaitForPath() 来等待 path 计算完成。

```C#
IEnumerator Start () {
    var path = seeker.StartPath (transform.position, transform.position+transform.forward*10, OnPathComplete);
    // Wait... (may take some time depending on how complex the path is)
    // The rest of the game will continue to run while waiting
    yield return StartCoroutine (path.WaitForPath());
    // The path is calculated now
}
```
还可以创建自己的 path objects，而不是使用 Seeker 的方法。这允许在计算之前改变 path object 的设置。

```C#
// Create a new path object, the last parameter is a callback function
// but it will be used internally by the seeker, so we will set it to null here
// Paths are created using the static Construct call because then it can use
// pooled paths instead of creating a new path object all the time
// which is a nice way to avoid frequent GC spikes.
var p = ABPath.Construct (transform.position, transform.position+transform.forward*10, null);
// By default, a search for the closest walkable nodes to the start and end nodes will be carried out
// but for example in a turn based game, you might not want it to search for the closest walkable node, but return an error if the target point
// was at an unwalkable node. Setting the NNConstraint to None will disable the nearest walkable node search
p.nnConstraint = NNConstraint.None;
// Start the path by sending it to the Seeker
seeker.StartPath (p, OnPathComplete);
```

每次指定一个 callback 函数看起来很枯燥。Seeker 上有个一个字段，可以设置一个 function，每次 path 返回时都调用它，这对性能也有好处，因为不必每次分配一个 delegate。

```C#
// Set the path callback, this should be done once
seeker.pathCallback += OnPathComplete;
// Now we can skip the callback function parameter
seeker.StartPath (transform.position, transform.position+transform.forward*10);
```
注意 callback 是永久的，但是 component 则可能不是。所以最好在组件销毁时取消 callback：

```C#
public void OnDisable () {
    seeker.pathCallback -= OnPathComplete;
}
```

seeker.pathCallback 是一个委托，可以添加多个函数，而不限制为一个函数。

Seeker 组件目的是为游戏中的一个角色进行路径查询。因此它设计为每次只进行一个 path 请求。如果在前一个请求没完成之前，发送了一个新请求，则取消前一个，并打印一个警告日志。如果特别指定想取消前一个 path 请求而又不想打印警告日志，可以使用 Seeker.CancelCurrentPathRequest()。

如果想同时计算多个 path，可以跳过 seeker，直接使用 AstarPath。

### Other types of paths

除了标准的 path，还有一些其他类型的 path，例如 MultiTargetPath。

These can be started easily as well, especially the MultiTargetPath since the Seeker has a special function for it

```C#
// Start a multi target path, where endPoints is a Vector3[] array.
// The last parameter specifies if a path to all end points should be searched for
// or only to the closest one
seeker.StartMultiTargetPath (transform.position, endPoints, true);
```

返回的 path 是 Path 的实例，但是可以转换为 MultiTargetPath 来获得所有数据。

The generic way to start a type of path is simply

```C#
Path p = MyPathType.Construct (...);    // Where MyPathType is for example MultiTargetPath
seeker.StartPath (p, OnPathComplete);
```
The Construct method is used instead of a consructor so that path pooling can be done more easily.


## Calling AstarPath directly

有时你想要对每个 path 进行更多的控制。为此可以直接调用 AstarPath 组件。使用的主要函数是 AstarPath.StartPath。如果想同时计算很多路径，这很有用。

但是 AstarPath.StartPath 计算的路径不会进行 post-processed。但是在 path 计算之后，可以调用 Seeker.PostProcess，来应用组件上挂载的 modifiers。

```C#
// There must be an AstarPath instance in the scene
if (AstarPath.active == null) return;
// We can calculate multiple paths asynchronously
for (int i = 0; i < 10; i++) {
    // As there is not Seeker to keep track of the callbacks, we now need to specify the callback every time again
    var p = ABPath.Construct(transform.position, transform.position+transform.forward*i*10, OnPathComplete);
    // Start the path by calling the AstarPath component directly
    // AstarPath.active is the active AstarPath instance in the scene
    AstarPath.StartPath (p);
}
```
