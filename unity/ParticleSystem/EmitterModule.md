# EmissionModule

ParticleSystem 的 EmissionModule 的脚本接口。

Emission 模块有三种发射粒子的方法：随时间发射，随移动距离发射，周期性 burst 发射，而 burst 可以配置很多个。如果配置多个方法（多个 burst），每个发射方法都是独立运行的，最终的粒子数是它们每个发射的粒子的总和。

## 属性

- burstCount

  burst 的数量。每个 burst 包括：Time，Count，Cycles，Interval，Probablity。

  EmissionModule 可以配置多个 burst。

- enabled

  指示 EmissionModule 是否开启。

- MinMaxCurve rateOverDistance / float rateOverDistanceMultiplier

  emitter 随移动距离生成新粒子的速率。

  emitter 只在它移动的时候生成新的粒子。如果粒子系统的 GameObject 包含一个 Rigidbody 或 Rigidbody2D，则它的 Emitter Velocity 属性被设置为 Rigidbody 的 velocity，unity 基于 Rigidbody 的 velocity 计算距离。否则，Unity 基于 GameObject 的 Transform 组件自上一个 update 移动了多远来计算距离。

- MinMaxCurve rateOverTime / float rateOverTimeMultiplier

  粒子系统随时间发射粒子的速率。

## 方法

- GetBurst
- GetBursts
- SetBurst
- SetBursts

这些方法读取或设置某个或全体 burst。

粒子系统发射粒子的根本方法是调用 ParticleSystem.Emit()，使用它可以任意地发射粒子。内置的 EmissionModule 提供了三种最常见的发射方法，使得对这些发射方法不需要再编写脚本来实现。如果这些方法不满足需要，则可以通过自定义脚本来实现。

Particle System 的 Play、Stop 方法就是针对这个模块的，它们启动和停止 Emission Module 的运行，而不影响 Emit 的发射。即使 ParticleSystem 调用了 Stop，仍然可以通过 Emit 发射粒子。

EmissionModule 必须 enable，才能通过 Play/Stop 控制它的运行，否则即使 Play，也不会发射粒子。

Play 开启 EmissionModule 的发射。如果 PS 被暂停，Play 从上一次 Pause 的 time 恢复它的运行。Pause 暂停粒子系统的模拟，就像 deltaTime = 0。如果 PS 被 stop，Play 使 PS 从 time = 0 开始运行，并应用 startDelay。如果 PS 已经运行，Play 没有效果。Stop 完全停止 Emission 的发射。

Play 和 Stop 都可以指定一个 bool withChildren，指示是否同时开启和关闭所有的 child ParticleSystem。

Emission Module 只包含如何发射粒子的配置，没有控制开始和停止的方法，它们通过 PS 的 Play Stop 控制。

Particle 包含粒子的所有属性，ParticleSystem 的不同模块控制 Particle 的不同属性。因此 ParticleSystem 各种模块的属性反映的也是 Particle 的各种属性。

PS.Emit 发射可以指定一个 count 数字，按照 PS 各个模块的当前配置立即发射 count 个粒子。Emit 还可以传入一个 ParticleSystem.EmitParams，它包含了 Particle 一样的属性集合。被粒子系统发射的粒子的属性本是各个模块按照自己的配置设置好的，传入这个参数，它包含的属性会覆盖掉被发射粒子上的那些属性。任何没有修改的属性将会继承 inspector 上指定的行为。

Emit(EmitParams emitParams, int count) 可以按显示指定的 Particle 属性发射 count 个粒子。

emitParams 还包含一组 Reset 方法，可以将指定的属性重置会 Inspector 上指定的值。


