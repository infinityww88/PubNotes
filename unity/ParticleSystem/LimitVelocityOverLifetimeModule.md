控制速度如何随生命周期衰减。

Speed：设置粒子的速度上限。Speed 可以设置为
  - Constant：生命周期保持为常量值
  - Curve：随生命周期的速度上限曲线，生命周期中不同时刻可以有不同的速度上限
  - Random Between Two Contants：粒子生成时，在这两个常量值之间随机一个数，作为生命周期中的固定速度上限，只在粒子生成时发生
  - Random Between Two Curves：粒子生成时，生成一个 0-1 之间的随机因子 r，在生命周期保持固定，然后在生命周期的每个时刻，采样相应的 CurveA(t) 和 CurveB(t) 的值，然后用这个固定的因子在两个值之间插值，因此最终的速度上限为 ```lerp(CurveA(t), CurveB(t), r)```
Dampen：当粒子速度超过上限时，减小速度，使速度降到上限的因子，控制粒子速度有多快降到速度上限
Separate Axes：默认是约束整个速度的大小，选中 Separate Axes 时，可以分别控制 XYZ 轴的速度大小，每个轴的因子都是 Dampen
Drag：Dampen 是速度超过上限时应用的衰减因子，Drag 是不管速度超没超过速度上限都应用的衰减因子，类似空气阻力，让速度逐渐慢下来

Dampen 做到不是简单的 ```v = v * 某个系数```，而是 ```v = lerp(当前速度, 上限速度, Dampen)```，而 Drag 更接近于 ```v = v * (1 - drag * dt)```，最终会减小到0.

想要“硬限速” Dampen = 1
想要“柔和限速” Dampen = 0.2 ~ 0.5
想要“空气感” 加 Drag
想要“爆炸后逐渐停” Drag + Curve


Multiply by Size：开启后，在 Drag 基础上，再乘以跟粒子大小相关的因子，使得更大的粒子被 drag 影响更多
Multiply by Velocity：开启后，在 Drag 基础上，再乘以跟粒子速度相关的因子，使得更快的粒子被 drag 影响更多
