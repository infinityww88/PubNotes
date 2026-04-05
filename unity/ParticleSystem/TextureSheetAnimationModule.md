Unity 粒子系统里的 Texture Sheet Animation（纹理序列动画）模块，本质就是：

让一个粒子在生命周期内播放“精灵表动画”（Sprite Sheet）

常用于：

🔥 火焰动画
💥 爆炸
☁️ 烟雾
⚡ 能量效果

默认粒子只显示一个静态图像，依靠众多粒子共同模拟整体的粒子效果。但是这个模块还可以进一步让每个粒子播放精灵动画，随时间显示不同的图像，进一步增加粒子效果。

相当于每个粒子都是 SpriteRenderer，然后随时间播放一个 Sprite 动画。

## 核心原理

你准备一张图，比如：

4 x 4 的网格（共16帧）

Texture Sheet Animation 做的事情是：在粒子生命周期中按顺序切换这16个小格子，就像播放帧动画一样。

## 用法

- 准备贴图

  要求：一张 Sprite Sheet（序列帧图），每一帧大小一致。例如：16 帧爆炸动画。

- 材质设置

  Particle System 使用的材质：Shader：Particles/Standard Unlit。必须支持透明（否则效果不对）。

- 开启模块

  Particle System → Texture Sheet Animation → 勾选 Enable

## 关键参数

### Tiles（切分网络）

Tiles X = 4 Tiles Y = 4 表示：4列 × 4行 = 16帧

### Animation（动画模式）

- Whole Sheet（常用）：播放整张图片动画

- Single Row：只播放某一行（用于随机动画）。可以配合：Random Row（随机选一行），每个粒子可以在多个 Row 中随机选择一行的精灵动画。这样可以在一张图里放多种爆炸

### Frame over Time（最重要）

控制粒子在生命周期内播放到第几帧

范围：0 → 1

不是帧数，是比例！

举例：

如果你有 16 帧：

- 0 → 第0帧：只播放静态第一帧
- 0.5 → 第8帧：播放一半
- 1 → 第15帧：播放全部

常见设置：

- 正常播放动画：0 → 1（线性）

  从第一帧播放到最后一帧

- 停留最后一帧（爆炸残留）

  曲线：0 → 1 → 1 → 1，后面不再变化

- 倒放动画 1 → 0，从最后一帧往前播放

### Start Frame（起始帧）

控制粒子从哪一帧开始：

- 固定值：所有粒子同步
- Random：每个粒子随机帧

用于：打破同步感

### Cycles（循环次数）

粒子生命周期内播放几遍动画。

### Frame over Time（FPS 模式）

Time Mode = FPS，按指定帧率播放动画。

Affected UV Channels，一般默认 UV0.


