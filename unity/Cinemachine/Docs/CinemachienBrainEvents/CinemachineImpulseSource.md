使用 Cinemachine Impulse Source 组件可在非碰撞或碰撞器触发器事件中生成脉冲。

作为通用型脉冲源，该组件提供一系列 GenerateImpulse() API 方法，能够在指定位置按预设速度与强度生成脉冲。

既可直接在游戏逻辑中调用这些方法，也可将其与 UnityEvent 事件系统配合使用。

可以将此组件的脚本作为参考示例，用于创建自定义脉冲生成类。

选择想要触发 camera shake 的 GameObject，在 Inspector 中添加 Cinemachine Impulse Source 组件。

默认一个 Impulse Source 影响范围内的每个 Impulse Listener，但是你可以应用 channel filtering 让 Impulse Sources 只影响部分 Impulse Listeners，而不会影响另一些。

Impulse Channel，Impulse Type，Impulse Shape 等属性见 CinemachineCollisionImpulseSource。

# API

- void GenerateImpulse()

  在相应的 channels 上广播脉冲信号，使用 Inspector 上指定的默认速度，默认位置就是 transform 的 position。
  
- void GenerateImpulseWithVelocity(Vector3 velocity)

  在相应的 channels 上广播脉冲信号，使用一个自定义的冲击速度 impact 这个 source 的 transform 的 position。

- void GenerateImpulseWithForce(float force)

  在相应的 channels 上广播脉冲信号，使用一个自定义的冲击力，以及标准方向，和这个 source 的 transform position。

  force：impact 的 magnitude，1 为 normal。

- void GenerateImpulseAtPositionWithVelocity(Vector3 position, Vector3 velocity)

  - position：impulse 产生的世界空间的位置。
  - velocity：impact 的 magnitude 和 direction。

过时 API：

- void GenerateImpulse(Vector3 velocity)
- void GenerateImpulse(float force)
- void GenerateAt(Vector3 position, Vector3 velocity)





