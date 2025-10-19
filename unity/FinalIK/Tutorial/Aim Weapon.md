这个 scene 展示了如何只使用 6 个静态 aim poses（只有一帧的 AnimationClip）和 AimIk 创建 360 度自由的 aiming。

Aim Poses（forward，left，back，right，up，down）是基于角色朝向 target 的方向进行 crossfade 的。

6 个 poses 的 directions 和 ranges 定义在 Aim Poser 的 AimPoser.cs 中。poses 的名字必须完全匹配 animator controller 中的参数。

Direct blend trees 用于 work around Mecanim 的 cross-fading 问题（不能 cross-fade back 到它正在 cross-fading 自的 state，而是忽略这个调用，即如果转给你从 forward crossfading 到 left，但是中途 target 移动又改成 crossfading 到 forward）。

**AimIK 工作在这上面（IK 是动画系统输出结果的 post-process），用来修改 static poses，来保持 gun 瞄准到 target。所有的 AimIk 所做就是 rotating spine hierarchy。**

LookAtIK 还用来选择 head 来面向 target。


SimpleAimingSystemMecanim.cas 用于在 aim poses 之间 cross-fading，并更新 IK target 的 position。

Aim Poser 中的 Poses 的名字必须完全匹配 Animator Controller 中 Upperbody Aiming layer 中的 Direct blend tree 的参数。

Pose 成员

- bool visualize：显示 这个 pose 在 scene view 中的方向和范围
- string name：引用的参数名
- Vector3 direction：pose 的方向
- float yaw = 75：yaw 范围，航偏角，左右旋转
- float pitch = 45：pitch 范围，俯仰角，上下旋转
- bool IsInDirection(Vector3 d)：确定这个 Pose 是否在指定的方向上
- SetAngleBuffer(float value)：设置 angleBuffer 来防止当角度只需要改变一点时，立即切换回上一个 pose。即在各个方向之间设置一定的缓冲区，各个 pose 的角度范围不是完全互斥，而是有一定重叠的，anglebuffer 就是 overlap angle，只有超过这个 buffer 才算进入下一个 pose。

AimPoser 成员：

- float angleBuffer = 5：angle buffer
- Pose[] poses：poses 数组
- Pose GetPose(Vector3 localDirection)：给定一个方向，返回第一个包含这个方向的 pose
- void SetPoseActive(Pose pose)：设置 poses 数组中给定 pose 为 active，即设置其 angleBuffer，其他 pose angleBuffer 都设置为 0

这个例子中，character 上有两个 IK，AimIK 和 LookAtIK，还有 SimpleAimingSystem 脚本。

Animator Controller 中复杂的动画设置（layer 和 blend tree）应该是为这个例子准备的。Aim Controller 只是复用了这个例子中的模型，要展示的内容和动画设置无关。

这个动画设置中，有两个 Layer：Base Layer 和 Upperbody Layer。

BlendTree 和 AnimationClip 一样本身也是一个 AnimationState。但是它的数据是通过包含的子状态混合而来的，而 AnimationClip 的数据是从文件中简单采样而来，但是它们在运行时的目的都是一样，在任何时刻输出动画数据（character pose）。

BlendTree 的类型：1D，2D，Direct（全方位）。Blend Tree 之所以叫 BlendTree，就是因为它的子状态不仅可以是 AnimationClip，还可以是任何 AnimationState 包括 BlendTree，只要它能在任何时刻提供动画数据（skeleton pose）。

Base Layer 中是一个 1D BlendTree。它包含3个状态：Aim MP40 Standing Breath（Idle），Walk，Run。而且第一个 Idle 动画和后面二者 Walk、Run 明显不是为同一个角色创建的动画（来源不同）。但是这没有关系，因为 Unity 通过 avatar 可以 retargeting 动画。另外 Idle 动画中包含 MP40（尽管应该没有动画 MP40 bone，和后面两者没有区别），而 Walk 和 Run 中没有，这也没有关系，因为这个 Base Layer 只用来播放 Lowerbody 动画，因为 Upperbody 动画将会被 Upperbody Layer 的数据覆盖。Upperbody Layer 具有 AvatarMask。

Upperbody Layer 中是一个 Direct BlendTree。这个 BlendTree 有 6 个子状态：Aim MP40 Standing Left、Right、Forward、Back、Up、Down。Layer 有 6 个参数分别对应这个 6 个子状态，每个参数控制一个。1D BlendTree 使用一个参数控制所有子状态的权重，而 Direct BlendTree 使用单独的参数控制每个子状态。

6 个子状态都是只有一帧的 AnimationClip，这一帧定义来每个状态的 Upperbody Pose，这样在任何时刻，这些子状态以及这个 BlendTree 只输出相同的数据，而 Lowerbody 有 Base Layer 输出不同的 pose。因此综合结果就是，下半身以正常方式行走，上半身保持一个姿势不变。

动画系统的核心就是混合数据：Blending。Playable 将这个功能完全暴露出来，使得你可以以任何方式混合数据，而不仅是 Animation System 提供的这些方法，甚至不仅可以混合动画数据，还可以混合音频数据，甚至任何脚本数据。Blending 是自然变化感觉的核心，类似模糊逻辑，事物同时出在多个状态中，只是有的状态显著，有的不显著，但是状态的显著性可以通过 weight 参数调整。

AimPoser GameObject 包含了这个 6 个状态的 Pose。

AimIK 的骨骼链是 Spine 1 > Spine 2 > Spine 3 > Neck，Aim Transform（用于 IKPosition 的 Transform）是 MP 40，为 Hand bone 下面。

SimpleAimingSystem：

- LimitAimTarget：

  确保 aiming target 不会太近（当 target 距离 first bone 比距离 last bone 更近会导致 solver 不稳定）

  沿着从 first bone 到 target 的方向强制一个最小距离

- DirectCrossFade(string state, float target)

  将指定参数平滑移动到 target，BlendTree 相应地自动加大权重混合那个状态的 pose

  ```C#
  float f = Mathf.MoveTowards(animator.GetFloat(state), target, Time.deltaTime * (1f / crossfadeTime));
  animator.SetFloat(state, f);
  ```

- Pose()

  根据 character 到 target 的方向，判断当前 AimPose。然后激活 AimPose（设置 angleBuffer，其他 pose 设置 angleBuffer = 0）。对当前 active Pose 在每个 LateUpdate 向 weight = 1 blend，其他 Pose 向 weight = 0 blend。相应的 Pose 就会平滑过渡。

AimIK 和 LookAtIK 组件会在自身 LateUpdate 中更新 solver.Update()。

但是 SimpleAimSystem 在 Start() 将 AimIK 和 LookAtIK 组件都 disable 了，然后在它的 LateUpdate 中手动调用 aimIk.solver.Update() 和 lookAtIk.solver.Update()，这主要是用来精确控制二者的先后顺序。就像 IK 是动画系统输出的后处理，当有多个 IK 时，后面的 IK 也是前面 IK 的后处理。

