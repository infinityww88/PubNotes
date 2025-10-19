# Quaternion

## Overview

- 表示围绕一个axis的旋转一定angle的旋转
- 紧凑的：一个axis，一个angle
- 没有万向锁问题
- 容易差值
- 可以用\*串联两个Quaternion，右手边的Quaternion是左手边的parent，还可以用*变换一个Vector3
- 想象Quaternion变换Vector3时，因为Vector和axis都没有位置，因此必须找到一个参考位置，最直白的就是原点，从原点出发的vector3围绕经过原点的axis旋转angle角度
- Unity内部使用Quaternion表示所有旋转
- 理解Quaternion和Vector3的关系时，总是将它们对齐到原点处来理解，axis经过原点，Vector3从原点出发

## 静态成员

- identity：单位旋转（无旋转）

## 成员属性

- eulerAngles：表示旋转的欧拉角

## 成员方法

- SetFromToRotation
  - Vector3 fromDirection, Vector3 toDirection
  - 将Quaternion设置为将fromDirection旋转到toDirection的旋转
- SetLookRotation
  - Vector3 lookDirection，Vector3 hintUp = Vector3.up
  - 将Quaternion设置为一个从identity坐标系到一个forward指向lookDirection，up落在lookDirection和hintUp确定的平面上的坐标系的旋转
- ToAngleAxis
  - 将Quaternion转换为axis和angle

## 静态方法

- 计算方法
  - Angle(Quaternion a, Quaternion b)
    - 经过原点的单位向量按照a旋转得到ia，按照b旋转得到ib，ia与ib的夹角就是Angle的返回值
  - Dot
  - Normalize
- 创建方法
  - AngleAxis
    - 以angle和axis创建一个Quaternion
    - axis的解释由使用这个Quaternion的上下文决定
  - Euler
    - 以zxy欧拉角的方式创建一个Quaternion
  - FromToRotation(Vector3 fromDirection, Vector3 toDirection)
    - 创建一个将fromDirection旋转到toDirection的旋转
  - Inverse
    - 返回Quaternion的逆
  - LookRotation(Vector3 forward, Vector3 hintUp = Vector3.up)
    - 创建一个旋转，将identity坐标系的旋转到forward指向参数forward，up落在参数forward和hintUp定义的平面上的坐标系
- 差值方法
  - Lerp(Quaternion a, Quaternion b, float t)
    - 使用t在a和b直接插值，并将结果标准化
    - t被限制在[0, 1]
    - Lerp比Slerp快，但是a和b相差较远时，插值的结果很差
  - LerpUncalamped
    - 和Lerp相同，但是不限制t在[0, 1]，因此t=2时将得到两倍的a-b差值
  - Slerp
    - 球面差值，真正平滑的Quaternion插值
  - SlerpUncalamped
  - RotateTowards(Quaternion from, Quaternion to, float maxDegreesDelta)
    - 类似插值，但不是使用百分比t，而是使用步长maxDegreesDelta
    - 从from开始沿着向to方向的旋转前进maxDegreesDelta角度
    - 旋转从不溢出，如果from到to的方向小于maxDegreesDelta，将直接返回to
    - 负数maxDegreesDelta将沿着from到to的反向步进，终点不是to，而是to的反向，等价与将to反向，然后以maxDegreesDelta的绝对值调用RotateTowards
  
## 操作符

- operator\*
  - 联合两个旋转lhs和rhs
  - 结果就像顺序应用lhs和rhs，lhs在先，rhs在后，rhs在lhs变换之后的基础上进行变换，lhs相对Quaternion应用的坐标系，rhs相对于lhs应用之后的坐标系
  - lhs是rhs的parent
  - 对vector3的变换 lhs \* rhs * vector3

## Tips

- 立即Quaternion时，总是从identity开始，每个旋转都是从identity开始
- 理解Quaternion.AngleAxis(30, Vector3.up)到Quaternion.AngleAxis(60, Vector3.up)，不要理解为从30到60，而是前者从0到30，后者从0到60
- 欧拉角zxy顺序指的是与vector3的结合顺序，如果表示为Quaternion乘法应该是Qy \* Qx * Qz * vector3，这与矩阵的结合顺序一样，另一个与矩阵相同的地方是lhs为rhs创建reference frame（参考坐标系，右边的是坐标的子变换，右边的在左边的变换后的坐标系中变换
- Quaternion只是在程序中表示的变换，就像用Vector3表示位移一样，在Unity内部Quaternion或Vector3统统转换为矩阵，Unity内部统一使用矩阵表示变换，Quaternion的联合就是矩阵的联合，以矩阵的方式理解Quaternion的连乘
- 当把Quaternion连乘的结果赋给transform时，还需要在参考一次使用的坐标系
  - 如果是localRotation：参考父坐标系
  - 如果是Rotation：参考世界坐标系
  - 如果是Space.Self：参考自身坐标系
- Matrix4x4同时表示Translate，Rotation，Scale。它包含的是创建这个矩阵所有矩阵链的累积效果，因此立即一个matrix需要立即它是如何被创建的，它的translate，rotation，scale如何应用依赖于创建它使用的矩阵和它们的顺序。Matrix4x4.TRS创建的矩阵等价于创建3个分别对应Translate，Rotation，Scale的矩阵然后以TRS的顺序相乘到一起，Matrix4x4.TRS内部可能就是这样实现的。如果需要不同与TRS的顺序的矩阵，则需要手工创建T、R、S矩阵然后按照需要的顺序将它们相乘在一起。重要的是，通过一组矩阵相乘创建单一矩阵，每个矩阵都应该只表示单一的变换，或者是translate，或者是rotation，或者是scale，因为只有这样才能理解最终的矩阵的变换效果。任何包含一个以上变换的矩阵都可以拆分成多个只包含单一变换的矩阵相乘的结果。这就是把一个复杂的事情分解成大量单一简单的小组件来理解整体的方法。欧拉角也是将一个变换分解为围绕x、y、z3个轴的旋转，然后以zxy的顺序相乘等结果
