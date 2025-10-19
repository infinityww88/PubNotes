Transition 是 Animancer 基本的操作单位，它包含了动画数据的来源，过渡的模式，过渡的时间，开始时的时间线，End 事件的时间线，和 End 事件回调。这些数据加起来才是从一个动画切换到另一个动画的全部信息。Transition 就是这些信息的包装容器。

动画数据的来源有多种，不仅仅是 AnimationClip，尽管是 AnimationClip 是最常用和最基础的动画数据来源，即 ClipState，对应的 Transition 就是 ClipState.Transition。除了 Clip，还有 BlendTree，AnimatorController，都是动画数据的来源，对应的 State 分别是 LinearMixerState 和 ControllerState。它们只是数据来源不同，但是作为动画过渡其他数据都是一样的。因此 Animancer 将它们统统抽象为 Transition，作为统一操作的单位。

使用 Clip 直接播放动画是因为它是最经常使用而且最简单的 State（ClipState），因此 Animancer 为它提供了 shortcut 方法。对于其他动画数据来源需要稍微复杂一点的设置（BlendTree，Controller），因此就只能通过 Play(Transition) 来播放并创建 State。例如 Play(ControllerTransition) 可以创建一个 ControllerState，Play(LinearMixerTransition) 可以创建一个 LinearMixerState。而 ControllerTransition 和 LinearMixerTransition 可以在 Project 中创建 Asset 并在 Inspector 中编辑，因为它们相对复杂。另外 AnimationClip 本身也是 asset，也可以在 Project 中创建 ClipTranstion asset，可以视为设置最容易的 Transition。

Transition 本身也是 ScriptableObject，即 asset，可以在 Inspector 中编辑。

Transition 的各个参数时创建 State 时使用初始参数（Speed，StartTime，EndTime，EndEvents）。它们只在播放时使用。当动画已经被播放时，即状态创建之后，播放速度等参数就只能在 State 上设置了。Transition 是创建 State 的数据，State 是动画的运行时数据。

每种 State 有自己的 Transition，因为每个 State 的 Transtion 应用的数据源不一样（Clip，BlendTree，Controller）。每个 Transition 包含创建这个 State 的各种数据，包括动画源，Speed，StartTime，EndTime，EndCallback 等等。调用 Animancer.Play(Transition) 将使用这个 Transtion 模板创建一个相应的 State。

- ClipState.Transition;
- MixerState.Transition;
- ControllerState.Transition;
