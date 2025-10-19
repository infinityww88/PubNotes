在游戏开始时播放一个 UnityEngine.AnimationClip。

属性

- Animator：这个脚本控制的 Animator 组件。如果想在运行时设置这个 value，最好使用正规的 AnimancerComponent，而不是 SoloAnimation
- Clip：在 SoloAnimation.OnEnable 中被播放的 AnimationClip。如果想在运行时设置这个 value，最好使用正规的 AnimancerCom，而不是 SoloAnimation
- FootIK：如果是 Humanoid，是否在模型上应用 Foot IK。
  Unity开发者表示，他们认为启用这一功能后它看起来会更好，但通常情况下，它只会让腿部以与动画师预期的略微不同的姿势结束。
- IsPlaying
- NormalizedTime：无视 loop，持续增长
- Speed
- StopOnDisable