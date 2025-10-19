IK（无论是 Unity built-in IK，还是 FinalIK），Unity Constraint，Animation Rigging 都是约束。

层叠约束在游戏中是非常常见的技术。一个效果是由多个约束子系统综合而成的。这些约束按照层叠顺序先后求值。每个约束独立地求值，它不知道其他约束地存在，因此一个后面的约束可能导致结果违反前面的约束。但是这种层叠约束不保证最终结果满足所有约束，而是尽可能满足所有约束。最终结果依稀可见每个约束发挥作用的痕迹。

正因为层叠约束中每个都是独立的，因此它们可以以任意组合联合使用。在内部就是一个约束的输出作为下一个约束的输入而已。所以 FinalIK 可以在一个 character 上应用多个 IK 组件，多个 Animation Rigging，多个物理引擎 joint 约束，以及自定义脚本执行的约束，这些约束可以任意组合，最终结果依赖于它们执行的顺序。

约束是瞬时计算的函数，而不是像动画系统中的 State。状态是持久的，随着时间流逝一直存在的，知道状态发生变化。因此状态是和时间联系在一起的，这就是为什么动画片段在运行时称为 State 的原因。因为任何时候 character 都处于一个动画状态（最通常的就是 idle），这个状态随着时间持续，直到状态被改变。在状态持续过程中，始终不断地输出当前动画数据。对于 AnimationClip 生成的最简单的 AnimationState，就是简单地随时间在 AnimationClip 文件中采样数据（对关键帧插值）而已。

而约束与时间无关，约束是瞬间应用的。约束就像是一个没有状态，只有输入和输出的函数，而状态有随着时间持久的数据。他们之间的区别就像函数式程序和面向对象程序的区别。约束瞬间将系统状态值约束到有效范围内，但是可以有一个权重，控制约束的程度。基于约束达成的平滑效果，都是有动画系统在 animate 权重值，甚至 target value。只要说到平滑变化就是动画相关的事情了。

Animations store the names of each of the objects in the Hierarchy that they animate so that they can figure out what to control when they are played, but if an object is renamed then the animation will no longer have the correct name so it won't control that object anymore. 

动画片段记录它使用的骨骼的名字，以及每个骨骼的关键帧数据，仅此而已。AnimationClip 和使用它的模型是隔离的，它们是在运行时绑定的。当将一个 AnimationClip 应用到一个模型上时，Unity 必须知道 Clip 中活动的一个 bone 对应模型的那个 bone。对于 Generic 动画，就是简单地使用名字查找对应的 bone。Clip 文件中 bone 的数据输出给模型中的同名 bone，不管 hierarchy 结构是否对的上。而对于 Humanoid 动画，可以使用 Avatar Retargeting 技术应用到不同模型的骨骼上，因为不同的人物模型具有相同的 avatar 结构，或者可以认为 avatar 为每个相应部分的 bone 定义了一个统一的别名 alias，然后就可以像 Generic 动画一样通过名字来映射 bone 了。

Animancer 就是一个 Playable Graph 的管理器，使用 State 管理 Node，并提供事件功能。Layer 和 Mixer 都是 sub-tree，动画片段是基本的 state。

示例实践是最好的学习方法，play around 各种细节，观察结果，建立联系，多么难的技术都可以学会，没有什么是学不会的。

