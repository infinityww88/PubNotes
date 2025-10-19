# Blending

Animations 通常可以被想象为一个 FSM，animated object 在任意时刻总是在一个特定状态（这就是之前说的 character 总是在播放一个动画），但是在技术上当 blending 发生时这不是完全正确的。Blending 是在多个 animations 之间插值的过程，将它们组合为一个单一的 output。Animancer 中有一些不同种类的 blending：

- 如果你有一个 animation，它的开始和前一个动画的结束并不是 character 的相同的 pose，你可以使用 Fading 来平滑地在这些 animations 之间执行一定时间的 transition，而不是立即对齐 snapping 到新的 pose
- 如果你想要同时播放多个单独的动画，例如 walk 和 wave，你可以使用 layers 保持每个 group 分离，并控制它们分别影响身体的哪些部分
- 如果你有 Walk 和 Run 动画，你可以使用 Mixers 来同时播放两个动画的组合使得这个 character 可以**以任意速度**移动，而不是只以两个特定的速度

所有的 animations 和 layers 有一个 AnimancerNode.Weight，它是一个 0-1 之间的 value，决定它们影响 blended 结果的程度。例如，如果两个动画都具有 0.5 的 weight，则 output 将会它们之间 50% 的方式。

因此相比于使角色显式位于 walking 或 running 状态，一个角色可以是两个状态的混合，同时上身的 waving 在第二个 layer 上，并 fading 向一个标准的 standing 动画，所有一切同时发生。

说白了就是在角色身上同时播放多个动画，即角色处于多个状态的混合。Transition 是 Blending 的一种

有 3 种 Blending 的情景

- Fading

  平滑地在 animations 之间随时间 transition，而不是立即在它们之间 snapping

- Layers

  同一时间播放多个单独的动画，允许你独立地活动不同的身体部分，并且在彼此之上添加 animations

- Mixers

  在多个 animations 之间插值，基于一个你控制的任意的参数
