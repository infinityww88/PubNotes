# RigidbodyPauser

Pause、unpause rigidbodies。当 paused，rigidbodies 不能被交互或 simulated。

## Properties

- bool Paused

  rigidbodies 是否被认为是 paused 的。

## 方法

- void InitializeState()
- void ResetState()

- void Pause()
- void Unpause()

- void UpdateRigidbodies()

  使用初始设置，重置 rigidbodies。

- void UpdateRigidbodies(Transform t, RigidbodyType rbType, bool getInChildren)

  为 rigidbodies 赋值。
