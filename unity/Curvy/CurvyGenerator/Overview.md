# Curvy Generator

Generator是一个独立的体系，绑定在Curvy上，因为它使用spline作为输入。这只是通常情况，日后可能将它扩展到更多的功能

除非显式说明，CurvyGenerator将所有输入输出当作局部于CurvyGenerator GameObject

## Preface

简短来说，Curvy Generator使用一些输入（例如spline data），处理它，吐出结果。一些默认的使用场景包括：

- 沿着一条曲线推挤一个形状来创建一个mesh（volume）
- 沿着path或volume克隆其他geometry
- 通用path操作（混合mix，transform，scale，rotate，etc...)
- 更多

通过一个graph tree中热插拔模块是管理复制设置的流行方式，被大量软件工具诸如Substance Designer或Shader Tree所使用。Curvy Generator也是如此

## 关键概念

- 模块可以通过使用slots被连接起来，每个slot使用特定的数据类型
- 数据类型可以被子类型化，例如Path继承于Shape，因此你可以将一个Path插入一个Shape slot
- 智能缓冲：如果一个模块的输入没有改变，它返回缓冲的输出而不是重新计算
