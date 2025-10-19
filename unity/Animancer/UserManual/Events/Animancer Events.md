# Animancer Events

Animancer 包含一个自定义的事件系统，它与 Unity Animation Events 有很多不同之处。

Events 可以在 Inspector 中使用 Transitions 配置，也可以在 Code 中配置。

注意普通 events 和 End Events 有一些不同。

## Events in Transitions

Serializable Transitions 还允许你在 Inspector 中配置 Animancer Events。

In addition to their other details, the serializable Transitions also allow you to configure Animancer Events in the Inspector:

![animancer-event-inspector](../../../Image/animancer-event-inspector.gif)

- Transition Preview Window 可以用于观察当事件发生时 animated character 是怎样的
- 一个 transition 定义它如何 fade in，但不是它如何 fade out（因为这被下一个 state 的 transition 确定），因此 Inspector timeline 只是简单地使用一个默认值显示 fade out 的 duration（只用于显示，实际被下一个 transition 确定）。如果 end time 小于 animation length，它在 animation end 显示 fade out ending。如果 end time 大于 animation length，它显示一个默认的 0.25 second fade。
- Event Time Fields 总是作为 normalized time 被序列化，不管你使用哪个字段输入这个值
- 每个使用一个 Transition 来播放一个特定 animation 的脚本将会对这个 animation 有它自己的事件序列，但是你还可以使用 Transition Assets，使得很多东西都可以引用相同的 asset，因此共享相同的 events（尽管使用 Shared Event Sequences 有一些潜在的问题）。

### Controls

- 你可以一次选择并编辑一个event，或者你可以点击 timeline 旁边的 foldout arrow 来同时显示所有的 events。
- 双击 timeline 在那个时刻添加一个 event
- 选择一个 event 后：
  - Left 和 Right 箭头向旁边推动 event time 一个 pixel
  - 按住 Shift，一次移动 10 pixels
  - 事件时间值被舍入以节省显示空间，0.123 变成 0.12，0.999 变成 1

## Events in Code

Animancer Events 还可以在 code 中配置：

```C#
// MeleeAttack.cs:

[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

public void Attack()
{
    // 在 Transition 的 Inspector 中配置事件只是 Transition code 中自动执行这些事件注册

    // Play clears 清除所有 events（查看 Auto Clear 细节）
    var state = _Animancer.Play(_Animation);

    // 当 animation 通过长度的 40% 时，调用 OnHitStart 来激活 hit box
    state.Events.Add(0.4f, OnHitStart);

    // 当 animation 通过长度的 60% 时，调用 OnHitEnd 来激活 hit box
    state.Events.Add(0.6f, OnHitEnd);

    // 当动画完成时，返回 Idle
    state.Events.OnEnd = EnterIdleState;
}

```

可以使用 Lambda 表达式和匿名方法来定义你想要运行的 event 的 code，而不需要创建另一个单独的方法。

```C#
void PlayAnimation(AnimancerComponent animancer, AnimationClip clip)
{
    var state = animancer.Play(clip);

    // 所有下面的选项都是功能等价的

    // Lambda expression:
    state.Events.OnEnd = () =>
    {
        Debug.Log(clip.name + " ended");
    };

    // One-line Lambda expression:
    state.Events.OnEnd = () => Debug.Log(clip.name + " ended");

    // Anonymous method:
    state.Events.OnEnd = delegate()
    {
        Debug.Log(clip.name + " ended");
    };
}
```

AnimancerEvent.CurrentEvent 和 AnimancerEvent.CurrentState 允许你访问当前被触发的 event，和触发它的 state（动画）：

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

private void Awake()
{
    var state = _Animancer.Play(_Animation);
    state.Events.OnEnd = OnEnd;
}

public void OnEnd()
{
    Debug.Log(AnimancerEvent.CurrentState + " ended due to " + AnimancerEvent.CurrentEvent);
}
```

### Shared Event Sequences

每个播放一个特定 Transition 的 object 都会共享相同的事件序列，意味着一个 object 做出的修改将会影响其他的 objects。这通常在使用 Transition Assets 在多个 objects 之间共享相同的 transtion 当时仍然需要为每个 object 指定特定的 events 时发生。

如果你添加同一个 event 到一个 sequence 多次，Animancer 将会使用打印一个 warning，你可以尝试一下 workarounds：

最简单的 workaround 是在开始时实例化一个 Transition Asset copy。

```C#
[SerializeField] private ClipTransition _Animation;

private void Awake()
{
    _Animation = Instantiate(_Animation);
    // 现在你可以根据需要修改这个 _Animation.Transition.Events
}
```

这为每个 object 赋予一个单独的 transition 拷贝，因此他们不再共享相同的事件序列，但是这浪费了一些额外的处理时间和内存，因为所有其他 transition 数据都被复制了。

一个更高效的解决方案是为每个 object 创建你自己的事件序列。

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private ClipTransition _Animation;

private AnimancerEvent.Sequence _Events;

private void Awake()
{
    // 通过复制 transition 中的事件序列初始化你的 events
    _Events = new AnimancerEvent.Sequence(_Animation.Transition.Events);
    // 现在你可以根据需要修改 _Events
}

private void PlayAnimation()
{
    // 然后当你i播放它时，你只需要将 transtion events 替换成自己的
    var state = _Animancer.Play(_Animation);
    state.Events = _Events;
}
```

## Hybrid Events

在 Transitions 中设置 Events 通常是根据动画配置 timing 的最好方式，但是在 Code 中设置 Events 对于创建可靠脚本以及避免 bugs 更佳。幸运的是，你可以通过使用一个 Transition 来配置 Time，但是简单地将它的 Callback 保留为空白并在 Code 设置 Callback 来同时拥有二者的好处。

射仪一个 hybrid event 最可靠的方式通常是在 Inspector 中为它设置一个名字，使得你可以在 code 中指定它。

![animancer-hybrid-hit-event](../../../Image/animancer-hybrid-hit-event.png)

```C#
[SerializeField] private ClipState.Transition _GolfSwing;

private void Awake()
{
    // 设置名为 Hit 的 event 在触发时调用 HitBall 方法
    _GolfSwing.Events.SetCallback("Hit", HitBall);
}

private void HitBall() { ... }
```

没有名字，你还可以通过 index 访问 event：

```C#
_GolfSwing.Events.SetCallback(0, HitBall);
```

## Event Names

EventNamesAttribute 允许你提供一个指定集合的名字，event 只能拥有其中的名字，将通常的 text field 替换为 dropdown menu，以避免需要在 script 和 Inspector 输入相同的 event name。

Without Attribute

![animancer-hybrid-hit-event](../../../Image/animancer-hybrid-hit-event.png)

With Attribute

![animancer-hybrid-hit-event-named](../../../Image/animancer-hybrid-hit-event-named.gif)

注意使用 dropdown menu 选择的 value 仍然被存储为 strings。在脚本中修改名字不会自动更新任何之前在 Inspector 设置的 values。

## Auto Clear

调用 AnimancerComponent.Play 或 Stop 自动清除所有 states 的 events，以确保你不需要担心其他脚本之前可能使用相同的动画。每个播放一个 animation 的脚本负责管理期望会发生什么，而不关心其他脚本的期望。

这通常意味着在任何时间每个 object 上只有一个 state 实际具有 events，因此 AnimancerEvent.Sequences 在一个 Object Pool 被回收：

- 访问 AnimancerState.Events 属性将会从 pool 中得到一个 event sequence，如果它还没有一个的话
- 你可以将自己的 AnimancerEvent.Sequence 赋予那个属性，当 events 被清理时它将会从 state 移除（但是既然是你生成的 sequence，它将不会被清除或添加到 pool 中）
- Transitions 每一个有自己的 sequence（事件序列），当它们被播放时赋予到属性上

事件序列也是一个单独的对象（数据）

例如，如果一个 character 有一个 Attack 动画，它想要在完成时返回到 Idle，但是 character 在 Attack 中间被 enemy hit 了，角色现在会想要播放 Flinch 动画并在之后返回 Idle。在那一刻，我们不在关心 Attack animation 的结束。如果你想要再次 attack，我们只需要播放这个动画，重新注册 callback。但是如果 character 有一个特殊技能，让它们执行一个 attack combo，其恰好包含相同的 Attack animation，跟着一些其他动画在 sequence 中，这样的话就不想 animation 仍然具有 End Event 返回 Idle。

就是说，为每个被允许彼此中断的 animations/actions 强制规则通常是非常重要的，因此它在 Interrupt Management example 中被展示。

## Garbage

Animancer Events 使用 Delegates 是一个非常方便的方式来确定每个 event 实际上做什么，然而它们也有在不再使用时需要被 GC 的缺陷，而这通常是非常常见的，因为无论何时一个新的 animation 被播放，events 是 Automatically Cleared 的。

GC 可以通过 caching 你的变量来避免，这意味着你简单地创建你的 delegates 一次（通常在 startup 时）然后每次重用它们：

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

private System.Action _OnAnimationEnd;

void Awake()
{
    _OnAnimationEnd = () => Debug.Log("Animation ended");
}

void PlayAnimation()
{
    _Animancer.Play(_Animation).Events.OnEnd = _OnAnimationEnd;
}
```

Transitions 有它们自己的 events，它们不会被 cleared，并当动画播放时自动赋值到动画上（这说明事件总是需要在每次播放动画时添加的，即事件序列对象，它和动画是分离的，只是 Transitions 可以自动完整这个过程，如果使用 code 则需要每次播放动画时手动设置，这也是为什么在 Transitions Inspector 上设置 event）。因此添加你的 events 给 Transition 是另一种 caching 方法，这通常比将 delegate 存储到一个单独的字段更加方便。

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private ClipState.Transition _Animation;

void Awake()
{
    _Animation.Events.OnEnd = () => Debug.Log("Animation ended");
}

void PlayAnimation()
{
    _Animancer.Play(_Animation);
}
```

You can also make your own AnimancerEvent.Sequence like so:

你还可以制作自己的 AnimancerEvent.Sequence 像这样：

```C#
// MeleeAttack.cs:

[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Animation;

private AnimancerEvent.Sequence _Events;

private void Awake()
{
    // 指定 capacity 是可选的，它在必要时仍会扩展
    // 但是如果 elements 的数量是已知的，指定它会更高效
    _Events = new AnimancerEvent.Sequence(2);
    _Animation.Events.Add(0.4f, OnHitStart);
    _Animation.Events.Add(0.6f, OnHitEnd);

    // End Event 不包含在 event sequence 中，这就是 end event 和普通 event 的区别，end event 需要单独指定
    _Animation.Events.OnEnd = EnterIdleState;
}

public void Attack()
{
    var state = _Animation.Play(_Animation);
    state.Events = _Events;
}
```

你的 event sequence 将会在另一个动画被播放时从 state 上移除，但是它不会被清理，因此你只需要简单地在下一次播放时重新将它赋值。

## Looping

根据 animation 是否是 loop，Events 行为有所不同：

- 在一个 Non-looping 动画中，它们将会在动画经过指定时间的那帧被触发一次
- 在一个 Looping 动画中，它们将会在每个 loop 中经过指定时间的那帧触发一次
  - 如果动画播放地足够快到在一个 frame 执行了多个 loops，event 将会触发在那帧被触发正确的次数。如果你想要确保你的 callback 在每帧只被触发一次，你可以存储 AnimancerPlayable.FrameID 并且每次方法被调用时检查它是否改变了
  - Looping Events 必须位于 0 <= normalizedTime < 1 之间才能是函数正确工作。范围之外的 Events 将会在下一个 update 中导致一个 ArgumentOutOfRangeException
  - AnimationEvent.AlmostOne 是一个常量，包含小于1的最大可能的 float，如果你想要设置一个 event 在 loop 的最右端 end，使用这个常量。

## Other Details

事件系统提供了其他一些值得注意的细节：

- Events 是使用 AnimancerEvent.Invoke 方法被触发的，它设置 static AnimancerEvent.CurrentEvent 和 AnimancerEvent.CurrentState，允许任何东西可以访问触发它的 state 和 event 的细节。
- 改变 AnimancerState.time 阻止那个 state 在那一帧中触发更多的事件
- AnimancerState.Events sequence（List）不能被它自己的 events 修改（不能再 event handle 中修改 events，就像不能再 List 循环中修改 List）
- Animancer Events 也工作于 Mixers。Blend Trees 会触发它们包含的所有 AnimationClips 上正常的 Animation Events，但是这允许 events 被放置在 MixerState 自身上使得它们根据 mixed states 的 weighted average normalized time 被触发
- 它们在技术上还可工作于 Controller States，尽管它们被绑定在整个 ControllerState，并且不检查 Animator Controller 内部真正在做什么
- 如果你想要运行自己的 code 作为 animation update 的一部分，你可以实现 IUpdatable

## UltEvents

默认地，事件系统使用 UnityEvents 来定义 event callbacks。然而，它可以被修改以使用任何其他类似的 events 类型。特别地，UltEvents 比 UnityEvents 有一些显著的优势，因此如果你想使用它们，你可以像下面这样做：

- Import Animancer 和 UltEvents
- 选择 Assets/Plugins/Animancer/Animancer.asmdef，并且添加一个对 UltEvents Assembly Definition 的 Reference
- 进入就 Player Settings，添加 ANIMANCER_ULT_EVENTS 作为 Scripting Define Symbol。或者你可以简单地编辑 AnimancerEvent.Sequence.Serializable.cs 脚本来改变 event type

祝你 UnityEvents 和 UltEvents 的序列化数据结构是完全不同的，因此在它们之间切换将会导致现有的 events 丢失。

![reference-ultevents](../../../Image/reference-ultevents.gif)

![animancer-ultevents](../../../Image/animancer-ultevents.gif)
