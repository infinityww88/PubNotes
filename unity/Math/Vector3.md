静态方法

- float Angle(Vector3 from, Vector3 to)

  计算两个向量之间的夹角。

  角度是按从 from 到 to 方向算的。返回的角度总是在 0-180 度，因为方法总是返回两个向量之间的最小角度。

- float SignedAngle(Vector3 from, Vector3 to, Vector3 axis)

  返回 from -> to 的角度。from-to 定义了旋转平面。旋转轴按照左手定则定义。axis 参数给出一个参考，来决定返回的角度的正负号。

  如果 axis 在 from-to 旋转轴的正侧，结果为正，反之为负。

- Vector3 ClampMagnitude(Vector3 vector, float maxLength)

  返回 vector 的一个副本，并且 magnitude 被 clamp 到 maxLength，即长度小于 maxLength，vector 不变，长度超过 maxLength，vector 的长度限制到 maxLength。

- Vector3 Cross(Vector3 lhs, Vector3 rhs)

  计算两个向量的叉乘积，按照左手定则，从 lhs 到 rhs 方向。结果向量垂直 lhs 和 rhs，其 magnitude 等于两个向量的长度的乘积再乘以其夹角的正弦值。 

  Vector3.Cross（叉积）是Unity中用于计算两个三维向量垂直向量的核心数学工具，其结果向量的方向由左手定则确定（伸开左手，四指从第一个向量转向第二个向量，拇指指向结果方向），模长等于两个向量模长的乘积与它们夹角正弦值的乘积（|a×b| = |a||b|sinθ）。在3D游戏开发中，叉积的功能覆盖方向判断、法线计算、物理模拟等多个关键场景。

  左手定则由两个形式：一个是握拳，四指从第一个向量转向第二个向量，拇指方向就是结果向量方向；另一个是拇指、食指、中指构成坐标系，拇指指向第一个向量，食指指向第二个向量，中指方向就是结果向量方向。

- float Distance(Vector3 a, Vector3 b)

  计算点 a b 之间的距离。

- float Dot(Vector3 lhs, Vector3 rhs)

  计算两个向量的点乘积。模长等于 rhs 在 lhs 向量上的投影向量的长度，符号与夹角相关。夹角小于 90 度为正，大于 90 度为负。

- float Lerp(Vector3 a, Vector3 b, float t)

  t 被 clamp 到 [0, 1] 之间。

- float LerpUnclamped(Vector3 a, Vector3 b, float t)

  t 不会 clamp 到 [0, 1] 之间，在 [0, 1] 之外也正常返回值。

- Vector3 Max/Min(Vector3 lhs, Vector3 rhs)

  由 lhs rhs 各个分量最大值构成的新 vector。

- Vector3 MoveTowards(Vector3 current, Vector3 target, float maxDistanceDelta)

  将 current point 移动向 target，每次不超过 maxDistanceDelta。

- Vector3 OrthoNormalize(ref Vector3 normal, ref Vector3 targent)

  Normalizes normal。Normalizes tangent，并旋转它使它垂直 normal。

- Vector3 OrthoNormalize(ref Vector3 normal, ref Vector3 targent, ref Vector3 binormal)

  bi-normal：第二法线。

  Normalizes normal。Normalizes tangent，并旋转它使它垂直 normal。Normalizes binormal，并旋转它使它垂直 normal-tangent。

- Vector3 Project(Vector3 vector, Vector3 onNormal)

  将 vector 投影到 onNormal 向量上。

- Vector3 ProjectOnPlane(Vector3 vector, Vector3 onNormal)

  vector 在 plane 上的投影。因为是垂直投影，不需要给出 plane 上的点，只需给出 onNormal，因为所有以 onNormal 为法线平面，vector 的投影都一样。

  onNormal 不需要标准化。

- Vector3 Reflect(Vector3 inDirection, Vector3 inNormal)

  inDirection 和 inNormal 的意义是向量。向量可以在任何地方。因此可以想象这两个向量在空间中的任何一点（例如就是原点）。

  给出 inDirection 和 inNormal，计算反射向量。

  inNormal 向量定义一个 plane.

- Vector3 RotateTowards(Vector3 current, Vector3 target, float maxRadiansDelta, float maxMagnitudeDelta)

  类似 MoveTowards，但是 MoveTowards 将参数解释为 point 位置，以直线移动的方式将 current 每次以不超过 maxDistance 的距离移动向 target。

  RotateTowards 将参数解释方向，将其想象为位于原点的两个向量，以旋转的方式，将 current 每次以不超过 maxRedinasDelta 的角度移动向 target。

  如果 current 和 target 的模长不同，模长也会在 rotation 期间线性插值，模长变化的最大长度为 maxMagnitudeDelta。

  如果 maxRadiansDelta 为负数，则解释为反方向角速度，current 以此原理 target，直到 target 的反方向角度。

- Vector3 Scale(Vector3 a, Vector3 b)

  按每个分量相乘，返回结果向量，即 (ax * bx, ay * by, az * bz)。

- Vector3 Slerp(Vector3 a, Vector3 b, float t)

  Lerp 将参数向量解释为 point 位置，Slerp 将参数向量解释为方向。将方向 a 按照球面最短路径插值到方向 b。插值的同时模长也以 t 线性插值。

  t 被 clamp 到 [0, 1] 之间。

- Vector3 SlerpUnclamped(Vector3 a, Vector3 b, float t)

  球面插值可以超过 a 和 b 的向量，t 也不限制在 [0, 1] 之间。

- Vector3 SmoothDamp(Vector3 current, Vector3 target, ref Vector3 currentVelocity, float smoothTime, float maxSpeed = Mathf.Infinity, float deltaTime = Time.deltaTime)

  类似 Mathf 对 float 的 SmoothDamp（spring-damper 机制），只是这个函数针对向量。参数 current 和 target 解释为 point 位置。

