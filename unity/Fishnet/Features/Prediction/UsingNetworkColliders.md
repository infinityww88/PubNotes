# Using NetworkColliders

每种 NetworkCollider 的用法都一样，并且非常类似 Unity Callbacks。

当使用 client-side prediction 时，NetworkCollider 组件被设计为为 collisions 和 triggers 精确分发 Enter，Stay，Exit callbacks。

这些组件上，所有 events 都具有相同的名字：NetworkCollider，NetworkCollider2D，NetworkTrigger，NetworkTrigger2D。

每个 event 返回什么天然是不同的，依赖于你使用的是哪个组件。例如，NetworkCollision 组件会返回 Collider，NetworkCollision2D 则返回 Collider2D。

OnStay callback 不像 Unity 那样返回 Collision。由于 Unity 的限制，Fishnet 无法避免 hotpath allocations 而提供 Collision callback。如果你需要返回 Collision，请使用 Unity 的 OnStay callback。它可以在 prediction 中正常工作。

## Usage

示例脚本放在 player object 上。这个脚本展示订阅所有 3 个 events（OnEnter，OnStay，OnExit），并使用 OnEnter event 播放一个声音，以及对 player 应用一个 force。

```C#
//假设这个脚本继承 NetworkBehaviour
[SerializeField]
private AudioSource _hitSound;

private NetworkCollision _networkCollision;

private void Awake()
{
    //获取放在 object 上的 NetworkCollision 组件
    //可以将这个组件放在任何你通常需要使用 Unity collider callbacks 的地方
    _networkCollision = GetComponent<NetworkCollision>();
    // Subscribe to the desired collision event
    _networkCollision.OnEnter += NetworkCollisionEnter;
    _networkCollision.OnStay += NetworkCollisionStay;
    _networkCollision.OnExit += NetworkCollisionExit;
}

private void OnDestroy()
{
    //因为 NetworkCollider 和这个脚本放在同一个 object 上，我们不需要 unsubscribe，callbacks 会随着 object 销毁而销毁。
    //但是如果你的 NetworkCollider 在另一个 object 内，则需要 unsubscribe 它们。
    if (_networkCollision != null)
    {
        _networkCollision.OnEnter -= NetworkCollisionEnter;
        _networkCollision.OnStay -= NetworkCollisionStay;
        _networkCollision.OnExit -= NetworkCollisionExit;
    }
}

private void NetworkCollisionEnter(Collider other)
{
    //只在当前没有 reconciling 时播放音效。
    //如果你准备在 reconcilations 中播放音效，audio 将会在每个 reconcile，每个 tick 执行，直到 player 不再 reconciling 到 collider 中。
    if (!base.PredictionManager.IsReconciling)
        _hitSound.Play();
        
    //总是在 enter 时对 player 应用 velocity，即使在 reconciling
    PlayerMover pm = GetComponent<PlayerMover>();
    //For this example we are pushing away from the other object.
    Vector3 dir = (transform.position - other.gameObject.transform).normalized;
    pm.PredictionRigidbody.AddForce(dir * 50f, ForceMode.Impulse);
}

private void NetworkCollisionStay(Collider other)
{
    // Handle collision stay logic
}

private void NetworkCollisionExit(Collider other)
{
    // Handle collision exit logic (e.g., deactivate visual effects)
}
```

你可能会疑惑，PredictionRigidbody是什么，以及为什么我们要将力作用于它而非直接作用于 Rigidbody。PredictionRigidbody（及其 2D 版本）是一种用于向预测刚体施加力的​​必需但简洁的方式​​，其核心目的是在客户端预测物理行为时，确保力的作用符合网络同步逻辑，避免因浮点数误差或物理引擎差异导致的同步问题。

简单来说，它封装了对预测刚体的力操作，使开发者无需直接操作 Rigidbody，即可实现与服务器端一致的物理模拟效果。
