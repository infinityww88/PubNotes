Cinemachine Impulse 用于生成和管理响应游戏事件的摄像机震动效果。

例如，当某个游戏对象与另一个发生碰撞，或场景中的某个物体发生爆炸时，你可以使用 Impulse 让 CinemachineCamera 产生震动效果。

Impulse 有两个部分：

- Impulse Source

  一个在空间中某点发出信号并向外传播的组件，类似于声波或冲击波。这种 emission 由游戏中的事件触发。

  该信号由一个方向和一个描述信号强度随时间变化的曲线组成。这两者共同有效地定义了沿指定轴向、持续指定时间的震动效果。这种震动从原点向外传播，当它到达某个 Impulse Listener 所在的位置时，该监听器可以对其作出响应。

- Impulse Listener

  一个 Cinemachine 扩展组件，允许 CinemachineCamera “感知” 到一个震动信号，并通过震动来对此作出反应。

  从单个“脉冲”的角度来理解会很有帮助。一个脉冲指的是 Impulse Source 单次发出信号的事件。场景中的碰撞和事件会触发脉冲，Impulse Source 生成脉冲，而 Impulse Listener 则对这些脉冲作出反应。

要在场景中设置和使用 Impulse：

- 向一个或多个你想要触发 camera shake 的 GameObjects 添加 Cinemachine Impulse Source 或 Cinemachine Collision Impulse Source 组件
- 向一个或多个 CinemachineCameras 添加一个 CinemachineImpulse Listener 扩展，这样它们就可以检测并响应 impulses 了

