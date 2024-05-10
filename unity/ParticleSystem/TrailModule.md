# TrailModule

添加 trails 到粒子上。可以让 trails 随着粒子的移动而产生，或者将粒子系统中每个 particle 连接起来。

Trail 有两种模式：

- 一种是真的 Trails，跟着粒子移动产生
- 一种是跟 LinearRenderer 一样，在粒子之间生成一个 Line 随粒子运动，直到粒子被销毁 

## 属性

- int ribbonCount

  将 alive 的粒子按照生成的先后顺序以 Nth 的方式分为 ribbonCount 个 group，然后对每个 group，按照粒子从最新到最久的顺序依次创建 LinearRenderer 将它们连接起来，group 之间没有连接。 

  如果 ribbonCount = 2，则 0-2-4-6-8 这些粒子为一组，使用 Line 串连起来，1-3-5-7-9 这些粒子为一组，使用 Line 串连起来。

  如果 ribbonCount = 3，则 0-3-6-9 为一组，1-4-7-10 为一组，2-5-8-11 为一组。

  依次类推。

  如果 ribbonCount = 1，则只有一个 group，所有粒子按照从最新到最久的顺序连成一条折线。

- bool attachRibbonsToTransform

  默认每个 ribbon group 只在粒子之间创建 line。开启这个选项，可以将每个 group 的最新粒子和 PS Transform 之间也创建一个 line。效果就是从 PS 的 transform 向外发出 ribbonCount 个彩带。

- bool dieWithParticles

  trails 是否在它们所属的 particle 销毁时立即消失。否则，每个 trails 将保持到 trails 上的所有 points 完全过期后才销毁。


