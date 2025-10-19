Mesh Splider 机械蜘蛛

MechSpider 有两个版本，MechSpiderCCD 和 MechSpiderFABRIK。

Spider 最顶层有一个 Transform 包含 MechSpider.cs 和 MechSpiderController.cs 组件。下面有一个 Body，包含一个机箱 mesh 作为 body，Body 下面有 6 条 legs。每个 legs 由 4 个 bone 组成。每个 leg bone 有一个 mesh，最后一个 bone 是 Foot。Leg root 具有 RotationLimitAngle 和 MechSpiderLeg 组件，Leg 2 和 Leg 3 具有 RotationLimitHinge 组件，Foot 具有 RotationLimitAngle 组件。

MechSpiderFABRIK 版本中 Leg Root 具有 FABRIK 组件，MechSpiderCCD 版本中 Leg Root 具有 CCD 组件。

MechSpiderLeg 成员：

- MechSpiderLeg unSync：另一条我们不想与其完全同步的 legs，它在同时 stepping

  ```C#
  // 如果 unSync leg 正在 stepping，什么都不做
  if (unSync != null) {
    if (unSync.isStepping) return;
  }
  ```

  蜘蛛有 6 条腿，两侧各有两条，L1 L2 和 R1 R2，以及前后两条腿 F 和 B。其中 L1 L2 互为 unsync，R1 R2 互为 unsync，F 和 B 互为 unsync。unsync 的两条腿同一时间只有一条腿前进。

- Vector3 offset：用于调整的相对 default position 的 offset

- float minDelay, maxOffset, stepSpeed, velocityPrediction, raycastFocus：用于 steping（前进 leg）的参数

- AnimationCurve yOffset

- Transform foot

- Vector3 footUpAxis

- float footRotationSpeed

- ParticleSystem sand：FX for sand

- private IK ik：引用 Leg root 上的 IK 组件，或者 CCD IK，或者 FABR IK，IK 组件是通用的 IK 组件引用，主要目的就是调用它的 UpdateSolver。MechSpiderLeg 在 Awake 中获取 GameObject 挂载的 IK 组件

  ```C#
  // IK solver 具有 OnPostUpdate 组件，用来在 IK 过程完成后进行后处理
  ik.GetIKSolver().OnPostUpdate += AfterIK;
  ```
  IK 过程本身就是基于各自参数调整 bone 的 transform，和任何简单的操作 GameObject（例如 ParentConstraint 等等）是一样的。当 IK 完成之后，可以进行进一步后处理，即根据需要再次调整 GameObject 的 transform

  ```C#
  private void AfterIK()
  {
      if (foot == null) return;
      foot.localRotation = lastFootLocalRotation;

      smoothHitNormal = Vector3.Slerp(smoothHitNormal, hit.normal, Time.deltaTime * footRotationSpeed);
      Quaternion f = Quaternion.FromToRotation(foot.rotation * footUpAxis, smoothHitNormal);
      foot.rotation = f * foot.rotation;
  }
  ```

- Vector3 position

  ```C#
  public Vector3 position {
      get {
          return ik.GetIKSolver().GetIKPosition();
      }
      set {
          ik.GetIKSolver().SetIKPosition(value);
      }
  }
  ```

- bool isSteping：判断当前 leg 是否正在 stepping 过程中

  ```C#
  public bool isStepping {
      get {
          return stepProgress < 1f;
      }
  }
  ```

  当 stepProgress 小于 1 时就是在 stepping 过程中，当 stepProgress = 1，stepping 结束。

- Start()

  IKSolver 以 Point[] 方式存储骨骼链，每个 Point 存储一个 bone 的数据，不仅包括 transform，还包括其他 IK 相关数据，例如 Weight，RotationLimit 等等。因此通过 Solver 访问骨骼链，就通过 GetPoints，得到 Point[]，其中就包含了骨骼链的各个 transform。

  Start 函数中，通过 ik.GetIKSolver().GetPoints() 获得的骨骼链的最后一个 bone

  ```C#
  var points = ik.GetIKSolver().GetPoints();
  position = points[points.Length - 1].transform.position;
  ```

  ```C#
  defaultPosition = mechSpider.transform.InverseTransformPoint(position + offset * mechSpider.scale);
  ```

  offset 缩放到 mechSpider 的 scale 之后，作为偏移和最后一个 bone 的 position 相加，转换到 mechSpider 空间中，作为这个 leg foot 默认的 rest position，保存在 defaultPosition

  然后通过 StartCoroutine(Step(position, position)) 开始一个 Step 过程

- IEnumerator Step(Vector3 stepStartPosition, Vector3 targetPosition)

  从 stepStartPosition 向 targetPosition 执行 step。Start 函数使用相同的 stepStartPosition 和 targetPosition 执行 step。

  开始时将 stepProgress 设置为 0，然后每一帧（yield return null）移动 IK Position：

  ```C#
  while (stepProgress < 1) {
      stepProgress += Time.deltaTime * stepSpeed;
      position = Vector3.Lerp(stepStartPosition, targetPosition, stepProgress);
      position += mechSpider.transform.up * yOffset.Evaluate(stepProgress) * mechSpider.scale;
      lastStepPosition = position;
      yield return null;
  }
  ```

  每帧使用 stepSpeed 增加 stepProgress。然后从 stepStartPosition 向 targetPosition Lerp，得到新的 position。然后使用一个 yOffset 曲线在 Y 轴上偏移 position 的 y，模拟 leg 迈步的效果。yOffset 只是偏移 position 的 y 分量，并且在 0 和 1 处为 0，确保开始和最后 foot 都是位于 ground 上的。

  在经过很多 frame 之后，while 循环退出，这个 leg 的 root 落在地面上。使用 sand 粒子系统发射 20 个粒子，模拟 foot 落地时弹起尘土的效果。sand 时 body 下面的一个 child GameObject。所有的 leg 共享这一个 sand 粒子系统。每个 foot 落地时都用这个 sand 发射一组粒子。sand 粒子系统在 world 空间中模拟，因此只需要用一个就可以为所有 foot 模拟尘土效果，而不必为每个 foot 设置一个单独的粒子系统。粒子系统的本质就是发射粒子，不管是被哪个粒子系统发射的。

- Vector3 GetStepTarget(out bool stepFound, float focus, float distance)

  用来查找下一个 Foot 应该放置的位置。

  先用 MechSpider 的前进速度计算和配置的预测时间计算 Foot Rest Position 下一次应该踏在的位置。之后 Step Coroutine 将 Foot 随时间 Lerp 到这个位置，并且中间加入一个 Y 曲线，形成跨越效果。

  计算到下一个预测 rest position 还需要进一步修正。因为地形不平坦可能导致这个位置在 terrain 之下。因此需要进行一次 raycast，将这个位置调整到 ground 上。但是调整的方向不是 MechSpider.up，而是旋转一下 up 向量，使得 raycast 向着 MechSpider 之外的远离的方向调整。

- void Update()

  position 是 Property，代理的是 ik.GetIKSolver().IKPosition。每次设置它都是在设置 IKPosition。注意不是每次设置都引起 IK 计算。IK 计算在 IK 组件每次 Update Solver 时才会计算，在此之前对 IKPosition 的设置都不会导致 IK 计算。

  Update 先执行，然后是 Coroutine，然后是 LateUpdate。
    
  每次 Update 首先调用 UpdatePosition(mechSpider.raycastDistance * mechSpider.scale)，但看起来这似乎没有必要，因为 UpdatePosition 中对 position 的修改总会被 Step Coroutine 修改。将这段代码注释掉之后似乎也没有影响，效果与之前一样。

  基本过程就是根据前进方向预测下一个 Foot 应该所在的位置，然后随时间 Lerp IKPosition 到这个位置，中间加入 Y 跨越曲线（起始和终止都是 0）。然后重复此过程。

  预测的位置大概正确就可以，IK 组件确保骨骼链正确的弯曲。这就是 IK 系统的强大之处。

MechSpider 和 MechSpiderController 主要用来控制 MechSpider 的 Body（root）的运动和呼吸效果，以及摄像机跟随。

两个版本的 MechSpider（CCDIK 和 FABRIK）区别就在于 Leg 上的挂载的 IK 组件是 CCD 还是 FABR。而且代码中完全没有涉及具体的 IK 组件调用，只使用基类 IK 来引用它们，并依赖于它们自身的 Update。这一是用来展示不同类似的 IK 组件之间的可替换性，而是展示二者的效果。看起来 FABRIK 效果好于 CCDIK。
