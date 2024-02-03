# More Effective Coroutines

MEC 比 Unity coroutine 快 2 倍，并且每帧 0 内存分配。它已经被详尽测试和完善，以最大化性能，并为 app 创建坚实的基础。

## 从 Unity Coroutine 迁移到 MEC

Unity Coroutine:

```C#
StartCoroutine(_CheckForWin());
```

MEC:

```C#
Timing.RunCoroutine(_CheckForWin()); // run in update segment
Timing.RunCoroutine(_CheckForWin(), Segment.FixedUpdate); // run in fixed update
Timing.RunCoroutine(_CheckForWin(), Segment.LateUpdate); // run in late update
Timing.RunCoroutine(_CheckForWin(), Segment.SlowUpdate); // run in slow update
```
注意要确保对任何移动或改变 GameObjects 的 coroutines 的 RunCoroutine 调用使用 CancelWith(gameObject)，否则会在 screen 切换的中间遇到 null reference 异常。

Unity Coroutine 的函数签名是 IEnumerator，而 MEC Coroutine 的函数签名是 IEnumerator\<float\>。

要等待下一帧，使用 yield return Timing.WaitForOneFrame，或者就是 yield return 0. 它们两个等价，但是建议使用前者，因为它更具有可读性。

要等待指定的时间，Unity 使用 yield return new WaitForSeconds(0.1f)，MEC 使用 yield return Timing.WaitForSeconds(0.1f)。

Unity 默认的 coroutines 允许使用 yield return 为简写来创建一个 coroutine，并等待它完成才在继续执行。

```C#
IEnumerator _EnableHappyFace() {
    yield return _CheckForWin();
    HappyFaceObject.SetActive(true);
}
```

上面的 yield return _CheckForWin() 等价与 yield return StartCoroutine(_CheckForWindow())，但是 Unity 在幕后为你调用了 StartCoroutine。

MEC 对应的简写方式是：

```C#
IEnumerator<float> _EnableHappyFace() {
    yield return Timing.WaitUntilDone(_CheckForWin());
    // 等价于 yield return Timing.WaitUntilDone(Timing.RunCoroutine(_CheckForWin()))，MEC 幕后自动调用 RunCoroutine
}
```

注意，因为 yield return _CheckForWin() 实际上是 MEC 创建了一个新的 Coroutine，因此当 Kill 主 Coroutine 后，新创建的 Coroutine 不会被自动 Kill。要使新的 Coroutine 与主 Coroutine 一起被 Kill，可以使用 LinkCoroutines 或 KillWith（就像 CancelWith）。

注意 LinkCoroutines 需要两个 Coroutine Handle。调用 Timing.RunCoroutine() 立即返回 CoroutineHandle，Coroutine 函数内部也可以使用 Timing.CurrentCoroutine 得到 Coroutine 的 Handle。但是立即返回或得到的 Handle，不是 valid 的，而是 uninitialized 的。此时 Link 或 KillWith 都是无效的，只有至少 Timing.WaitForOneFrame 之后，才能得到有效的 Handle。

KillWith 可以在创建 Coroutine 的时候就连接主 Coroutine，不用等到 Handle 变成 valid 的，即：

```C#
yield return Timing.WaitUntilDone(_CheckForWin().KillWith(Timing.CoroutineHandle));
```

这对串联 Coroutines 非常重要。

## CancelWith

很多时候会想要在 coroutine 中修改 gameobjects。MEC coroutines 不会像 Unity 那样在 GameObject 销毁或 disabled 时自动停止运行在它们上面创建的 coroutines。这是因为这对所有 coroutines 并不总是有意义的，有些 coroutine 并不修改 GameObject，也不想随着 GameObject 销毁而停止。要想 MEC coroutines 像 Unity 那样随着 GameObject 销毁而停止，可以使用 CancelWith：

```C#
Timing.RunCoroutine(_moveByButton().CancelWith(gameObject));
```

## Pause and Resume coroutine

Unity coroutine 不支持暂停和恢复，MEC 支持：

```C#
Timing.PauseCoroutines(handle);
Timing.ResumeCoroutines(handle);
```

重复暂停和恢复已经处于那个状态的 coroutine 也没问题。

如果 coroutine 已经 yield 一个 WaitForSeconds，则 coroutine 暂停时 seconds 不会 count down。

## WaitUntilDone

Unity 默认的 coroutines 有一些情景，可以 yield return 一些变量。例如可以 yield return asyncOperation。MEC 也有一个函数完成相同的事情：WaitUntilDone：

```C#
yield return Timing.WaitUntilDone(wwwObject);
yield return Timing.WaitUntilDone(asyncOperation);
yield return Timing.WaitUntilDone(customYieldInstruction);
// With MEC Pro you can do a little more with WaitUntilDone:
yield return Timing.WaitUntilDone(newCoroutine);
// The above automatically starts a new coroutine and holds 
the current one.
yield return 
Timing.WaitUntilTrue(functionDelegateThatReturnsBool);
yield return 
Timing.WaitUntilFalse(functionDelegateThatReturnsBool);
```

## SlowUpdate

MEC 提供了一个 Unity 没有的 Update Loop：Slow Update。

slow update loop 默认每秒运行 7 次。它使用绝对 timescale，因此 slow down Unity timescale 不会 slow down SlowUpdate。它很适合诸如显示 text 这样的任务。

SlowUpdate 和 yield return Timing.WaitForSeconds(1/7f) 的区别：

- SlowUpdate 使用绝对时间，时间缩放不会影响
- 所有的 SlowUpdate ticks 同时发生。这很重要，因为每秒改变 7 次 text 只有在所有 text 同时改变看起来才流畅

SlowUpdate 还可以用来检查临时的 debugging 变量。

注意 Unity 的 Time.deltaTime 变量在 SlowUpdate 中不会返回正确的值，因为 Unity Time 对这个 Slow Update Loop 完全不知道。但是可以使用 Timing.DeltaTime。在 MEC 中，Timing.DeltaTime 和 Timing.LocalTime 总是具有正确的值，不管在哪个 timing segment。

## Tags

可以为 coroutine 提供一个 string 的 tag。但为一个 coroutine 或一组 coroutines 设置 tag，后面可以使用 KillCoroutine(tag) 或 KillAllCoroutines(tag) 结束它们。

```C#
Timing.RunCoroutine(_shout(1, "Hello"), "shout");
Timing.KillAllCoroutines("shout");
```

## LocalTime and DeltaTtime

MEC 在每个 segment 内跟踪 local time，保持 LocalTime 和 DeltaTime 变量的更新，就像 Time.time 和 Time.deltaTime 一样。默认的 Time class 在大多数情况下也可以用，但是在 SlowUpdate 中不行，而且在 EditorUpdate 和 EditorSlowUpdate segment 中完全不可用。因此在 MEC coroutine 中最好使用 Timing.LocalTime 而不是 Time.time。
 
## 辅助函数

Timing 中还有一些辅助函数，可用于简化一些常见应用：

- CallDelayed：在指定的时间后调用 action
- CallContinously：在指定的时间内每帧调用 action
- CallPeriodically：在一定时间内，每 x 秒调用一次 action

这三个功能用 coroutine 都可以很容易实现，但是这些基本功能太常用，因此提供了包装函数。

```C#
using UnityEngine;
using System.Collections.Generic;
using MovementEffects;
public class Testing : MonoBehaviour
{
    void Start ()
    {
        CoroutineHandle handle = 
            Timing.RunCoroutine(_RunFor10Seconds());

        handle = Timing.RunCoroutine(_RunFor1Second(handle));

        Timing.RunCoroutine(_RunFor5Seconds(handle));
    }

    private IEnumerator<float> _RunFor10Seconds()
    {
        Debug.Log("Starting 10 second run.");

        yield return Timing.WaitForSeconds(10f);

        Debug.Log("Finished 10 second run.");
    }

    private IEnumerator<float> _RunFor1Second(CoroutineHandle waitHandle)
    {
        Debug.Log("Yielding 1s..");

        yield return Timing.WaitUntilDone(waitHandle);

        Debug.Log("Starting 1 second run.");

        yield return Timing.WaitForSeconds(1f);

        Debug.Log("Finished 1 second run.");
    }

    private IEnumerator<float> _RunFor5Seconds(CoroutineHandle
waitHandle)
    {
        Debug.Log("Yielding 5s..");

        yield return Timing.WaitUntilDone(waitHandle);

        Debug.Log("Starting 5 second run.");

        yield return Timing.WaitForSeconds(5f);

        Debug.Log("Finished 5 second run.");
    }
}
```

```C#
// 两秒后开始 _RunFor5Seconds
Timing.CallDelayed(2f, delegate {
	Timing.RunCoroutine(_RunFor5Seconds(handle));
});

// 和上面一样，但是不创建闭包（闭包将创建一个 GC alloc，保存局部变量）
// handle 传递给 CallDelayed，CallDelayed 将它作为变量 x 传递回 RunCoroutine。
Timing.CallDelayed<IEnumerator<float>>(handle,
	2f,
	x => { Timing.RunCoroutine(_RunFor5Seconds(x)); }
);
```

## Fluid Architecture

还有一种流式语法可以更简洁创建 Coroutine，它是完全可选的：

```C#
Timing.RunCoroutine(_Foo().CancelWith(gameObject));

_Foo().CancelWith(gameObject).RunCoroutine();
```

流式语法就是把 RunCoroutine 放在最后：coroutine_function.modifier.modifier.RunCoroutine，而不是 RunCoroutine(coroutine_function.modifier)。这种语法称为 fluid 是因为这种逻辑从 starting point 流向 conclusion.

但是要记住，如果忘记使用 RunCoroutine，编译器不会报错，但是不会执行 coroutine。因此还是建议使用函数调用式的语法。

## FAQ

- WaitForEndOfFrame

  MEC 没有提供这个等价物，但是提供了一个 segment 用于在 frame end 执行逻辑。

  WaitForEndOfFrame 实际做到事情有点 confusion。如果只是想等待下一帧执行，WaitForEndOfFrame 不是一个理想的命令，更好的是使用 yield return null。

  很多人使用 Unity coroutines 时使用 WaitForEndOfFrame 只是因为它是最接近 WaitForOneFrame 的名字的命令（Unity 没有提供 WaitForOneFrame，在 Unity 中等待下一帧只需要 yield return null）。但是却没有意识到潜在的问题。

  MEC 为此定义了常量 Timing.WaitForOneFrame。

- StopCoroutine

  MEC 结束 coroutine 使用 Timing.KillCoroutines()，可以传递一个 handle 或一个 tag。

  KillCoroutine 用于在 coroutine 外面来停止 coroutine，在 coroutine 内部，使用 yield break 来停止。

- 停止所有 coroutines

  Timing.KillCoroutines()。如果想暂停、恢复 coroutine，使用 Timing.PauseCoroutines()，Timing.ResumeAllCoroutines().

- 陷入另一个 coroutine，等待其完成再继续

  Timing.WaitUntilDone(coroutineHandle)。注意另一个 coroutine 无论是如何创建的，都是独立的，终止外面的 coroutine 不会终止内部的 coroutine。因此要使内部的 coroutine 随外面的 coroutine 的终止而终止，可以用 Timing.LinkCoroutines(handle1, handle2) 将它们连接在一起，但是这需要两个 handle 都是 valid 的，但是刚开始创建的 Coroutine 返回的 handle 都还不是 valid，而是 uninitialized，Coroutine 至少 yield 一次后 handle 才有效。要一开始就将内外两个 handle 连接在一起，可以在创建内部 coroutine 时立即 link 两个 coroutine，可以用 yield return Timing.WaitUntilDone(_Coro().KillWith(Timing.CurrentCoroutine))。

- 与 Unity Coroutine 的一些区别

  Unity coroutine 挂载到一个 object 上，而 MEC 使用一个中央 object 来运行所有 coroutine。这意味着：

  - 如果 gameobject 是 disabled 的，Unity coroutine 不会开始，MEC coroutine 和 gameobject 没有关联，因此 gameobject 的状态与 coroutine 无关。

  - 如果 disable 一个 GameObject，则挂载到它上面的所有 coroutine 都会退出，而且在 gameobject re-enable 之后不会恢复。MEC coroutine 则不会，除非显式告诉它这样做，而且 MEC coroutine 可以显式暂停和恢复。

  - 如果 start Unity coroutine 的 GameObject 被销毁，所有挂载到它上面的 coroutines 都会被 killed。MEC coroutine 则不会。

  - MEC coroutine 可以创建 coroutine groups，这可以同时暂停、恢复一组 coroutines。Unity coroutines 不允许在外面暂停和恢复 coroutines。Unity coroutines 总是以 gameobject 分组。

  - MEC coroutine 可以运行在 LateUpdate 或 SlowUpdate segment。

  - MEC coroutine 的创建是 static，可以在任何地方创建，不依赖任何 GameObject。Unity coroutine 只能在 GameObject 内创建。

## Editor Update

Unity Coroutine 不能运行在 editor 中，但是 MEC coroutine 可以。

Editor coroutines 通常用于让开发者在游戏运行之前预览效果，或者执行在 app 编译之前需要完成的更新或网络同步任务。Editor coroutines 在进入 play mode 时被销毁。

Editor coroutines 中不能使用 Time.time 或 Time.deltaTime，应该使用 Timing.LocalTime 和 Time.DeltaTime。

要保守地使用 editor coroutines。一个无限循环或非常耗时的函数可能摧毁你的整个项目。总是确保备份好项目。

要在 editor 中运行 coroutines，使用 EditorUpdate 或 EditorSlowUpdate segment。确保 class 有 [ExecuteInEditMode] tag，然后正常运行它们。

## Realtime Update

RealtimeUpdate 是另一个 segment。它就像 update，但是 Timing.LocalTime 和 Timing.DeltaTime 忽略 Unity 的 timescale。这可以用于在游戏暂停 (timescale=0) 时控制菜单。

## Manual Timeframe

Manual timeframe segment 可以用于一些不常见的游戏机制。

如果只是在 default mode 运行它们，则 manual timeframe coroutines 会在 update segment 运行，在 update coroutines 之后，在 late update coroutines 之前。

如果改变 Timing.Instance.SetManualTimeframeTime 中的 delegate，则可使 coroutine 有和其他 segemnts 不同的 manual timeframe count time，这可以改变 time flow 速率，甚至使时间倒流，只要你可以编写能处理 backward 的 coroutine（能使用负数时间）。

```C#
void Start() {
    Timing.Instance.SetManualTimeframeTime = SetTime;
}
private float SetTime(float lastTime)
{
    return lastTime + (time.deltaTime * speedScrubberValue);
}
```

另一个使用 manual timeframe segment 的方法是使一个 coroutine 运行在一些 frames，而在另一些中不运行。这可用于策略游戏，其中 projectiles 可以从 board 上一个地方飞到另一个地方，但是它们应该只能在每次点击 next turn 时飞行一段固定时间。

## Layers and Tags

Layers 和 tags 都是用来确定一个特定 coroutine 实例的方法。它们的实际区别只是 tag 是一个字符串，layer 是一个整数而已。可以指定 layer 或 tag，或者两个都指定。一旦指定，就可以 pause/resume/kill，或者 RunCoroutineSingleton。

在 Unity 中，每个 GameObject 被赋予一个唯一的数字，可以通过 gameObject.GetInstanceID() 获得。每次游戏运行，InstanceID 都是不同的，但是一次运行中，InstanceID 保持不变，并且与其他 GameObject 不同，是唯一的。

Timing.KillCoroutines(enemy.gameObject.GetInstanceID());

如果创建 Coroutine 时传递一个 GameObject，MEC 自动调用 GetInstanceID，并将 Coroutine 放在那个 layer 中。

Unity Coroutine 在 disable GameObject 时，所有关联的 coroutines 都被 cancel。但有时想要在 gameobject disable 时暂停 coroutine，reenable 时恢复 coroutine。为此有一个扩展方法 PauseWith。但是如果想要一些更复杂的逻辑，可以很容易在 MEC 中设置：

```C#
void Start ()
{
    Timing.RunCoroutine(_MoveUpAndDown(), gameObject);
}
void OnEnable()
{
    Timing.ResumeCoroutines(gameObject);
}
void OnDisable()
{
    Timing.PauseCoroutines(gameObject);
}
// instead of the above you could use the PauseWith extension:
// Timing.RunCoroutine(_MoveUpAndDown().PauseWith(gameObject));

```

## RunCoroutineSingleton

有时想要运行一个 coroutine，但是不想运行那个 coroutine 的多个副本。为此可以使用 RunCoroutineSingleton，并指定 layer/tag 的唯一组合（只有 layer，只有 tag，或者 layer 和 tag 的组合）。

Tags 会导致一个内存分配，因此如果想要尽可能高效，可以使用一个 handle 来定义 singleton。

```C#
CoroutineHandle handle;

//...

handle = Timing.RunCoroutineSingleton(_MoveThatThing(), handle, SingletonBehavior.Overwrite);
```

第三个参数是一个 enum，它决定发现冲突时如何处理：

- Abort：如果已经有一个匹配参数的 coroutine，不会运行新的 coroutine，旧的 coroutine 继续运行
- AbortAndUnpause：和 Abort 类似，但是如果当前的 coroutine 是暂停的，还会恢复它
- Override：终止任何匹配的 coroutines，然后运行新的 coroutine
- Wait 会自动暂停新的 coroutine，直到匹配的 coroutine 完成再运行它

可以用 Wait 实现的一个功能时设置一些列 coroutines 一个接一个运行，通过给它们以相同的 tag，并设置它们 Wait。每个 coroutine 只会等待它创建时和 tag 匹配的 coroutines。

## Pause and Resume

可以暂停具有特定 tag 或 layer 的所有 coroutines，之后再恢复它们。

Timing.PauseCoroutines("tag0");

Timing.ResumeCoroutines("tag0");

## Controlling Coroutines by Handle

RunCoroutine() 返回一个 CoroutineHandle。这个 object 可以用来使另一个 coroutine 等待另一个，通过 yield return Timing.WaitUntilDone(handle)。

Handle 还可以用来设置 layer 和 tag。

```C#
CoroutineHandle handle = Timing.RunCoroutine(_Foo());
string oldTag = handle.Tag;
handle.Tag = "newTag";

if (handle.Layer == null) {
    handle.Layer = gameObject.GetInstanceID();
}
```

Layer 是一个 nullable int(int?)，因此它需要在 code 中转换为一个正常的 int，并且在查询 tags 或 layers 时应该检查 value 是否是 null（null value 意味着没有 tag 或 layer 赋值）。

还可以通过 handle 获取或改变 coroutine 运行在的 timing segment。

handle.Segment = Segment.SlowUpdate;

### IsRunning, IsPaused, IsValid

IsRunning 在 coroutine 终止之前返回 true，之后返回 false。Paused 和 locked coroutines 被认为是 running 的。

如果 Coroutine 被暂停或 locked，IsPaused 返回 true。

一旦 coroutine handle 指向一个有效的 coroutine（不管 corotuine 当前是否运行），IsValid 返回 true。


### Linking coroutine handles

Handles 可以 link 到另一个 handle，使用 LinkCoroutine。这意味着 master coroutine 在结束时（通过 Kill 命令或者仅仅是运行到 function 结束）会发送一个 kill 命令到 slave coroutine。它还会复制任何 apuse 或 resume 命令（同时暂停或恢复）。

linked coroutines 随着 master 一起 pause，resume，kill。

### Getting the current coroutine handle

在 coroutine 内部可以用 Timing.CurrentCoroutine 得到 coroutine handle，在函数内部设置 link，改变 tags 等等。

## Extension Methods

- CancelWith：使用一个 GameObject 或一个 Func<bool>

  如果传递一个 GameObject，coroutine 会自动随着 GameObject disable 或 destroy 而终止。对于改变 gameobject 的 coroutine 应该设置 CancelWith。CancelWith 会保证 coroutine 干净地退出而不抛出任何异常。

  如果想要安全地修改 2 个甚至 3 个 gameobjects，有重载的函数可以一次传递 2 或 3 个 gameobjects。如果想要安全地修改更多的 gameobjects，可以链式调用 CancelWith。这些 gameobjects 应该是 and 关系，只要有一个 gameobject 变得 disable 或 destory，coroutine 就终止。

  如果传递一个 Func<bool>，coroutine 会在 function 返回 false 时终止。

- PauseWith：就像 CancelWith，但是当 gameobject disable 时，coroutine 会暂停，reenable 后 coroutine 恢复

- KillWith：这会观察传递近的 coroutine handle，一旦 coroutine 结束，coroutine 也会结束。这和创建 link 的 coroutine 类似。

- Append and Prepend

  有两个函数可以用来将两个甚至更多的 coroutines 串联起来。

  Timing.RunCoroutine(_TurnRight().Append(_TurnLeft())); // 先向右转，然后向左转。

  Append 还可以 append 一个 delegate 到 coroutine 的结束。例如在 coroutine 结束时销毁 gameobject。

  Timing.RunCoroutine(_MoveToFinalPosition(obj1).Append(delegate { Destroy(obj1); }));

### RerouteExceptions

Timing.RunCoroutine(_HandleNosePick().RerouteExceptions(ex => { Debug.Log("Unimportant nose picking exception " + ex; });

## Fluid Commands

除了 _CoroutineFunc().RunCoroutine()，WaitUntilDone 也可以这样写：

yield return _CoroutineFuncToWaitFor().WaitUntilDone();


