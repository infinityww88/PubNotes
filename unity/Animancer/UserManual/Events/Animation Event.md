# Animation Events

当使用 Animancer 时，Unity 的内建 Animation Event system 工作起来就像没有使用 Animancer 一样。Unity Manual 解释了如何使用一个 model import setting 的 Animation Tab，或者 Animation Window 设置 events。要接收 events，你简单地挂载一个 script 到 Animator 组件所在的相同的 object，engine 将会在那个 script 查找一个具有 event 指定的 Function name 的方法。

为了组织目的，使你的 event listener 脚本继承 AnimancerComponent 将会很方便（而不是拥有两个单独的组件），但是绝大多数 event 实际上与 Animancer 没有任何直接交互，只是用于包含 Unity Animation Event 的脚本方法。

注意任何具有一个 string 或 AnimationEvent 参数的 event 每次被触发时会分配一些 Garbage，这可能是潜在的性能问题。

## Simple Events

这个 SimpleEventReceiver 组件有一个 OnEvent callback，它被使用 "Event" 名字函数的 Animation Events 触发。这意味着你可以开始一个 animation，然后注册一个 callback 用于事件的发送。它会自动断言那个 AnimationClip 实际上有一个指定名字的 event（在 Unity Editor 中）。

SimpleEventReceiver 组件主要用于你可以如何使用 AnimationEventReceiver 结构实现你自己的 events 的示例，但是它可以很好地用于一个简单的游戏，如果你设置你所有的 animations 只有一个名为 Event 函数的 event（Attack 脚本使用这个 event 指示 hit time，Walk 脚本使用它播放 footstep 声音，等等）。这个 callback 使用触发的 AnimationEvent 作为参数，因此你可以访问它的 values，包括它所在的 AnimationClip。

![simple-event](../../../Image/simple-event.png)

在 Code 中使用 simple events 类似使用 EndEvents，你简单地访问 SimpleEventReceiver.OnEvent，而无需访问 state：

```C#
[SerializeField]
private AnimancerComponent _Animancer;

[SerializeField]
private SimpleEventReceiver _EventReceiver;

...

var state = _Animancer.Play(clip);
state.Events.OnEnd = ...;// See Animancer Events.
_EventReceiver.OnEvent.Set(state, ...);
```

建议你总是使用 Set（Inspector？） 而不是只赋值 Callback 来确保你只接收来自你指定的 state 的 callback。否则来自一个 fading out animation 的 events 可能触发一个你刚为一个新的 fading in animation 注册的 callback（因为它总是使用相同的 Function 名字）。

## End Animation Events

EndEventReceiver 组件和 SimpleEventReceiver 类似，除了它使用 End 作为函数名（而不是 Event 作为函数名），以及它触发 animation 的 End Event 而不是拥有自己的 callback。你可以设置 End Events 在任何你想要的时间发生，因此这简单地就是另一种完成相同事情的方式。

![end-event](../../../Image/end-event.png)
