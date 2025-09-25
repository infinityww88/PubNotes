Configurable Joint 的 target velocity 的单位是弧度每秒，而 HingeJoint 和 ArticulationBody 的 Revolute 关节的 target velocity 是度每秒。



ArticulationBody 关节系统比 Rigidbody-Joint 系统更精确更稳定，因为它只允许 child -> parent 这样的关节连接，降低了关节结算的复杂度，代价就是应用的场景受限了。



FixedJoint 理论上应该与将 Rigidbody 的 Collider 直接挂载到 Connected Body 上面一样。但是实际上，FixedJoint 仍然会进行解算（复制 position 和 rotation），而且在复杂的关节系统中不稳定，不能像直接将 Collider 挂载到另一个 Rigidbody 一样。FixedJoint 只能单独用于简单的固定场景。它有 Break Force 和 Break Torque，用于当关节力量超过这个阈值，关节直接断开。因此要想在复杂的关节系统中使用真正固定的效果，还是直接使用 Collider Attach。而 ArticulationBody 的 Fixed Joint 则很稳定，和直接挂载 Collider Attach 一样。



仔细观察 RB（rigidbody）的 FixedJoint，在关节受力很大的时候，两个 RB 的 anchor 并不是实时重合的，会产生一定偏离，并一直尝试回到重合位置。而 ArticulationBody 的 FixedJoint 不会如此，总是保持重合。而直接挂载 Collider 则更是严格 Fixed 的。



另外看起来，Rigidbody-Joint 和 ArticulationBody 可以相互交互。一个 Rigidbody 可以影响（推挤）另一个 ArticulationBody。刚体之间交互依靠的是 Collider 的碰撞检测，二者都使用相同的 Collider。而碰撞后的效果依赖于刚体的速度、角速度、质量，而这在二者中都用对应的属性，因此 Unity 可能直接使用各自的属性进行了碰撞检测和恢复。



例如，用 HingeJoint 创建一个跷跷板，然后在一端创建一个 1kg 的 cube Rigidbody，在另一端创建一个 10kg 的 cube ArticulationBody，就会发现 ArticulationBody，Rigidbody，Joint 可以正常交互。10kg 的 AB cube 比 1kg 的 RB cube 更重，AB 可以把 RB 弹起来更高，RB 更不容易推动 AB。



二者都使用相同的 Collider，刚体碰撞检测是基于 Collider 的。因此 Rigidbody 和 ArticulationBody 的碰撞检测都可以检测到相同的碰撞。另外 Rigidbody 和 ArticulationBody 是平行的类，具有相同的属性和方法，在解析碰撞时，要使用的速度、角速度、质量等，双方都有，因此可以视为同一体系的刚体，可以想象为在解析碰撞、解算碰撞反应时，可以将 ArticulationBody 临时转换为一个 Rigidbody，或者将 Rigidbody 临时转换为一个 ArticulationBody。这就是为什么两个物理系统可以正常相互交互的原因。



ArticulationBody 可以是 Rigidbody-Joint 并行的物理系统，Rigidbody 的属性和方法在 ArticulationBody 上都有对应体。







