ControllerState 是 AnimancerState 的子类。它播放一个 RuntimeAnimatorController。

你可以像 Animator 一样控制这个 State。

每个 State 有自己的 Transition 定义。

Float1ControllerState 是 ControllerState 的子类，它管理一个 float 参数。

```C#
public abstract class AnimancerTransition : ScriptableObject, ITransition, IAnimationClipSource { ... }

public class AnimancerTransition<T> : AnimancerTransition where T : ITransition { ... }

public class Float1ControllerTransition : AnimancerTransition<Float1ControllerState.Transition> { ... }
```

AnimancerTransition 的主要作用是使 Transition 可序列化（ScriptableObject），使得可以在 Inspector 中配置它们。

AnimancerTransition<T> 和 AnimancerTransition 不是一个定义。AnimancerTransition<T> 生成类的泛型，这些生成类继承自 AnimancerTransition，只是泛型名字和抽象类名相同。因为泛型具体类名是在泛型类名基础上加上泛型参数的，因此肯定不会和泛型类名一样。

ITransition：一个可以创建 AnimancerState 的 object，它管理 state 应该如何播放的细节。

某种程度上将，Transition 是动画系统的基本行为单元。因此 State 只是保存数据，或者说数据单元。任何时候播放一个动画，都是一个 Transtion，从前面的状态到新的状态的过渡 transition。所有每次播放动画都是执行一个 transition。因此 ITranstion 定义了 Transtion 的行为，包括创建状态，应用参数等等。ITransition 才是脚本中我们应该操作的基本单元，而为了简化只操作 State 和 fadeDuration 只是 shortcut，ITransition 包含 State 和所有 Transition 需要的数据，不仅仅是 fadeDuration，而且把它们放在一起，复合高聚合的原则。每次播放一个动画都是在播放一个 ITransition 而不仅仅是一个 State。

Layer -> Transition -> State

```C#
public new class Transition : Transition<Float1ControllerState>
```

- CreateState

  创建并返回一个新的 AnimancerState。

  调用 AnimancerPlayable.Play(ITransition) 等价于调用 ITransition.CreateState 然后调用 ITransition.Apply.

  也可以使用 AnimancerUtilities.CreateStateAndApply

  当一个 Transition 首次用在一个 object（Clip，AnimatorController）上时，这个方法被调用，以创建这个 state 并将它注册到内部的字典中。

- FadeMode
- FadeDuration
- Apply(AnimancerState state)

  被 AnimancerPlayable.Play(ITransition) 调用，以应用任何对 state 的修改。

ITransitionDetailed : ITransition

- IsLooping
- NormalizedStartTime
- Speed
- MaximumDuration
- IsValid：这个 transition 是否可以创建一个有效的 AnimancerState

