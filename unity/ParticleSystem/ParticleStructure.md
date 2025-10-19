# ParticleStruture

粒子系统不是一种优化，尽管它内部是优化的C++实现
通过大量小的图形（sprite，mesh）的变换模拟非固态的可变化的事物，这种需求充斥游戏中的各个方面，而且具有统一的特征和过程，只是具体的参数不同而已，游戏将这些统一的特此和过程抽象为单一的系统——粒子系统，提供了各种配置其细节参数的接口，使得基于这个统一的系统可以模拟所有的可变事物，这才是粒子系统的本意

所有模块都是数据配置

ParticleSystem基于ECS实现，每个组件只是数据容器，ParticleSystem内部包含每个组件对应的System用来处理它包含的数据。数据组件就是就是操作粒子系统的接口，system作为隐藏在ParticleSystem内部

ParticleSystem唯一提供的手动操作粒子系统的方法是Emit

ParticleSystem的运行可以分为两个部分：发射模块 & 粒子管理器。这两部分是完全相互独立的。发射模块模块只管发射粒子，粒子发射之后就与它没有关系了，而是被粒子管理器管理，粒子管理器管理粒子的生命周期以及在声明周期中的变化。

Main模块中的Duration、Looping、StartDelay是配置发射模块的时间参数

Duration是发射模块工作时间长度，即它只在这段时间内发射粒子

    while (Time.time - particleSystem.startTime < Duration) {
        Emit(particles)
    }

Looping指定粒子系统是否在到达Duration之后重新开始允许，即以Duration为周期循环允许。Looping时，Duration作为周期影响Emission模块burst的定义。burst的定义总是在一个周期中的，当周期开始时burst也重新开始计算。但是对于Rate Over Time和Rate Over Distance，它们和周期无关，当粒子系统Looping时，可以视为无限运行，它们只需要关注流失的时间和移动过的距离就可以了。

Burst定义（Time，Count，Cycles，Interval，Probability）可以理解为：

    在每个周期Duration中，从Time时间点开始，以Interval为小周期，执行Cycles个burst，每个burst发射Count个粒子，每次burst发射的概率为Probability

StartDelay是整个粒子系统的初始启动延迟时间，一旦粒子系统启动，就会一直运行。在Looping时，每个Duration之间也不会有这个Delay。

粒子的发射模块和粒子管理模块完全是自主运行的，程序与粒子系统的交互界面就是包括Main模块在内的各种模块的配置。唯一例外就是粒子系统提供了手动发射粒子的函数Emit，允许程序不经过发射模块而直接发射粒子。无论自动还是手动方式发射的粒子都将被粒子管理模块管理。Emit函数允许程序在Emission模块提供的Rate Over Time、Rate Over Distance，Burst不满足需求时创建自定义的发射行为。

Main模块中的StartLifeTime与StartSpeed和StartRotation一样，是粒子的属性而不是粒子系统的属性，它定义粒子发射时的生命周期
