Configurable Joint 的 target velocity 的单位是弧度每秒，而 HingeJoint 和 ArticulationBody 的 Revolute 关节的 target velocity 是度每秒。



ArticulationBody 关节系统比 Rigidbody-Joint 系统更精确更稳定，因为它只允许 child -> parent 这样的关节连接，降低了关节结算的复杂度，代价就是应用的场景受限了。



FixedJoint 理论上应该与将 Rigidbody 的 Collider 直接挂载到 Connected Body 上面一样。但是实际上，FixedJoint 仍然会进行解算（复制 position 和 rotation），而且在复杂的关节系统中不稳定，不能像直接将 Collider 挂载到另一个 Rigidbody 一样。FixedJoint 只能单独用于简单的固定场景。它有 Break Force 和 Break Torque，用于当关节力量超过这个阈值，关节直接断开。因此要想在复杂的关节系统中使用真正固定的效果，还是直接使用 Collider Attach。而 ArticulationBody 的 Fixed Joint 则很稳定，和直接挂载 Collider Attach 一样。



仔细观察 RB（rigidbody）的 FixedJoint，在关节受力很大的时候，两个 RB 的 anchor 并不是实时重合的，会产生一定偏离，并一直尝试回到重合位置。而 ArticulationBody 的 FixedJoint 不会如此，总是保持重合。而直接挂载 Collider 则更是严格 Fixed 的。



另外看起来，Rigidbody-Joint 和 ArticulationBody 可以相互交互。一个 Rigidbody 可以影响（推挤）另一个 ArticulationBody。刚体之间交互依靠的是 Collider 的碰撞检测，二者都使用相同的 Collider。而碰撞后的效果依赖于刚体的速度、角速度、质量，而这在二者中都用对应的属性，因此 Unity 可能直接使用各自的属性进行了碰撞检测和恢复。



例如，用 HingeJoint 创建一个跷跷板，然后在一端创建一个 1kg 的 cube Rigidbody，在另一端创建一个 10kg 的 cube ArticulationBody，就会发现 ArticulationBody，Rigidbody，Joint 可以正常交互。10kg 的 AB cube 比 1kg 的 RB cube 更重，AB 可以把 RB 弹起来更高，RB 更不容易推动 AB。



二者都使用相同的 Collider，刚体碰撞检测是基于 Collider 的。因此 Rigidbody 和 ArticulationBody 的碰撞检测都可以检测到相同的碰撞。另外 Rigidbody 和 ArticulationBody 是平行的类，具有相同的属性和方法，在解析碰撞时，要使用的速度、角速度、质量等，双方都有，因此可以视为同一体系的刚体，可以想象为在解析碰撞、解算碰撞反应时，可以将 ArticulationBody 临时转换为一个 Rigidbody，或者将 Rigidbody 临时转换为一个 ArticulationBody。这就是为什么两个物理系统可以正常相互交互的原因。



ArticulationBody 可以是 Rigidbody-Joint 并行的物理系统，Rigidbody 的属性和方法在 ArticulationBody 上都有对应体。



Unity 的物理系统是比较受限的，只能在有限的条件下提供“真实”效果：



* 只能模拟宏观低速的情况
* 物理单位只能使用米/分米、千克、秒这样的单位。千米/厘米/毫米、吨/克/毫克、毫秒/微秒 这些物理量都很难正确模拟
* 速度只能限制在米每秒这样的范围，即使像子弹这样的物理刚体，都是高速物体，都无法正常模拟，只能用射线模拟



还有重要的一点：物理系统中相互交互的物体的质量、力/力矩与质量的差距不能太大，要尽可能接近，这样才能得到最稳定的效果。例如一个用 Fixed Joint 固定的 1kg 的平板，从上方掉落 1kg-10kg 左右的 cube，能比较真实地模拟。但是如果 cube 的质量为 1000kg，cube 就会直接隧穿平板，这就是物理量相差太大时，无法正确模拟的情况。同样还有，当 1kg 左右的 rigidbody 在连接的关节中受力过大，例如收到 10000N 的力，也会产生不稳定模拟。要产生稳定的模拟，1kg 左右的 rigidbody 不应该承受超过 100N 的力 或 100N\*M 的力矩。这也是上面说的 Fixed 关节有时不稳定的原因，根本原因还是受到的力或力矩太大（1kg 的 rb 收到 1000N 的力诸如此类）。ArticulationBody 能较为真实地模拟 Fixed 关节，是因为它在内部会自动缩放 AB 的质量，使得关节双方的质量差距不会太大，也不会使 AB 受到太大的力或力矩，因此能产生稳定模拟。Joint 为了弥补这个问题，提供 Mass Scale 和 Connected Mass Scale，它在关节解算时，会将 AB 的质量乘以这个因子，对质量进行缩放，用于将两个 AB 的质量差距尽可能缩小，以产生稳定模拟。但是这样会使关节解算违反能量守恒定律，但是能显著提升视觉效果的稳定性和合理性。



因此物理引擎是十分娇贵的系统，不能随心所欲地使用，设计物理系统时，目标不是完全匹配现实，而是为游戏提供稳定的模拟效果，因此也不必完全遵循现实世界的物理量。例如一辆车的 body 和 wheel 的质量比不一定需要跟现实世界一样。现实世界中一个 1kg 的刚体通过关节连接一个 1000kg 的刚体，在物理引擎中，可能将其建模为 10kg 和 50kg 的两个刚体。只要视觉效果看起来对就行。不需要按照现实世界建模，因此可以直接使用默认 rb 的 1kg 作为参考基准，其他刚体、关节的参数（spring，damper，force）等等根据视觉效果试错调整来设置，不可能通过计算来设置，只要达成稳定、满足预期的效果即可。



不用期待用 Unity 物理引擎完完全全地模拟现实。物理引擎的目的就和其他系统（例如渲染、特效）一样，只是为了给玩家提供看起来“真实”的效果，而实际不一定与现实一样真实。物理引擎还是为游戏玩法提供支持，而不是为了完全模拟现实世界。



ArticulationBody 的 Prismatic 和 Configurable Joint 实现的类似关节的区别：



* Configurable Joint 的 Linear Motion 为 free 时，rb 是完全自由移动的，无论如何设置 Limit 和 Limit Spring，都没有作用，没有弹簧力。只有将 Motion 设置为 Limited，Limit 和 Limit Spring 才起作用。当 Motion 设置为 Limited，必须为 Limit 设置为一个正数范围值，rb 超出 limit 边缘时才会有弹簧效果，limit 才成为软边界。如果 limit 设置为 0，rb 的活动范围将完全静止。即使设置 spring 无论任何数值，rb 也不会移动，就像 fixed。如果 limit 设置为整数范围，而 spring 设置为 0，则没有弹簧力，则 limit 范围将成为硬边界，rb 从不会超出。
* Prismatic Motion 设置为 Free 时，只有 stiffness（spring）为 0 时，ab 才能自由没有限制地移动，当 stiffness > 0 时，就会有弹簧效果，弹簧中和点由 target 定义。当 Motion 设置为 Limited 时，出现 Lower Limit 和 Upper Limit，它们是 Prismatic Motion 的硬边界，ab 从不会超出这个范围。如果 Lower Limit 和 Upper Limit 都为 0，则 ab 被完全固定，如同 fixed。target 仍然是沿着 anchor axis 定义的偏移，Lower Limit 和 Upper Limit 也是沿着 anchor axis 定义的范围，Limit 并不是在 target 两端定义的范围，而是在 anchor 两端定义的范围，target 可以在 limit 范围之内，可以在 limit 的范围之外，但无论如何 target 定义了弹簧中和点，Lower Limit 和 Upper Limit 定义了范围的硬边界。ab 的运动硬性限制在 limit 的范围内，但是在 target 周围弹性运动。





