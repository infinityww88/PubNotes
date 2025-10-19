一个包装类，允许访问被 animations 控制的 float 属性。

```C#
public AnimatedFloat(IAnimancerComponent animancer, string propertyName);
public AnimatedFloat(IAnimancerComponent animancer, params string[] propertyNames);
```

```C#
private AnimatedFloat _FootWeights;
_LeftFoot = _Animancer.Animator.GetBoneTransform(HumanBodyBones.LeftFoot);
_RightFoot = _Animancer.Animator.GetBoneTransform(HumanBodyBones.RightFoot);
_FootWeights = new AnimatedFloat(_Animancer, "LeftFootIK", "RightFootIK");
```

AnimationClip 中每个属性都表示为一个 Curve，Curve 通过控制点 key 控制。AnimatedFloat（以及 AnimatedInt 等）用来访问 clip 中指定属性的动画曲线。

AnimationClip 就是各种属性曲线的集合。

AnimatedFloat 可以同时访问几个属性的曲线。然后通过索引访问曲线值。

AnimationClip 在动画时自动采样，AnimatedFloat 自动读取这一帧的曲线值。

```C#
// Note that due to limitations in the Playables API, Unity will always call this method with layerIndex = 0.
private void OnAnimatorIK(int layerIndex)
{
    // _FootWeights[0] is the first property we specified in Awake: "LeftFootIK".
    // _FootWeights[1] is the second property we specified in Awake: "RightFootIK".
    UpdateFootIK(_LeftFoot, AvatarIKGoal.LeftFoot, _FootWeights[0], _Animancer.Animator.leftFeetBottomHeight);
    UpdateFootIK(_RightFoot, AvatarIKGoal.RightFoot, _FootWeights[1], _Animancer.Animator.rightFeetBottomHeight);
}
```