真实世界中，刚体是在物理力和力矩下不可变形的物理 body。刚体中任何两点总是保持相同，不管在其上施加的任何外力。

要模拟基于物理的行为，例如移动、重力、碰撞、关节，你需要在 scene 中配置 item 为 rigid bodies。为此，为 GameObject 添加 Rigidbody 组件。

## 基于物理移动的 Rigid body GameObjects

Unity 中，Rigidbody 组件提供要给基于物理的方式，来控制 GameObject 的移动和位置。相比于 Transform 属性，你可以模拟应用力 force 或 力矩 torque 来移动 GameObject，然后让物理引擎计算结果。

只有两种效果：

- 力（force）
- 力矩（torque）

绝大多数情况下，如果 GameObject 有一个 Rigidbody，你应该使用 Rigidbody 属性来移动 GameObject，而不是 Transform 属性。Rigidbody 属性应用来自物理系统的 forces 和 torque，这将改变 GameObject 的 Transform。如果直接改变 Transform，Unity 不能正确计算物理模拟，你可能看见不想要的行为，尤其是在使用 Joint 的 rigid bodies 上。

Unity 全局地处理基于物理的移动，而不是局部地。当一个 Rigidbody GameObject 通过基于物理的运动移动，它独立任何 Parent 或 Child GameObject 移动。一个带有 Rigidbody 的 Child GameObject 仍然使用它的 local position 来初始化，但是 Unity 在全局空间（世界空间）计算基于物理的运动。

要通过脚本控制 Rigidbody，主要通过两个方法来控制：

- AddForce（添加力）
- AddTorque（添加力矩）

## 没有基于物理移动的 Rigid body GameObjects

有一些情形，你可能想物理系统检测 GameObject，但不是去控制它。例如，你可能想 Colliders 检测一个 GameObject，但是想要通过其他系统（通过 Transform）控制 GameObject 的移动，GameObject 上的 Collider 可以影响物理世界。

Unity 中非基于物理系统的运动称为 Kinematic Motion。Rigidbody 有一个 Is Kinematic 属性，开启时，定义其所在的 GameObject 为非基于物理的运动，将它从物理系统的控制中移除。这允许你通过 Transform 而不是 Unity 的物理模拟计算来移动。

Kinematic Rigidbody 可以施加基于物理的力到 physics-based Rigidbody GameObjects，但是不接收 physics-based force。例如，一个 kinematic Rigidbody 可以碰撞并推开 physics-based movement 的 Rigidbody，但是后者不能推开 kinematic Rigidbody。

如果使用 Joint 将一个 kinematic Rigidbody 连接到 non-kinematic Rigidbody，Joint 不能施加力并移动 kinematic Rigidbody。Joint 只能移动 non-kinematic Rigidbody。但是仍然可以通过 Transform 移动 kinematic Rigidbody，Joint 可以调整 non-kinematic body 的 pose 来满足 joint 的约束。

## Rigidbody optimization

当 Rigidbody 以一个很慢的速度移动，速度小于 Sleep Threshold（Physics Project Settings），Unity 设置 Rigidbody 为 Sleep，这意味着 physics system 不会将它包括在 physics 计算中。当一个 sleeping Rigidbody 接收一个 collision 或 force，Unity wake up Rigidbody，并继续将它包含在 physics 计算中。

默认地，Rigidbody 的 sleeping 和 waking 是自动发生的。但是你可以使用脚本控制它，通过 Rigidbody.Sleep 和 Rigidbody.WakeUp。

Sleeping 的 Rigidbody 无法响应 通过脚本而不是物理系统移动的 Static Collider（没有 Rigidbody 的 Colliders）。为此，可以使用 Rigidbody.WakeUp 唤醒 sleeping Rigid body。

