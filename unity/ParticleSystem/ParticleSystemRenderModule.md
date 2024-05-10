# ParticleSystemRenderer

和 TrailRenderer, LineRenderer, MeshRenderer, SkinMeshRenderer 一样，ParticleSystemRenderer 也是 Renderer 的子类，Renderer 的 material 就是应用到 Particle 的 material。以下属性是在 Renderer 基类基础上，新增的属性。

使用这个类渲染 Particle 到 screen 上。

## 属性

- ParticleSystemRenderSpace alignment

  控制 particle face 的方向。

  - View：Particles 总是面向 Camera Plane
  - World：Particles 总是面向 World -Z 方向 
  - Local：Particles 总是面向 PS Local -Z 方向
  - Facing：Particles 总是面对 eye 的位置（VR 中的 eves 相机位置）
  - Velocity：Particles 总是和它们运动的方向对齐

  对于很多应用程序而言，通常就是将 particle 总是面向 camera。

  unaligned particles 可以被设置为对齐到 world 或它们的 local transform 方向。

- bool allowRoll

  允许 billboard（总是面向 camera）particles 绕着它们自己的 z-axis 旋转。

- float flip

  和 MainModule 的 flipRotation 类似。沿着每个轴翻转一定百分比数量的 particles。

- bool freeformStretching

- float lengthScale

  particles 在它们运动方向上拉伸的程度，定义为 particle 的长度和宽度的比。
  
  这为不移动的 particles 定义一个 base length。value 1 表示 neutral，不拉伸或压缩。大于 1 的 value 使 particles 在运动时长度总是大于宽度。

- SpriteMaskInteraction maskInteraction

  控制 PS Renderer 如何与 SpriteMask 交互。

  SpriteMask 与 UI Mask 一样，只显示 Sprite 的一部分。

  默认 particels 不与 SpriteMask 交互，无论是否指定一个 SpriteMask，particle 总是可见的。这个选项可以使 ParticleSystemRenderer 只渲染 SpriteMask 的内部或外部（VisibleInsideMask/VisibleOutsideMask）。

- minParticleSize/maxParticleSize

  对 StartSize、SizeOverLifetime 等 Size 控制模块的最终结果进行 min-max clamp。

- mesh

  particle 使用 Mesh 渲染而不是一个 billboarded Texture。

- meshCount

  PS 用来渲染 particle 的 Meshes 的数量。

- ParticleSystemMeshDistribution meshDistribution

  指示 system 如何随机分配 meshes 给 particles。

  - UniformRandom：每个 mesh 都有相同的机会被选择
  - NonUniformRandom：为每个 mesh 分配一个权重，使得每个 mesh 有不同的被选择的概率

- float normalDirection

  指示如何计算 billboard 的 lighting。0 意味着 Unity 将 billboard 视作一个 sphere 来计算光照的 normal，1 则是将 billboard 当做一个 flat quad 来计算光照。

  value = 0 使 billboard 看起来像一个 sphere，billboard 中心的 normal 朝向 camera，从中心像四周开始像 sphere 一样偏移 normal。 

- Vector3 pivot

  修改旋转 particle 的 pivot point。解释为 particle size 的 multiplier。基础值是 particle 的中心，则 0 对应 particle 的中心，0.5 意味着将 pivot 修改到 particle 的边缘。

- renderMode

  PS 如何绘制粒子：

  - Billboard：将 particles 渲染为总是面向 active camera 的 billboard
  - Stretch：在运动方向上拉伸 particles
  - HorzontalBillboard
  - VerticalBillboard
  - Mesh
  - None

- bool rotateWithStretchDirection

  基于 particles 拉伸的方向渲染 particles。这添加到其他 particle rotation 的结果上。只在 freeformStretching 开启后有效。

- sortMode

  PS 如何排序 particles：

  - None：不排序
  - Distance：基于到 Camera position 的距离排序
  - OldestInFront：最久的 particles 渲染在最前面
  - YoungestInFront：最新的 particles 渲染在最前面
  - Depth：基于到 Camera Plane 的深度排序

- Material trailMaterial

  设置 TrailModule 使用的 Material。

- float velocityScale

  指示 particles 如何基于 velocity 拉伸。这个属性可以使 particle 随着 speed 增加而变长。

## 方法

BakeMesh。

各种 Renderer 都具有 BakeMesh 方法，LinearRenderer、TrailRenderer、ParticleSystemRenderer、SkinnedMeshRenderer 都有。它们将当前的 mesh 结果（particles 的 billboards，lines，trails，SkinnedMesh）的快照（mesh 数据，例如顶点、三角面、法向量、uv 等等）存储到一个 mesh 中。
