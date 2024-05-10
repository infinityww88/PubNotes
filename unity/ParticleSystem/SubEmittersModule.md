# SubEmittersModule

sub-emitters 模块允许从 parent system 发射的粒子的位置上的 child emitters 再次发射粒子。

这个模块在 parent system 的粒子的 birth、death、collision 等事件触发 child particle emission。

PS 的 child PS 可以是普通的 PS，和 Parent PS 一起 Play 或 Stop，还可以被设置为 SubEmitters。

每个 Emitter 使用一个 Child PS，指定一个 Event Type，以及一个可选的概率。当 Parent PS 的粒子发生相应的事件时，以一定概率触发 Child PS 的 Emission 运行（发射粒子）。

## 属性

- bool enabled
- int subEmittersCount

  Sub-Emitter 的总数。

## 方法

添加、移除、获取设置 SubEmitter。

一个 SubEmitter 包含 4 种属性：

- ParticleSystem subEmitter

  用于发射 child particle 的 PS。

- ParticleSystemSubEmitterType type

  触发 Child Emitter 发射的事件：

  - Birth：Parent PS 的粒子生成时
  - Collision
  - Death
  - Trigger
  - Manual：脚本中使用 ParticleSystem.TriggerSubEmitter 手动触发

- ParticleSystemSubEmitterProperties properties

  sub-emitter particles 从 parent particle 继承的属性：

  - InheritNothing
  - InheritEverything
  - InheritColor
  - InHeritSize
  - InheritRotation
  - InheritLifetime
  - InheritDuration

- float emitProbability

  触发 SubEmitter 发射粒子的概率（0-1）


