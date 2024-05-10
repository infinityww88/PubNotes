# MainModule

ParticleSystem 的一般通用属性：

- ParticleSystemCullingMode cullingMode

  Particle offscreen 时是否继续模拟。

- Transform customSimulationSpace

  相对于自定义 transform 组件模拟粒子。

- float duration

  Play 之后 EmissionModule 的运行（发射粒子）时间，duration 结束之后，EmissionModule 不再发射粒子。但这只是停止了 EmissionModule 的运行，粒子本身被 ParticleSystem 管理，粒子的生命周期和 EmissionModule 的运行时间 duration 是无关的。

  只能在 PS 没有 play 的时候设置这个属性。

- Vector3 emitterVelocity

  当前 particle system 的 velocity。如果设置这个属性为特定 value，emitterVelocityMode 自动切换为 Custom。这个值可以用于 EmissionModule 的 Emit by Distance 方法。

- ParticleSystemEmitterVelocityMode emitterVelocityMode

  当 ParticleSystem 在 world 中移动时，控制 ParticleSystem 如何计算它的 velocity。

  - Transform：基于 frames 之间 Transform 的变化计算 velocity
  - Rigidbody：使用 Rigidbody/Rigidbody2D 的 velocity
  - Custom：直接使用 emitterVelocity 

- float flipRotation

  使一部分 particles 按照原来设置相反的方向旋转（2D 就直接翻转旋转速度，3D 按每个轴翻转旋转速度）。0-1 之间的百分比。

  它基本就是 PS 各个处理 Rotation 的模块的上面整体将效果乘以 -1，即先正常模拟 Rotation，然后将结果乘以 -1。StartRotation 乘以 -1，RotationByLifetime 乘以 -1。

- MaxMinCurve gravityModifier / float Multiplier

  逐粒子缩放 Physics.gravity 或 Physics2D.gravity，应用到粒子的重力。

- ParticleSystemGravitySource gravitySource

  指示使用哪个重力设置：Physics3D Physics2D。

- bool loop

  Particle System 在 duration 之后是否循环运行（循环 EmissionModule）。

- int maxParticles

  发射的最大粒子数。

- bool playOnAwake

  ParticleSystem 在 awake 时自动播放。Child Particle System 共享 Parent PS 的这个设置。

- bool prewarm

  如果 loop 为 true，当开启这个属性时，PS 开始之前看起来就好像它已经模拟了一个 loop。

- ParticleSystemScalingMode scalingMode

  控制 Particle System 如何应用它的 Transform 组件到它发射的 particles 上。

  - Hierarchy：根据 PS 的 Transform 和它的所有 parents 的 Transform 缩放 particles
  - Local：只使用 PS 自己的 Transform 缩放粒子，忽略它的 parents
  - Shape：只应用 Transform scale 到 shape 组件，当不影响 particles 的 size 和运动。Shape 组件控制 Particles 在哪里生成

- ParticleSystemSimulationSpace simulationSpace

  粒子模拟的坐标空间：

  - world：粒子生成后独立 PS 运动
  - Local：粒子生成在 PS 的坐标空间运动（随 PS 一起平移、旋转）

- float simulationSpeed

  覆盖 Particle System 的默认 playback speed，用于加速或减慢整个模拟的速度，就像视频的加速、减速播放。

生成粒子的各种初始化属性（startXXX）：

- Color
- Delay/Multiplier
- Lifetime/Multiplier
- Rotation/3D/X/Y/Z/Multiplier
- Size/3D/X/Y/Z/Multiplier
- Speed/Multiplier


粒子的属性只有 Color、Lifetime、Rotation、Size、Speed（Velocity） 5 种。ParticleSystemSubEmitterProperties 也是列出 SubEmitter 粒子只能继承 Parent Particle 的 Color、Size、Rotation、Lifetime、Duration 这几个属性。


- ParticleSystemStopAction stopAction

  指示粒子系统 stop 并且所有粒子都 died 后，是否 Disable 或 Destory GameObject，还是调用 MonoBehaviour.OnParticleSystemStopped。

  - None
  - Disable
  - Destroy
  - Callback

- bool useUnscaledTime

  使用 unscaled 还是 scaled 的 deltaTime 来模拟 PS。

