使用 CinemachineCamera 的第三人称跟随功能，使相机相对于追踪目标保持恒定的位置和距离（受阻尼控制约束），并跟踪目标的移动和旋转。

第三人称跟随的 mini-rig 设置定义了相机相对于目标的位置和距离。通过合适的肩部偏移，这个迷你装备可以生成第三人称视角的相机——角色在画面中偏移，相机从角色肩部上方观察。**通过不同的设置，它也可以生成第一人称视角的相机。**

![CinemachineRigSceneView](../../Images/CinemachineRigSceneView.png)

会产生如下结果：

![CinemachineRigGameViewExample](../../Images/CinemachineRigGameViewExample.png)

Rig 和 Camera Position 通过 3 个枢轴点 pivot points（origin，shoulder，hand）以及一个位于手部后方的相机共同定义。

- Origin(A)：tracking target 的 origin 位置。当 target 水平绕轴旋转 pivot，rig 绕着这个 origin 随之旋转。
- Shoulder(B)：默认情况下，它会偏移到一侧，以形成过肩跟随位置。追踪目标的垂直旋转会传递到此处，因此 rig 会围绕原点水平旋转，并围绕肩膀垂直旋转。
- Hand(C)：相对于肩膀的垂直偏移量。手臂长度会影响相机垂直旋转时追踪目标在屏幕上的位置。默认情况下，它会从肩膀处偏移，以便垂直旋转时能让角色在屏幕上保持良好的位置。对于第一人称相机，该值可以设置为0。
- Camera(D)：相机的旋转将始终与追踪目标的旋转保持平行，但位置会固定在手部后方指定的相机距离处。相机始终直接注视着手部。

注意 rig 上的 rotations：

- B 绕 A 水平旋转。使用 A 作为原点，B 的位置基于 Shoulder Offset 的 X Y Z 值计算。

  ![CMShoulderOffsetexample](../../Images/CMShoulderOffsetexample.png)

- C 绕着 B 垂直旋转。C 点的位置是根据 B 点的 Vertical Arm Length 计算得出的。正值会使 C 点位于 B 点上方，负值则会使 C 点位于 B 点下方。

  ![CMVerticalDistanceexample](../../Images/CMVerticalDistanceexample.png)

A 作为 Origin 原点，B 先从 A 偏移，C 再从 B 垂直偏移。

# Controlling the Camera

该相机没有直接的输入控制。你必须有一个控制器脚本来移动和旋转追踪目标；相机将根据该追踪目标来定位和定向自身。当追踪目标是角色本身时，相机的旋转始终与角色的旋转相匹配。当追踪目标是一个可以独立于角色旋转的不可见游戏对象时，相机将能够围绕角色进行旋转。

# Built-in Collision Resolution

第三人称跟随组件内置了碰撞解决方案系统，因此当目标靠近障碍物时，相机会自动调整位置以避免穿入障碍物内部；该内置碰撞解决方案确保相机始终能观察到目标，即使中间存在障碍物阻挡。当目标过于接近障碍物时，相机 rig 会通过弯曲和拉伸来保持相机位于障碍物外部，同时始终确保目标处于视野范围内。

# Shaky Movement, Steady Aim

当与 CinemachineThirdPersonAim 扩展组件结合使用时，可以构建出一个强大的相机装备系统，即使相机移动出现抖动或噪声干扰，也能为射击类游戏保持稳定的瞄准效果。CinemachineThirdPersonAim会重新调整相机朝向，确保屏幕中央始终锁定固定目标点，从而修正因相机抖动产生的偏差。

# 属性

- Damping：相机跟踪目标的响应灵敏度。每个轴向可单独设置参数。该数值表示相机追上目标新位置所需的大致时间。数值越小，相机响应越灵敏；数值越大，相机响应越迟缓。
- Shoulder Offset：肩膀枢轴点相对于追踪目标原点的位置。该偏移量是在目标本地空间中的。
- Vertical Arm Length：Hand 相对于 Should 的垂直偏移量。 Arm 长度会影响相机垂直旋转时追踪目标在屏幕上的位置。
- Camera Side：指示 camera 在哪个 shoulder 上（左肩、右肩、以及二者插值的任何地方）。
- Camera Distance：指示 hand 到 camera 的距离。
- Camera Collision Filter：指示哪些 layers 被包含在 collision resolution，哪些 layers 被排除。
- Ignore Tag：具有此标签的障碍物将被碰撞解决方案忽略。建议将该字段设置为目标对象的标签。
- Camera Radius：指定相机在不调整位置的情况下，可以接近可碰撞障碍物的最近距离。
- Damping Into Collision：指定相机修正遮挡的渐进程度。数值越高，相机调整位置的过程越平缓。
- Damping From Collision：指定相机在通过内置碰撞解决方案系统修正后，恢复至正常位置的渐进程度。数值越高，相机回归正常位置的过程越平缓。

