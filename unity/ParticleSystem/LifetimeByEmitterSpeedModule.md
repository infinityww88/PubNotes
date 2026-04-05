Unity 粒子系统里的 Lifetime by Emitter Speed（根据发射器速度决定生命周期） 模块，属于一个“动态控制粒子寿命”的高级功能。

根据粒子系统 Particle System 的速度，决定粒子的生命周期。不是粒子本身的速度。

粒子 Lifetime = f(发射器当前速度)

Speed Range（速度范围）：Min ~ Max，发射器速度在哪个区间内会影响粒子。

例如 Speed Range: 0 ~ 10

- 0：静止
- 10：高速移动

Lifetime（最重要）：Lifetime Curve

- 输入：速度（0~1映射）
- 输出：粒子生命周期倍率

注意输出的不是秒数，而是粒子初始生命周期的倍数因子：

```最终 Lifetime = Start Lifetime × 曲线值```

场景：速度越快，寿命越短（常用）或 速度越快，寿命越长。

Clamp：超出 Min-Max 区间的速度，Clamp 到 Min 和 Max 的值。
