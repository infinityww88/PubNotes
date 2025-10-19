# Unity async/await

async 用在 Unity 中，不借用任何插件或包装 Task 的 coroutine，并且通过每一帧检查是否完成的peseude-async（伪异步）

Coroutines 是解决特定问题非常棒的方法。但是它有一些特定缺点

- coroutines 不能返回 values。这鼓励开发者创建巨大的 coroutine 方法，而不是通过很多小的方法进行组合。
- coroutines 使错误处理变得困难。你不能将 yield 放在 try-catch 中，因此不能处理异常。同样，当 exceptiosn 发生，stack trace 只能告诉你异常抛出的 coroutine，因此你只能它可能被调用自哪个其他 coroutines

```C#
public class AsyncExample : MonoBehaviour
{
    IEnumerator Start()
    {
        Debug.Log("Waiting 1 second...");
        yield return new WaitForSecond(1.0f);
        Debug.Log("Done!");
    }
}
```

等价 async-await 版本是

```C#
public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        Debug.Log("Waiting 1 second...");
        await Task.Delay(TimeSpan.FromSeconds(1));
        Debug.Log("Done!");
    }
}
```

Unity coroutines 是通过 C# 迭代器 iterator 实现的。StartCoroutine 方法创建的 IEnumerator 迭代器对象被 Unity 保存，并且每一帧这个 iterator object 前进一步（next）来获得被 coroutine yield 的新 values。'yield return' 的不同的 values 被 Unity 读取，来触发特殊 behaviour，例如执行一个嵌套的 coroutine（如果返回的是另一个 IEnumerator），延迟一定的 seconds（如果返回的是 WaitForSeconds），或者只是等待直到下一个 frame（当返回 null）

Unity 中 async 方法默认将运行在 main unity thread 中。在 non-unity C# 应用程序，async 方法经常自动运行在单独的线程中。

一个 async 方法被 await 分为多个 region，每个 region 以及 await 的方法都可能在不同的线程中运行，而不是方法中的 region 总是 main thread 运行，await 方法在其他线程中运行，即使字面上两个被 await 分开的 region 也可能运行在不同的线程。C# 就是简单将 async 方法内部分割成多个片段，每个片段都放在线程池中运行，不会做任何线程同步，需要 code 自己保证线程安全。

Unity API 必须在 main thread 中调用。在底层，Unity 提供一个默认的 SynchronizationContext 称为 UnitySynchronizationContext，它自动收集每一帧被排队的任何 async code，并在 main unity thread 连续运行它们。

MonoBehaviour 的 Start 函数也可以是 coroutine，或者 async 的。因为 Unity 只是简单调用它，并不需要等待它完成。那些需要等待 Start 完成的 code，自己通过各种方式确认 Start 异步 code 是否完成。例如，如果有多个 GameObject 的 Start 很耗时，如果同步地依次等待每个执行完毕，将浪费很多时间。而通过将它们实现为异步的，就可以同时加载了。

## Custom Awaiters

为了可以直接 await TimeSpan，而不是每次都调用 Task.Delay 包装，例如像想要这样的效果：

```C#
public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        // 创建了一个 TimeSpan 对象，但是它不是可以直接 await 的
        await TimeSpan.FromSeconds(1);
    }
}
```

我们只需要为 TimeSpan 添加一个自定义的 GetAwaiter 扩展方法

```C#
public static class AwaitExtensions
{
    public static TaskAwaiter GetAwaiter(this TimeSpan timeSpan)
    {
        // Task.Delay(timeSpan) 是可以 await 的，但是 GetAwaiter 方法需要返回 Awaiter
        // 此外，可以看出 Task.Delay 可以 await，是因为它也有一个 GetAwaiter 方法
        return Task.Delay(timeSpan).GetAwaiter();
    }
}
```

为了在新版本的 C# 中支持 awaiting 一个给定的对象，所有需要做的就是这个 object 有一个 GetAwaiter 方法，其返回一个 Awaiter object。这非常棒，因为它允许我们来 await 任何东西，通过上面的扩展方法，而不需要改变 TimeSpan 类。

我们可以用这种方法支持 awaiting 任何其他类型的对象，包括 Unity 用于 coroutine instructions 的类。我们可以使 WaitForSeconds，WaitForFixedUpdate，WWW 等 都成为 awaitable的，就像它们在 coroutine 中是 yieldable 的一样。我们还可以添加一个 GetWaiter 方法到 IEnumerator 来支持 awaiting coroutines 以允许 async code 和旧的 IEnumerator code 互换。在 asset store 中下载 Async Await Support 或者在 github 上下载 Unity3dAsyncAwaitUtil(https://github.com/svermeulen/Unity3dAsyncAwaitUtil/releases)，得到是这些变为可能的code。这允许你这样做

```C#
public class AsyncExample : MonoBehaviour
{
    public async void Start()
    {
        // Wait one second
        await new WaitForSeconds(1.0f);
 
        // Wait for IEnumerator to complete
        await CustomCoroutineAsync();
 
        await LoadModelAsync();
 
        // You can also get the final yielded value from the coroutine
        var value = (string)(await CustomCoroutineWithReturnValue());
        // value is equal to "asdf" here
 
        // Open notepad and wait for the user to exit
        var returnCode = await Process.Start("notepad.exe");
 
        // Load another scene and wait for it to finish loading
        await SceneManager.LoadSceneAsync("scene2");
    }
 
    async Task LoadModelAsync()
    {
        var assetBundle = await GetAssetBundle("www.my-server.com/myfile");
        var prefab = await assetBundle.LoadAssetAsync<GameObject>("myasset");
        GameObject.Instantiate(prefab);
        assetBundle.Unload(false);
    }
 
    async Task<AssetBundle> GetAssetBundle(string url)
    {
        return (await new WWW(url)).assetBundle
    }
 
    IEnumerator CustomCoroutineAsync()
    {
        yield return new WaitForSeconds(1.0f);
    }
 
    IEnumerator CustomCoroutineWithReturnValue()
    {
        yield return new WaitForSeconds(1.0f);
        yield return "asdf";
    }
}

```

可以看到，这样使用 await 非常强大，尤其是当你开始像 LoadModeAsync 那样组合很多 async 方法时。

对于返回值的 async 方法，方法返回泛型版本的 Task，类型参数为要返回的值，就像上面的 GetAssetBundle。

另外 WaitForSeconds 使用 Unity 时间（timeScale），而 TimeSpan 使用的是系统真实时间。

## 触发 Async Code 和 异常处理

上面定义的一些方法，一些是 async void，一些是 async Task。何时使用一个而不是另一个呢？

主要的区别是，定义为 async void 的方法不可以被其他 async 方法 await，它们只是调用之后被系统管理并异步执行，调用的代码不会在此停住。因此建议总是应该定义 async 方法有一个 Task 的返回类型，这样其他 async 方法就可以 await 它们了。

唯一的例外，就是当你在 non-async 代码中调用 async 方法，例如

```C#
public class AsyncExample : MonoBehaviour
{
    public void OnGUI()
    {
        if (GUI.Button(new Rect(100, 100, 100, 100), "Start Task"))
        {
            RunTaskAsync();
        }
    }
 
    async Task RunTaskAsync()
    {
        Debug.Log("Started task...");
        await new WaitForSeconds(1.0f);
        throw new Exception();
    }
}
```

这里的问题是，当异常发生在 RunTaskAsync 中时，它们将会静默。异常不会被打印在 unity console 中。

这是因为当异常发生在返回 Task 的 async 方法中时，它们被返回的 Task 对象捕获，而不是被抛出并被 Unity 处理。这种行为存在有一个很好的理由：允许 async code 和 try-catch blocks 正确地工作。例如

```C#
async Task DoSomethingAsync()
{
    var task = DoSomethingElseAsync();
 
    try
    {
        await task;
    }
    catch (Exception e)
    {
        // do something
    }
}
 
async Task DoSomethingElseAsync()
{
    throw new Exception();
}
```

C# 运行时管理着所有同时运行的 async object，当在 async 方法内部抛出异常时，系统捕获这个异常并记录在 Task 中，当再次调度 await 的代码时，将这个异常在调用代码中抛出。而 async void 的方法并没有 await 它的代码，也没有 Task 可以保存这个异常，因此当 async void 方法发生异常时，系统就直接抛出来了。

但是这又留下另一个问题，当我们想在 non-async code 中调用 async 方法时应该怎么办。例如我们只想开始一个异步任务，但是并不像等待执行完。我们不想为了打印异常而不得不添加一个 await。如果异步任务发生异常，它不会在抛出到 Unity 中并打印。

要记住这条规则：**永远不要调用 async Task 方法而不 awaiting 返回的 Task。如果你不想等待异步行为完成，你应该只调用 async void 方法**。

async void 方法不能被 await，异常会被系统直接抛出来，而不是记录到 Task 等到调度 await 时再抛出。async void 抛出异常和普通抛出异常的过程一样，如果是在主线程调度，就在主线程抛出，如果实在其他线程调度，就在其他线程抛出，抛出异常的线程如果不捕获异常线程就会退出。但是 Unity 主线程抛出的异常会被 Unity 捕获并打印在 console 上，但是主线程并不会停止，而是继续下一帧，try-catch 应该是加在每一帧上面的。

因此，正确的用法是：

```C#
public class AsyncExample : MonoBehaviour
{
    public void OnGUI()
    {
        if (GUI.Button(new Rect(100, 100, 100, 100), "Start Task"))
        {
            RunTask();
        }
    }
 
    async void RunTask()
    {
        await RunTaskAsync();
    }
 
    async Task RunTaskAsync()
    {
        Debug.Log("Started task...");
        await new WaitForSeconds(1.0f);
        throw new Exception();
    }
}
```

如果运行这段代码，就会看见异常了。

标记为 async void 的方法表示一些异步行为的 root level 的 entry point。一个想象它们的很好的方式是它们是 fire and forget 的任务，离开并在后台执行一些东西，而调用代码立即向下继续执行。

async void 和 async Task 也是一种很好的使用约定，告诉你那些方法应该 await，那些直接调用不需等待。但是你仍然可以为 async Task 创建 async void 的版本，只需要创建一个 wrap 方法就可以了，就像 RunTask 一样。即 async Task 如果是在 non-async 方法调用而发生异常，异常会被忽略，如果是在 async void 调用并 await，则异常会被抛出。

在 Vistual studio 中，调用 async Task 方法而没有 await，将会给出一个警告，这可以很好地避免错误。

作为创建自己的 async void 方法的代替方式，你可以使用一个辅助方法（包含在Async Await Support 这个 package中）为你执行 await。

```C#
public class AsyncExample : MonoBehaviour
{
    public void OnGUI()
    {
        if (GUI.Button(new Rect(100, 100, 100, 100), "Start Task"))
        {
            RunTaskAsync().WrapErrors();
        }
    }
 
    async Task RunTaskAsync()
    {
        Debug.Log("Started task...");
        await new WaitForSeconds(1.0f);
        throw new Exception();
    }
}
```

WrapErrors() 方法简单来说是一个 generic way 来确保 Task 被 await，因此 Unity 总是可以收到抛出的异常。它简单地执行一个 await，仅此而已

```C#
public static async void WrapErrors(this Task task)
{
    await task;
}
```

## 在 coroutine 中调用 async

可以简单地使用另一个 extension 方法实现在 coroutine 中等待 async 方法

```C#
public static class TaskExtensions
{
    public static IEnumerator AsIEnumerator(this Task task)
    {
        while (!task.IsCompleted)
        {
            yield return null;
        }
 
        if (task.IsFaulted)
        {
            throw task.Exception;
        }
    }
}
```

现在可以像这样在 coroutines 中调用 async 方法了

```C#
public class AsyncExample : MonoBehaviour
{
    public void Start()
    {
        StartCoroutine(RunTask());
    }
 
    IEnumerator RunTask()
    {
        yield return RunTaskAsync().AsIEnumerator();
    }
 
    async Task RunTaskAsync()
    {
        // run async code
    }
}
```

## 多线程

我们还可以使用 async-await package 执行多线程代码。

第一种方式是使用 ConfigureAwait 方法：

```C#
public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        // Here we are on the unity thread
 
        await Task.Delay(TimeSpan.FromSeconds(1.0f)).ConfigureAwait(false);
 
        // Here we may or may not be on the unity thread depending on how the task that we
        // execute before the ConfigureAwait is implemented
    }
}
```

被 await 分割的 code region 可以在不同的线程中恢复执行。

Unity 提供了一个称为 default SynchronizationContext 的东西，它将会默认在 main unity thread 中执行异步代码（await 在 main thread 中）。ConfigureAwait 方法允许我们覆盖这个行为，因此结果将会是 await 下面的 code 不在保证运行在 main unity thread 中，而是会继承来自我们执行的任务的 context，有时这正是我们想要的。

如果你想显式在一个后台线程执行代码，还可以

```C#
public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        // We are on the unity thread here
 
        await new WaitForBackgroundThread();
 
        // We are now on a background thread
        // NOTE: Do not call any unity objects here or anything in the unity api!
    }
}
```

WaitForBackgroundThread 也包含在 async-await package 中，它开启一个新的 thread 并确保 Unity 的 default SynchronizationContext 行为被覆盖。

如何返回 Unity thread 中呢？

你可以简单地通过 awaiting 任何我们之前创建的 Unity 特定 objects 来实现，例如

```C#
public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        // Unity thread
 
        await new WaitForBackgroundThread();
 
        // Background thread
 
        await new WaitForSeconds(1.0f);
 
        // Unity thread again
    }
}
```

await-async package 还提供了 WaitForUpdate，如果你想返回 unity thread 而没有任何延迟，可以使用它（上面的 WaitForSeconds 还有 1s 的延迟）。

```C#
public class AsyncExample : MonoBehaviour
{
    async void Start()
    {
        // Unity thread
 
        await new WaitForBackgroundThread();
 
        // Background thread
 
        await new WaitForUpdate();
 
        // Unity thread again
    }
}
```

当然，涉及多线程时，你需要非常小心并行问题，但在很多提升性能的情形中，这是值得的。

## 陷阱和最佳实践

- 避免使用 async void，多用 async Task，除了在 'fire and forget' 情形下，你在 non-async code 中开始 async code。
- 添加 Async 后缀到所有 async Task 方法后面，提醒你应该在前面添加 await，并且添加一个 async void 版本而没有名字冲突。
- 在 visual studio 中调试 async 方法还不可行。但是 ”VS tool for Unity“ 团队已经开始解决这个问题。

## UniRx

Yet another way to do asynchronous logic is to use reactive programming with a library like UniRx. Personally I am a huge fan of this type of coding and use it extensively in many projects that I’m involved with. And thankfully, it is very easy to use alongside async-await with just another custom awaiter. For example:

```C#
public class AsyncExample : MonoBehaviour
{
    public Button TestButton;
 
    async void Start()
    {
        await TestButton.OnClickAsObservable();
        Debug.Log("Clicked Button!");
    }
}
```

I find that UniRx observables serve a different purpose from long-running async methods/coroutines, so they naturally fit alongside a workflow using async-await like in the examples above. I won’t go into detail here, because UniRx and reactive programming is a separate topic in itself, but I will say that once you get comfortable thinking about data flow in your application in terms of UniRx “streams”, there is no going back.
