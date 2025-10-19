动画切换过渡是非常常用的功能，包含一组非常常用的参数，Transition 将这些参数打包在一起，包括：

- Animation Clip
- Fade Duration
- Speed：播放速度倍率，负数反向播放
- StartTime：动画播放时跳转到这个位置
- EndTime：End 事件的时间
- End Callback
- Events：Transition 上还有 AnimancerEvent.Sequence

这个类是可序列化的，既可以在 Inspector 中配置，也可以在 Project 中创建 asset 资源。还可以在 Transition 上配置 End 事件回调，但是不能在 Inspector 上设置 Event Sequence。

_Animancer.Play(Transition)，Play 创建 State，设置 fadeDuration 和 Speed，跳到 StartTime，设置 End 事件时间。

_Animancer.Playable.PauseGraph() 冻结 PlayableGraph 到它的当前 state，之后你需要调用 UnpauseGraph 来恢复播放。

_Animancer.Evaluate() => _Animancer.Playable.Evaluate() 求值所有当前播放的动画，应用它们的 states 到 animated objects，类似 AnimationClip.Sample()。
_Animancer.Evaluate(float deltaTime)

```C#
// Start paused at the beginning of the animation.
_Animancer.Play(_WakeUp); // 将 _WakeUp 设置为当前状态
_Animancer.Evaluate();  // 求值 PlayableGraph 当前状态到 animated object
_Animancer.Playable.PauseGraph(); // 暂停 PauseGraph

// Initialise the OnEnd events here so we don't allocate garbage every time they are used.
// 直接在 Transition 上设置 End 回调函数，这样由 Transition 引用 End 事件，而不需要每次在创建 State 时都重新分配一个 lambda
_WakeUp.Events.OnEnd = () => _Animancer.Play(MovementAnimation);
_Sleep.Events.OnEnd = _Animancer.Playable.PauseGraph; // _Sleep.Events.OnEnd 冻结 PlayableGraph
```

可以通过 state.NormalizedTime 和 state.Time 读取和设置动画播放的时间。

Unity Animation 窗口：

- 使用 Mecanim AnimatorController 时，可以预览、编辑、创建动画片段
- 使用 Animancer 时，只能预览编辑当前动画，但是不能在左上角的下拉菜单中选择创建新的动画片段

每个 AnimancerComponent 都自己的 PlayableGraph，通过 _Animancer.Playable 访问，可以被暂停和恢复。对于一次性动画，在播放完毕时应该通过 End 事件暂停 PlayableGraph 以节省性能，但是对于需要持续播放动画的 character 则应该一直播放 PlayableGraph，因为 character 始终处于一个动画状态，除非 death 状态。但是 death 状态后角色通常也被销毁了，AnimancerComponent 组件也会随之销毁，因此可以不用暂停。

```C#
// Apply the starting state and pause the graph.
var state = _Animancer.Play(_Open); // 将 Open 动画设置为当前状态，并冻结在第一帧
state.NormalizedTime = _Openness; // 使用 NormailzedTime 控制动画播放的位置
_Animancer.Evaluate();
_Animancer.Playable.PauseGraph();

// 在结束时总是冻结 PlayableGraph 以节省性能
state.Events.OnEnd = _Animancer.Playable.PauseGraph;
```

```C#
// Get the state to set its speed (or we could have just kept the state from Awake).
var state = _Animancer.States[_Open];

// If currently near closed, play the animation forwards.
// 使用 state.Speed 正负号控制正向反向播放动画
if (_Openness < 0.5f)
{
    state.Speed = 1;
    _Openness = 1;
}
else// Otherwise play it backwards.
{
    state.Speed = -1;
    _Openness = 0;
}

// And make sure the graph is playing.
_Animancer.Playable.UnpauseGraph();
```

这个例子中在 Editor 中，AnimancerComponent 在 Inspector 中就有 state 了，这是因为 Door.cs 脚本中设置 Awake 在 Editor 也可以执行，其中注册了 Open 动画 State。

```C#
#if UNITY_EDITOR
private void OnValidate()
{
    if (_Animancer == null || _Open == null)
        return;

    // 当调用 OnValidate 时，延迟一帧调用指定的 lambda。否则 Unity 在重新编译脚本后会给出一个错误
    UnityEditor.EditorApplication.delayCall += () =>
    {
        if (_Animancer == null || _Open == null)
            return;

        Awake();
    };
}
#endif
```

SoloAnimation 组件用来简单播放一个单一动画，指定：

- Animator
- Animation Clip
- Speed
- Foot IK：是否应用 Foot IK Pass
- Stop On Disable：如果为 true，当 disable 这个 object 时，将会停止和 rewind 所有 animations。否则只是简单地暂停，并从当前位置恢复
