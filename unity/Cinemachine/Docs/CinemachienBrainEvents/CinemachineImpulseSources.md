Impulse Source 是一个从场景空间中的某个点发出振动信号的组件。游戏事件可以导致 Impulse Source 在事件发生的位置发出信号。事件触发脉冲，而源则生成脉冲。带有 Impulse Listener 扩展的 CinemachineCamera 会通过震动来响应这些脉冲。

在下图中，人物的脚部是 Impulse Source（脉冲源）。当它们与地面发生碰撞（A）时，会产生脉冲。摄像机是一个 Impulse Listener（脉冲监听器），它会通过震动（B）来响应这些脉冲，从而使得游戏视图中的画面产生抖动效果（C）。

![ImpulseOverview](../../Images/ImpulseOverview.png)

Cinemachine 自带两个类型的 Impulse Source components：

- Cinemachine Collision Impulse Source

  因响应 cllisions 和 trigger zone 而产生 Impulse。

- Cinemachine Impulse Source

  因响应非 collisions 的事件而产生 impulses。

场景中可以有多个 Impulse Sources，例如：

- 每个巨人的脚上有一个 Impulse Sources，这样每当它行走时，大地就会震动
- projectile 上有一个 Impulse Sources，这样当它碰撞到目标时就会爆照而产生震动
- 在一个凝胶状行星的表面，每当有物体触碰，它便会微微颤动

默认情况下， Impulse Source 会影响范围内的所有脉冲接收器，但你可以通过通道筛选功能，让特定源只对特定接收器产生作用。

# 关键 Impulse Source 属性

除了 vibration signal 定义了 camera shake 的基本形状，Impulse Source 还控制其他一些重要属性，其定义它产生的 impulses。

Source 有范围，有通道，有信号强度曲线。


