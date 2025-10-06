Impulse Source 是一个从场景空间中的某个点发出振动信号的组件。游戏事件可以导致 Impulse Source 在事件发生的位置发出信号。事件触发脉冲，而源则生成脉冲。带有 Impulse Listener 扩展的 CinemachineCamera 会通过震动来响应这些脉冲。

在下图中，人物的脚部是 Impulse Source（脉冲源）。当它们与地面发生碰撞（A）时，会产生脉冲。摄像机是一个 Impulse Listener（脉冲监听器），它会通过震动（B）来响应这些脉冲，从而使得游戏视图中的画面产生抖动效果（C）。

![ImpulseOverview](../../../Images/ImpulseOverview.png)

Cinemachine 自带两个类型的 Impulse Source components。
