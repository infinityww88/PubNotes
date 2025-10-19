# Rigidbody2D

Rigidbody的2D对应部分，下面只列出与Rigidbody的不同之处

## 属性

- attachedColliderCount

    rigidbody2d下挂载的collider2d的数量

- bodyType

无论是那种类型的rigidbody2d，如果它的一个collider2d被设置为trigger，它总是对它的任何一个collider2d到所有其他类型的rigidbody2d的碰撞产生一个trigger消息

- Dynamic

    完全物理控制物体，与所有类型的collider2d碰撞，只应通过力和力矩控制它的运动

  - Kinematic

    停止响应力、力矩，以及到其他Kinematic和Static Rigidbody2D的contacts检测

    KinematicBody2D可以通过velocity、angularVelocity或者显示设置位置/旋转而移动

    KinematicBody2D只能与dynamic rigidbody2d发生碰撞。例外是如果useFullKinematicContacts=true，所有类型的rigidbody2d以及static collider都可以于KinematicBody2D碰撞，**等价于在计算碰撞时将KinematicBody2D当作DynamicBody2D**

  - Static

    停止响应力、力矩，以及到其他Kinematic和Static Rigidbody2D的contacts检测

    StaticBody2D不应该以任何方式改变位置，它被设计为从不移动，物理引擎内部对其进行了优化

- gravityScale

    object被重力影响的程度。重力在Physics2D中是全局设置，但是可以为每个rigidbody设置重力系数

- sharedMaterial

    PhysicsMaterial2D被应用于所有挂载的Collider2D，除非Collider2D自己设置了material。如果两个都没有设置material，则使用全局默认的material

- simulated

    指示rigidbody是否应该被物理引擎模拟

    当不模拟时，任何挂载的Collider2D或Joint2D都不参与物理模拟，相当于有效的从物理系统中移除

    simulated=false于kinematic不同，kinematic仍然对场景中其他的rigidbody2d有影响，但是simulated=false则是彻底不参与物理引擎的任何计算

- sleepMode

    Sleeping是一种优化，用于在物体静止时临时将物体从物理模拟中移除（但是在施加外力，发生碰撞时自动唤醒）

    可以在Inspector中设置

  - NeverSleep：从不自动睡眠，即使已经进入静止状态，除非手动使物体进入睡眠
  - StartAwake：RigidBody2D初始时awake
  - StartAsleep：RigidBody2D初始时sleep

- useAutoMass

    rigidbody整体质量是否应该从挂载的Collider的density自动计算

    useAutoMass=false，通过mass显式设置质量；useAutoMass=true，mass从挂载的Colliders的density和area自动计算

- useFullKinematicContacts

    如果开启，在进行碰撞接触检测时，Kinematic就像Dynamic，可以与collider以及任何类型的rigidbody2d碰撞（发送碰撞消息），尽管不会有真正的**碰撞响应**发生。即Kinematic行为像是trigger，但是发送Collision消息（向碰撞双方发送）

    只应用在KinematicBody2D上，只有bodytype选择kinematic时，这个选项才会出现在Inspector上

    当需要检测碰撞接触的详细信息但是又不想有真正的碰撞响应（分离、摩擦、弹力）时很有用。因为Trigger消息只通知被碰撞的collider2d

    GetContacts方法中也参考这个配置

## 方法

    同一个Rigidbody下的Collider不会发生collision & trigger，因为它们是构成单一rigidbody的形状定义，经常会有重叠，而且它们在rigidbody上是固定的，在它们之间产生碰撞触发消息没有任何意义

### 代理

    代理方法代理调用自身的每一个collider，并返回极值
    代理方法忽略属于rigidbody2d自身的collider

- Cast
- ClosestPoint
- Distance
- GetContacts
- IsTouching
- IsTouchingLayers
- OverlapCollider
- OverlapPoint

### 转换

- GetPoint/GetVector

    将rigidbody自身空间的位置/向量转换到世界空间

- GetRelativePoint/GetRelativeVector

    将世界空间的位置/向量转换到自身空间

- GetPointVelocity/GetRelativePointVelocity

    获取rigidbody在世界空间/自身空间中某个点的线性速度，考虑rigidbody的angularVelocity

### 状态信息

- GetAttachedColliders

    返回rigidbody2d上所有的collider2d

- IsAwake
- IsSleeping
