Mixer（Blend Tree）是动画混合

Layer 是动画加法

Animancer 和 PlayableGraph 是一个 GameObject 的动画控制器。每个 GameObject 都有各自的 Animancer 和 PlayableGraph。

在一个 Layer 中，animation 可以独立地播放它们的状态，和其他 layers 独立管理，同时和那些 layers 一起混合出 output。

## 属性

- ApplyAnimatorIK

  等价于在 AnimatorController layers 上设置 IK Pass。由于 Playables API 的限制，layerIndex 总是 0。Layer 将这个 value 设置到所有 State。

- ApplyFootIK

  登记与在 AnimatorController states 上设置 Foot IK。Layer 将这个 value 设置到所有 State。

- ApplyParentAnimatorIK

  是否使 AnimatorNode.Parent 也设置 node 的 ApplyAnimatorIK 以匹配它。默认为 true

- ApplyParentFootIK

- AverageVelocity

  一个 Animancer 或 PlayableGraph 控制的是一个 GameObject。所有当前播放的动画的 root motion 的平均 velocity，使用它们当前的 AnimancerNode.Weight 作为权重。

- ChildCount

  Animancer 通过各个类和接口提供了在 PlayableGraph 上遍历 Node 的功能。

- CommandCount

- AnimancerState CurrentState

  Layer 当前播放的动画 state。特别地，它是 Layer 上任何 Play 或 CrossFade 方法创建的最新的 State。

  通过 AnimancerState 自身上的方法单独创建的 States 不会注册这个属性。每次这个属性改变时，AnimancerLayer.CommandCount 都会增加。可以在创建 State 改变这个属性时记录它，并在之后和它比较判断 State 是否改变了，即使重新播放同一个 Clip。

- EffectiveSpeed

  在 PlayableGraph node 中从 root 到当前节点的 Speed 相乘的结果，它是当前状态的实际播放速度。

- FadeSpeed

  Node fading 向 AnimancerNode.TargetWeight 的速度

- Index

  Playable 连接都 parent 的 port 号。

- IsAdditive

  决定 layer 是否被设置为 additive blending。否则它会 override 任何之前的 layers。

- KeepChildConnected

  指示 child playables 是否总是连接到 layer 上

- Layer

  Layer 是它自己的 root

- Speed

  AnimancerState.Time 每帧前进的速度（默认为 1）

- TargetWeight

  这个 node 根据 AnimancerNode.FadeSpeed fading 到的 AnimancerNode.Weight

- Weight

  这个 node 的当前混合权重，决定它影响最终结果的程度。

## 方法

- void AddChild(AnimancerState)

  添加一个新的 port，并使用 AnimancerState.SetParent(AnimancerNode, int) 将 state 连接到它上面。这是操作 PlayableGraph 的一个方法。

- void AppendIKDetails(StringBuilder, string, IPlayableWrapper)

  追加 IPlayableWrapper.ApplyAnimatorIK 和 IPlayableWrapper.ApplyFootIK 的细节

- CopyIKFlags(AnimancerNode)

  从 AnimancerNode.Parent 复制 AnimancerNode.ApplyAnimatorIK 和 AnimancerNode.ApplyFootIK 设置，如果 AnimancerNode.ApplyParentAnimatorIK 和 AnimancerNode.ApplyParentFootIK 分别是 true

- void CreateIfNew(AnimationClip, AnimationClip)

  为每个指定的 clip 调用 AnimancerLayer.GetOrCreateState(AnimationClip, bool) 。

  如果你只想创建一个单一的 state，使用 AnimancerLayer.CreateState(AnimationClip)

- void CreateIfNew(AnimationClip, AnimationClip, AnimationClip)

- void CreateIfNew(AnimationClip, AnimationClip, AnimationClip, AnimationClip)

- void CreateIfNew(AnimationClip[])

- CreatePlayable()

  创建和分配这个 node 管理的 Playable

- CreatePlayable(out Playable)

  创建和分配这个 layer 管理的 AnimationMixerPlayable

- ClipState CreateState(AnimationClip)

  在这个 layer 上创建和返回播放这个 clip 的 ClipState

- ClipState CreateState(Object key, AnimationClip)

- T CreateState<T>()

  创建并返回一个挂载到 layer 上的新的 T

- void DestroyPlayable()

  销毁这个 UnityEngine.Playables.Playable

- void DestroyStates()

  销毁连接到 layer 上的所有 states。Layer 就是一个 Playable Graph 上的子树 root node。

- GetEnumerator()

  返回一个 enumerator，迭代直接连接在 layer 上的所有 staes（不在 MixerState 中）

- AnimancerState GetOrCreateState(AnimationClip, bool)

  调用 AnimancerPlayable.GetKey(AnimationClip) 并返回使用这个 key 注册的 state，如果不存在就创建一个。

  如果状态已经存在，但是有错误的 AnimancerState.Clip：
  - allowSetClip = false 导致它抛出一个 System.ArgumentException
  - allowSetClip = true 允许改变 AnimancerState.Clip

  使用这个 clip 作为 key 的 state 但是具有不同的 clip，可能是后来手动改变了 State.clip

- AnimancerState GetOrCreateState(ITransition)

  返回使用 ITransition 作为 key 注册的 state，如果没有就创建一个(ITransition.Create) 并使用 ITransition 作为 Key 来注册它。

  ITransition 实现了 IHasKey 接口，它有一个 IHasKey.Key 方法。因此所有的 Transition 都可以作为 Key。

  Animancer 允许使用 string，AnimationClip，ITransition，和 Object 作为 Key 来注册 AnimancerState。

- AnimancerState GetOrCreateState(Object key, AnimationClip clip, bool allowSetClip)

- AnimancerState GetOrCreateWeightlessState(AnimancerState)

  如果 State.Weight 不是 0，这个方法查找一个 Weight 的 State 副本，或者创建一个新的 Weight = 0 的 AnimancerState。

  这再次佐证，PlayableGraph 中一个 Clip 可以有两个 ClipState，一个 Weight = 0，一个 Weight > 0，这用来重复播放一个 Clip，但是允许前面的 State fade out，新的 State in。这就必须有两个 ClipState，它们共同使用一个 Clip。

- GetTotalWeight()

  计算这个 Layer 中所有 states 的 Weight 的总和。

- int IndexOf(Key key)

  返回这个 object 在 list 中的位置，或者 -1 如果不存在的话。

- AnimancerState Play(AnimancerState)

  停止所有其他动画，播放这个 State，并返回它。

  动画将会从当前 AnimancerState.Time 继续播放。要从头开始播放，使用

  ```C#
  ...Play(clip).Time = 0;
  ```

- AnimancerState Play(AnimationClip)

  停止所有其他动画。播放这个 clip，返回 state。

  本质是创建一个 ClipState.Transition，然后播放这个 Transition。

- AnimancerState Play(AnimationClip state, float fadeDuration, FadeMode mode = FixedSpeed)

  在 fadeDuration 时间内 fade in state，同时 fade out 这个 layer 中所有其他动画。

- AnimancerState Play(ITransition)

- AnimancerState Play(ITransition transition, float fadeDuration, FadeMode mode)

  FadeMode：

  - FixedDuration
  
    计算在指定的 fadeDuration 时间内将 AnimancerNode.Weight 过渡到 target value 的 fade speed。

  - FixedSpeed
  
    计算在指定的 fadeDuration 时间内将 Weight 从 0 过渡到 1 的 fade speed，无视实际开始的 weight。

  - FromStart
  
    如果 state.Weight != 0，这个 mode 将使用 AnimancerLayer.GetOrCreateWeightlessState(Animancer.AnimancerState) 获得它的一个 weight = 0 的副本，使得它可以 fade 这个副本，同时 fade 原来的 state 以及所有其他的 states。

    在接下来的 frames 中重复地使用这个 mode 可能导致不期望的效果。因为它每次都会创建一个新的 state。此时你应该使用 FixedSped。

    这个 mode 只用于 ClipState

  - NormalizedDuration

    就像 FixedDuration，除了 fadeDuration 被乘以 animation length

  - NormalizedFromStart

    ~= FromStart

  - NormalizedSpeed

    ~= FixedSpeed

- SetMask(AvatarMask mask)

  设置这个 Layer 将要影响的 bones

- SetWeight(float)

  设置这个 node 的当前 blend weight，它决定 node 影响最终结果的程度。

  这个方法允许任何当前进行的 fade 继续。如果你不想这样，你可以设置 AnimancerNode.Weight 属性。

- StartFade(float targetWeight, float fadeDuration = 0.25f)

  开始在 fadeDuration 时间内 fade AnimancerNode.Weight 到 targetWeight。

  如果 targetWeight = 0，当 fade 完成时 AnimancerNode.Stop 将会被调用。

  如果 AnimancerNode.Weight 以及等于 targetWeight，fade 会立即结束。

- Stop()
  
  设置 AnimancerNode.Weight = 0 并在所有动画上调用 Animancer.AnimancerState.Stop 来停止播放它们，并 rewind 它们到 start。

- AnimancerState TryPlay(Object key)

  停止 layer 上所有的动画，播放注册为 key 的动画，并返回 state。如果没有注册为 key 的 state，这个方法什么也不做，并返回 null。  

- AnimancerState TryPlay(Object key, float fadeDuration, FadeMode mode = FixedSpeed)

