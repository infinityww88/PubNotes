Quaternion 用于表示一个旋转。

它使用一个旋转轴和角度表达旋转。注意旋转总是绕着使用 Quaternion 旋转的 object 的中心的，因此这个旋转轴总是在 object 的中心定义的。

你可以使用一个 quaternion 串联一系列旋转到一个 Quaternion 中。

Unity 内部使用 Quaternion 表示所有 rotation。因此所有用 EulerAngles 指定的旋转都会被转换为 Quaternion，即一个旋转轴和一个角度。

Quaternion 可以使用 * 旋转另一个 Quaternion（串联 Quaternion），或者另一个 Vector3.

Quaternion、Matrix4x4 的乘法都是左乘。更加 parent（更 base）的位于更左边，被应用的目标位于乘法的右边。

# 属性

- eulerAngles

  返回与这个 Quaternion 等价的欧拉角表示。

# 成员方法

- void SetFromToRotation(Vector3 fromDirection, Vector3 toDirection)

  设置这个 Quaternion，它表示的旋转，可将 fromDirection 旋转到 toDirection，旋转轴按照左手定则定义。

- void SetLookRotation(Vector3 forward, Vector3 upwards=Vector3.up)

  通过静态函数 LookRotation 定义一个旋转，然后复制给这个 Quaternion。

- void ToAngleAxis(out float angle, out Vector3 axis)

  直接使用 axis 和 angle 设置这个 quaternion。
  
# 静态方法

- float Angle(Quaternion a, Quaternion b)

  返回两个 Quaternion a 和 b 之间的角度。结果角度在 0-180 之间。

  可以想象一个坐标系中的任意一个向量，例如 Vector3.right，分别按照 a b 进行旋转得到两个向量，求得的结果就是这两个向量之间的夹角。

- Quaternion AngleAxis(float angle, Vector3 axis)

  直接使用 axis 和 angle 创建一个 Quaternion。

- float Dot(Quaternion a, Quaternion b)

  两个 rotation 的点乘积。它意义是两个四元数所表示的旋转之间的相似度，其值大小反映了旋转状态的接近程度。

  - Dot(a, b) = 1：表示 a 和 b 表示完全相同的旋转
  - Dot(a, b) = -1：表示 a 和 b 表示完全反向的旋转，即 b 是 a 的逆旋转，b = Quaternion.Inverse(a)，a 旋转的角度比 b 多 360°
  - 0 < Dot(a, b) < 1：表示 a 与 b 的旋转方向大致相同。值越接近 1，相似度越高，例如 Dot(a, b) = 0.99 表示二者的旋转角度之差小于 2°
  - -1 < Dot(a, b) < 0：表示 a 与 b 的旋转方向相反。值越接近 -1，相反程度越高，例如 Dot(a, b) = -0.99 表示二者旋转角度之差接近 180°

  实际应用场景中，Quaternion 的点乘积常用于

  - 判断旋转状态是否完成
    
    在需要将物体旋转到目标方向的场景（如角色转向、摄像机跟踪），可通过点乘积判断当前旋转与目标旋转的差异。

    若点乘积接近 1（如 > 0.999），说明旋转已完成，可停止插值（如 Quaternion.Slerp或 Quaternion.RotateTowards），避免不必要的计算。

    ```C#
    Quaternion targetRotation = Quaternion.Euler(0, 90, 0);
    float similarity = Quaternion.Dot(transform.rotation, targetRotation);
    if (similarity > 0.999f) {
        Debug.Log("旋转完成！");
    }
    ```

  - 平滑过渡检测

    在插值旋转（如 Slerp）时，若当前旋转与目标旋转的相似度足够高（如 Dot > 0.99），可提前终止插值，提升性能。

    这种方式比直接比较欧拉角更可靠，避免了欧拉角的循环问题（如 360°与 -360°的差异）。

  - 反向旋转检测

    通过点乘积可快速判断两个旋转是否互为反向。

    若点乘积接近 -1（如 < -0.999），说明其中一个旋转是另一个的反向（如 b = Quaternion.Inverse(a)），可用于触发反向动作（如AI转身、动画切换）。

    ```C#
    Quaternion currentRotation = transform.rotation;
    Quaternion inverseRotation = Quaternion.Inverse(currentRotation);
    float reverseSimilarity = Quaternion.Dot(currentRotation, inverseRotation);
    if (reverseSimilarity < -0.999f) {
        Debug.Log("当前旋转与反向旋转对齐");
    }
    ```

    单位四元数要求：点乘积的结果仅在单位四元数（模长为1的四元数，如 Quaternion.identity或 Quaternion.LookRotation生成的旋转）下才有明确的几何意义（表示旋转夹角的余弦值）。

    若四元数未归一化，需先调用 Quaternion.Normalize()进行归一化处理。

- Quaternion Euler(float x, float y, float z)

  以欧拉角构建一个 Quaternion，顺序是 ZXY。

  或者说创建一个 Quaternion，其效果等价于按照欧拉角 x y z 旋转的效果。

- Quaternion FromToRotation(Vector3 fromDirection, Vector3 toDirection)

  创建一个 Quaternion，它的旋转效果等价于将 fromDirection 旋转到 toDirection。

- Quaternion Inverse(Quaternion rotation)

  返回 rotation 的逆旋转。

- Quaternion Lerp(Quaternion a, Quaternion b, float t)

  使用 t 对两个旋转 a 和 b 进行插值，并对返回结果归一化。

  它比 Slerp 快，但是如果 rotations 离的很远，角速度不是一致的。

  t 被 clamped 到 [0, 1] 之间。

- Quaternion LerpUnclamped(Quaternion a, Quaternion b, float t)

  t 不 clamped 到 [0, 1] 之间，结果也不会 clamped [a, b] 之间。

  它比 Slerp 快，但是如果 rotations 离的很远，效果很差。

- Quaternion LookRotation(Vector3 forward, Vector3 upwards=Vector3.up)

  Quaternion 只是表达一个逻辑上的旋转，具体应用要看在哪个坐标系，因为 Quaternion 的旋转轴要在一个坐标系中定义。

  在一个坐标系中应用一个 Quaternion，坐标系就是 Identity 的。

  LookRotation 定义了一个旋转， 它可以将 identity rotation 的 object（旋转=0）的 z 轴旋转到 forward 方向，然后再旋转 object 使 y 轴位于 forward-upwards 的平面内。

  这个旋转是如此的效果，它计算并确定了一个 axis 和 angle，但不一定应用到 identity rotation 的 object，可以应用到任何 object 上，都是绕着这个 axis 旋转这个角度。只是这个旋转通过 look at 方式定义而已。

  定义好这个旋转，具体效果就看再哪个坐标系应用这个旋转了。

- void Normalize()

  四元数的乘法、积分等运算会引入微小的浮点数误差（如10⁻⁶级别的偏差）。

  即使初始为先单位四元数，多次运算后模长也会逐渐偏离1。

  例如，在无人机姿态估计中，连续用陀螺仪角速度更新四元数（q_new = q_old * Δq，其中Δq为小旋转四元数），若未每次归一化，模长会从1逐渐变为1.01、1.02……最终导致旋转角度误差累积至10°以上，影响飞行稳定性。

  四元数未归一化会导致很多严重的问题。因此要保证四元数归一化。

- Quaternion RotateTowards(Quaternion from, Quaternion to, float maxDegreesDelta)

  每次以不超过 maxDegreesDelta 角度将 from 移动向 to。

- Quaternion Slerp(Quaternion a, Quaternion b, float t)

  球面线性插值。

- Quaternion SlerpUnclamped(Quaternion a, Quaternion b, float t)

