一个 Animancer.AnimancerPlayable graph 中所有 states 基类，这个 graph 管理一个或多个 UnityEngine.Playables.Playable。

## 属性

- IsPlaying

  Time 当前是否在自动前进

- IsActive

  如果这个 state 在播放并且在一个或者向一个非 0 的 weight fading

- IsStopped

  如果 state 没有播放，并且 weight = 0

- ApplyAnimatorIK

  Unity 是否应该在它或者它的 children 具有 Animancer.AnimancerNode.Weight 的 animated object 上调用 OnAnimatorIK

  OnAnimatorIK 回调用于设置 Animatin IK。它被 Animator 组件在更新 IK system 之前立刻调用。在这里设置 IK goals 的 position 和它们各自的权重。

  这等价于在 AnimatorController layers 上开启 IK Pass，除了由于 Playables API 的限制，layerIndex 总是 0.

  这个值默认从 false 开始，但是在 Animancer.IPlayableWrapper.Parent 被设置时，可以通过 Animancer.AnimancerNode.CopyIKFlags(Animancer.AnimancerNode) 自动改变。

  IK 只在至少一个 Animancer.ClipState 有一个大于 0 的 Animancer.AnimancerNode.Weight 时起作用。其他 node 类型(非 ClipState 类型，例如复合 State 类型）或者存储这个值用于应用到它的 children，或者根本不支持 IK。

  node 指的是 playable graph 上的节点，即 state。

  ```C#
  using UnityEngine;
  using System.Collections;
  
  public class ExampleClass : MonoBehaviour
  {
      float leftFootPositionWeight;
      float leftFootRotationWeight;
      Transform leftFootObj;
  
      private Animator animator;
  
      void Start()
      {
          animator = GetComponent<Animator>();
      }
  
      void OnAnimatorIK(int layerIndex)
      {
          animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, leftFootPositionWeight);
          animator.SetIKRotationWeight(AvatarIKGoal.LeftFoot, leftFootRotationWeight);
          animator.SetIKPosition(AvatarIKGoal.LeftFoot, leftFootObj.position);
          animator.SetIKRotation(AvatarIKGoal.LeftFoot, leftFootObj.rotation);
      }
  }
  ```

- ApplyFootIK

  这个 object 或者它的 children 是否应该应用 IK 到 character feet 上。

  这等价于在 AnimatorController State 上开启 Foot IK。

  这个值对 Animancer.ClipState 默认是 true（其他 node 类型为 false），但是当 Animancer.IPlayableWrapper.Parent 被设置时，它可以通过 Animancer.AnimancerNode.CopyIKFlags(Animancer.AnimatorNode) 自动改变。

  IK only takes effect while at least one Animancer.ClipState has a Animancer.AnimancerNode.Weight above zero. Other node types either store the value to apply to their children or don't support IK.

  Humanoid 动画始终在 retargeting 的。因为动画片段和具体的模型时分离独立的，尽管创建它时是在某个具体的模型上。在运行时播放动画必须将 AnimationClip 和实例模型骨骼绑定，即使是在创建 clip 的模型上播放 clip，这个过程也是执行的，只不过此时动画效果最准确，因为绑定到的模型骨骼恰好和动画文件匹配。如果在比例不同的骨骼上播放，就可能导致 Feet 漂浮。这就是为什么有 FootIK 的原因。在 State 上开启 FootIK，就可以在 State 播放过程中对 Feet 执行 IK，这和普通的 IK 没有区别。

  如果让动画在它创建时的模型上播放时，在 Humanoid 模式中可以关闭 FootIK，因为 Foot 不会离开地面。也可以 Generic 播放，此时不通过 avatar，而是直接通过骨骼 Hierarchy path 直接绑定。
  
  这就是 Generic 比 Humanoid 动画性能更好的原因。人物动画既可以是 Humanoid 的，也可以是 Generic 的。

- ApplyParentAnimatorIK

  Animancer.AnimancerNode.Parent 是否应该设置这个 node 的 Animancer.AnimancerNode.ApplyAnimatorIK 来匹配它。默认为 true

- ApplyParentFootIK

- ChildCount

- EffectiveSpeed

  这个 node 的 Animancer.AnimancerNode.Speed 和它的每个 parent（Wrap Node，例如 layer）的 Animancer.AnimancerNode.Speed 相乘，得到这个 state 的实际播放速度。

- FadeSpeed

  这个 node fading 到 Animancer.AnimancerNode.TargetWeight 的速度

- Layer

  这个 node 连接到的 root Animancer.AnimancerLayer

- LayerIndex

  这个 State 连接到的 AnimancerLayer 的 index

- Speed

  Animancer.AnimancerState.Time 每帧前进的快慢（默认为 1）。

  负值反向播放动画。

  要暂停一个动画，设置 Animancer.AnimancerState.IsPlaying 为 false，而不是将这个值设置为 0.

  state.Speed = 1; // 正常速度
  state.Speed = 2; // 双倍速
  state.Speed = 0.5f; // 半速
  state.Speed = -1; // 反向正常速度

- TargetWeight

  Animancer.AnimancerNode.Weight 过渡到的权重，根据 Animancer.AnimancerNode.FadeSpeed 速度

- Weight

  这个 node 当前的混合权重，决定它对最终结果的影响程度。

  设置这个属性取消任何当前正在进行 fade。如果你不想这样，使用 SetWeight。

  调用 Animancer.AnimancerPlayable.Play(UnityEngine.AnimationClip) 立即设置所有 states 的权重为 0，设置新的 state 为 1. 这是于其他值例如 Animancer.AnimancerState.IsPlaying 分离的，因此一个 state 可以在任何地方暂停，并且仍然在 character 上面显示它的 pose，或者它可以以 weight = 0 播放并仍然想触发 events（尽管 states 再达到 0 weight 时正常情况下会停止，因此你会需要显式设置它重新播放。

  调用 Animancer.AnimancerPlayable.Play(UnityEngine.AnimationClip,System.Single, Animancer.FadeMode) 不会立即改变 weights，但是在每个 state 上调用 Animancer.AnimancerNode.StartFade(System.Single,System.Single)，设置 Animancer.AnimancerNode.TargetWeight and Animancer.AnimancerNode.FadeSpeed。然后每个 State 在 Update 中向着那个 target 以那个 speed 过渡。这个过渡始终执行的，只是正常情况下，target weight = 1

- RemainingDuration
  
  这个 state 从它的当前 AnimancerState.NormalizedTime 以当前 Animancer.Node.EffectiveSpeed 走到 AnimancerState.NormalizedEndTime 需要花费的时间。

  ```C#
  var state = animancer.Play(clip);

  state.RemainingDuration = 1; // 在 1s 内从当前时间播放到 end
  state.RemainingDuration = 2; // 在 2s 内从当前时间播放到 end
  state.RemainingDuration = 0.5f;
  state.RemainingDuration = -1; // 从当前时间远离 end 播放，即反向播放
  ```

  要控制从 start 播放需要的时间，使用 AnimancerState.Duration。

  设置这个 value 会改变 AnimancerNode.EffectiveSpeed，而不是 AnimancerState.Length。

  当新的 State 开始播放时，使用原来的 State 的 Duration 剩余的时间 fade 作为新的 State 的 fadeDuration

- Duration

  以当前 AnimancerNode.EffectiveSpeed 从 start 完全播放动画到 end 需要的时间

  ```C#
  var state = animancer.Play(clip);

  state.Duration = 1; // Play fully in 1 second.
  state.Duration = 2; // Play fully in 2 seconds.
  state.Duration = 0.5f; // Play fully in half a second.
  state.Duration = -1; // Play backwards fully in 1 second.
  state.NormalizedTime = 1; state.Duration = -1;// Play backwards from the end in 1 second.
  ```

  要控制从当前位置播放到 end 需要的时间，使用 RemainingDuration。

  设置这个值，会改变 AnimancerState.EffectiveSpeed 而不是 AnimancerState.Length

- Events

  一个 AnimancerEvent 的列表。

- Length

  当 AnimancerNode.Speed = 1 时这个 state 完全播放需要使用的时间。

- Object Key

  在 root AnimancerPlayable.States 字典中用来标识这个 state 的 object。

- Clip

  这个 state 播放的 AnimationClip

## 方法

- SetWeight

  设置混合权重，就像 Weight，但是允许当前正在进行的 fade 过程继续。

- StartFade

  调用 Animancer.AnimancerNode.StartFade 在 fadeDuration fade Animancer.AnimancerNode.Weight。

  如果 targetWeight = 0，Animancer.AnimancerNode.Stop 在 fade 完成时将被调用。

  如果 Animancer.AnimancerNode.Weight 已经等于 targetWeight，则 fade 立即结束。

- Stop

  停止动画，立即 inactive State，使它不再影响 output。State 上的事件 Events 在 Animancer.Play 的那一刻就被清除了，只剩下 State fade out。

- Play

  立即播放这个动画，没有任何 blending，设置 IsPlaying=true，Weight=1，并清除 Events。这个方法不改变 Time，它将从当前 value 继续。

- GetEnumerator

  获得这个 node 所有 child states 的 enumerator

- 