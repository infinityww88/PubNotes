Unity 粒子系统里的 Force over Lifetime（生命周期力）模块，可以理解为：在粒子“活着的整个过程中”，持续给它施加一个力（加速度）

它是做“粒子运动变化”的核心模块之一，比如：风吹效果、火焰上升、爆炸扩散（持续加速）、漩涡 / 扰动。

Force over Lifetime 本质是：

每一帧都给粒子加一个力 → 改变速度 → 改变运动轨迹

类似物理里的加速度（Acceleration）

力的方向是相对于粒子系统本身（Local Space）或世界空间（World Space）的，不是相对于粒子本身的。

XYZ 每个轴分别设置 Force 的大小，每个值都可以是：

- Constant（常量）
- Curve（随时间变化）
- Random Between Two Constants
- Random Between Two Curves

Space：Local（跟随粒子系统方向） or World（始终固定方向）

Randomize（随机化）：每个粒子受到不同的力，用于更自然的效果，避免整齐划一。只用于 Random Between Two Values 的模式。Random Between Two Values 是随机粒子的初始 force，Randomize 是每一帧都扰动一下这个 force。

因为它施加的是加速度，因此粒子速度会越来越快/慢，更接近真实的物理效果。而 Velocity over Lifetime 是直接修改粒子速度本身，没有加速过程。
