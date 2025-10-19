End Events 和普通的 events 有所区别。

当开始一个动画之后，通常会想要等它结束以做一些事情。Animancer 提供了几种方式来完成这件事。最常用的方法就是 Events 和 Coroutines，但是你还可以手动检查 animation normalized time 是否到达 1 来确定动画是否完成了。

## Events

Animancer Event 系统允许你在动画的特定时刻允许一个脚本函数。每个 AnimancerEvent.Sequence 还有一个 endEvent，它和其他 events 不太一样，以用来更好地定义 animation end。

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

void PlayAnimation()
{
    var state = _Animancer.Play(_Animation);
    state.Events.OnEnd = OnAnimationEnd;
    state.Events.NormalizedEndTime = 0.75f;

    // Or set the time and callback at the same time:
    state.Events.endEvent = new AnimancerEvent(0.75f, OnAnimationEnd);
}

void OnAnimationEnd()
{
    var state = AnimancerEvent.CurrentState;
    Debug.Log(state + " Ended");
}
```

下面总结了常规 events 和 end events 之间的区别

| normal events | end events |
| --- | --- |
| 每个 state 可以有多个 events | 每个 state 只能有一个 end events |
| 每个 event 在经过指定时间只触发一次（或者对于 looping 动画每次经过触发一次 | End Events 在指定时间经过后的每一帧都触发。这确保了即使动画已经经过了定义的时间，它仍然会简单地在下一帧触发，而不是根本不触发，并将 character 卡在那个状态 |
| 每个 event 必须有一个有效的 time | 默认 End Event time 是 NaN，这导致它基于 play speed 自动确定运行时实际使用什么值，正的速度像前播放，并在 normalized time 1 处结束，负的速度反向播放，并在 normalized time 0 处结束 |
| | |

除了名字叫 End，End Events 本质上在动画结束时不做任何事情。你可以使用 callback 做任何事情。

你还可以使用 End Animation Events（MonoBehavior 组件）来触发注册的 OnEnd，但是这不够方便。

## Coroutines

在 coroutines 中，你可以 yield return 任何 AnimancerState 来等待它结束。特别是，它将等待直到 state 或者停止播放，或者经过它的 end time。

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

void Awake()
{
    StartCoroutine(CoroutinePlayAnimation());
}

IEnumerator CoroutinePlayAnimation()
{
    Debug.Log("Starting animation");

    var state = _Animancer.Play(_Animation);
    yield return state;

    Debug.Log("Animation ended");
}
```

你还可以 yield 一个整个 Layer 或者 AnimancerComponent，来等待所有的 states 完成。

注意 yield 一个 state 不会创建 Garbage，但 start 一个 coroutine 会。

## Manual

你可以保持对一个被任何 AnimancerComponent.Play 方法返回的 AnimancerState 的引用，并在每个 every update 检查它的 NormalizedTime。一旦 value 达到 1 动画就完成了。

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

private AnimancerState _State;

void Awake()
{
    _State = _Animancer.Play(_Animation);
}

void Update()
{
    if (_State.NormalizedTime >= 1)
        Debug.Log("Animation ended");
}
```

因为 states 被保留在一个内部的字典中，你还可以在需要的时候有效地获得它们：

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

void Awake()
{
    _Animancer.Play(_Animation);
}

void Update()
{
    // State 是运行时动画数据源，Playable Graph 的 Node，AnimationClip 是生成基本 State 的最简单方法
    var state = _Animancer.States[_Animation];
    if (state.NormalizedTime >= 1)
        Debug.Log("Animation ended");
}
```

注意如果一个 state 还没有为这个 animation clip 创建（因为它还没有被播放），然后 _Animancer.States\[_Animation] 将会抛出一个异常。因此你可能想要使用 _Animancer.States.TryGet(_Animation, out var state) 或 _Animancer.States.GetOrCreate(_Animation)。
