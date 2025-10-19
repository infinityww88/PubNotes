# Animator

Interface to control the Mecanim animation system.

AnimatorController 和 Animancer 只是组织管理 PlayableGraph 的方式，Animator 才是处理和播放 PlayableGraph 的组件。

Unity 内置了一个对人形动画的 IK 系统，在 Animator 中保留了对 IK 系统的控制接口。这些接口通过 Avatar（AvaterIKGoal） 指定要操作的骨骼，然后指定一个 IK target。

Avatar

- isHuman：如果 avatar 是一个 Humanoid avatar，返回 true
- isValid：如果 avatar 是一个有效的 mecanim avatar 返回 true。它可以是 generic，也可以是 human avatar

Generic Avatar 只有一个约定映射节点，就是 root。

Foot IK 也是 IK 的一种，和普通的 IK Pass 一样，是动画的后处理，只是它不必我们自己手动设置 target，而是 Unity 采样原始动画中 Avatar 的 feet 的 position/rotation，然后在 IK Pass（或者一个单独的 IK Pass）中应用这些 feet targets。是否应用这个过程就是通过 iKOnFeet 开关控制。

## 属性

- angularVelocity：从上一帧计算的 avater 角速度
- velocity
- applyRootMotion
- avatar
- bodyPosition：body 的质心位置
- bodyRotation：body 的质心旋转
- deltaPosition：avatar 相对于上一帧的 delta position
- deltaRotation：avatar 相对于上一帧的 delta rotation
- fireEvents：Animator 是否发送 AnimationEvent 类型事件
- hasRootMotion：当前 rig 是否有 root motion
- hasTransformHierarchy：这个 object 是否有一个 transform hierarchy
- isHuman：rig 是 humanoid 还是 generic
- layerCount
- parameterCount：染回 controller 中参数的数量
- parameters：被 animator 使用的 AnimatorControllerParameter 列表
- pivotPosition：pivot 的当前位置
- pivotWeight
- rootPosition：gameobject 的 root position
- rootRotation：gameobject 的 root rotation
- runtimeAnimatorController
- speed：animator 的 speed
- targetPosition

  返回 SetTarget 指定的 target 位置。只有在调用了 SetTarget 之后，一个 frame 被求值时这个 position 才有效。Animator.applyRootMotion 必须被开启使得 targetPositio 被计算。

- targetRotation
- updateMode：Normal，AnimatePhysics（在 FixedUpdate 中更新，是动画系统和物理引擎同步），UnscathedTime（独立于 Time.timeScale 更新，暂停游戏时的 UI 动画）

## 方法

- ApplyBuiltinRootMotion

  应用默认的 Root Motion。

  在 MonoBehavior.OnAnimatorMove 或 StateMachineBehaviour.OnStateMove 使用它，在你不想手动处理 root motion 的 frames 的时候。

- CrossFade

  创建一个从当 state 到另一个 state 的 crossfade

- Transform GetBoneTransform(HumanBodyBones humanBoneId)

  返回 human bone id 映射到的 Transform

  HumanBodyBones 是一个枚举，指定了人体骨骼的各个部分

- Get/Set Controller 变量，Trigget

- Get/Set LayerName, Get/Set LayerIndex, Get/Set LayerWeight

- StartPlayback，StopPlayback

- Update：基于 deltaTime 求值 animator（手动模拟）

### IK 相关方法

- Get/Set IKHintPosition(AvatarIKHint hint, Vector3 hintPosition)

  AvatarIKHint: LeftKnee, RightKnee, LeftElbow, RightElbow

  Pole、Bend Goal

- Get/Set IKHintPositionWeight

- Get/Set IKPosition(AvatarIKGoal, Vector3 goalPosition)

  设置 IK goal 的 position。End effector 将尝试到达到这个方向。

  AvatarIKGoal: LeftFoot, RightFoot, LeftHand, RightHand

  IK 总是旋转骨骼使 end effector 到达 target position

- Get/Set IKPositionWeight

- Get/Set IKRotation(AvatarIKGoal goal, Quaternion goalRotation)

  设置 IK goal 的 rotation。End effector 将尝试旋转到这个方向。

- Get/Set IKRotationWeight

- SetLookAtPosition(Vector3 lookAtPosition)

- SetLookAtWeight

  SetLookAtWeight(float weight);
  SetLookAtWeight(float weight, float bodyWeight);
  SetLookAtWeight(float weight, float bodyWeight, float headWeight);
  SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight);
  SetLookAtWeight(float weight, float bodyWeight = 0.0f, float headWeight = 1.0f, float eyesWeight = 0.0f, float clampWeight = 0.5f);

- MatchTarget(Vector3 matchPosition, Quaternion matchQuatation, AvatarTarget targetBodyPart, MatchTargetWeightMask weightMask, float startNormalizedTime, float targetNormalizedTime = 1)

  AvatarTarget: Root, Body, LeftFoot, RightRot, LeftHand, RightHand

  自动调整 GameObject position 和 rotation，使得在指定的时刻，targetBodyPart 能位于指定的位置和方向上。

  自动调整 GameObject position 和 rotation 使得当 current state 在指定的 progress 上，AvatarTarget 到达 matchPosition。Target matching 只工作在 Layer 0 上。你同时只能 queue 一个 match target，你必须等第一个完成，否则之前的 target matching 将会丢弃。

  如果你调用一个 MatchTarget，而 start time 比 clip 的 normalized time 小，而且 clip 可以 loop，MatchTarget 将会调整时间以匹配下一个 loop。例如 start time = 0.2, normalized time = 0.3, start time 将会成为 1.2。Animator.applyRootMotion 必须被开启使的 MatchTarget 生效。

  MatchTarget 只会执行一次，它和 clip loop 无关。

- SetTarget(AvatarTarget targetIndex, float targetNormalizedTime)

  为当前 state 设置 AvatarTarget 和 targetNormalizedTime。

  一旦 frame 被求值，使用 Animator.targetPosition 和 Animator.targetRotation 来查询 position 和 rotation。





   
