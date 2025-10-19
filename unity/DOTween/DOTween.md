# DOTween

## 术语

- Tweener：一个 tween，控制和动画一个 value
- Sequence：一个特殊的 tween，相比控制一个 value，它以 group 的形式控制、动画其他 tweens
- Tween：通用指代一个 Tweener 或者 一个 Sequence
- Nested tween：包含在一个 sequence 的 tween（tweener 或者 sequence）

Tween 是一个通用术语，指代 Tweener 或 Sequence，Tweener 是 Tween + er 表示实现 Tween 的东西。

### 前缀

前缀对于使用智能提示非常重要

- DO：所有 tween shortcuts 的前缀。Shortcuts（可以直接在 object 上调用）

  ```C#
  transform.DOMoveX(100, 1);
  transform.DORestart();
  DOTween.Play();
  ```
  
- Set：所有 setting 的前缀，可以链式添加到一个 tween 上

  ```C#
  myTween.SetLoops(4, LoopType.Yoyo).SetSpeedBased();
  ```

- On：所有可以链式设置到 tween 的回调

  ```C#
  myTween.OnStart(myStartFunction).OnComplete(myCompleteFunction);
  ```

## DOTween.Init

你首次创建一个 tween 时，DOTween 会自动初始化它自己，使用各种默认设置。

如果你想自己使用特定的值初始化，在创建任何 tween 之前调用 Init 一次。你可以在任何时候使用 DOTween global setting 修改所有设置

可选地，你可以在 Init 方法之后连接 SetCapacity，这允许你设置 Tweeners/Sequences 初始容量（pool）

## 创建一个 Tweener

Tweener 是 DOTween 的工作蚂蚁（单位）。它们控制一个属性并向着一个给定的 value 动画它。

DOTween 可以 tween float, double, int, uint, long, ulong, Vector2/3/4, Quaternion, Rect, RectOffset, Color, string。

你还可以创建自定义 DOTween plugins 来 tween 自定义的类型（class）。

### 通用方式

最灵活的 tweening 方式，允许 tween 任何值，无论是 public 还是 private，static 还是 dynamic。ShortCuts 在背后使用通用方式实现。

就像 shortcuts，通用方式也具有 FROM 的版本。只需要 chain 一个 From 到一个 Tweener 就可以使 tween 称为一个 FROM tween 而不是 TO tween。

static DOTween.TO(getter, setter, to, float duration)

### 快捷方式

DOTween 包含许多 Unity Objects 的 shortcuts，例如 Transform，Rigidbody，和 Material。可以在这些 objects 上直接开始一个 tween （自动将 object 作为 tween target）。

每个 Shortcuts 还有一个 FROM 版本。当将 tweener 变成 FROM 版本，target 会立即跳到 FROM 的 value，然后动画到当前 value，立即指的是 FROM 被调用的时刻，不是 tweener 开始的时刻。

- AudioMixer
- AudioSource
- Camera
- Light
- LineRenderer
- Material
  - Blendable tweens
- Rigidbody
  - Move
  - Rotate
  - Path（没有 From）Bezier
  - Spiral（没有 From）
- Rigidbody 2D
  - Move
  - Rotate
  - Path（没有 From）
- SpriteRenderer
- TrailRenderer
- Transform
  - Move
  - Rotate
  - Scale
  - Punch（没有 From）
  - Shake（没有 From）
  - Path（没有From）
  - Blendable Tweens
    - DOBlendableMoveBy
    - DOBlendableLocalMoveBy
    - DOBlendableRotateBy
    - DOBlendableLocalRotateBy
    - DOBlendableLocalScaleBy
  - Sprial（没有 From）
- Tween：tween 其他 tweens 的属性
  - DOTimeScale：动画一个 tween 的 timeScale 到给定的 value
- CanvasGroup
- Graphic
- Image
- LayoutElement
- Outline
- RectTransform
- ScrollRect
- Slider
- Text：已打字机方式将文本动画出来
- TextMeshPro

DOBlendableXXX：允许其他 tweens 一起动画这个 target，而不是彼此冲突地设置属性。既然 DOTween 提供了一个这样的 tween，说明是可以同时存在多个 tweener 控制一个属性的。因此不会在创建一个控制 target 指定属性的 tweener 时自动移除之前操作同一个target同一个属性的

DOPath：提供一组 waypoint，pathType = Linear/CatmullRom/CubicBezier，提供 duration，resolution（路径分辨率）

### 附加通用方法

以特定方式动画一个 value 的通用方法。它们也具有 From 版本。

- static DOTween.Punch(getter, setter, Vector3 direction, float duration, int vibrato, float elasticity)

- static DOTween.Shake(getter, setter, float duration, float/Vector3 strength, int vibrato, float randomness, bool ignoreZAxis)

- static DOTween.ToAlpha(DOGetter<Color> getter, DOGetter<Color> setter, float endValue, float duration)
  
  getter/setter 返回和设置一个 Color 值，这个方法操作Color.a属性

- static DOTween.ToArray(DOGetter<Vector3> getter, DOSetter<Vector3> setter, Vector3[] endValues, float[] durations)

- static DOTween.ToAxis(DOGetter<Vector3> getter, DOSetter<Vector3> setter, float endValues, AxisConstraint axisConstraint = AxisConstraint.X)

## 创建 Sequence

Sequences 就像 Tweeners，但并不是动画一个属性或 value，而是动画其他 Tweeners 或 Sequences （统称 Tweens）作为一个 group。

Sequences 可以被包含在其他 Sequences 中，没有嵌套深度限制。

Sequenced tweens 不需要一个接着一个。可以使用 Insert 方法创建重叠 tweens。

一个 Tween (Sequence 或 Tweener) 只能被嵌套在一个 Sequence 中，意味着你不能再多个 Sequences 中重用一个 tween。此外，main Sequence 控制它所有的嵌套元素，你不能单独地控制其中嵌套的 tweens。

不要使用空 Sequences。

1. 创建一个新的 Sequence 来使用，并保存它的引用

    static DOTween.Sequence()

2. 向 Sequence 添加 tweens，intervals，callbacks

   所有这些方法都必须在 Sequence starts（通常是你创建它的下一帧，除非它被暂停）前被应用，否则它们不会有效果

   任何嵌套的 Tweener/Sequence 需要在添加到 Sequence 之前被完全创建，因为之后它们将被 lock

   由此可以看出 Sequence 对内部的 tweens 进行的特殊处理，一旦开始，Sequence 就是固定的了，不能再进行任何修改了

   Delays 和 Loops（当不是无限循环时）即使在嵌套的 tweens 中也是工作的

   - Apppend(Tween tween)
   - AppendCallback(TweenCallback callback)
   - AppendInterval(float interval)
   - Insert(float atPosition, Tween tween)
   - InsertCallback(float atPosition, TweenCallback callback)
   - Join(Tween tween)：在最近的 tween 或 callback 相同的时间点插入给定的 tween
   - Prepend(Tween tween)
   - PrependCallback(TweenCallback callback)
   - PrependInterval(float interval)

## 设置，选项，回调

DOTween 使用链式方法设置一个 tween。或者你可以修改全局默认选项，它将被应用到所有新创建的tweens。

### Global settings

通用设置

DOTween 类的静态变量

- bool timeScale

  应用到所有 tweens 的全局 timeScale

- bool userSafeMode

  如果为 true，tweens 会稍微慢一些但是更安全，允许 DOTween 自动关心当 tween 运行时 targets 被销毁这样的事情。

  如果为 false，意味着你必须自己注意，在 target 被销毁之前 kill 掉 tween

  on iOS safeMode works only if stripping level is set to "Strip Assemblies" or Script Call Optimization is set to "Slow and Safe"

应用到所有新创建的 tweens 的默认设置

- bool defaultAutoKill
- bool defaultAutoPlay
- float defaultEaseOvershootOrAmplitude(1.70158f)
- float defaultEasePeroid(0)
- float defaultEaseType(Ease.OutQuad)
- LoopType defaultLoopType(LoopType.Restart)
- bool defaultRecyclable(false)
- bool defaultTimeScaleIndependent(false)
- UpdateType defaultUpdateType(UpdateType.Normal)

### Tweener 和 Sequence settings

Tweener 或 Sequence 上的实例属性

- float timeScale：tween 的内部 timeScale，控制这个 tween 的播放速度

  这个属性可以被其他 tween 控制和动画，来实现平滑的慢动作效果

- SetAs(Tween tween / TweenParams tweenParams)

  将当前 tween 的各种属性设置为给定 tween 或者 tweenParams 的对应属性

- SetAutoKill(bool autoKillOnCompletion = true)

  tween 一旦完成就被 kill，否则它将一直保留在内存中，而你可以重用它（重新播放）

- SetEase(Ease easeType / AnimationCurve animCurve / EaseFunction customEase)

  如果设置给 Sequence，ease 将被应用到整个 Sequence，就像他是一个单独的 animated timeline。Sequence 独立于全局默认的 ease setting，总是默认具有 Ease.Linear ease

- SetId(object id)

  为 tween 指定一个 id，可以是 int，string，或其他 object

- SetLink(GameObject target, LinkBehaviour linkBehaviour = LinkBehavior.KillOnDestroy)

  Link 这个 tween 到一个 GameObject，并设置一个基于 gameobject active 状态的行为。KillOnDestroy 会导致 tween 在 GameObject 被销毁时 kill。如果 tween 被添加到 Sequence，则没有效果。

  target 和 SetTarget 设置的 target 没有关系

  KillOnDestroy 总是被求值，即使你选择了其他行为，也是在 KillOnDestroy 基础上添加新的行为

- SetLoops(int loops, LoopType loopType = LoopType.Restart)
  
  设置循环选项(Restart, Yoyo, Incremental)

  如果 tween 已经开始了，则没有作用。如果 tween 位于一个 Sequence 中，无限循环不被应用

  loops = -1 使循环变成无限循环

  Restart：loop 结束时将从头开始

  Yoyo：loop 结束时从后向前播放，然后再从前向后，依次类推

  Incremental：每次一个 loop 结束时，它的 endValue 和 startValue 的差会添加到 endValue，即上个 loop 的 endValue 成为下一个 loop 的 startValue，上个 loop 的 （endValue - startValue）+ endValue 成为下一个 loop 的 endValue。这样就创建了一个每个 loop 递增的 tweens。只用于 Tweeners。

- SetRecyclable(bool recyclable)

  设置 tween 的回收行为。

  如果为true，tween 在 kill 之后将被回收，否则将被销毁

- SetRelative(bool isRelative = true)

  设置 tween 为相对的，即 endValue 不作为绝对值，而是相对于 startValue 的差值，真正的 endValue = startValue + endValue。如果 tween 是 Sequence，设置所有嵌套的 tweens 为 relative。

  对于 From tween 没有效果。因为这种情况下，你在设置 From setting chain 时直接选择 tween 是不是相对的。

  对于已经开始的 tween 没有效果

- SetTarget(object target)

  target 可以被 DOTween 静态方法用作一个 filter

  当使用 generic tween method 时很有用，shortcuts 自动设置 target

- SetUpdate(UpdateType updateType, bool isIndependentUpdate = false)

  设置 tween 的 update 类型，是否忽略 Unity 的 timeScale。

  Normal，Late，Fixed，Manual（通过手动调用 DOTween.ManualUpdate）

  isIndependentUpdate：忽略 Unity Time.timeScale。

链式回调

TweenCallback callback = () => {};

- OnComplete(TweenCallback callback)

  tween 最终结束时，包含 loops

- OnKill

- OnPlay
  
  在任何最终delay之后。并在每次从 paused state 恢复之后也会调用

- OnPause

  tween 从 paused 变为 play。如果 tween 设置为 autoKill = False，在 tween 到达完成时也会调用
  
- OnRewind

  当 tween rewinded，或者调用 Rewind，或者反向播放到达 start positoin

- OnStart

  tween 第一次进入 play state，在任何最终 delay 之后。OnStart 只会调用一次，而 OnPlay 在每次从 paused 恢复之后还会调用。类似 MonoBehavior 的 Start 和 OnEnable/OnDisable。

- OnStepCompelete

  每次 tween 完成一个 loop cycle（意味着，如果 loops = 3，OnStepComplate 将会被调用 3 次，相比之下，OnComplete 只在所有 loops 之后最终调用一次

- OnUpdate

  每次 tween updates 时调用一次

- OnWaypointChange(TweenCallback<int> callback)

  当一个 path tween 当前 waypoint 变化时。传递最新的 waypoint 索引

附加在嵌套 tweens 上的 callback 也会以正确的顺序工作。

### Tweener 特定的设置和选项

这些选项特定于 Tweener，对 Sequence 没有效果。

除了 SetEase（只是一个基于当前时间线的公式），对正在运行的 tween 链式添加这些设置没有效果。

- From(bool isRelative = false)

  将 tween 从 to 改为 from，并将 target 立即 设置到 给定的 fromValue，然后动画的之前的值。必须在其他 Tweener setting 之前设置，出来了上面介绍的 Tween 相关的设置。

  isRelative 设置 tween 为 relative，真正的 fromValue = currentValue = endValue。

- From(T fromValue, bool setImmediately = true, bool isRelative = false)
  
  直接设置 tween 的 fromValue，而不依赖 target 开始时的 value。

  setImediately = false 不会立即将 target 设置到 fromValue，而是等到 tween 开始

- SetDelay(float delay)

  设置 tween 的开始 delay。如果应用到 Sequence，不会真正添加一个 delay，而是简单在 Sequence 开始处添加一个 interval，和 PrependInterval 相同。

- SetDelay(float delay, bool asPrependedIntervalIfSequence)

  asPrependedIntervalIfSequence 只用于 Sequence，如果为 false，这个 delay 是一次发生的，否则作为一个 Sequence 的 interval，将会在每个 loop cycle 的开始重复

- SetSpeedBased(bool isSpeedBased = true)

  如果 isSpeedBased = true，设置 tween 为基于速度的（duration 表示 每秒运动的 units/degrees 的数量）。如果你想速度是常量，还要设置 ease = Linear

  如果 tween 以及开始，或者是一个 Sequence，或者是 Sequence 中一个嵌套的 tween，没有效果

#### SetOptions

一些特定类型的 Tweener 具有特殊的 options。这些是自动的，如果一个 Tweener 具有一个特殊选项，你可以看见特殊 SetOptions 方法出现在 Tweener 上，否则不会。

这些选项通常只用于使用 generic 方法创建 tween 时，对于 shortcuts，这些选项已经包含在它们的 main creation 方法中了。

所有其他设置可以以任何顺序连接到一起，但是 SetOptions 必须在 tween creation 方法之后立即调用（在任何其他 setting 方法之前），否则它将没有效果。

- Color: SetOptions(bool alphaOnly)
- float: SetOptions(bool snapping)

  平滑地 snap 到 int

- Quaternion: SetOptions(bool useShorttest360Route)
- Rect: SetOptions(bool snapping)
- String: SetOptions(bool richTextEnabled, ScrambleMode scrambleMode = ScrambleMode.None, string scrambleChars = null)
- Vector2/3/4: SetOptions(AxisConstraint constraint, bool snapping)
- Vector3Array: SetOptions(bool snapping)
- Path: SetOptions(bool closePath, AxisConstraint lockPosition = AxisConstraint.None, AxisConstraint lockRotation = AxisConstraint.None)
- Path: SetLookAt(Vector3 lookAtPosition/lookAtTarget/lookAhead, Vector3 forwardDirection, Vector3 up, bool stableZRotation)

### Tween Params

Tween Params 用来存储可以应用到多个 tweens 的 settings。不是必要的，只用作一个额外的 utility class。

要使用它，创建一个新的 TweenParams 实例，或者调用一个现有 TweenParams 的 Clear() 方法，然后就像正常 tween chaining 一样添加 setting。要应用它们，在 tween 上调用 SetAs。

```C#
TweenParams tParams = new TweenParams().SetLoop(-1).SetEase(Ease.OutElastic);
transformA.DOMoveX(15, 1).SetAs(tParams);
transformB.DOMoveX(10, 1).SetAs(tParams);
transform.DOMoveX(45, 1).SetDelay(2).SetEase(Ease.OutQuad).OnComplete(MyCallback);
```

## 控制一个 tween

有3种方法操作一个 tween。它们都共享相同的方法名，除了 shortcut-enhanced 那些，后者具有一个附加的 DO prefix。

- 通过静态方法和过滤器

  DOTween 类包含很多静态方法，允许你控制 tweens。它们中的每个都带有一个 All version（例如 DOTween.KillAll），其应用到所有现有的 tweens，以及一个简单版本（DOTween.Kill(myTargetOrId)），其带有一个参数允许你通过一个 tween id 或 target 过滤操作（id 通过 SetId 手动设置，target 可以通过 SetTarget 手动设置，或者shortcut 方法自动设置）

  Static 方法还返回一个 int，其表示实际执行请求操作的所有 tweens 的数量

  ```C#
  DOTween.PauseAll();
  DOTween.Pause("badoom");
  DOTween.Pause(someTransform);
  ```

- 直接从 tween 上调用

  除了调用 DOTween 静态方法，还可以直接在 tween 上直接调用相同的方法

- 从一个 shortcut-enhanced 应用上调用

  和上面相同，但是你可以从 shortcut-enhanced object 上调用相同方法，这些方法带有 DO 前缀

### 控制方法

所有这些方法被上面 3 中方式共享，只是 shortcuts 带有 DO prefix

- CompeteAll/Complete(bool withCallbacks = false)

  将 tween send 到 end time position（对无限循环 tween 没有效果）

  withCallbacks 只用于 Sequence：如果为 true，内部 Sequence callbacks 将会被 调用，否则将被忽略

- FlipAll/Flip()

  反正一个 tween 的方向（forward 变 backward，或者反之）

- GotoAll/Goto(float to, bool andPlay = false)

  Send tween to the given position in time

  to：要到达的时间位置。如果高于 tween duration，则简单到达 tween end

  andPlay：tween 在 send 到给定时间位置之后将会 play，否则 paused

- KillAll/Kill(bool complete = true, params object[] idsOrTargetsToExclude)

  Kill tween。

  Tween 在完成时会自动 kill，除非调用 SetAutoKill(false) 阻止这种行为，但是你可以使用这个方法随时 kill 它

  complete = True，在 kill 之前立刻完成这个tween（设置 target 到 final end value）

  idsOrTargetsToExclude，只用于 KillAll，排除的 ids 或 targets

- PauseAll/Pause()

- PlayAll/Play()

- PlayBackwardsAll/PlayBackwards()

- PlayForwardAll/PlayForward()

- RestartAll/Restart(bool includeDelay = true, float changeDelayTo = -1)

- RewindAll/Rewind(bool includeDelay = true)

  Rewinds 并且 pauses 这个 tween

- SmoothRewindAll/SmoothRewind()

  Smoothly rewinds the tween （排除 delays）

  一个 ”smooth rewind“ 动画这个 tween 到它的 start position（而不是 jumping 到那个位置），跳过所有流逝的 loops（出列 LoopType.Incremental）同时保持动画流程

  如果在还在等待 delay 的 tween 上调用这个函数，它简单地设置 delay 为 0，并暂停 tween。

  一个被 smoothly rewinded 的 tween，将使它的 play direction 翻转

- TogglePauseAll/TogglePause()

  如果 tween paused，则 play，反之亦然

### 特殊控制方法

- ForceInit()

  强制 tween 立即初始化它的设置

  用于你想从一个 tween 获取数据，而这些数据直到 tween 被初始化时才有用的情形

- GotoWaypoint(int waypointIndex, bool andPlay = false)

  只用于 使用 Linear ease 创建的 paths tweens。

  Send 一个 path tween 到给定 waypoint index。

## 从 tweens 获得数据

### 静态 DOTween 方法

- static List<Tween> PausedTweens()
- static List<Tween> PlayingTweens()
- static List<Tween> TweensById(object id, bool playingOnly = false)
- static List<Tween> TweensByTarget(object target, bool playingOnly = false)
- static List<Tween> IsTweening(object idOrTarget, bool alsoCheckIfPlaying = false)
- static List<Tween> TotalPlayingTweens()

### 实例方法（Tween、Tweener、Sequence）

- float fullPosition

  获取和设置 tween 的 time position（包含 loops，排除 delays）

- int CompletedLoops()

  返回 tween 完成的 loops 的总数量

- float Delay()

  返回 tween 的最终 delay

- float Duration(bool includeLoops = true)

  返回 tween 的 duration（排除 delays，包含 loops 如果 includeLoops = true）

- float Elasped(bool includeLoops = true)

  返回 tween 当前流逝的时间（排除 delays，包含 loops 如果 includeLoops = true）

- float ElapsedDirectionalPercentage()

  返回 tween 的流逝时间的百分比（0~1），基于一个单个 loop，并且计算最终 backwards Yoyo loops 作为 1 到 0，而不是 0 到 1

- float ElaspedPercentage(bool includeLoops = true)

- bool IsActive()

  如果 tween 被 kill，返回 FALSE

- bool IsBackwards()

  如果 tween 是 reversed 并且被设置为 go backwards，返回 TRUE

- bool IsComplete()

  如果 tween 完成，返回 True。如果 tween 被 kill，返回 false

- bool IsInitialized()

- bool IsPlaying()

- int Loops()

- Vector3 PathGetPoint(float pathPercentage)
  
  基于给定 path 百分比返回一个 path 上的 point。如果 tween 不是 path tween，或者 tween 无效，或者 path 还没有初始化，返回 Vector3.zero。

  Path 在 tween 开始之后才初始化，或者 tween 是在 Path Editor 中创建的

  你可以调用 ForceInit 强制初始化一个 Path

  pathPercentage 0~1

- Vector3[] PathGetDrawPoints(int subdivisionXSegment = 10)

  获得一组 points，可以用于绘制 path。如果 tween 不是 path tween，tween 无效，或者还没有初始化，返回 NULL

- float PathLength()

  返回路径长度，否则返回-1

## WaitFor coroutines/Tasks

### Coroutines

Tweens 提供了一组有用的 YieldInstructions，你可以将其用在 Coroutines，允许你等待一些事情发生。所有这些方法有一个可选的 bool 参数 允许返回一个 CustomYieldInstruction

- WaitForCompletion()

  创建一个 yield instruction，等待 tween 被 kill 或者完成

- WaitForElapsedLoops(int elapsedLoops)

  创建一个 yield instruction，等待 tween 被 kill，或者经历指定数量的 loops

- WaitForKill()

  创建一个 yield instruction，等待 tween 被 kill

- WaitForPosition(float position)

  创建一个 yield instruction，等待 tween 被 kill，或者达到指定 time position（包含 loops，排除 delays）

- WaitForRewind()

  创建一个 yield instruction，等待 tween 被 kill，或者 rewinded

- WaitForStart()

  创建一个 yield instruction，等待 tween 被 kill，或 started（意味着 tween 被第一次进入 playing state，在任何最终 delay 之后）

### Tasks

这些方法返回一个 Task，用于 async operations，等待一些事情发生

- AsyncWaitForCompletion()
- AsyncWaitForElapsedLoops(int elapsedLoops)
- AsyncWaitForKill()
- AsyncWaitForPosition(float position)
- AsyncWaitForRewind()
- AsyncWaitForStart()


## 更多方法

### DOTween 静态方法

- Clear(bool destroy = false)

  Kill 所有 tweens，清空所有 pools，重置 max Tweeners/Sequences 容量到 default values

  这个方法只应给用于 debug purposes，或者当你计划在 project 中不再创建/运行任何 tweens，因为它完全反初始化 DOTween 和它内部的 插件

  destroy = true，还销毁 DOTween gameObject，并且重置它的初始化，default settings，和任何其他东西。因此之后你再使用它时需要重新初始化

- ClearCachedTweens

  清空所有缓存的 tween pools

- Validte()

  校验所有 active tweens 并且移除最终无效的哪些（通常是因为它们的 target 被 destroy）。这是一个稍微昂贵的操作，因此谨慎使用。而且在 safe mode 开启时，完全不需要使用它

- ManualUpdate(float deltaTime, float unscaledDeltaTime)

  更新所有 UpdateType.Manual 的 tweens

### 实例方法

- ChangeEndValue(float newEndValue, float duration = -1, bool snapStartValue = false)
  
  改变一个 Tweener 的 end value，并且 rewind 它（但不暂停）

  对于 Sequence 中的 Tweeners 没有效果

  对于接受单一 axis 的 shortcut（DOMoveX/Y/Z，DOScaleX/Y/Z 等），你还是可以传递一个完全的 Vector2/3/4 value，即使只有 axis 被使用

  snapStartValue = true，start value 将成为 target 当前 value，否则还是之前的值

- ChangeStartValue(newStartValue, float duration = -1)

- ChangeStartValue(newStartValue, newEndValue, float duration = -1)
  
## 编辑器方法

- static DOTweenEditorPreview.PrepareTweenForPreview(bool clearCallbacks = true, bool preventAutoKill = true, bool andPlay = true)

  为 editor preview 准备给定 tween，将 UpdateType 为 Manual 以及额外设置

  clearCallbacks = true previewing 时移除所有 callbacks

  preventAutoKill = true 防止 tween 在 previewing 完成时被自动 kill

  andPlay = true 立即开始播放 tween

- static DOTweenEditorPreview.Start(Action onPreviewUpdated = null)

  在 editor 中开始 tween 的 update loop。在 start 之前，必须将 tween 添加到 preview loop 中，通过 PrepareTweenForPreview

  onPreviewUpdate 在 Editor 中每次 update 调用的 callback

- static DOTweenEditorPreview.Stop()

  停止 preview update loop，并清除任何 callback

## Virtual 方法

virtual 方法不能放在 Sequence 内部。

- static Tweener DOVirtual.Float(float from, float to, float duration, TweenCallback<float> onVirtualUpdate)

  Tween 一个 虚拟 float

  你可以先生成的 tween 添加正常的 setting，但是不使用 SetUpdate 或者你可以覆盖 onVirtualUpdate 参数

- static float DOVirtual.EasedValue(float from, float to, float lifetimePercentage, Ease easeType / AnimationCurve animCurve)

  基于给定 ease 和 lifetime percentage（0~1）返回一个 value

  包含不同的重载方法，允许使用一个 AnimationCurve ease 或自定义 overshoot/period/amplitude

- static Tween DOVirtual.DelayedCall(float delay, TweenCallback, bool ignoreTimeScale = true)

  在给定时间之后调用 callback，返回一个 Tween，你可以存储它并进行 pause/kill 等操作

## 创建自定义 plugins
