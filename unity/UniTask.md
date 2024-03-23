# UniTask

async 异步函数的调用会生成一个 Task（在 UniTask 中是 UniTask），并开始异步执行，可能在不同的线程，也可能在同一个线程。

async task 的生命周期与 gameobject 甚至 scene 是完全分开独立的。类似 MEC coroutine 不依赖 GameObject 一样，UniTask 的 task 被 UniTask 系统独立管理。

async task 要么执行完毕退出，要么抛出异常退出。

要通过外界取消、终止 async task，必须通过某种形式的信号通信，例如设置一个 bool 变量 IsRun/IsDone 等等。async 异步编程约定的通信方式是从 async 开始的地方一路向下传递一个 CancellationToken 变量。在所有需要检测外部是否想要取消 async task 的地方，检查 cancellationToken.IsCancellationRequested。如果其为 true，则说明外界已经请求取消 async task 了，task 内部就可以结束执行了。

CancellationToken 有很多种方法生成，一般方式是创建一个 CancellationTokenSource 变量 _cts，_cts.Token 就是 CancellationToken。外界可以持有 _cts，在它上面调用 Cancel 方法，将 _cts.Token 传递给 async task。

CancellationTokenSource 还包含几个超时自动 cancel 的方法。

CancellationTokenSource 位于 System.Threading 中。

自定义的 async task 只能通过检查 CancellationToken.IsCancellationRequested 来确定是否要退出 task。一些系统或第三方提供的 UniTask 提供了 WithCancellation() 函数，可以将 token 传入，让这些 task 随着 token cancel 而取消，例如 DOTween 的 Tween，或者 UnityWebRequest 或 Resources.LoadAsync 等等。注意这些操作在 cancel 时不是简单退出，而是抛出 System.OperationCanceledException 异常，因此在 await 外面注意用 try-catch 包围并处理异常。但是如果不抛出异常，也不会报错，UniTask 调度系统会最终捕获异常并移除 task。无论是检查 token.IsCancellationRequested 还是抛出 System.OperationCanceledException 而退出 task，取消点后面的 task 代码都不会执行了。

自定义的 async task 也可以在检测到 token.IsCancellationRequested 的时候，向外界抛出异常。

DOTween 要启用 UniTask 的支持，需要在 Script Compilation Setting 中添加 UNITASK_DOTWEEN_SUPPORT 宏定义。

DOTween 支持的 await 适用于 tween Complete(true/false) 和 Kill(true/false) 的时间点。但是如果想重用 tweens（SetAutoKill(false)），不会按照预期工作。对于其他的时间点，Tween 提供了扩展方法：AwaitForComplete()、AwaitForPause()、AwaitForPlay()、AwaitForRewind()、AwaitForStepComplete。

async 优于 coroutine（包括 MEC）的几点是：

- async task 直接嵌入，在一个 async 函数中直接 await 另一个 async 函数。而 coroutine 则必须为嵌入的 IEnumerator 创建一个新的 coroutine 并等等其完成
- async task 可以返回 value，await 可以返回一个结果，coroutine 不能
- async task 可以进行 try-catch 进行异常处理，coroutine 不能。这非常重要，尤其是异步代码中包含资源申请的情况，coroutine 会随着 GameObject 直接被取消，无法执行任何清理工作，而 async task 在可以在 try-finally 或 using 块中进行资源清理工作

UniTask 是 UniTask 包为 Unity C# 环境提供的轻量级异步编程代替品，代替 C# 语言自身提供的 Task 异步编程模型。UniTask 都是在 Unity 主线程中执行的，因此可以直接调用各种 Unity API，而 C# 的 Task 都是在线程池中调度的。但是 UniTask 也提供了两个特殊的 task，可以将后续的代码在线程池中调度，执行完毕再回到主线程：

```C#
// 多线程示例，在此行代码后的内容都运行在一个线程池上
await UniTask.SwitchToThreadPool();

/* 工作在线程池上的代码 */

// 转回主线程
await UniTask.SwitchToMainThread();
```

C# Task 中，async Task func() 或 async Task<T> func() 都生成一个异步 task，并返回 task 的引用，其他 async 代码可以 await 这个 task。async void func() 则生成一个异步 task，但是不返回 task 的引用。因此这个 task 异步执行，但是不能被其他异步函数 await，属于发射即忘的异步 code。

UniTask 中对应的类型分别是 async UniTask func()，async UniTask<T> func()，和 async UniTaskVoid()。

但是即使返回 task 引用的也可以不 await，task 总是异步执行的，await 只是在两个 async task 之间进行同步。

async code 可以很方便的实现状态机逻辑。

游戏开发中一旦涉及复杂逻辑就要想到状态机。

可以用 MonoBehaviour 实现状态机。OnEnable/OnDisable 作为状态进入退出的点，Update 或创建一个 UniTask 进行状态检查和更新，确定后面要进入的状态。

Unity 物理引擎通常在每一帧更新后进行碰撞检测。因此，如果在当前帧中添加了一个碰撞体/Trigger到场景中，并希望在同一帧内进行碰撞查询，需要等待到下一帧才能正确地检测到该碰撞体。测试中，在 Start 中创建碰撞体/触发器并进行检查，如果用 SceneManagement.LoadScene() 重新加载场景，甚至需要等待 2 帧才能正确检测到 Start 中添加的碰撞体。总之，Unity 物理检测不能期望添加的碰撞体立即能检测。如果想直接检测，可以使用 AssetStore 上的 Intersection Helper。

因为 UniTask 的生命周期是与 GameObject 甚至 Scene 独立的，因此务必要注意 Task 的管理，尤其是 Task 何时以及怎样清理，否则很容易产生资源泄露。UniTask 为 MonoBehaviour 组件提供了 GetCancellationTokenOnDestroy() 方法，它产生一个 token，在组件被销毁时，会对 token 进行 cancel 请求。将这个 token 传递给所有需要随着这个组件进行清理的 Task，就可以实现 Coroutine 那种将异步代码和 GameObject 进行绑定的效果。

