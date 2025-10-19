```C#
// Enable the OnAnimatorIK message.
_Animancer.Layers[0].ApplyAnimatorIK = true;
```

```C#
_LeftFoot = _Animancer.Animator.GetBoneTransform(HumanBodyBones.LeftFoot);
_RightFoot = _Animancer.Animator.GetBoneTransform(HumanBodyBones.RightFoot);
_FootWeights = new AnimatedFloat(_Animancer, "LeftFootIK", "RightFootIK");
_Animancer.Play(_Animation);
```