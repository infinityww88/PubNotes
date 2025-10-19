# States

当你播放一个 AnimationClip，Animancer 创建一个 ClipState 来管理它并保持对它的进度的追踪。ClipState 是最常用的 AnimancerState，但是有一些其他类型的 Controller States 和 Mixer States，它们在一个 state 中管理多个动画。

AnimancerComponent.Play 方法返回它播放的 state：

```C#
void PlayAnimation(AnimancerComponent animancer, AnimationClip clip)
{
    // Play the animation and control its state:
    var state = animancer.Play(clip);
    state.Time = ...
    state.NormalizedTime = ...
    state.Speed = ...
    state.OnEnd = ...
}
```

你还可以访问和创建 states 而不立即播放它们：

| Code | Description |
| --- | --- |
| var state = animancer.States.GetOrCreate(clip); | 访问一个 state 而不播放它（Play 方法内部使用它） |
| var state = animancer.States[clip]; | 如果存在，获得 state，否则为 null |
| var state = animancer.States.Create(key, clip); | 创建一个 新的 state，即使对那个 animation 已经存在一个 state。注意，你必须为每个 state 提供一个不同的 key |
| var state = new ClipState(animancer, clip); | 创建一个新的 state 但不给它一个 key。你可以使用它的 AnimancerState.Key 属性为它赋予一个 key |
| | |

Playable Graph 的用途是，同一个数据是有很多不同的并行子部分的输出根据一定的权重混合而成的，这种情况经常出现，因此 Unity 提供了 Playable 作为这种情形的解决方案。例如动画混合，一个 transform 的最终变换是由多个动画片段的数据混合而成的，已达到 CrossFade 的效果。还是音频系统中，最终的声音是有多个声源混合而成的。

Animancer 是：

- Mecanim 和 Animancer system 都构建在 Playable API graph 之上
- 有 3 种类型的 Playable Graph: Animation, Audio, Script
- Playable Graph 有向图

  它不必是一个连接的 graph，意味着它可能有一些断开的子图。

  Playable Graph 只有一个输出，graph 中的任何 node 都可以连接到 output。

  从 Output Node 回溯所有连接的 nodes，得到一个子连接有向图（output-bigraph），这个有向图产生这个 Playable graph 的最终输出。

  Graph 中的每个 node 产生数据，并依据权重 pipe 它们到下游的 node。

  Graph 中的每个 node 接收连接到它们的上游 nodes 的数据，使用权重 blend 每个 node 数据，然后扇出到下游。

  重复这个机制，直到数据到达 output node

- Mecanim 构建在 Playable Graph 之上，并强制使用 FSM，因此脚本不能直接操作 playable graph，而是必须通过 FSM 并做一些 hacking 来得到想要的效果。它就好像 Render Pipeline 的固定管线，应用程序不能自定义它的机制，只能通过固定管线上的一些开关来操控它

- Animancer 只是 Playable Graph 的一个高级 API（用于动画操作），因此它不强制使用任何机制，意味着脚本可以直接操作 playable graph。它就像是 Render Pipeline 中的可编程管线。
- 在 Animancer 中，你可以创建任何数量的 nodes（states）在 Playable Graph 中，并以任意的有向图结构连接它们。在基本用法中，Animancer.Play(clip) ，Animancer 只是创建了一个单一 node 在 graph 中，并连接它到 output node，并播放。下一次调用 Animancer.Play(clip1)，Animancer 断开之前的 clip node 到 output 的连接，将它留在 graph 中，然后连接 clip1 node 到 output 并播放。这就是为什么 Animancer 需要在内部字典中记录它创建的所有 states ，因此下一次它播放一个 clip 时，它不需要在 graph 中重新创建 state，因为这个 clip 的 node 以及在 graph 中存在了，它只是没有连接到 output node 并播放。

```C#
void PlayAnimation(AnimancerComponent animancer, AnimationClip clip)
{
    // Play the animation and control its state:
    var state = animancer.Play(clip);
    state.Time = ...
    state.NormalizedTime = ...
    state.Speed = ...
    state.OnEnd = ...
}
```

还可以自己创建和访问 states，而不立即播放它们：

```C#
// 访问一个 state 而不播放它（Play 方法内部使用这个方法
var state = animancer.States.GetOrCreate(clip);

// 如果 state 存在于 graph 中（以及 Animancer 内部的字典中），返回它
var state = animancer.States[clip];

// 创建一个新的 state，即使对这个 animation 已经存在一个 state（两个 state 使用同一个 clip 数据。你必须为每个 state 提供一个不同的 Key
var state = animancer.States.Create(key, clip);

// 创建一个新的 state，而不给它一个 key。你可以通过使用 AnimancerState.Key 属性为它赋予一个 key
var state = new ClipState(animancer, clip);

```

AnimancerState

- ClipState
  - Play
  - CrossFade
  - GetOrCreateState
  - GetState
  - CreateState
- ControllerState/MixerState: 在单个 state 中管理多个 animations（AnimationController）


## Keys

Animancer 在内部的 dictionary 保存它的状态

 - 每次 Animancer 播放一个 clip，它在内部创建并维护一个 AnimancerState
 - CreateState/GetOrCreate 可以预注册一个 states 到字典中
 - Play/CrossFade 内部使用 GetOrCreateState
 - 如果你播放同一个 animation，你得到同一个 state
 - 通过在 Inspector 将 clip 添加在 Animations Array 中，在 startup 时预注册 clip，或者在脚本中使用 GetOrCreateState(clip) 动态注册

默认使用 AnimationClip 作为 key，但是可以使用任何 object 作为 key (every variable in C# is an object)

NamedAnimancerComponent 覆盖了它的 GetKey 方法，使用 clip 的 name 作为 key。一旦预注册一个 clips，你可以在任何脚本中调用 Play("Animation Name") 而不需要直接应用一个 AnimationClip

很多 AnimancerComponent 方法使用 object 作为 key
- 当没有提供 key 参数时，AnimancerComponent 使用 clip 作为 key，因此你需要保存 clip 引用，以查找 AnimationState
- 当提供了 key 参数, AnimancerComponent 使用它作为 key

另一种设置 state key 的方法：

```C#
var state = new ClipState(animancer, clip);
state.Key = "Attack";
```

你甚至不需要在 dictionary 中注册一个 state。Animancer 所做的只是添加 node（state）到 playable graph，dictionary 只是保持脆它创建的所有 nodes 的追踪的方式。你可以告诉 Animancer 创建 node 当时不需要添加它到 dictionary，而是自己追踪它。为此，简单地创建一个新的 ClipState（或者任何你想要的 type）而不设置它的 AnimancerState.Key。此时，你必须自己保持对 state 的引用。

如果你有多个 states 播放相同的 clip（例如，你需要在多个 layers 上播放它，你需要使用不同的 keys 注册它们（或者不注册它们，只是创建 state）。每个 State（node）只是一个具有各种配置（Speed，Time，NormalizedTime 等）的 data source。CrossFadeNew 使用这个方法来 fade out 一个 clip，同时 fade in 另一个 clip state（创建两个独立的 State，但是引用同一个 clip，即使用相同的动画数据。因为它需要两个数据源来工作，即使两个数据源产生相同的数据序列，但是它们具有不同的播放指针 play head —— State.Time，因此两个数据源在同一时间产生不同的数据）
  
```C#
void PlayAnimation(AnimancerComponent animancer, AnimationClip clip)
{
    // Trying to play an animation before registering it does nothing.
    animancer.Play("Attack");

    // But if you create a state with a key first, then you only need that key to play it later on.
    animancer.States.Create("Attack", clip);
    animancer.Play("Attack");

    // Or you can create the state and set its key manually:
    var state = new ClipState(clip);
    state.Key = "Attack";
}
```

### Enum Keys

object 是一个 Reference Type，使用 Value Type 例如 enum 在这些方法中，隐式地创建一个 new object 来保存这个 value。这称为 Boxing，但是对 performance 有很大影响，尤其是因为 new object 在调用之后立即丢弃时，会导致 GC。不是说你不可以使用 enum，而是应该注意这些问题。

### Object keys

另一种方法是使用 objects 作为 keys，相对于使用 enum，你可以这样生成 class：

```C#
public static class CreatureAction
{
    public static readonly object Idle = new object();
    public static readonly object Walk = new object();
    public static readonly object Run = new object();
    // Etc.
}

animancer.States.Create(CreatureAction.Walk, _Walk);.
```

### Component Keys

如果一个脚本只有一个 animation 需要播放，它可以使用自己作为 key，因此一个 Walk script 可以使用 animancer.States.Create(this, _Walk) 创建一个 state，并使用 animancer.Play(this) 播放它。

## Performance

创建一个 state 并连接它到 Playable Graph 中需要一点时间。在各种主要的用例中，这个代价非常小而不值得考虑，因此你应该只要创建 states 就可以。这就是为什么大多数使用 Animancer 的常见方式是直接将你要播放的 AnimationClip 提供给它。如果这个 clip 的 state 还不存在于 graph 中，它可以瞬间创建一个新的 state，然后在之后每次播放它们时重用它们。

提前初始化 states：
- 在初始化 code 中（Awake/Start）使用 AnimancerComponent.GetOrCreateState/CreateState
- 使用一个 NamedAnimancerComponent，然后在 Inspector （或使用脚本）将 clips 赋予 Animation array。它只是简单地在 Awake 方法中调用 CreateStates
- AnimancerState.Dispose 从 playable graph 移除 state