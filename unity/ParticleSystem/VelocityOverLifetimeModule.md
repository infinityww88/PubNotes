Main 模块的 Start Speed 是一个标量值，表示速度的值。速度的方向由 Shape 模块发射粒子时确定。

Start Speed 设置为 curve 时，curve 的横坐标是 (0, 1) 之间的值，纵坐标表示速度的标量值。当每个粒子生成时，生成一个 0-1 之间的数值，然后在 curve 上采样，得到数值作为速度值。Curve 模式用来实现粒子速度的分布控制。例如 (0, 0.1) 占据 (0, 1) 的 10%，当把 (0, 0.1) 的 curve 值设置为 5，就可以保证粒子有 10% 的概率 start speed = 5。

Linear XYZ 设置粒子的附加速度。当开启 VelocityOverLifeTimeModule 模块时，StartSpeed = StartSpeed + LinearXYZ，即每次计算粒子的速度时，Main 模块的 Start Speed + 这个模块的 Linear XYZ 才是粒子真正的初始速度，后面再叠加下面的其他速度控制。

每次计算时，粒子的最终速度 = StartSpeed + LinearXYZ + Orbital + Radial。

- StartSpeed 在粒子首次生成时固定或随机或采样确定，一旦粒子生成，之后就是固定的
- LinearXYZ、Orbital、Radial 每次粒子更新速度时，都重新到模块中获取一次，如果其值是固定的，就使用固定数值。如果是 Random 的，每次更新就取一个随机值。如果是 Curve 的，Curve 横坐标表示的是 LifeTime，按照粒子当前的 LifeTime 在 Curve 上取本次的 Speed

Space 指示 Linear XYZ 是在 Local 还是 World 空间指定的。

Orbital XYZ 表示粒子绕着 XYZ 轴的切线速度（角速度），用来控制粒子绕原点的旋转。原点由 Offset XYZ 控制，默认就是粒子系统的 position，加 XYZ 产生偏移。

Orbital XYZ 的值的单位是弧度/秒，即每秒旋转的弧度。如果设置为 3.14，则粒子每秒绕原点（Offset XYZ）旋转一周。每个粒子在计算更新速度时，分别针对每个轴（X、Y、Z），根据

```线速度 = 角速度 x 半径```

得到 Orbital 对粒子施加的线性速度，即这个轴的角速度（Orbital XYZ）乘以这个粒子距离 Offset XYZ 的距离（半径），然后附加到 StartSpeed + Linear XYZ 上。

Offset XYZ + ParticleSystem Position 定义 Orbital 的原点，粒子到 Orbital 原点的距离也决定了 Orbital 线速度的大小，因为角速度是一定的。

Radial 是粒子接近或远离 Orbital 的径向速度（粒子位置到原点的方向），作为最后一个附加速度，添加到 StartSpeed + LinearXYZ + Orbital 之后，得到粒子的最终速度。

Speed Modifer 为粒子的最终速度乘以一个因子。因此粒子的最终速度为

```最终速度 = SpeedModifier x (StartSpeed + LinearXYZ + Orbital + Radial)```

