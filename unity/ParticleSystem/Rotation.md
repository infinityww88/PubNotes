Start Rotation 和 Rotation Over Lifetime 的旋转，两者本质上都是“作用在粒子自身局部空间”的旋转，但它们的“参考方向来源”不同。

## Start Rotation（初始旋转）

作用时机：粒子生成瞬间

作用对象：粒子自身

参考系：相对于粒子系统的初始朝向（发射时的方向）

可以理解为：粒子一出生，就带着一个“初始角度偏移”

举例：

粒子默认面向 +Z（或 Billboard 朝向摄像机），Start Rotation = 90° → 粒子一生成就“转了90°”。

## Rotation Over Lifetime（生命周期旋转）

作用时机：粒子整个生命周期持续变化
作用对象：粒子自身
参考系：基于粒子当前自身旋转继续叠加

可以理解为：在 Start Rotation 的基础上，每一帧继续“自转”

- ❌ 不是相对于世界坐标
- ❌ 不是相对于粒子系统 Transform 持续变化
- ❌ 不会自动跟随系统旋转变化（除非 Simulation Space 设置）

可以把粒子当成一个小物体：

- Start Rotation → 出生时“摆好角度”
- Rotation Over Lifetime → 在空中持续“自转”

多人会误以为，Rotation Over Lifetime 是“绕粒子系统旋转”

其实不是，它是：绕粒子自身中心旋转（自转），不是公转。

Rotation Over Lifetime 的旋转是在“粒子自身坐标系”上进行的（自转），不是在粒子系统坐标系下定义的公转。

- 旋转轴：粒子自身的轴（local axes）
- 旋转中心：粒子自身中心
- 旋转方式：类似一个小物体在原地转

数值本身（X/Y/Z 角度）是基于粒子“当前局部坐标轴”定义的。

- X → 绕粒子自己的 X 轴转
- Y → 绕粒子自己的 Y 轴转
- Z → 绕粒子自己的 Z 轴转

这个“粒子自己的轴”来源于：

- 初始方向（发射方向 / Billboard 对齐方式）
- Start Rotation
- Renderer 的 Alignment 设置

如果用 Mesh + 固定朝向，你会明显看到：Rotation Over Lifetime 就是标准“自转”。

Rotation Over Lifetime 不会直接使用粒子系统坐标系。

## 总结

粒子的最终旋转 = Start Rotation(3D Start Rotation) + Rotation Over Lifetime

Rotation OverLifetime 总是相对于粒子自身解释的，不是 Particle System Local 也不是 World。

但是 Start Rotation 则会依赖 Simulation Space 和 Render Alignment。

Shape 模块本身之影响粒子的位置，不影响粒子的旋转。在它眼里，粒子只是一个点而已，它会按照选择的 Shape 在空间中选择几个点，然后将生成的粒子放在这几个点上。但是方向都是一致的。真正影响粒子方向的首先就是 Render Alignment（View、Local、World、Velocity），它们先将粒子旋转到相应的约束（里面面对摄像机、Local Rotation Identity、World Rotation Identity、或面向速度方向），此时粒子就有了初始的朝向，后面的所有 Rotation 都是基于粒子自身坐标系的旋转。接着在这个基础上应用 Start Rotation，Start Rotation 就是基于粒子自身坐标系定义的，尽管当 Render Alignment = Local、Simulation Space = Local 时，粒子自身坐标系的方向和 Particle System 的坐标系方向相同，看起来像是基于粒子系统坐标系坐标轴的旋转，但实际上是相对于粒子自身的。然后就是 Rotation Over Lifetime，这个也是基于粒子自身坐标系的（ Rotation(Space.self) ）。

而且 Start Rotation、Rotation OverLifetime 是每一帧都从计算的。对于 Local、World 这样的 Render Alignment，这看起来没有必要，因为它是固定的，但是对于 View（面向摄像机、Velocity）这样的 Render Alignment，每一帧都需要从新开始计算 Start Rotation，因为每一帧都是不同的。Rotation Over Lifetime 则总是每帧更新。

总之，Start Rotation、Rotation Overlife Time 是让粒子沿着自身坐标轴旋转（翻滚）。对于复杂的粒子系统来说，确定每个粒子的自身坐标系几乎不可能，也不需要。只需要知道，它们只是让粒子自身翻滚而已。对于 Rotation Over Lifetime，如果只设置一个轴的旋转，就会看到每个粒子都在绕自己的一个轴在旋转，尽管每个粒子轴向都是不同的，但是它们只在绕自己的一个轴旋转。

## 速度模块 vs 旋转模块

旋转是粒子自身的旋转翻滚，绕自身的坐标轴。而速度模块，将粒子作为一个点，它只修改粒子的位置，不考虑粒子的旋转。因此速度模块的值都是相对于粒子系统的坐标系或世界坐标系的。例如下面的示例，每个粒子都绕自身快速旋转（Rotation Over Lifetime），但是它们的位移运动确实绕着粒子系统的 Y 轴。

![](Image/VelocityVsRotation.gif)
