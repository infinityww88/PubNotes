# Description

RootMotionController 是一个工具组件，设计用于增强 root motion 支持。这个组件负责计算和提供 root motion velocity 和 rotation 给 Character。

RootMotionController 组件必须添加到具有 Animator 的 GameObject 上，通常是你的 Character 的 Model。

# Methods

- virtual void FlushAccumulatedDeltas()

  刷新任何累积的 deltas。

  当 character toggle root motion 时，这阻止了 delta 累积。

- virtual Quaternion ConsumeRootMotionRotation()

  返回当前 root motion rotation，清除累积的 delta rotation。

- virtual Vector3 ConsumeRootMotionVelocity(float deltaTime)

  返回当前 root motion velocity ，并清理累积的 delta positions。
