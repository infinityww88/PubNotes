# ParticleSystem

内置 Particle System 的脚本接口。Unity 强大通用的粒子系统实现。

通用参数保存在 Main Module 中。在脚本中可以通过 ParticleSystem.main 访问。

## 访问属性

粒子系统属性按照它们所属的模块被组织在一起，例如 ParticleSystem.noise 和 ParticleSystem.emission。这些属性是结构体，但是不像正常的 C# struct 一样。它们 native code 的脚本接口，因此对比正常 C# struct，知道如何使用它们非常重要。

关键差别就是不需要将 sruct 赋值回到 ParticleSystem 组件中。当设置一个 module struct 的任何属性时，Unity 立即将属性值赋值给 ParticleSystem。

另外，因为每个 module 是一个 struct，在将任何新值赋值给 module 之前，必须将 module 缓存到 local variable 中，例如：

```C#
ParticleSystem.emission.enabled = true; // 无法编译
```

而应该写成：

```C#
var emission = particleSystem.emission; // 存储 module 到 local variable 中
emission.enabled = true; // 将新值直接应用到 ParticleSystem 上
```

## Module effect multipliers（乘数因子）

每个模块有一些特殊的 multiplier 属性，允许你改变整个 curve 效果，而不需要编辑 curve 自身。这些 multiplier 属性的名字都是在它们影响的 curve 名后面加上 Multiplier。例如 ParticleSystem.emission.rateMultiplier 控制 ParticleSystem.emission.rate 的整体效果。

## Constant value shorthand

对于简单的 constant values，参数支持 shorthand notation。要为一个参数设置一个常量，只需要将数值赋值给它。在 ParticleSystemCurveMode.Constant mode 中，不需要创建 MinMaxCurve 或 MinMaxGradient 对象。例如

```C#
var emission = ParticleSystem.emission;
emission.rate = new ParticleSystem.MinMaxCurve(5.0f);
```

可以写成

```C#
var emission = ParticleSystem.emission;
emission.rate = 5.0f;
```

## 属性

Particle System modules 尽管是结构体，但不需要赋值回到 System 中。它们是 native code 的接口，而不是 C# managed code 中的独立 objects。

- collision

  CollisionModule 允许粒子和一个预定义的 planes 列表，或者 2D、3D physics worlds 碰撞。


- colorBySpeed

- colorOverLifetime

- customData

  CustomDataModule，一旦配置，这个模块将会产生 per-particle 数据，这些数据可以用在脚本或 shaders 中。要在脚本中读取数值，只需要调用 ParticleSystem.GetCustomParticleData。要在 shader 中读取，在 ParticleSystemRenderer 模块中开启 custom data streams，或者在脚本中调用 ParticleSystemRenderer.SetActiveVertexStreams。一旦开启，custom 数据将会通过一个 TEXCOORD channel 传递给 vertex shader。ParticleSystemRenderer Inspector 会告诉你使用的是哪个 channels。

  只支持两个 custom data：Custom1 和 Custom2。每个 data 只支持两种数据类型：Color 或 Vector4（都是四个分量的数据）。每个数据都支持 4 种模式：

  - Constant
  - Curve
  - Random Between Two Constants
  - Random Between Two Curves

  就像任何其他数据（startSize，startSpeed 等）一样，要么是常数，要么是随机数。它们的只是粒子系统生成的数据，具体行为要看脚本或 shader 如何解释它们，就像 size，color，speed 分别被相应模块处理一样。

- emission

  EmissionModule 提供了常见的控制发射粒子的方法。粒子系统的各个模块只是控制粒子在生命周期的行为，以及 lifetime 结束之后回收粒子。对于发射粒子，基本方法是通过 ParticleSystem 的 Emit 来发射指定数量的粒子，而何时发射发射多少，在根据需要在脚本中控制。但是 Unity 通过 EmissionModule 提供了对于常见的控制粒子发射的方法，包括随时间发射，随移动距离发射，按指定周期 burst。这些是最常见的控制粒子发射的方法，如果只需要这些，就无需编写脚本来 Emit 粒子了，而可以直接使用 EmissionModule 模块。如果 EmissionModule 不满足，则可以关闭这个模块，然后在脚本中显式控制粒子的发射。

  因此 EmissionModule 对于粒子系统的运行不是必须的，只是常用而已。

- externalForces

  ExternalForcesModule 开启 ParticleSystemForceField 和 WindZone 组件来影响 Particle System。它模拟粒子效果在力场中的效果。

- forceOverLifeTime

  对 particles 应用 forces。Forces 在每帧中应用到 particle 的 velocities。

- bool has3DParticleRotations

  确定 Particle System 是否只绕着 Z axis 旋转它的粒子，还是分别绕着 X Y Z axis 旋转粒子。

- bool hasNonUniformParticleSizes

  确定 PS 使用一个 value 缩放整个粒子，还是可以在 X Y Z 上分别缩放粒子。

- inheritVelocity

  基于生成粒子的 object 的速度应用速度到粒子上。对于绝大多数粒子系统，就是 GameObject 的速度，但是对于 sub-emitter，速度来自 sub-emitter 的 parent particle 的速度。

- isEmitting

  确定 Particle System 是否正在发射粒子。ParticleSystem 在 emission module 完成时，或PS 在被暂停时，或使用 StopEmitting flag 调用 Stop 停止后，将停止发射粒子。

  Play/Stop 只是开启和停止 emission 模块的运行，但是 emission 模块的完成不表示 PS 被停止了，它仍然正常运行，只是 emission 模块完成了它的 duration。因此正在运行的 PS 不一定正在发送粒子。isEmitting 可以判断粒子系统是否实实在在正在发送粒子。 

- isPlay/isPaused/isStopped

  分别对应调用 Play，Pause，Stop 之后的状态。注意正在运行的 PS 不一定正在发送粒子，例如 EmissionModule 已经完成或被 disable 了。

- lifetimeByEmitterSpeed

  基于每个粒子生成时 emitter 的速度，控制每个粒子的 initial lifetime。

- lights

  LightsModule 允许挂载 real-time Lights 到一定百分比的粒子上。这是一个简单和强大的模块，允许粒子向周围环境投射光线。Lights 可以从他们挂载的 particles 继承属性，例如 color 和 size。支持 Point 和 Spot Lights，以及 shadow casting 和 Light cookies。

- limitVelocityOverLifetime

  LimitVelocityOverLifetimeModule 通过应用 drag 或简单随时间减小速度（dampen）来降低 particle 的 velocity。

- main

  MainModule 提供通用设置的访问，显示在所有模块的上方。

- noise

  NoseModule 可以应用 urbulence（湍流）到粒子的运动上。还可以为每个 axis 独立地应用 Noise 行为。

- particleCount

  当前 alive 的粒子总数，不包括 child particle systems。

- uint randomSeed

  相同的 randomSeed 可以达到确定性效果。

- rotationOverLifetime

  随 lifetime 旋转 particles。

- shape

  配置 particles 的初始位置和方向。

- sizeBySpeed

  基于粒子的速度控制 size。

- sizeOverLifetime

  随粒子的 lifetime 控制 size。

- subEmitters

  SubEmittersModule。child particle system 粒子的发射被连接到 parent particle system 的粒子的 birth，death，和 collision 事件上。

  Parent PS 发射的粒子在特定事件时触发 child PS 发射粒子。

- textureSheetAnimation

  TextureSheetAnimationModule 允许添加动画到 particle textures 上。这通过小人书 textures 实现。textures 包含大小相同的动画帧 sprite。

- float time

  Plackback position（seconds）。读取当前 current playback time 或 seek 一个新的 playback time。对一个 loop system，这个 value 在 duration 中 wraps。对于指定了 StartDelay 的 system，获取的 time 忽略了 delay。

- float totalTime

  读取当前 playback time。对于 loop system，返回值不会在 duration 中 wrapped，并包含 start delay。

- trails

  TrailModule 添加 trails 到 particles。

- trigger

  TriggerModule 可以用于在粒子接触一组 collision shapes 时 kill particles，或者调用一个脚本命令来应用特定的粒子行为。

- velocityOverLifetime

  随粒子的 lifetime 设置粒子的 velocity。

## 方法

- void Clear()/Clear(bool withChildren=true)

  移除粒子系统的所有粒子。这个方法还移除任何 linked 的 sub-emitters 的粒子，但不包括没有 linked 的普通 child PS 的粒子。使用 withChildren 参数可以移除非 linked 的 child PS 的粒子。

  粒子系统的 child particle system 有两种：

  - 正常独立的粒子系统，独立的发射，只是挂载到 parent particle system。
  - 连接到 parent particle 的 child ps，它们在 parent particle 的特定事件发生时发射粒子。

- void Emit(int count)/Emit(ParticleSystem.EmitParams emitParams, int count)

  立即发射指定数量的粒子，还可以用 emitParams 覆盖生成的粒子上面的属性。

- int GetCustomParticleData(List<Vector4> customData, ParticleSystemCustomData streamIndex)

  ParticleSystemCustomData: Custom1 Custom2。指定 custom particle data 设置到哪个 stream 上。

  返回 per-particle data 到 customData 中。

- int GetParticles(out Particle[] particles)

  获取 ParticleSystem 当前 alive 的粒子。只要 particles 参数数组是预分配好的，这个方法就是免 allocation 的
  。

  这个方法只获取调用时 PS 的当前 alive 的粒子。

- bool IsAlive() / IsAlive(bool withChildren=true)

  如果 PS 包含 live particles 或它仍然在创建新的 particles，返回 true。如果 PS 已经停止发射粒子，并且所有粒子都已经 dead，返回 false。
  
  withChildren = true 还同时检测 child PS。

- Pause(bool withChildren=true) / Play(bool withChildren=true) / Stop(bool withChildren=true)

- void SetCustomParticleData(List<Vector4> customData, ParticleSystemCustomData streamIndex)

  为每个粒子设置 custom data。

  CustomParticleData 和粒子发射一样，它们不需要通过模块执行，可以通过脚本完成，模块只是提供简洁方式。因此如果开启了 Custom Data module，它也会写入数据到 particle data buffer。因此如果想要写入自己的 custom data，需要关闭 Custom Data module。

  但是如果想要修改 Custom Data module 生成的 data：

  1. 使用 ParticleSystem.GetCustomParticleData 来获取 particle data
  2. 修改 particle data
  3. 使用 SetCustomParticleData 来应用修改后的 particle data 到 Custom Data module 中

- void SetParticles(out Particle[] particles)

  显式设置粒子到粒子系统中。将粒子系统想象为一个 objects pool。

- void Simulate(float t, bool withChildren = true, bool restart = true, bool fixedTimeStep = true)

  以给定时间 t 向前模拟 ParticleSystem，然后暂停它。

  参数：

  - t：向前模拟的时间 t。如果 restart 为 true，PS 会重置到 time=0，然后向前模拟这个时间。如果 restart 为 false，PS 从当前时间向前模拟 t
  - withChildren：同时向前模拟 child ParticleSystem
  - 本次 Simulate：是否将 PS 重置到 time=0
  - fixedTimeStep：只以 Time 设置中的 Fixed Time 指定的步长更新整数个 fixed intervals

- void TriggerSubEmitter(int subEmitterIndex)

  对这个 ParticleSystem 的所有粒子触发指定的 sub emitter。

