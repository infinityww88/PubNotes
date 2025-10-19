# Coroutines

- IEnumerator是迭代器，它可以用来产生一系列数据
  - Current
  - MoveNext
  - Reset
- IEnumerable是可迭代的东西，可以从它得到一个迭代器IEnumerator
  - GetEnumerator
- Unity Coroutine同时接受IEnumerator和IEnumerable，如果是IEnumerable，Unity直接调用GetEnumerator得到对应的IEnumerator
- MEC Coroutine函数的类型总是IEnumerator\<float>，Unity Coroutine函数的类型则是IEnumerator，这就是为什么Unity Coroutine需要System.Collections，而MEC Coroutine则需要System.Collections.Generic

## More Effective Coroutines

```C#
using MEC
using System.Collections.Generic
```

System.Collections(IEnumerator) 除了 Unity coroutines，很少使用

- 替换 StartCoroutine(_CheckForWin()) 为 Timing.RunCoroutine(_CheckForWin(), Segment.FixedUpdate)
- 替换 Inumerator _CheckForWin() 为 IEnumerator<float> _CheckForWin()

- 等待下一帧
  - yiled return Timing.WaitForOneFrame
  - yield return 0

- 等待指定秒数
  - yield return Timeing.WaitForSeconds(0.1f)

- 在 Unity Coroutine 中, *yield return SubCoroutine()* 会创建一个新的 coroutine SubCoroutine 并且等待它执行完毕再继续运行。它是 yield return StartCoroutine(SubCoroutine()) 的简写，Unity 在幕后自动为你完成。在 MEC 中，你需要这样做：
  ```C#
  yield return Timing.WaitUntilDone(Timing.RunCoroutine(SubCoroutine()));
  // 或者
  yield return Timing.WaitUntilDone(SubCoroutine());
  ```

MEC coroutines 在它们创建所在的 GameObject 被销毁或 disabled 时，不会像 Unity 的 coroutine 那样自动停止运行。因为不是对所有 coroutines 都是合理的，一些 coroutines 就需要一直在背后运行。

如果 coroutine 不工作在 gameobject 上，最好情况是需要耗费检查的时间，最坏的情况则将会导致不期望的行为。如果你想像 Unity coroutine 一样检查，使用 CancelWith 扩展：

```C#
// 协程 _moveMyButton 和 gameObject 关联在一起
Timing.RunCoroutine(_moveMyButton().CancelWith(gameObject));
```

这样总是检查 gameObject 的状态，因此当它被 disabled 或 destroyed 时，coroutine 将会被 stopped 或 destroyed。

或者你可以手动检查，每个 yield return statement 之后执行以下检查：

```C#
if (gameObject != null && gameObject.activeInHierarchy) {
  return 0;
}
```

- yield return Timing.WaitUntilDone(MyCoroutine)
- yield return Timing.WaitUntilTrue(FunctionThatReturnsBool)
- yield return Timing.WaitUntilFalse(FunctionThatReturnsBool)

## Slow Update

- Timing.Instance.TimeBetweenSlowUpdateCalls = 1/7f;
- absolute timescale
- Timing.RunCoroutine(Coroutine(), Segment.SlowUpdate)
- 使用 Timing.DeltaTime 而不是 Time.deltaTime

Tags：使用 KillCoroutine(tag) 或 KillAllCoroutine(tag) kill coroutine 或者 coroutine group

LocalTime 和 DeltaTime

Unity.Time 类适合绝大多数对时间的访问，但是在 SlowUpdate 中不能正确工作，而在 EditorUpdate 和 EditorSlowUpdate segment 中完全不可用。使用 TimingLocalTime 和 Time.DeltaTime

## 更多功能

- CallDelayed: 在指定时间（seconds）之后调用指定的动作
- CallContinously: 在指定时间内（seconds）每帧调用指定动作
- Call Periodically: 在指定时间内每个指定秒数调用一次指定动作
- 这三个中的每个都可以很容易地使用 coroutines 手动创建，但是这些基本功能经常被使用，因此被包含在了基础模块中

Unity Coroutines 被附加在它们开始的 object，而 MEC 使用一个中心的 object 运行所有的 coroutines。如果当前 object 是 disabled 的，Unity Coroutine 不会开始，但是 MEC coroutine 则不关心。如果你 disable 一个 gameobject，则它上面的所有的 Unity coroutine 都会退出运行（它们不会在 re-enable 时 resume）。MEC coroutines 不会这样，除非你显式指定它们这样做。 

如果一个 GameObject 被销毁了，它上面挂载的所有 coroutines 都被 kill。MEC coroutines 不会这样。

Unity Coroutines 不允许你在 gameobject 外面暂停和恢复 coroutines。

MEC coroutines 允许你在 LateUpdate，SlowUpdate 和更多 segments 中运行 coroutine。

## 协程生命周期的高级控制

Timing 是一个组件。

默认地，它创建一个 gameobject 来保存自身，所有的静态函数在这里处理。

你可以添加它到任何 gameobject，使用组件实例来调用函数，所有的 coroutines 保存在那个组件实例中。

OnError delegate 和 TimeBetweenSlowUpdateCalls 变量被附加在 Timing 组件上，因此你可以对不同的 timing objects 设置不同的 error handling，或者设置 SlowUpdate 运行在不同的 rate。

每个 Timing 组件是一个作用域，管理使用它创建的全部 coroutines。

## Editor Update

Unity coroutine 不能运行在 editor 中，但是 MEC coroutine 可以。

Editor coroutines 通常用于：

- 为开发者在游戏运行前提供一个预览效果，例如驱动 Editor Scene 的物理引擎。
- 执行 update 实时编辑
- 那些需要在 app 被编译之前需要完成的网络同步任务

当点击 play 按钮时，Editor coroutines 都会被销毁，并且在 play mode 中不会运行。

Time.time 和 Time.deltaTime 在 editor mode 中不能工作，相反，你应该使用 Timing.LocalTime 和 Timing.DeltaTime。

Segment.EditorUpdate/EditorSlowUpdate

[ExecuteInEditMod]

## RealtimeUpdate

  - Segment.RealtimeUpdate
  - just like update, but Timing.LocalTime and Timing.DeltaTime ignore Unity's timescale
  - This can be useful while controlling menus that happen while your game is paused(if you pause by turning the timescale to 0)
- Layers and Tags
  - coroutine can be marked by both layer and tag
  - layer is int, tag is string
  - You can supply one, the other, or both
  - Once you specify layer/tag, you can pause/resume, kill, or RunCoroutineSingleton
- Timing.RunCoroutine(_MoveUpAndDown(), gameObject.GetInstanceID())
- Timing.ResumeCoroutines(gameObject.GetInstanceID())
- Timing.PauseCoroutines(gameObject.GetInstanceID())
- In Unity every GameObject is assigned a unique number(gameObject.GetInstanceID()), this id can be change every time you run the application, but it is guaranteed that no other gameObject will be assigned the same id during a single run.
- RunCoroutineSingleton
  - Run coroutine only once
  - Apply a unique tag to every coroutine in the set
    - Timing.RunCoroutineSingleton(coroutine(), "singletontag")
    - CoroutineHandle handle
      - handle = Timing.RunCoroutineSingleton(coroutine(), handle, SingletonBehavior.Overwrite)
- SingletonBehavior: how conflicts will be handled
  - Abort: fail to run the your coroutine if there is already one defined that matches your parameters
  - Overwrite: kill any matching coroutines and run yours
  - Wait: keep your coroutine paused until all the matches have finished and then execute yours
    - With wait, you can set up a queue of coroutines to run one after the other by giving them all the same tag and setting them to wait.
- Pause and Resume
  - pause all coroutines with a particular tag or layer and resume them later
  - Timing.PauseCoroutines("tag")
  - Timing.ResumeCoroutines("tag")
- Controlling Coroutines by Handle
  - Timing.RunCoroutine() return a CoroutineHandle
  - Handle can be used to make one coroutine wait for another using "yield return Timing.WaitUntilDone(handle)"
  - get/set handle.Tag or handle.Layer
  - get/set handle.Segment
  - IsRunning/IsPaused/IsValid
  - Linking coroutine handles
    - Handles can be linked to one another using the LinkCoroutine function.
    - The master coroutine will send a kill commond to the slave coroutine when it ends(either from kill command or just by ending the function)
    - It will also copy any pause or resume commands(but not any calls to WaitForSeconds, instead, the Timeing.PauseCoroutines command)
    - The slave will always be terminated or paused along with the master
- GetMyHandle
  - Get your own handle from within a coroutine
  - A special function that does not cause a one frame delay even though it's in a yield return statement
  - Accept a lambda as parameter, GetMyHandle calls the lambda and pass handle of current coroutine to it
  - yield return Timing.GetMyHandle(x => myHandle = x)
  - You can use your own handle to set up links on the fly, change your own tags, etc.
- Extension Methods
  - Run the same coroutine but change the way it runs while running it
  - AddDelay: runs the coroutine after a delay
    - Timing.RunCoroutine(Coroutine().AddDelay(1f))
  - CancelWith
    - Cancel with GameObject
      - Coroutine will automatically be terminated if the GameObject is destroyed or disabled
      - Chain CancelWith calls to associate with multiple GameObject
        - Timing.RunCoroutine(Coroutine().CancelWith(obj1, obj2).CancelWith(obj4))
    - Cancel with bool funciton
      - Coroutine will be terminated as soon as that function returns false.
  - Append and Prepend
    - Chain two or more coroutines together.
    - Append a delegate to the end of a coroutine, so it can be called when coroutine is done.
  - Superimpose
    - combine two coroutines into a single handle
    - it won't finish until both coroutines are done
    - use WaitUntilDone function to make a coroutine wait until both functions finish before continuing
    - handle = Timing.RunCoroutine(Coroutine0().Superimpose(Coroutine1().Superimpose(Coroutine2())))
  - Hijack
    - alter the return value of a coroutine
- Unity StartCoroutine return a Coroutine, MEC RunCoroutine return a handle, they are the same thing which is just a reference to the actual coroutine, and can be used to pause/resume/stop the coroutine.
  - From outside of coroutine, Unity Coroutine can only stop the coroutine, but MEC can also pause and resume the coroutine.
