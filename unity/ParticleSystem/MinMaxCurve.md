# MinMaxCurve_MinMaxGradient

Min-Max Curve 是粒子 float 属性的数据类型。它定义如何为属性生成 float 数据。所有的 float 属性都是这个类型。

粒子系统中粒子自身的特有数据基本都是用这种方法

它描述如何基于 ParticleSystem.MinMaxCurve.mode 在一个 min 和 max limit 之间返回一个 value。可能是一个常量，也可能是一个随机值。

ParticleSystemCurveMode:

- Constant：总是返回一个常数值
- Curve：使用一个 time 参数在 curve 上求值
- TwoCurves：在两个常数值之间求一个随机数
- TwoConstants：使用一个 time 在两个 curve 上分别求值，然后再两个结果之间求一个随机数 

属性：

- float constant
- float constantMin/constantMax
- AnimationCurve curve
- AnimationCurve curveMin/curveMax
- float curveMultiplier：应用到 curve 的整体缩放
- ParticleSystemCurveMode mode

方法：

- float Evalute(float time)/Evaluate(float time, float lerpFactor)

  time 是在一条 curve 上 Evaluate 的 normalized time。

  lerpFactor 是两个 curve Evalute 的值再次进行 blend（lerp）的因子。

  自动对 time 和 lerpFactor 在 0-1 之间 clamp。


MinMaxGradient 与 MinMaxCurve 一样，只是生成的数据类型不是 float，而是 color。

这两个类型不仅可以用在粒子系统中，如果程序需要相似的功能，也可以使用它们，就像 AnimationCurve。

MinMaxXXX 求值都是调用 Evalute，其内部会根据 mode 判断用哪种方式得到结果。但总是需要传递一个 time，它只对 Curve 模式有意义，Constant 模式会忽略这个参数。

如果传递 time 则是使用 MinMaxXXX 的 code 的工作。例如粒子系统的模块可以以粒子的剩余生命周期占比作为 time 参数在 MinMaxXXX 上求值。

