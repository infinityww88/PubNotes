找到 Dummy Humandoid GameObject 上的 AimController 组件。在 Aim Target (1) 和 Aim Target (2) 之间切换它的 Target，或者设置为 null 来 disable aim。Play around 其他参数来调整 aiming 行为。

主要是展示 Aim Controller 组件的用法。它是在 character 切换 Aim Target 时，帮助进行平滑切换的一个组件，不然，角色会直接从瞄准的一个 target 切换到另一个 target。

角色动画本身设置了一个非常复杂的 AnimatorController，由 2 个 layer 组成，每个 layer 包含有多个状态组成的 BlendTree。但是这和 IK 无关。IK 只是对 Animation 系统输出的后处理，它不管动画数据是怎么来的。因此这里可以忽略 AnimatorController 的设置，只需要知道它输出骨骼动画即可。另外这个例子中也没有展示不同的动画状态。在实际工作中，会使用 Animancer 而不是 AnimatorController。

AimController 是 FinalIK 的一个组件脚本，而不是 Demo 的脚本。

targetSwitchSmoothTime 和 weightSmoothTime 一个是 blend IKPosition 到 target.position，一个是 blend IKPositionWeight 到 master weight.

AimIK 本事是 Component MonoBehavior，ik.transform 指定是 AimIK 所在的 GameObject，就是 character 模型 GameObject。ik.solver 才是真正进行 IK 计算的地方。ik.solver.transform 才是 IK 要操作的 end effector，ik.solver.IKPosition 是 target 的位置。IK 的 source（ik.solver.transform）是 Transform，而 IK 的 dest（ik.solver.IKPosition）是 Vector3。这是因为 IK source 即 IK 要操作的是一个 bone，在 Unity 中就是一个 Transform，而 target 只是一个空间中的位置，因此是 Vector3，只是一些 IK 组件（例如 AimIK）为了方便操作 IKPosition，提供了一个 target transform，然后组件自动将 target transform 的 position 设置为 IKPosition。另外没有 IKRotation，只有 IKPosition，因为 IK 的目标是使 end effector 到达指定位置，仅此而已。还有一个 IKPositionWeight 用来控制 IK 应用到 end effector 上的权重。

AimController 不仅操作 AimIK 组件，还操作 AimIK 组件所在的 GameObject（character）。它的用途是切换 aim target 时，平滑过渡 character pose 和 rotation。

## General

- AimIK ik：引用 AimIK 组件
- float weight：Master weight of IK solver

## Target Smoothing

- Transform target：要瞄准到的 target transform。不要使用被赋值到 AimIK 的 Target transform（因为 Aim Controller 要切换 AimIK 瞄准的 target）。如果想停止 aiming，设置为 null。
- float targetSwitchSmoothTime：切换 target 需要的时间，将 switchWeight 从 0 过渡到 1 的时间，switchWeight = 1 时 AimIK 的 IKPosition 位于 target.position + offset（目标位置）

  ```C#
  switchWeight = Mathf.SmoothDamp(switchWeight, 1f, ref switchWeightV, targetSwitchSmoothTime);
  if (switchWeight >= 0.999f) switchWeight = 1f;

  if (target != null) {
      ik.solver.IKPosition = Vector3.Lerp(lastPosition, target.position + offset, switchWeight);
  }
  ```

- float weightSmoothTime：Blend in/out AimIK weight 需要的时间（将 AimIK 的 IKPosiitonWeight blend 到 Master Weight 的时间

  ```C#
  float targetWeight = target != null ? weight : 0f;
  ik.solver.IKPositionWeight = Mathf.SmoothDamp(ik.solver.IKPositionWeight, targetWeight, ref weightV, weightSmoothTime);
  ```

## Turning Towards The Target

- bool smoothTurnTowardsTarget：允许平滑转向 target，从上一次的 target 逐渐过渡到新的 target，使用 smoothDampTime 过渡方向
- float maxRadianDelta：使用 Vector3.RotateTowards 转向 target 的速度
- float maxMagnitudeDelta：使用 Vector3.RotateTowards 移向 target 的速度
- float slerpSpeed：slerp 向 target 的 speed
- float smoothDampTime：使用 Mathf.SmoothDampAngle 转向 target 的 yaw 和 pitch 的 Smoothing time

  ```C#
  if (smoothTurnTowardsTarget) {
      Vector3 targetDir = ik.solver.IKPosition - pivot;
      // Slerp
      if (slerpSpeed > 0f)
        dir = Vector3.Slerp(dir, targetDir, Time.deltaTime * slerpSpeed);
      // RotateTowards
	  if (maxRadiansDelta > 0 || maxMagnitudeDelta > 0f)
        dir = Vector3.RotateTowards(dir, targetDir, Time.deltaTime * maxRadiansDelta, maxMagnitudeDelta);

      // SmoothDamp
      if (smoothDampTime > 0f)
      {
          float yaw = V3Tools.GetYaw(dir);
          float targetYaw = V3Tools.GetYaw(targetDir);
          float y = Mathf.SmoothDampAngle(yaw, targetYaw, ref yawV, smoothDampTime);

          float pitch = V3Tools.GetPitch(dir);
          float targetPitch = V3Tools.GetPitch(targetDir);
          float p = Mathf.SmoothDampAngle(pitch, targetPitch, ref pitchV, smoothDampTime);

          float dirMag = Mathf.SmoothDamp(dir.magnitude, targetDir.magnitude, ref dirMagV, smoothDampTime);

          dir = Quaternion.Euler(p, y, 0f) * Vector3.forward * dirMag;
      }

      ik.solver.IKPosition = pivot + dir;
  }
  ```
- Vector3 pivotOffsetFromRoot：aim target 绕着 character root 相对旋转的 pivot position

  ```C#
  private Vector3 pivot {
    get {
        return ik.transform.position + ik.transform.rotation * pivotOffsetFromRoot;
    }
  }

  void ApplyMinDistance() {
      Vector3 aimFrom = pivot;
      Vector3 direction = (ik.solver.IKPosition - aimFrom);
      direction = direction.normalized * Mathf.Max(direction.magnitude, minDistance);
      ik.solver.IKPosition = aimFrom + direction;
  }

  private void RootRotation() {
      float max = Mathf.Lerp(180f, maxRootAngle * turnToTargetMlp, ik.solver.IKPositionWeight);
      if (max < 180f) {
          Vector3 faceDirLocal = Quaternion.Inverse(ik.transform.rotation) * (ik.solver.IKPosition - pivot);
          float angle = Mathf.Atan2(faceDirLocal.x, faceDirLocal.z) * Mathf.Rad2Deg;
          float rotation = 0f;
          if (angle > max) {
              rotation = angle - max;
              if (!turningToTarget && turnToTarget) StartCoroutine(TurnToTarget());
          }
          if (angle < -max) {
              rotation = angle + max;
              if (!turningToTarget && turnToTarget) StartCoroutine(TurnToTarget());
          }
	      ik.transform.rotation = Quaternion.AngleAxis(rotation, ik.transform.up) * ik.transform.rotation;		
      }
  }

  ```
- float minDistance：从第一个 bone 开始的最小 aiming 距离。防止 target 和第一个 bone 距离太近而导致 solver 计算失败

- Vector3 offset：应用到 target 的世界空间中的位置。可以用于在脚本中模拟瞄准误差，即不完全精确的瞄准

## Root Rotation

- float maxRootAngle：角色将会绕着 Y 轴旋转保持 root 朝向 aiming direction 这个角度内。Root 不一定完全朝向 target，只需要位于这个角度内，然后让 AimIK 旋转骨骼完成最终的瞄准
- bool turnToTarget：如果开启，当 maxRootAngle 被超过之后，将 root 旋转以朝向 target 方向
- float turnToTargetTime：将 root 旋转想 target 需要的时间

## Mode

- bool useAnimateAimDireciton

  如果为 true，AimIK 将考虑 weapon 的当前方向为 forward aiming 方向，并在这基础上工作。这允许你无缝地将 AimIK 用于 recoil（回退）和 reload 动画。如果 weapon 在动画片段中没有完美 aiming forward，调整下面的 Vector3 

- Vector3 animatedAimDirection

  character space 中 animated weapon aiming 的方向。调整这个值来调整 aiming 的方向。useAnimationAimDirection 必须被开启

