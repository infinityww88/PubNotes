Configurable Joint 的 target velocity 的单位是弧度每秒，而 HingeJoint 和 ArticulationBody 的 Revolute 关节的 target velocity 是度每秒。



ArticulationBody 关节系统比 Rigidbody-Joint 系统更精确更稳定，因为它只允许 child -> parent 这样的关节连接，降低了关节结算的复杂度，代价就是应用的场景受限了。



FixedJoint 理论上应该与将 Rigidbody 的 Collider 直接挂载到 Connected Body 上面一样。但是实际上，FixedJoint 仍然会进行解算（复制 position 和 rotation），而且在复杂的关节系统中不稳定，不能像直接将 Collider 挂载到另一个 Rigidbody 一样。FixedJoint 只能单独用于简单的固定场景。它有 Break Force 和 Break Torque，用于当关节力量超过这个阈值，关节直接断开。因此要想在复杂的关节系统中使用真正固定的效果，还是直接使用 Collider Attach。而 ArticulationBody 的 Fixed Joint 则很稳定，和直接挂载 Collider Attach 一样。



另外看起来，Rigidbody-Joint 和 ArticulationBody 可以相互交互。一个 Rigidbody 可以影响（推挤）另一个 ArticulationBody。刚体之间交互依靠的是 Collider 的碰撞检测，二者都使用相同的 Collider。而碰撞后的效果依赖于刚体的速度、角速度、质量，而这在二者中都用对应的属性，因此 Unity 可能直接使用各自的属性进行了碰撞检测和恢复。



ArticulationBody 可以看作是 Rigidbody-Joint 一套并行的系统，Rigidbody 的属性和方法在 ArticulationBody 上都有对应体。





