## SimpleEventReceiver

只是用来展示 AnimancerEventReceiver 如何使用。监听 Animator 发出的 Event 信息。

SimpleEventReceiver 只是接收 Animator 发出的 Event 事件的脚本，然后触发它包含的 AnimancerEventReceiver OnEvent 的 HandleEvent。由使用 SimpleEventReceiver 的脚本在它的 OnEvent 上注册 State 和回调函数。

```C#
SimpleEventReceiver.OnEvent.Set(state, (animationEvent) => { ... });
```

OnEvent 是结构体。

## EndEventReceiver

类似 SimpleEventReceiver，使用名为 ”End“ 的 Animation Events 调用一个 AnimancerState 的 endEvent。它不注册回调，而是直接调用 State 的 endEvent。但是 ”End“ Animation Events 可以在动画片段中的任何时间点设置，这就相当于设置 AnimancerState.NormalizedEndTime，因此这就相当于在 AnimationClip 中设置 NormalizedEndTime，通过 ”End“ 事件。

这个组件必须总是挂载到 Animator 同一个 GameObject 上，以接收来自它的 Animation Events。

注意 Unity 在触发一个具有 AnimationEvent 参数的 Animation Event 时总是分配一些 garbage。

属性

- Animancer：触发 endEvent 所在的 Animancer
- AnimationEvent CurrentEvent：触发 ”End“ Animation Event 的参数

方法

- bool End(AnimancerComponent, AnimationEvent)

  尝试调用 AnimancerState 的 endEvent。指定 AnimancerComponent，生成 AnimationEvent 并传递它。

## AnimationEvent

- animationState
- animationClipInfo
- animationStateInfo
- floatParameter
- functionName
- intParameter
- stringParameter
- time

## AnimancerEventReceiver

- Action<AnimationEvent> Callback
- string FunctionName
- AnimancerState Source

AnimancerLayer.CommandCount：记录 CurrentState改变的次数。通过存储这个值，之后比较它和当前值，来判断 state 之后是否被改变过，即使它已经变回到相同的状态。

这个函数主要目的是在 AnimationClip 中注册的事件和 Animancer 之间建起桥梁。因为如果只使用 Animancer 事件，必须在代码中指定事件发生的时间，这就失去了在 AnimationClip 中定义事件的好处了（可编辑）。另外 AnimationEvent 事件直接调用 Animator GameObject 上的回调函数，而关心它执行什么。而且不同的动画可能有相同的事件名字，需要我们手动编写代码进行判断处理。这个类就是来简化这些过程的。

它不是一个组件，而是一个普通的结构体。使用方法是声明一个实例 onEvent，然后在 animancer.Play(clip) 之后，将 state 和要执行的回调函数注册到 onEvent 里面。然后在收取 AnimationEvent 的脚本中触发 onEvent.HandleEvent，它会坚持当初注册的 State 是否还是当前的 State。例如 SimpleEventReceiver 就是这样的一个例子。SimpleEventReceiver 只是简单地包含一个 AnimancerEventReceiver OnEvent，然后监听 Animator 发出的 Event 事件。使用 SimpleEventReceiver 的脚本在使用 Animancer.Play(clip) 创建一个 State 之后，将 State 和 Event 事件的回调函数注册到 SimpleEventReceiver.OnEvent 上。当 SimpleEventReceiver 收到 Event 事件时，就会执行 SimpleEventReceiver.OnEvent.HandleEvent(AnimationEvent)。

这种方式的好处：

- 确保只在 State 上执行回调，而不是同名的 Animator 事件都触发回调
- 将事件时间和 Animancer 解耦，使得可以在 AnimationClip 中定义

EndEventReceiver 是 AnimancerEventReceiver 的另一个用例。但是有两点区别：

- 它不明确指定引用的 State，而是通过 AnimationEvent 参数中的 clip 遍历 PlayableGraph，找相应的 State。

  目前猜测在 PlayableGraph 中（不知道是 Animator 还是 Animancer 的约束），一个 clip 只能有一个权重相同的 state（Graph 中的 node）。如果 clip 不同，或者 clip 相同但是 weight 不同（例如从头播放当前动画片段，但是不直接跳到开头而是 blending，这样之前的状态就要保留并创建新的 state，原来的 state 在切换时就被标记为丢弃的，只是在 fade out 完成时才彻底回收），在 Graph 中就有 2 个节点，但是权重不同。

  这么看其实 SimpleEventReceiver 也可以这样找，但是它不能这样。因为每个 State 的同名事件（Event，End）的处理不同，即有不同的回调函数，因此必须将它们关联起来。EndEventReceiver 直接调用 State.Event.OnEnd，因此它们直接就是关联的，因此可以不指定 State。但是对于 SimpleEventReceiver 这样的自定义普通事件，State 和 回调函数没有关联在一起，因此需要同时指定 State 和相应的回调，将它们记录在 AnimancerEvent 中联系在一起。既然已经明确指定了 State，那就不必想 EndEventReceiver 一样在 Graph 中遍历了。

- 不指定事件回调，因为 End 回调以及在 State.Events.OnEnd 上注册了，因此直接调用它就可以了。

AnimancerEventReceiver onEvent 只是一个静态结构体，只用是用来保存这个 state 和 onEvent 以及事件名，然后在调用它的 HandleEvent 时，进行判断开始注册的 state 是否还 active，因为如果 state 已经无效了，再执行它就没意义了，例如另一个动画也有相同的事件名。还会检查动画片段是否相同，指定的函数名和 AnimationEvent 中的函数名是否相同，都是为了保证只对注册的 state 才执行 callback。

## AnimancerEvent

AnimancerState.Events 列表中的 Event 类型。

Unity 中 AnimationClip 的 AnimationEvent 没有特殊的 End 事件，只有位于最后一帧的普通事件。Animancer 对 EndEvent 进行了特殊处理。
