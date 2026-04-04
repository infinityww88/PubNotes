Unity 粒子系统中的 Inherit Velocity（继承速度）模块 用来让“新生成的粒子继承其发射源（Emitter / 父物体）的运动速度”，从而让粒子在视觉上更符合真实运动（例如尾迹、烟雾、火焰被甩动的效果）。

如果不使用 Inherit Velocity：

- 粒子只按自身 Start Speed 运动
- 发射器移动时，粒子不会“跟随惯性”
- 会出现“粒子像粘在世界空间”的感觉

启用 Inherit Velocity 后：

- 粒子会继承发射器的移动速度
- 发射器移动越快，粒子初速度越明显
- 常用于：
  - 子弹尾迹
  - 移动角色产生的尘土
  - 火焰拖尾
  - 爆炸随物体运动产生的偏移效果

## Mode

- Inital

  粒子只在生成的瞬间继承一次速度（添加到 Start Speed 上），之后无视发射源的速度。这是常用选项。

- Current

  - 粒子持续继承发射器当前速度

  - 发射器在运动时，粒子速度会动态变化

  - 更“物理”，但可能不稳定

## Multiplier

控制继承速度的强度。公式概念上类似：

```粒子初速度 += 发射器速度 × Multiplier```

举例：

- Multiplier = 0 → 不继承速度
- Multiplier = 1 → 完整继承
- Multiplier > 1 → 放大继承效果
- Multiplier < 1 → 弱化继承效果

## 工作原理

假设：发射器（GameObject）在移动，它的速度 = V

当粒子生成时：

```粒子初始速度 = Start Speed + (V × Multiplier)```

如果：

- 发射器静止 → 粒子正常发射
- 发射器快速移动 → 粒子会“带着惯性飞出”

## 典型使用场景

- 角色移动产生尘土

  角色向前跑，粒子系统挂在脚下，使用 Inherit Velocity 的效果：尘土会自然向后“拖”。

- 飞行物尾迹

  火箭 / 子弹 / 飞行器，粒子系统作为尾焰，效果：尾迹会被速度拉长，而不是固定在空间。

- 爆炸随物体运动

  爆炸发生在移动的载具上，粒子会继承载具速度，效果：爆炸不会“掉在原地”，而是跟随运动偏移。

## 与 Transform 运动的关系

Inherit Velocity 依赖的是：发射器在世界空间中的位移变化（ΔPosition / ΔTime）。粒子系统会时刻记录自己的移动速度。

- 移动 Transform → 有继承速度
- 不移动 → 速度为 0
- Rigidbody 运动 → 也会被计算进去（如果是通过 Transform 更新）

## 与 Simulation Space 的关系

Inherit Velocity 通常在 World Space 下更自然，Local Space 下，效果可能不明显或不符合预期，因为粒子时刻绑定在 Local Space，而 Particle System 可能在时刻运动。World Space 免除了额 Particle System 的移动的影响。
