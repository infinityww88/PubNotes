# PredictionRigidbody

当应用外部力，通常是通过 collisions，这个类提供精确的 simulations 和 re-simulations。

使用 PredictionRigidbody 非常简单明了。简而言之，你需将原本直接作用于刚体（Rigidbody）的力变化，改为作用于 PredictionRigidbody 实例，以实现更精准的物理模拟和状态同步。

## 在 Script 之外使用

正如上文所述，你应始终将力作用于 PredictionRigidbody 组件，而非直接作用于 Rigidbody。

我们的首个指南演示了如何在 replicate 方法内实现这一点，以及如何利用 PredictionRigidbody 进行状态同步，但未展示如何从外部脚本（如游戏中的缓冲器）添加力。

从外部脚本添加力的复杂度很简单，关键在于记住将力施加到 PredictionRigidbody 而非 Rigidbody。以下是一个示例，展示了如何使用世界对象的触发器来排斥玩家：

若要让 triggers 和 collisions 在预测模式下正常工作，必须使用 NetworkTrigger/NetworkCollision 组件。否则，受 Unity 限制，此类交互将无法生效。查看 API 文档了解这些组件的信息。

有趣的事实是：Fish-Networking 是唯一有能力在 prediction 中模拟 Enter/Exit events 的 framework，即使 Fusion 也没有这个能力。

```C#
private void NetworkTrigger_OnEnter(Collider other)
{
    //当碰撞到 trigger 应用一个向上的 impulse。
    if (other.TryGetComponent<RigidbodyPlayer>(out rbPlayer))
        rbPlayer.PredictionRigidbody.AddForce(Vector3.up, ForceMode.Impulse);
    //这里不要调用 PredictionRigidbody.Simulte()。Simulate 只能在 replicate 方法中调用。
    //可以子啊 replicate 之外调用 AddForce，但是 Simulate 只能在 replicate 中调用。
}
```

许多控制器可能希望直接设置速度，PredictionRigidbody 支持此功能。建议查阅其 API 以了解所有可用功能。

最后一个示例展示如何直接设置 velocities：

```C#
float horizontal = data.Horizontal;
Vector3 velocity = new Vector3(data.Horizontal, 0f, 0f) * _moveRate;
PredictionRigidbody.Velocity(velocity);
```
