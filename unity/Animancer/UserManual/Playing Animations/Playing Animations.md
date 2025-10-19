# Playing Animations

添加 AnimancerComponent 到你的 model 上，并使用脚本控制它：

1. 添加一个对 AnimancerComponent 的引用
2. 添加一个对 AnimationClip 的引用
3. 简单地调用 animancer.Play(clip)

AnimancerController.Play 返回一个 AnimancerState，它可以被用来访问和控制 animation 细节，例如 Speed 和 Time。

## Example

```C#
using Animancer;
using UnityEngine;

public sealed class PlayAnimation : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    private void OnEnable()
    {
        _Animancer.Play(_Clip);

        // 你可以使用返回的 AnimancerState 控制 animaiton
        // var state = _Animancer.Play(_Clip);
        // state.Speed = ..
        // state.Time = ..
        // state.NormalizedTime = ..
        // state.Events.OnEnd = ..

        // 如果 animation 已经开始播放，它将会从当前 current time 继续
        // 因此要强制它从开始播放，你可以重置 TIme：
        _Animancer.Play(_Clip).Time = 0;
    }
}
```

![add-animancer-component](../../../Image/add-animancer-component.gif)

## Play Methods

根据你想要做什么，AnimancerComponent 类有一些具有不同参数集合的 Play 方法。

### Play Immediately

```C#
Play(AnimationClip clip)
Play(AnimancerState state)
```

这些方法立即 snap character 到新的 animation（pose）。这尤其适合 Sprite animations，因为没有东西需要 blend，character 每次只能显示一个 Sprite。

这些参数之间的区别在 States page 上被解释。

### Cross Fade

```C#
Play(AnimationClip clip,   float fadeDuration, FadeMode mode = FadeMode.FixedSpeed)
Play(AnimancerState state, float fadeDuration, FadeMode mode = FadeMode.FixedSpeed)
```

这些方法随着时间 fade 新的 animation，并同时 fade 旧的 animation，这称为 Cross Fading。这经常非常适合 Skeletal Animations，因为它允许一个 character model 平滑地从一个 animation 的 ending pose 平滑地迁移到另一个 animation 的 starting pose，而不需要两个 poses 完全相同。它还意味着如果一个 animation 在任何时间点被中断（开始播放一个新动画），transition 仍然可以是平滑的。

注意 FadeMode 参数时可选地，因此下面两行都是做相同的事情：

```C#
animancer.Play(clip, 0.25f)
animancer.Play(clip, 0.25f, FadeMode.FixedSpeed)
```

### Transition

```C#
Play(ITransition transition)
Play(ITransition transition, float fadeDuration, FadeMode mode = FadeMode.FixedSpeed)
```

这些方法允许 Transitions 在一个 call 中应用它们所有的细节。这包含 fadeDuration（除非你使用第二个方法来自己指定它们），以及任何其他定义在 transition 的细节，例如 Speed，Start TIme，以及任何 Animancer Events，当使用内置 transiton types 时，events 可以在 Inspector 中配置，而不需要在脚本中硬编码那些细节。

### Try Play

```C#
TryPlay(object key)
TryPlay(object key, float fadeDuration, FadeMode mode = FadeMode.FixedSpeed)
```

不像其他方法，这些方法使用一个 key 来查找一个现有的 State 来播放，但是如果它们还没有注册，就不能创建新的 state。一旦找到 state，它们简单地调用相应的 Play Immediately 或 Cross Fade 方法。

## Pausing

有一些不同的方法你可以 pause 和 stop 单独的 animations，或同时操作它们。

```C#
using Animancer;
using UnityEngine;

public sealed class PausingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    // 在当前 frame 冻结一个 animation
    public void PauseClip()
    {
        var state = _Animancer.States[_Clip];
        state.IsPlaying = false;
    }

    // 在 animations 的当前 frame 将它们全部冻结
    public void PauseAll()
    {
        _Animancer.Playable.PauseGraph();
    }

    // 停止一个 animation 影响 character，并将它 rewind 它到 start
    public void StopClip()
    {
        _Animancer.Stop(_Clip);
        // 或者你可以在 state 上直接调用它
        var state = _Animancer.States[_Clip];
        state.Stop();
    }

    // 停止所有 animations 影响 character 并 rewind 它们到 start
    public void StopAll()
    {
        _Animancer.Stop();
    }

    // 停止所有之前的 animations 并播放一个新的
    public void Play()
    {
        _Animancer.Play(_Clip);
    }

    // 播放一个 animation 而不影响其他的 animation
    public void PlayIsolatedClip()
    {
        var state = _Animancer.States.GetOrCreate(_Clip);
        state.Play();
    }
}
```

## Edit Mode

Animancer 允许你在 Edit Mode 播放动画，就像它们正常那样被播放，这可以用于在 scene 中预览它们。

使用这个功能的最简单方法是在 MonoBehavior.OnValidate event message 中，它在 Unity Editor 处于 Edit Mode 时，每当这个脚本的一个实例被加载，或者 value 在 inspector 被修改，就会被调用。因此你简单地使用它调用 AnimancerUtilities.EditModePlay:

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private AnimationClip _Idle;

private void OnValidate()
{
    AnimancerUtilities.EditModePlay(_Animancer, _Idle);
}
```

AnimancerUtilities.EditModePlay 关心一些额外的事情，它们通常在 Play Mode 不是问题，但是它的核心仍然只是一个正常的对 AnimancerComponent.Play 的调用：

```C#
[System.Diagnostics.Conditional("UNITY_EDITOR")]
public static void EditModePlay(AnimancerComponent animancer, AnimationClip clip, bool pauseImmediately = true)
{
#if UNITY_EDITOR
    if (UnityEditor.EditorApplication.isPlayingOrWillChangePlaymode ||
        animancer == null || clip == null)
        return;

    // Delay for a frame in case this was called at a bad time (such as during OnValidate).
    UnityEditor.EditorApplication.delayCall += () =>
    {
        if (UnityEditor.EditorApplication.isPlayingOrWillChangePlaymode ||
            animancer == null || clip == null)
            return;

        animancer.Play(clip);

        if (pauseImmediately)
        {
            animancer.Evaluate();
            animancer.Playable.PauseGraph();
        }
    };
#endif
}
```

- The [Conditional] 属性导致 compiler 从运行时 builds（当 UNITY_EDITOR 没有定义）移除任何对那个方法的调用，这允许我们再开发期间支持实用的功能，比如这个，而在运行时根本不影响性能
- 它检查 EditorApplication.isPlayingOrWillChangePlaymode 来避免在 PlayMode 做任何事情。否则在 script 的 Inspector 改变任何东西，在 Play Mode 将会播放指定的 Idle animation 并在 gameplay 中间暂停 graph，即脚本的剩余部分不希望发送的事情
- 如果我们尝试在 OnValidate 之外直接播放动画，Unity 实际会给出错误，因此它还使用 EditorApplication.delayCall 来等待一帧
- 传递 pauseImmediately 参数为 true 导致它简单地显示动画的第一帧，然后当 false 时将允许 animation 来正常播放。默认 value 是 true，因为多数情况下不想在编辑一个 scene 时模型被 animating 和 moving。但这通常是个人喜好，因此自由地尝试使用哪个值
- 还要注意 Edit Mode 下 animations 不算做可以将 scene 标记为 dirty flag 的 modifications（以告诉 Unity 需要保存还在内存中的 Scene 数据，到 Project 中的 asset 文件）。这通常没有问题，因为 scene 在任何时间被打开时，animation 将会被重新播放。然而，当 scene 被保存时，它可能在 animation 的任何时间点，并保存它当前具有的任何 values，这将在一个 version control system 显示为一个 modifications
- 这个功能对于 Sprite animations 尤其方便，使得你可以简单地播放你赋予每个 character 的任何 Idle animation 的第一帧，因此它将显示正确的 Sprite 而不需要手动设置 Sprite

|||
| --- | --- |
| States | 最常见的 AnimancerState 的类型是 ClipState，它播放单个 AnimationClip，并使用这个 clip 作为 key 在内部 dictionary 注册 |
| Inspector | Animancer 在 Inspector 显示所有 animations 的实时细节，因此你可以观察它们在做什么，以及手动控制它们以进行测试和调试 |
| Component Types | 有义序不同类型的 AnimancerComponent，并且你可以制作自己的类型，来添加和修改功能 |
| Directional Animation Sets | 将 animation group 到 up/right/down/left (including or excluding diagonals) 集合中，来实现在执行各种操作时可以面向任何方向的角色 |
|||
