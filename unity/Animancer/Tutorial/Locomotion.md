_Animancer.States.Current：Layer 0 的 AnimancerLayer.CurrentState. 这是在这个 Layer 上使用任何 Play 方法开始的最新的 State。

每个 Layer 都有自己当前的 State，_Animancer.States.Current 是访问 Layer 0 的 Current State 的 shortcut。

```C#
// 如果另一个动画仍在 fading out，对齐它们的 NormalizedTIme，确保它们在 walk cycle 中相同的进度位置上进行混合
if (Animancer.States.TryGet(otherAnimation, out var otherState)
    && otherState.IsPlaying)
    playState.NormalizedTime = otherState.NormalizedTime;
```

_Animancer.States.TryGet(key, out var state)：在 PlayableGraph 的 mapping 中查找 key 对应的 state。而 Play 在 mapping 中没有 state 时，会自动创建并播放。

State.IsPlaying 可以判断是否在播放（Fading out 也属于正在播放）。

state.Root.Cmoponent.Animantor.applyRootMotion:

- state.Root：graph 上的 root Playable
- Playable.Component：播放 Playable 的 AnimancerComponent 组件
- AnimancerComponent.Animator：Animator 组件
- Animator.applyRootMotion：应用 root motion

Transition.Apply(State)：Transition 就是记录动画 fade 的各种参数，以及应用的动画片段。但是这些参数不一定非要用在那个片段上。调用 Apply 将播放指定的 State，并应用这些参数。

当 Animator 应用 Root Motion 时调用 OnAnimatorMove。应用这个 Root Motion 到另一个 object。如果 character 的 Rigidbody 或 CharacterController 在 Animator 的 Parent 上，这很有用，使得 model 保持和 character 上的其他机制分离。

即 RootMotion 应用到 Animator 所在的 GameObject 上。但是有时我们会将模型挂载到另一个 GameObject 下面。这是将 RootMotion 应用到那个 Root 上更好。这就是在 OnAnimatorMove 中完成的。这个消息只是一个简单地回调，能够做什么完全依赖于编写的代码。这里是查询 Animator.deltaPosition 和 Animator.deltaRotation 并将它们应用到指定的 Transform 上。

```C#
private void OnAnimatorMove()
{
    if (!_Animancer.Animator.applyRootMotion)
        return;

    if (_MotionTransform != null)
    {
        _MotionTransform.position += _Animancer.Animator.deltaPosition;
        _MotionTransform.rotation *= _Animancer.Animator.deltaRotation;
    }
    else if (_MotionRigidbody != null)
    {
        _MotionRigidbody.MovePosition(_MotionRigidbody.position + _Animancer.Animator.deltaPosition);
        _MotionRigidbody.MoveRotation(_MotionRigidbody.rotation * _Animancer.Animator.deltaRotation);
    }
    else if (_MotionCharacterController != null)
    {
        _MotionCharacterController.Move(_Animancer.Animator.deltaPosition);
        _MotionCharacterController.transform.rotation *= _Animancer.Animator.deltaRotation;
    }
    else
    {
        // If we aren't retargeting, just let Unity apply the Root Motion normally.
        // 如果没有把 Animator 挂载到其他 GameObject 下面，就直接应用 Animator 的默认 RootMotion
        _Animancer.Animator.ApplyBuiltinRootMotion();
    }
}
```