# Particle

## 属性

- float angularVelocity

  粒子的 2d 角速度，度/秒

- Vector3 angularVelocity3D

  粒子的 3d 角速度（每个轴），度/秒

- Vector3 animateVelocity

  粒子的动画速度。

  可以 animated effects 的不基于物理的 velocity，而是基于随时间变化的速度。

  Noise 和 VelocityOverLifetime 模块使用这种类型的 velocity。这些模块不在 frames 之间存储速度，因为它们每帧通过计算（Noise 公式）或采样（AnimationCurve）得到一个速度。这个属性就反映这个例子在这一帧的速度。

- Vector3 axisOfRotation

  Mesh 粒子的旋转轴，粒子绕着这个周旋转。

  Mesh particles 绕着为每个 particle 设置的 axis travel。

- Vector3 position

  particle 的位置。position 是相对于 simulation space 定义的（world space 或 local space）。可以使用 Transform.TransformPoint 和 Transform.InverseTransformPoint 在 local 和 world 之间转换 points。

- uint randomSeed

  particle 的 random seed。每个粒子有它自己的 seed，以在 simulation 期间产生确定性的结果。

- float remainingLifetime

  粒子的剩余 lifetime。

- float rotation

  粒子的 2D 旋转角度（单位是度）。

  默认粒子是 2D 的，只在这个平面上旋转。这个平面通过 ParticleSystemRenderer 的 alignment 控制，包括：

  - View
  - World
  - Local
  - Facing
  - Velocity

  只有开启 3D rotation 后，粒子才忽略 alignment，而是在 world 中任意旋转。

- Vector3 rotation3D

  粒子的 3D 旋转，欧拉角。

- Color32 startColor

  粒子的初始颜色。粒子的当前颜色基于这个值和 active color modules 计算出来。颜色 alpha channel 用于 fade out particles。

- float startLifeTime

  粒子的初始 lifetime（seconds）。粒子系统在生成粒子的时候设置这个 value。

  粒子系统有点类似 ECS 系统（这也是粒子系统可以高效地管理大量粒子的原因）。粒子本身只保存数据，它的行为都被 ParticleSystem 控制。因此如果想控制粒子，只需要改变粒子上的属性，剩下的交给 ParticleSystem。例如将粒子的 lifeTime 设置为 0，粒子系统就会销毁这个粒子。

- float startSize

  粒子的初始大小。粒子的当前大小基于这个值和 active size modules 计算出来。单位是 world space 的单位 meters。

- Vector3 startSize3D

  粒子的 3D size。

- Vector3 totalVelocity

  粒子的整体速度。

  它等于 ParticleSystem.Particle.velocity 和 ParticleSystem.Particle.animatedVelocity 的和。

  因为一些模块使用 physics-based 的 velocity，另一些模块使用 animated velocity。使用这个属性可以不管哪些模块使用的哪些 velocity，总能得到粒子的当前整体速度。

- Vector3 velocity

  基于物理的 effects 使用的速度，meters/second。使用这个类型的速度的模块包括 Force module，Gravity，和 StartSpeed 等。粒子系统在 frames 之间存储 velocity，并在每个 simulation step 中将它应用到粒子的 position 上（乘以时间差 deltaTime）。

  velocity 还被 ParticleSystemRender 模块使用，如果后者的 Render Mode 设置为 ParticleSystemRenderMode.Stretch。

## 方法

- Color32 GetCurrentColor(ParticleSystem system)

  通过应用 system 的相关 curves 到粒子的 startColor 来计算粒子的当前颜色。

- float GetCurrentSize(ParticleSystem system)/GetCurrentSize3D

  参见 GetCurrentColor

- int GetMeshIndex(ParticleSystem system)

  返回用于渲染粒子的 mesh index。

  计算粒子的 Mesh index，用于选择粒子渲染哪个 Mesh。

- void SetMeshIndex(int index)

  显式设置一个例子的 Mesh Index。


