# Componment Types

AnimancerComponent 是控制动画的主入口。它还有一些子类，具有额外的功能。

- AnimancerComponent

  基本组件，包装 Animancer 的核心功能。它基本上只是一个 Animator 组件和内部 AnimancerPlayable 的包装器，所有魔法在这里发生。

  ![animancer](../../../Image/animancer.png)

- NamedAnimancerComponent

  在 Inspector 中还具有一个 Animations 数组和 Play Automatically 开关，可以使用 name 注册 animations，因此你可以使用 strings 引用它们，就好像 Unity Legacy Animation 组件

  ![NamedAnimancer](../../../Image/NamedAnimancer.png)

- HybridAnimancerComponent

  具有一个 Animator Controller 和绝大多数在 Animator 上常见的相同功能（例如 Play，CrossFade，GetCurrentAnimatorStateInfo，SetFloat，等等）。因此你可以在那个 Animator Controller 有一些 animations，而同时可以使用 Animancer 直接播放它们的 AnimationClip 的能力

  ![HybridAnimancer](../../../Image/HybridAnimancer.png)

- SoloAnimation

  播放一个 animation，它可以在 Inspector 中赋予，而没有 Animancer 额外的性能消耗。这是它做的所有事情。它不支持 Fading，Layers，Animancer Events，还有任何其他 Animancer 的其他功能。它甚至不是 Animancer 的真正的一部分，它只是一个 self-contained 脚本，设计用来播放一个动画，没有其他东西。如果你想做任何更多的事情，最后使用一个正常的 AnimancerComponent

当使用 Unity Editor 的 Add Component 菜单，所有 Animancer 组件都位于 Animancer sub-menu 之下。

可以继承它们来实现你自己的 variations。例如：

- 继承 AnimancerComponent，并添加一个 SpriteRenderer 或 SkinnedMeshRenderer 字段，使得你可以和 animations 一起引用它
- 编写一个 CharacterAnimationSet 类，它继承 ScriptableObject，为每个 character 定义一组 animations，然后编写一个 CharacterAnimancer 类，它继承自 AnimancerComponent 以允许 character 在同一个地方引用那些 animation 集合中的一个
- 继承 NamedAnimancerComponent 并添加一个 string 数组使得你可以为每个 animation 指定一个自定义名字，而不是总是使用 AnimationClip.name
- 继承 AnimancerComponent 并添加一些 AnimationEventReceiver 来监听特定 Animation Events

## Changing Components

你可以容易地改变使用的 AnimancerComponent 类型，通过简单地添加一个新类型的组件到同一个 object（使用 Inspector 而不是 script），它自动替换之前的 AnimancerComponent 组件。

![changing-components](../../../Image/changing-components.gif)

- 任何继承自 AnimancerComponent 的 custom 类都会继承这个功能。
- 这使用了一个序列化技巧使 Unity Editor 改变旧的组件类型，并立即销毁新添加的组件，允许它保留两个组件共享的字段的 values（例如 Animator 引用），而且任何对这个组件的其他地方的引用也会被保留
- 这个功能通过在 AnimancerComponent.Reset 中调用 AnimancerUtilities.IfMultiComponentThenChangeType，使得你可以在自己的脚本中调用这个方法来使用这个功能

## Animator Members

AnimancerComponent.Animator 属性允许你直接访问 Animator 组件，然而它的很多成员不能在 Animancer 中工作（很多情况下，它们只是简单地不相关）。

一些成员工作正常：

- Root Motion: angularVelocity, ApplyBuiltinRootMotion, applyRootMotion, bodyPosition, bodyRotation, deltaPosition, deltaRotation, gravityWeight, hasRootMotion, isHuman, pivotPosition, rootPosition, rootRotation, velocity
- avatar, humanScale, isOptimizable
- cullingMode, updateMode
- fireEvents
- Bone Transforms: GetBoneTransform, hasTransformHierarchy, SetBoneLocalRotation
- Inverse Kinematics: GetIKHintPosition, GetIKHintPositionWeight, GetIKPosition, GetIKPositionWeight, GetIKRotation, GetIKRotationWeight, leftFeetBottomHeight, pivotPosition, pivotWeight, rightFeetBottomHeight, SetIKHintPosition, SetIKHintPositionWeight, SetIKPosition, SetIKPositionWeight, SetIKRotation, SetIKRotationWeight, SetLookAtPosition, SetLookAtWeight, SetTarget, targetPosition, targetRotation
- isInitialized
- hasBoundPlayables, playableGraph
- Rebind
- StringToHash：可以工作，但没有任何作用，因为 Animancer 不依赖 hash codes

一些成员不能直接使用：

| Animator Members | Details / Alternative |
| --- | --- |
| CrossFade, CrossFadeInFixedTime, Play, PlayInFixedTime | 使用 AnimancerComponent.Play |
| GetAnimatorTransitionInfo, GetBehaviour, GetBehaviours, GetCurrentAnimatorClipInfo, GetCurrentAnimatorClipInfoCount, GetCurrentAnimatorStateInfo, GetNextAnimatorClipInfo, GetNextAnimatorClipInfo, GetNextAnimatorClipInfoCount, GetNextAnimatorStateInfo, HasState, IsInTransition | AnimancerComponent.States 允许你访问任何使用 key 注册的 state 的细节，Play 还会返回播放的动画的 state |
| GetBool, GetFloat, GetInteger, GetParameter, IsParameterControlledByCurve, parameters, parameterCount, ResetTrigger, SetBool, SetFloat, SetInteger, SetTrigger | Animancer 不使用 parameters |
| GetLayerIndex, GetLayerName, GetLayerWeight, layerCount, layersAffectMassCenter, SetLayerWeight | AnimancerComponent.Layers 让你访问所有 Layers 的细节 |
| keepAnimatorControllerStateOnDisable | 使用 AnimancerComponent.StopOnDisable |
| linearVelocityBlending | Does not work properly anyway, but Mixers can usually achieve linear blending by disabling Synchronisation on any non-locomotion states (such as Idle or Attack) when blending them with locomotion states (such as Walk or Run) |
| runtimeAnimatorController | Technically works, but the output from the controller gets overridden by Animancer. Use a HybridAnimancerComponent as demonstrated in the Hybrid Basics example |
| speed | Use AnimancerPlayable.Speed instead. Though you will usually only want to modify the speed of a single animation using AnimancerNode.Speed |
| Update | Use AnimancerComponent.Evaluate |
| MatchTarget, InterruptMatchTarget, isMatchingTarget | No direct equivalent. Using a curve to control Inverse Kinematics may help | 

以下成员是否可以工作还不确定：

- feetPivotActive
- logWarnings
- Animation Recording: playbackTime, recorderMode, recorderStartTime, recorderStopTime, StartRecording, StartRecording, StopPlayback, StopRecording
