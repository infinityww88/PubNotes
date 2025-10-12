Kinematic Character Controller

Core Scripts：

- KinematicCharacterMotor：这是 character system 的核心。脚本解析所有 character movement 和 collisions，基于给定的 velocity，orientation，和其他因素。
- PhysicsMover：这个脚本移动 Kinematic physics objects（moving platforms），这样 characters 可以正确地站在上面，或者被它们推开。
- KinematicCharacterSystem：以正确的顺序模拟 KinematicCharacterMotors 和 PhysicsMovers。
- ICharacterController：实现这个接口，将 class 赋值给 KinematicCharacterMotor 以实现你自己的 character controller。
- IMoverController：实现这个接口，将 class 赋值给 PhysicsMover 以实现你自己的 mover controller。

角色控制器是出了名的难以完美实现，不同游戏对它的需求也千差万别。可能性是无限的。因此，运动学角色控制器（Kinematic Character Controller）并不会试图预先打包所有问题的解决方案，而是专注于解决角色控制器动态响应这一核心物理难题，其余部分则完全交由开发者掌控。这种设计理念确保你能打造出专为游戏定制的角色控制器，并使其完美适配任何项目架构。

该组件要求开发者自行编写以下功能的代码：玩家输入、镜头控制、动画系统，甚至包括角色移动逻辑（例如指定移动速度和朝向等）。不过，它真正提供的是底层物理解决方案——通过一系列基础组件处理复杂的角色物理运算，让开发者能够相对轻松地构建完全自定义的角色控制器。

整个系统的核心是"KinematicCharacterMotor"组件，它通过胶囊体模拟角色碰撞，并能根据输入参数（速度、旋转等）精确计算运动轨迹。当你设定移动速度后，该组件会自动执行运动逻辑，实现合理的表面碰撞/滑动效果。此外，它还能提供精准的接地状态检测、处理移动平台站立、推动其他刚体等物理交互——这些正是构建角色控制器的底层基础。

要为KinematicCharacterMotor提供输入参数，你需要创建一个实现ICharacterController接口的自定义类，并将其赋值给KinematicCharacterMotor.CharacterController变量。完成此操作后，你的类将开始接收来自Motor的"回调"请求。这些"回调"本质上可以理解为KinematicCharacterMotor向你提出的问题：
● UpdateVelocity："当前应该采用什么移动速度？"
● UpdateRotation："角色需要如何旋转？"
● IsColliderValid："这个碰撞体是否应该被忽略？"
● 其他运动状态查询...

这些回调函数都会由 KinematicCharacterMotor 在角色更新循环中自动调用，你完全无需担心它们的执行顺序问题。通过实现这些回调，你就能精确控制 KinematicCharacterMotor 的所有行为表现。

这一设计原则同样适用于移动平台的创建。此时：

- ​PhysicsMover​ 承担与 KinematicCharacterMotor 相同的职责
- ​IMoverController​ 则对应 ICharacterController 的角色

通过实现 PhysicsMover 的回调接口，你就能精确控制移动平台的运行轨迹。


本小节将概述如何通过多个组件的协同运作，在"CharacterPlayground"场景中创建示例角色。请先打开该场景，然后跟随本节内容进行操作。

## Kinematic Character System Overview

本节将概述所有"核心"脚本如何协同运作，以实现正确的角色移动逻辑并构建完整的角色系统。请注意：你的KinematicCharacterMotors和PhysicsMovers组件需要遵循特定的执行顺序才能正常工作——这一关键功能由KinematicCharacterSystem类统一管理。

### 组件注册

当KinematicCharacterMotors和PhysicsMovers组件被创建时，它们会在OnEnable()生命周期中自动注册到KinematicCharacterSystem；同理，在OnDisable()时执行注销操作。KinematicCharacterSystem将统一管理所有已注册组件的更新行为，确保其按正确顺序执行。

### 基本模拟循环

当AutoSimulation为true时，KinematicCharacterSystem会在FixedUpdate()中执行以下流程：

- 预模拟插值阶段 PreSimulationInterpolationUpdate()
  - 保存所有已注册motor和mover的初始位姿（运动计算前）
  - 完成当前帧的插值运算
- 物理模拟阶段 Simulate()
  - 为所有PhysicsMovers计算目标速度（基于预设位姿）
  - 调用所有KinematicCharacterMotors的UpdatePhase1(), 解决初始穿模问题, 处理地面检测逻辑
  - 直接将PhysicsMovers传送到目标位置
  - 调用所有KinematicCharacterMotors的UpdatePhase2()，解析运动向量，计算机体最终位姿，将motor移动到目标位置
- 后处理阶段 PostSimulationInterpolationUpdate()
  - 将所有motor和mover的transform状态恢复为PreSimulationUpdate()保存的位姿

### Manual Simulation

需精确控制物理模拟过程，可将KinematicCharacterSystem.AutoSimulation设为false。此时你需要手动管理模拟流程——该模式在网络同步场景中尤为实用，例如当你需要在同一帧内多次调用Simulate()来重新模拟历史输入时。

查看 KinematicCharacterSystem.FixedUpdate() 默认 autoSimulation loop 如何工作。

### 更多信息

- 如果想要瞬移 teleport character 而不是正常移动，使用 KinematicCharacterMotor.SetPosition()
- 绝不要让 character 成为一个 moving transform 的 child
- character gameObject 的 lossy scale（global scale）必须是 (1, 1, 1)，否则 physics 计算不能正确工作。这意味着它所有的 parents 的 scale 都必须是 (1, 1, 1)
- 如果想在 play 中 resize capsule，总是使用 KinematicCharacterMotor 的 SetCapsuleDimensions 方法，因为它缓存了 capsule dimensions 的信息，这个信息稍后会被大多数 movement code 所使用。

KinematicCharacterMotor采用无GC分配的物理查询方法，这意味着它使用固定大小的数组来存储查询结果。默认配置下，该组件最多可支持32个射线检测结果和32个碰撞体重叠结果的存储。如需更大容量，你可直接修改KinematicCharacterMotor中的"MaxHitsBudget"（最大射线检测预算）和"MaxCollisionBudget"（最大碰撞检测预算）常量值。

可以通过修改KinematicCharacterSystem中的"Interpolate"参数，全局控制所有KinematicCharacterMotors和PhysicsMovers的插值功能开关状态。

若需实现基于动画根运动的角色移动，你只需在自定义角色控制器的OnAnimatorMove()方法中：

- 获取动画器根运动位移(animator.deltaPosition)
- 转换为速度向量(animator.deltaPosition/deltaTime)
- 在motor的"UpdateVelocity"回调中设置该速度

旋转控制同理可通过"UpdateRotation"回调实现。具体示例请参考Walkthrough教程中的实现方案。

## 介绍

KinematicCharacterMotor 是 Kinematic Character Controller (KCC) 资源包的核心组件，其设计理念和技术特性可总结如下：

​核心功能​

作为胶囊体角色碰撞器的物理运算中枢，通过输入参数（速度、旋转等）实现精确的运动模拟，采用"碰撞与滑动"算法（非刚体物理），处理以下复杂场景：
- 表面碰撞/滑动摩擦
- 移动平台站立检测
- 刚体推动交互
- 动态重力环境适应

提供实时接地状态检测（grounding status），解决斜坡弹出、凹面碰撞等常见问题

​技术架构​

需开发者实现 ICharacterController 接口，通过回调机制（如 UpdateVelocity/UpdateRotation）传递运动参数
物理运算与游戏逻辑分离，确保：
- 网络同步支持（适用于权威服务器架构）
- 零GC分配（提供性能优化选项）
- 任意项目架构集成

​典型应用场景​

- 需要高度定制化移动逻辑的游戏（如平台跳跃、攀爬系统）
- 对物理响应要求严格的多人游戏
- 2.5D/3D游戏的特殊平面锁定需求

该组件的优势在于将复杂的物理运算封装为底层服务，同时保留完整的控制权给开发者。如文档强调，这不是即插即用的解决方案，需要开发者具备3D数学和编程能力来实现输入、动画等上层系统