# Vector3

## 静态属性

- forward/back/up/down/left/right
- one/zero/negativeInfinity/positiveInfinity

## 属性

- magnitude/sqrmagnitude
- normalized
- x/y/z
- this[0/1/2]，对应this.x/y/z

## 构造函数

- Vector3(float x, float y, float z)
- Vector3(float x, float y)

## 方法

- Equals
  - 二进制笔记
  - 浮点近似比较使用operator==
- Set(float x, float y, float z)

## 静态方法

- 计算方法
  - float Angle(Vector3 from, Vector3 to)
    - 返回两个vector直接的角度（不是弧度）
    - 无符号，[0, 180]
  - SingedAngle(Vector3 from, Vector3 to, Vector3 axis)
    - [-180, 180]
    - axis用于判断角度正负，基于左手定则，拇指指向axis的方向，四指方向就是角度为正的方向
  - Vector3 Cross(Vector3 lhs, Vector3 rhs)
    - 两个向量的叉乘积
    - 结果向量平行参数向量构成的平面，模长等于参数向量构成的平行四边形的面积
    - 平面的法向量有两个方向，叉乘积法向量的方向有左手定则确定，有两种左手定则方式
      - 四指按照从lhs到rhs旋转方向弯曲，拇指方向即结果向量方向
      - 拇指指向lhs方向，食指指向rhs方向，中指指向即结果向量方向
  - Distance：返回两个向量的差向量的模长，(a - b).magnitude
  - float Dot
    - 两个向量的点乘积
    - lhs.magnitude \* rhs.magnitude * cos(lhs&rhs)
    - 两个向量夹角超过90度，cos为负数，点乘积为负
    - 结果等于一个向量在另一个向量上的投影长度，负数表示在投影在被投影向量的反方向上
  - Vector3 Project(Vector3 vector, Vector3 onNormal)
    - 计算一个向量在另一个向量上的投影向量
    - 类似Dot，但是Dot只返回投影长度，Project返回投影的向量，它和onNormal平行
  - Vector3 ProjectOnPlane(Vector3 vector, Vector3 planeNormal)
    - 计算一个向量在一个平面上的投影向量
    - 平面方向由法向量planeNormal指定
  - Vector3 Reflect(Vector3 inDirection, Vector3 inNormal)
    - 从一个平面反射一个入射向量为出射向量
    - 平面方向有inNormal指定
- 插值方法
  - Vector3 Lerp(Vector3 a, Vector3 b, float t)
    - t在[0, 1]之间
    - 用t在a和b之间进行插值
    - = (b - a) * t
  - LerpUnclamped：无限制lerp，= (b - a) * t
  - Slerp(Vector3 a, Vector3 b, float t)
    - 与Lerp的不同是，vector被当最纯粹的方向，而不是空间中的点，因此插值的角度变换是线性的
    - Magnitude也随着t插值，但是主要用途还是方向的线性插值（球面插值）
  - SlerpUnclamped
  - Vector3 SmoothDamp(Vector3 current, Vector3 target, ref Vector3 currentVelocity, float smoothTime, float maxSpeed = Mathf.Infinity, float deltaTime = Time.deltaTime)
    - 平滑地将一个向量变化到目标向量
    - current将向弹簧一样跟踪target，但不会超过target
    - 最常用的用途是平滑跟踪摄像机
    - currentVelocity被函数内部使用，因为这个函数是基于状态的，多次函数调用之间是有关系的，但是函数又不能自己保存状态，它可能被当前场景中多个脚本调用，因此就像IMGUI一样，调用者为函数调用提供一个持久状态，每次调用将其传递进去，这样函数就能基于上次的状态继续计算了。因此传递currentVelocity就是为函数一个session的多次调用声明了一个持久变量，初始值设为Vector3.zero
    - smoothTime调整的就是弹簧的弹性，即追踪的速度，smoothTime越小，追踪得越快。它描述的是在target保持不同的情况下，current追上它的时间
    - target是自由变化的，SmoothDamp试图使用指定的参数平滑地追踪target
    - maxSpeed：可选地限定最大速率，currentVelocity不超过maxSpeed
    - deltaTime：自上次调用SmoothDamp之后的时间
  - Vector3 MoveTowards(Vector3 current, Vector3 target, float maxDistanceDelta)
    - 类似lerp，但不是指定百分比，而是指定步长
    - 当current与target的距离小于maxDistanceDelta时，返回target
    - 如果maxDistanceDelta为负，移动方向是到target的反方向
    - MoveTowards通常用于两个平行向量
  - Vector3 RotateTowards(Vector3 current, Vector3 target, float maxRadiansDelta, float maxMagnitudeDelta)
    - 类似MoveTowards，但是施加了最大偏角约束
    - 将current向量旋转到target
    - 本次旋转偏角不超过maxRadiansDelta，模长变化不超过maxMagnitudeDelta
    - maxRadiansDelta和maxMagnitudeDelta独立约束，它们很可能不会同时达到target，先达到的那个在之后的调用中就保持不变
    - 如果maxRadianDelta为负，则方向旋转知道与target方向对立，然后停止
    - RotateTowards通常用于两个有夹角的向量，如果真的只表示方向，最好单位化，免去maxMagnitudeDelta的计算
- 构建方法
  - Vector3 Max(Vector3 a, Vector3 b)：返回x、y、z组件最大值构成的vector
  - Min
  - Scale：返回x/y/z组件逐个相乘的结果向量
  - Vector3 ClampMagnitude(Vector3 vector, float maxLength)：返回vector拷贝，模长限制不超过maxLength
  - Vector3 Normalize(Vector3 value)：返回一个向量的标准向量，如果向量太小，将返回零向量
  - void OrthoNormalize(ref Vector3 normal, ref Vector3 tangent)
    - 正交标准化
    - 标准化normal和tangent，并且在normal和tangent确定的平面内使tangnet垂直于normal
  - void OrthoNormalize(ref Vector3 normal, ref Vector3 tangent, ref Vector3 binormal)
    - 先调用OrthoNormalize(ref normal, ref tangent)
    - 标准化binormal（第二法向量），使得它同时垂直于normal和tangent
    - binormal的方向应该是binormal于plane夹角小于180度的方向，如果binormal于plane平行，返回的binormal可能就是任意一个垂直plane的方向
    - 空间中的点通常在标准的XYZ坐标系中指定，但是它们仅仅number而已，你可以在任何3个向量构成的坐标系中解释它们
    - 创建自己的坐标系在有效情况下很有用，例如你想沿着任意方向缩放一个mesh而不仅仅是沿着x/y/z方向。这种情况下通常只需要确定一个轴，另外两个轴无关紧要，只要它们单位化并相互垂直就可以。OrthoNormal就是为这种情况计算可以构建坐标系的3个单位向量
    - Matrix4x4中左上角的3x3矩阵表示旋转和缩放矩阵，另一种解释它的方式是，它的3列分别对应它确定的坐标系的x轴单位向量，y轴单位向量，z轴单位向量。如果你拥有了3个可以构建坐标系的向量，就可以直接将它们设置到3x3的矩阵，而不需要通过Matrix4x4.Rotate/Scale创建对应的矩阵，即你不需要知道由这3个向量构成的矩阵的rotation和scale是多少。第4列前3个元素表示位移向量，如果有这个向量就设置，没有就设置为0。最后一行是(0, 0, 0, 1)。通过这种方法构建的矩阵就是直接由构建它的3个向量确定的坐标系对应的矩阵

## 操作符

- operator+ operator-：一个向量加上减去另一个向量
- operator* operator/：一个向量乘以除以一个表量
- operator== operator!=：两个向量是否近似相等，使用Mathf.Epsilon作为容差

