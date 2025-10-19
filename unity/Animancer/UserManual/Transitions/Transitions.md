# Transitions

相比于 hard-coding 你的 fade durations，start 和 end time，speeds，和 events，在 Inspector 使用 transitions 定义这些细节通常更好，它允许你在 Edit Mode 预览它看起来怎样，并可以容易地被 non-programmers 修改，而不需要编辑和重新编译任何脚本。

Animancer 包含的每个 State types 具有它自己的 Transition Type，其包含各种相关细节使得当它被传递到 AnimancerComponent.Play(ITransition) 时，它将会创建那种类型的 state。例如，一个 ClipState.Transition 将会创建一个 ClipState 来播放一个 AnimationClip。

```C#
using Animancer;
using UnityEngine;

public class TransitionExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField] 
    private ClipState.Transition _Animation;

    private void OnEnable()
    {
        _Animancer.Play(_Animation);
    }
}
```

![transition-example](../../../Image/transition-example.gif)

Transitions 记录各种 transition 信息，控制如何从任何动画转换到当前动画的细节，否则你只能在 script 中自己编写这些数据和功能。

## Fields

ClipState.Transition 的常见字段

| Name | Code | 描述 |
| --- | --- | --- |
| Animation | Animation Clip asset | 要播放的动画片段 |
| Fade Duration | FadeDuration | transition 从任何之前的动画 CrossFade 到这个 动画需要花费的时间。不可以为负数，设置为 0 会立即播放动画 |
| Speed | Speed | 动画相对于常规速度播放的倍数。负数导致它反向播放 |
| Start Time | NormalizedStartTime | 如果开启，animation time 在开始播放时将会立即跳到这个 value。否则，它将会显式一个默认值：0x 用于正 speed，1x 用于 negative speed。如果 animation 是 inactive（AnimancerNode.Weight == 0），当你开始 transition，它的时间将会从 default value 开始，但是如果 animation 是 active 的，它将会从当前时间继续播放 |
| End Time | Events.NormalizedEndTime | 如果开启，这个 value 决定当 End Event 何时发生。除了触发事件之外，它不以任何方式影响 animation playback |
| Events | Events | timeline 可视化显式 transition 细节 |
| | | |

![AnimancerTransitionEvents](../../../Image/AnimancerTransitionEvents.png)

Timeline 可视化显式的 transition 细节包括：
- Labels 显式重要的时间（in seconds，rounded off）
- 蓝色的高亮区域表示 fading in 和 out。注意 transitions 只定义它们 fade in 的方式，因此显示的 fade out 简单地只是一个默认值。实际的 fade out 将会被下一个 fades in 的方式决定
- 底层的 Grey bar 在 End Time 不是 1x 时，表示 animation 的真实长度
- 右边的 button 添加一个 Animancer Event，Event 也会显示在这个区域

游戏中每个角色通常总是位于一个动画中，不可能不播放动画，否则角色在场景中就成为保持静止了。技能等动画可能只播放一次，但是 idle，walk，run 等动画通常都是循环的。因此 Transition 几乎总是从一个正在播放的动画 fade 过来，或者是循环的动画，或者是一个正在播放的一次性动画。Transition 时，新的动画定义一个 fade in 时间，在这个时间内，前一个动画的 weight 渐变为0，新的动画的 weight 渐变为1。Fade in 时间是新动画长度的一部分，但是与前一个动画的时间指针距离一个循环结束的时间的长度是没有关系的。因为前面说过，角色几乎总是位于一个动画中。对于循环动画，尽管前面的动画在循环，但是 weight 逐渐变为 0。对于一次性动画，如果前面动画的剩余时间小于 fade in 时间，当它播放完时，就不再提供数据了，但是新的动画的 weight 正在逐渐渐变为1并提供数据，因此角色仍然在动，因此动画仍然是平滑的。即使角色之前没有一个动画，新的动画逐渐权重变为1，效果仍然是平滑的。之前的一次性动画在播放完之后本来就可以认为之前已经没有动画了，然后全部只播放新的动画，只是新的动画权重还没有到1。因此 Transition 只需要定义新的动画的 fade in 就可以了，Transition 开始时完全不用管之前的动画处于什么状态。

### Time Fields

上面的一些自动显示一个 value 为两个单独的 fields：

![time-field](../../../Image/time-field.png)

- X 是 normalized time，意味着这个 value 是 animation 长度的 multiple。例如 0.5x 意味着动画的一半，1x 意味着动画的结束
- S 是固定的秒数。例如 0.5s 意味着半秒，1s 意味着完整的 1 秒

如果这个字段有一个开关，关闭它将会设置底层 value 为 float.NaN，根据这个字段，这将具有不同的效果。

## Previews

任何 transition 的 Inspector 的右边的 icon 打开一个 window，这可以让你预览它看起来怎样，因此你可以调整它的设置而无需进入 Play Mode。

![transition-preview](../../../Image/transition-preview.gif)

- Transitions 只定义将要播放的 animation，但是没有对之前或下一个 animation 的引用，因此 Preview Settings 允许你选择你想要使用的其他动画。
  - 这些设置只用作这个 window 中，不会作为 transition 的一部分，在运行时没有效果
  - 它会试图找出所有其他被这个 character 引用的动画，在 Previous Animation 和 Next Animation 下来菜单中列出来，但是你总是可以使用 object fields 选择任何 project 中的动画
  - 它会默认尝试 pick 给 idle 的动画
- regular time 在 Inspector 下面显示，使得你可以查看和控制 preview 的细节
- 你可以拖放任何 character model 到 preview scene，然后它将会尝试使用那个 character 继续 previewing transition

## Context Menu

Preview window 的 context menu 包含一些控制它的设置的功能：

- Show Transition

  如果开启，transition 被 previewed 将会显示在 preview window，就像在正常的 Inspector 中一样的

- Auto Close

  如果开启，window 将会在 target transition 不再存在时自动关闭（就像这个 object 被销毁了）

