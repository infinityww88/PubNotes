FingerRig 对每个 finger 使用一个 LimbIK solver。bone 3 是可选的，这可以用于大拇指。

LimbIK 用于 3-bones 的结构。

FingerRig 和 AimIK 等一样，继承自 SolverManager，是一个 IK 组件，将它挂载到 Hand 上，处理所有 finger 的 IK。

每个 Finger 包含一个 LimbIK solver，以及一些附加逻辑用来处理 finger。
