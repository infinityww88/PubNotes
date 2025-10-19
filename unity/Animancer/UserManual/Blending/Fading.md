# Fading

在调用 AnimancerComponent.Play 播放动画时，你可以指定不同的参数集合，依赖于你是否想要立即 snap 到新的 animation 还是在一段时间中优雅地 fade out 之前的动画，fade in 新的动画，即 Cross-Fading。

Fading 就是 Transition。前面讲的 Transition 是专门用于配置 transition 信息的类。

Fading 通常不用于 Sprite 动画，因为他们不能被混合，因为它们只控制一个值，就是 sprite index，因此不可能使角色同时处于两个状态中。但是 Fading 对骨骼动画非常重要，因为它允许一个角色模型平滑地从一个动画的结束 pose 变换到另一个动画的开始 pose，而不需要两个 pose 是完全相同的。它还意味着动画如果在任意时间点被中断（Cross-Fade 播放新的动画）仍然是平滑的，不管之前的动画处于哪个位置/Pose。


## Durations

```C#
void CrossFadeExample(AnimancerComponent animancer, AnimationClip clip)
{
    // Default 0.25 seconds fade duration.
    animancer.Play(clip, AnimancerPlayable.DefaultFadeDuration);

    // Fade over 0.8 seconds.
    animancer.Play(clip, 0.8f);

    // Fade for 20% of the new clip's duration.
    animancer.Play(clip, clip.length * 0.2f);
    animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed);

    // Fade for 10% of the old clip's duration.
    animancer.Play(clip, animancer.States.Current.Length * 0.1f);
}
```

使用 fade duration 参数的 Play 方法还有一个 FadeMode 参数，用来确定它如何工作。这个参数是可选的，如果不指定默认使用 FadeMode.FixedSpeed，因此下面两行代码完成相同的事情：

```C#
animancer.Play(clip, 0.25f);
animancer.Play(clip, 0.25f, FadeMode.FixedSpeed);
```
注意 fade duration 是完全独立于 animatin length 的，因此如果 fade 太长了甚至可能在 animation 结束时还没有完成 fading。

## Custom Fade

所有 fades 默认是 linear 的，例如它们以一个在开始 fade 时计算的常量 AnimancerNode.FadeSpeed 移动 AnimancerNode.Weight 到 AnimancerNode.TargetWeight。但是这并不总是给出最平滑的效果因此 Animancer 包含一个 CustomFade 系统，允许你使用一个标准 Interpolation.Function，一个 AnimationCurve，或一个自定义 delegate 修改一个 fade 过程。

要使用这个系统，简单地在调用 animancer.Play 之后立即调用任何 static CustomFade.Apply 方法

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Clip;

private void Awake()
{
    // Start fading the animation normally.
    var state = _Animancer.Play(_Clip, 0.25f);
    
    // Then apply the custom fade to modify the state you are fading in.
    CustomFade.Apply(state, Easing.Sine.InOut);// Use a delegate.
    CustomFade.Apply(state, Easing.Function.SineInOut);// Or use the Function enum.
    
    // Or apply it to whatever the current state happens to be.
    CustomFade.Apply(_Animancer, Easing.Sine.InOut);
    
    // Anything else you play after this will automatically cancel the custom fade.
    // 任何之后 play 的东西将会自动取消这个 custom fade
}
```

## Curve Preset Libraries

AnimationCurve 对于在 Inspector 中可视化编辑 curve functions 非常方便，然而它们可能对于设置复杂和一致的 curves 非常繁琐。

幸运的是，Unity 允许你定义 Curve Preset Libraries，因此你可以简单地从这里下载 Animancer Curve Presets，并使用它作为你自定义 curves 的开始。注意这些 curves 被手动配置以最少的 keyframes 的数量以得到更好的性能。它们不覆盖 Easing class 中完全相同的 functions 集合，并且那些相同的与准确的值也是有一定差异（因为是手动配置，而且是用样条曲线模拟 Easing 函数，而不是准确的数学计算）

![curve-presets](../../../Image/curve-presets.gif)

## Individual Fading

当你使用一个 fade duration 调用 Play 方法，它在内部在每个 animation 上调用 AnimancerNode.StartFade。例如，如果你有 Idle，Walk，Jump animations，并其你调用 Play(walk, 0.25f)，它将会在 walk state 上调用 StartFade(1, 0.25f)，在其他 states 上调用 StartFade(0, 0.25f)。第一个参数应该是 target weight。这意味着你可以使用 StartFade 来控制独立的 states，而不是只是同时对它们 cross-fading。

因为 AnimancerLayer 也继承自 AnimancerNode，这也意味着你可以 fade 整个 Layers in 和 out。Layer 只是 Playable Graph 上的一个子树。对于 layers 没有 CrossFade（Transition），因为它们通常不以那种方式使用，但是你可以手动模拟达到相同的效果，通过调用 StartFade(0, fadeDuration) 来 fade out 一些 layers，并且 StartFade(1, fadeDuration) fade in 另一些。
