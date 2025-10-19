# Movement scripts

Package包含一些移动脚本。这些脚本在scene中沿着一个path实际移动object，通常是character。

移动脚本主要角色是搜索paths并跟随它们。

这些脚本完全是可选的，可以只使用pathfinding而不使用移动脚本，或者可以自己编写移动脚本。但是对于很多游戏来说，它为构建character提供了良好的基础。

Package提供了AIPath，RichAI，和AILerp3个脚本。

- AIPath
  - 使用于所有graph types，并且工作良好
  - 平滑跟随patsh并响应物理
  - 可以很好支持local avoidance
  - 支持2D和3D游戏中的移动
- RichAI
  - 为navmesh/recast graph特别设计，不支持其他graph类型
  - 在navmesh/recast graph上比AIPath更好，它可以更好的处理被推离路径的情形，并且更平滑的跟随路径
  - 比AIPath更好地支持off-mesh links
  - 可以很好支持local avoidance
  - 支持3D游戏的移动，但不支持2D
- AILerp
  - 使用线性插值沿着Path移动，不以任何方式使用物理
  - 精确沿着路径运动，没有任何偏离
  - 不支持local avoidance（适用于部落冲突类型游戏，单位之间没有碰撞，可以重叠在一起
  - 最快的移动脚本，因为移动非常简单。但是如果游戏需要任何物理真实的效果，只能使用其他脚本
  - 这不是Point Graph，Grid Graph/Navmesh也可以使用AILerp，可以使用modifier修改之后的移动路径，只是没有任何偏离效果和局部回避
  - 同时支持3D和2D游戏中的移动

简而言之，

- 如果使用navmesh-based的graph，使用RichAI
- 其他graph类型，根据需要选择AIPath或AILerp

所有移动脚本实现Pathfinding.IAstarAI接口，包括自定义移动脚本

一些有用且通用的属性：

- destination：agent应该移动到的world中的位置
- reachedDestination：如果ai到达destination则为true
- velocity：agent实际的移动速度
- desiredVelocity：agent期望达到的移动速度

如果想要character跟随特定物体，可以使用AIDestination Setter。它在幕后简单地在每一帧设置destination属性为target的位置
