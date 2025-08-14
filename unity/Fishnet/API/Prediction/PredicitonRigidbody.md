# PredictionRigidbody

## Properties

- bool HasPendingForces

  如果由 pending forces 等待应用，返回 true。

- Rigidbody Rigidbody

  force 要应用的 rigidbody。

## Methods

和 Unity Rigidbody 一样的方法。

- void AddExplosiveForce(float force, Vector3 position, float radius, float upwardsModifier = 0F, ForceMode mode = ForceMode.Force)
- void AddForce(Vector3 force, ForceMode mode = ForceMode.Force)
- void AddForceAtPosition(Vector3 force, Vector3 position, ForceMode mode = ForceMode.Force)
- void AddRelativeForce(Vector3 force, ForceMode mode = ForceMode.Force)
- void AddRelativeTorque(Vector3 force, ForceMode mode = ForceMode.Force)
- void AddTorque(Vector3 force, ForceMode mode = ForceMode.Force)
- void AngularVelocity(Vector3 force)

其他方法

- void ClearPendingForces()

  清理 pending velocity 和 angular velocity forces。

- void ClearPendingForces(bool velocity)

  手动清理 pending forces。

- List<PredictionRigidbody.EntryData> GetPendingForces()

- void Initialize(Rigidbody rb)

  force 要应用的 Rigidbody。

- void InitializeState()
- void ResetState()

- void Reconcile(PredictionRigidbody pr)

  Reconciles 到一个 state。

  pr 保持要校准的 rigidbody，将这个 PredictionRigidbody 的 rigidbody 设置到参数的 rigidbody 中。

- void Simulate()

  按照添加的顺序，应用 pending forces 到 rigidbody。

- void Velocity(Vector3 force)

  清理 pending forces，并设置 velocity。Simulate 应该仍然被正常调用。