# Particle System

lifetime 控制粒子效果的剧烈程度。粒子的生存周期越短，emission 喷出粒子的视觉效果就越快，就越提供一种剧烈的感觉。例如火箭发动机尾焰的应该使用 lifetime 很短的粒子，而太阳日冕的效果则应使用 lifetime 很长的粒子。

duration 是粒子系统运行时间，粒子系统在这段时间发射粒子，即 emission 模块的工作时间。Looping 控制 duration 的循环，即发射模块循环工作。

粒子一旦发射（生成）后，由粒子的 lifetime 的控制，粒子的生存时间和 duration 无关。Emission 模块的工作时间 duration 和粒子的生存时间 lifetime 是相互独立的。

PlayOnAwake 控制的是粒子系统整体的是否工作，但是真正发射粒子的是 emission 模块。如果 PlayOnAwake = true，但是 emission 模块 disable，仍然不会发射粒子。

Sub Emitters 子粒子系统是父粒子系统发射的每个粒子在特定事件时触发一个子粒子系统的发射，事件包括：

- birth：粒子生产时触发子粒子系统
- collision：粒子碰撞到 collider 时触发子粒子系统
- trigger：粒子进入 trigger 时触发子粒子系统
- death：粒子生存周期结束时触发子粒子系统
- Manual：脚本控制触发子粒子系统

没有方法同时控制 gameobject Hierarchy 的多个粒子系统，只能逐个控制。

Shape 模块控制发射粒子的空间区域（2d，3d）。粒子只会在区域内随机生成。关闭 shape 模块，则每个粒子都从粒子系统的位置生成（位置相同）。

Emission burst 模块控制按周期发射一组粒子，就像蒸汽火车的蒸汽效果。可以控制周期时长，burst 多少个循环，每次 burst 发射多少个粒子。

Trail 模块，就像 Trail renderer 一样，跟踪粒子运动轨迹，生成具有生命周期的 line mesh，并且可以为 line 指定 Material。

Renderer 模块则是渲染粒子本身。

粒子效果不一定需要全部粒子的外观，可能只需要一部分，例如日冕边缘。

粒子系统可以与物理引擎交互，每个粒子视为一个物理对象。交互包括：

- 与 collider 碰撞
- 与 trigger 碰撞
- 对外界施加力，和被外界施加力

  - Force over Lifetime：粒子对外部世界施加的力
  - External Forces：外部世界（Wind Zone）对粒子施加的力。

粒子外观模块主要控制：生成时间、颜色、速度、旋转、大小、纹理这些属性。一些属性可以依赖另一些属性：

- Velocity over lifetime
- Limit Velocity over lifetime
- Lifetime by Emitter Speed
- Force over Lifetime
- Color over Lifetime
- Size over Lifetime
- Size by Speed
- Rotation by Speed


Inherit Velocity 将粒子系统速度加到粒子本身上。如果粒子系统运动，这可以产生更正确的 world space 粒子效果。

线性运行和旋转运动可以分别沿着 x y z 轴控制，可以同时施加线性运动和旋转运动，产生涡旋效果。

noise 可以为线性运动、旋转运动、粒子大型添加随机扰乱。

## 总结

- 粒子发射
  - 发射模块工作时间 duration
  - 粒子生存时间
  - 粒子触发子粒子系统发射
- 发射形状
  - 指定区域内随机生成粒子
  - 不指定区域，总是在相同位置生成粒子
- 粒子外观：
  - 颜色
  - 大小
  - 线性运动（x，y，z）
  - 旋转运动（x，y，z）
  - 生存时间和生成速度
  - 纹理
  - trail
  - 噪声
- 物理交互
  - 粒子碰撞 Collider
  - 粒子碰撞 Trigger
  - 粒子对外界施加力
  - 外界对粒子施加力
  - 重力常数
  - 速度继承
- 属性之间的相互依赖
  - 对 speed 的依赖
  - 对 lifetime 的依赖
