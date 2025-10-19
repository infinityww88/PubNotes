# Second Hand On Gun

如果 arm bones 被包含在一个双手 weapon 的 aiming 中，当 bones 旋转时，另一个 arm 可能会失去对 weapon 的接触。SecondHandOnGun.cs 使用 LimbIK 来将左手放回到动画中它相对于右手的位置。

如果 arm bones 没有被 AimIK 使用，额外的 LimbIK solving 没有必要。

IK 不支持 multi-effector 指的是一个 bone chains 中只能有一个 effector。但是一个 character 的骨骼可以有多个 IK 控制多个骨骼链，每个骨骼链有一个 IK 和 end effector。例如有两个 ArmIK 和两个 LegIK。

FBBIK 即 Full Body Biped IK 不是一个具体的IK，而是包含一组应用于人形骨骼的 IK 组件套装（容器）。

FABR IK 则是和 ArmIK、LimbIK 一样的具体的 IK 组件。

这里的例子就是，武器始终挂载到右手上，用 AimIK 来瞄准，之后左手可能失去对武器的接触，因此这里对左手使用一个 LimbIK 将左手调整到原始动画中相对于右手相同的位置。

AimIK 的 bones 包括 Spine 1 > Spine 2 > Spine 3 > Neck > Right Clavicle > Right UpperArm > Right Head，Aim Transform 为 MP-40，而 MP-40 在 Right Head 下面。

LimbIK  的 bones 包括 Left UpperArm > Left Forearm > Left Head

SecondHandOnGun.cs disable 了 aimIK 和 leftArmIK，手动 Update solver，以控制 IK 过程的顺序。

IK 本身就是一个一次的计算过程，得到 bones chain 的旋转结果。这个计算过程就是通过调用 solver.Update() 完成的。

```C#
void LateUpdate()
{
    // 将左手 world position，rotation 转换到右手空间
    // leftHand.rotation 为左手在世界空间中的旋转，Quaternion.Inverse 反转一个 Quaternion。
    // Quaternion.Inverse(rightHand.rotation) 可以将右手当前的 rotation 旋转回 identity。
    // 用它左乘 leftHand.rotation，结构就是当右手 identity 时左手的 rotation（相对右手，因为右手当前是 identity 的）
    leftHandPosRelToRight = rightHand.InverseTransformPoint(leftHand.position);
    leftHandRotRelToRight = Quaternion.Inverse(rightHand.rotation) * leftHand.rotation;

    // 执行 AimIk，右手骨骼链将被旋转
    aim.solver.Update();

    // AimIK 已经旋转了右手来瞄准 target，此时左手可能和 weapon 脱离了连接，Weapon 在右手下面，接触点在右手空间是保持不变的。因此将之前左手相对于右手空间的位置和旋转再次变换到在旋转之后的 righthand 空间中，这就是 AimIK 之后左手应该在的位置和旋转
    // 这个脚本还添加了一个 position offset 和 rotation offset 来进一步精细调整左手的 position 和 rotation。这些值通过在 Inspector 中编辑让左手精确放在接触点上
    leftArmIK.solver.IKPosition = rightHand.TransformPoint(leftHandPosRelToRight + leftHandPositionOffset);
    leftArmIK.solver.IKRotation = rightHand.rotation * Quaternion.Euler(leftHandRotationOffset) * leftHandRotRelToRight;

    // Update Left arm IK
    leftArmIK.solver.Update();
}
```

LimbIK 下面有 IKRotation，而 AimIK 只有 IKPosition。

AimIK 只是旋转 bones 使 Aim Transform 接近 Target Position。LimbIK 则不仅让 end effector 接近 IKPosition，还让它的方向接近 IKRotation。

LimbIK 包含的 solver 是 IKSolverLimb。

LimbIK 用于 3-segmented 的骨骼链，即骨骼链只有3个 Bone，Limb IK 直接暴露 Bone 1、Bone 2、Bone 3，而不是 Bones[]，即强制 3 个 Bones。3 个 bones 实际只有两个 segment。这个是专用于 character limb 的 hand 和 leg 的情景。

IKSolverLimb : IKSolverTrigonometric : IKSolver

IKSolverTrigonometric 基于余弦定理的 IK solver（三角函数）

- Transform target：end effector
- float IKRotationWeight：最后一个 bone rotation weight
- Quaternion IKRotation：IK rotation target
- Vector3 bendNormal：bend plane normal，bend 平面应该就是 pole 平面
- TrigonometricBone bone1：first bone（upper arm or thigh）
- TrigonometricBone bone2：first bone（forearm or calf）
- TrigonometricBone bone3：first bone（hand or foot）
- void SendBendGoalPosition(Vector3 goalPosition, float weight)

  设置 bend goal 就是设置 bend normal，调整 bend 平面

- void SetBendPlaneToCurrent()：设置 bend plane 来匹配当前 bone rotations
- void SetIKRotation(Quaternion rotation)：设置 IK rotation
- void SetIKRotationWeight(float weight)
- Quaternion GetIKRotation()
- Quaternion GetIKRotationWeight()

IKSolverLimb 成员

- AvatarIKGoal goal：这个 solver 的 AvatarIKGoal

  AvatarIKGoal 是 UnityEngine 的枚举，包括 LeftRoot, RightFoot, LeftHand, RightHand，用来指定 Avatar Mapping 中的逻辑 bone

- BendModifier bendModifier：Bend Normal modifier，一个枚举值，包括

  - Animation：相对于 first bone 的 animated rotation Bending，即第一个 bone 向哪个方向旋转，Bend Plane 就向哪个方向，Bones chain 就在这个平面中
  - Target：相对于 IKRotation Bending，即 IKRotation 定义了 Bend Plane
  - Parent：相对于 parentBone Bending，parentBone 向哪个方向旋转，Bend Plane 就在那个方向上
  - Arm：试图找到生物学最自然和放松的 arm bend plane 方向
  - Goal：使用一个 Bend Goal 来定义 Bend Plane

  Bend 就是 Pole。无论用哪种 modifier，都是在指定以何种方式确定 Bending 方向，就 Bending 平面，最终这个平面被 Bend Normal 确定，这也是为什么这个变量称为 Bend Normal Modifier 的原因。

  Bending 平面就是 Bone1 Bone2 Bone3 构成的平面，这个平面基本就是控制 Bone 2，来沿着 Bone 1 和 Bone3 的轴线旋转平面

- float maintainRotationWeight：维持 Bone 3 solving 之前的 rotation 的权重（尽可能不旋转 Bone 3 的方向

- float bendModifierWeight：bend normal modifier 的权重

- Transform bendGoal
