# Physics2D

具有大部分Physics3D相应的属性和方法，下面只列出不同之处

尽管Unity尽量将2d与3d引擎的接口往一致方向设计，但是根本上还是两个不同的引擎，即使整体概念是相同的，但是在使用方法与数据上仍然不是一致的。因此在使用的时候不能简单的类比，时刻记住2D与3D物理引擎的重要区别，它们可能导致截然不同的使用方式

## 静态属性

### 调试选项（仅用于Editor中）

- alwaysShowColliders
- showColliderAABB
- showColliderContacts
- showColliderSleep
- colliderAABBColor
- colliderAsleepColor
- colliderAwakeColor
- colliderContactColor
- contactArrowScale

### 碰撞解析

- baumgarteScale/baumarteTOIScale

    控制碰撞overlap解析的速度

### 平移运动

- linearSleepTolerance

    如果线性速率超过这个阈值，rigidbody不能sleep

- maxLinearCorrection

    解析约束时最大线性位置修正长度，可以帮助防止超越

- maxTranslationSpeed

    每次物理更新时最大线性速度，即线性速度约束到此上限。提升这个值可能引起大量问题。意味着不要使用这个值

- velocityThreshold

    任何相对速度小于这个阈值的碰撞将被处理为无弹性，即相互不反弹，只是简单的靠在一起

### 旋转运动

- angularSleepTolerance
- maxAngularCorrection
- maxRotationSpeed

### 迭代步骤

考虑velocity/position执行物理解析时的迭代次数

- velocityIterations
- positionIterations

### 其他配置

- callbacksOnDisable

    bool。控制当Collider2D被disable时，相应的OnCollisionExit2D或者OnTriggerExit2D回调是否应该被调用。如果当collider2D与其他的collider2D正发生碰撞时将**collider2D** disable，callbacksOnDisable=true将使collider2D收到exit消息，否则不会

- queriesStartInColliders

    当执行Ray/Line cast时，如果起点在一个Collider2D内部，queriesStartInColliders决定检测结果是否包含这个collider2D

- timeToSleep

    当一个rigidbody速度和角速度降到sleep阈值时，还需要经过这个时间才能sleep

### 方法

### 查询方法

#### Cast方法

查询方法概念上等价于在场景中以指定方向拖拽投射的图形。途中任何发生接触的物体都会被检测到

与3D物理查询不同，2D单体物理查询直接返回RaycastHit2D，它是一个结构体，通过判断collider属性判断是否hit到任何物体上

除了计算接触点的point和normal（基于被投射的物体表面），还返回一个centroid属性，如果把投射形状的中心放置在这个位置上，它正好与被投射的collider在接触点发生接触

查询方法可以接受一个ContactFilter2D对象，用来过滤查询的物体

对于多元查询，同时支持数组参数和List参数，List参数在空间不够用时自动扩展。返回查询到的结果个数。Physics2D提供了和Physics对应的CastAll和CastNonAlloc方法，但是2D基本的Cast以及包括了这些功能，因此CastAll/NonAlloc都是不必要的

如果射线图形的原点初始就在一个Collider内部甚至边界完全没有交集，这个collider也会被检测。这种情况下接触点的法向量无法计算，因为normal是基于被检测到的collider边界上的接触点计算的，此时返回direction的反向单位向量，且fraction=0

参数顺序：位置-形状-方向-ContactFilter-RaycastHit2Ds-distance

    BoxCast/All/NonAlloc
    CapsuleCast/All/NonAlloc
    CircleCast/All/NonAlloc
    LineCast/All/NonAlloc
    RayCast/All/NonAlloc

#### Overlap方法

Overlap方法对应3D中的Overlap方法，去掉Cast的distance方法，即不拖动图形，而是立即判断与指定图形重叠的Collider2D，而且只返回Collider2D，即与哪些Collider2D碰撞，不返回详细的碰撞信息RaycastHit2D

    OverlapBox/All/NonAlloc
    OverlapCapsule/All/NonAlloc
    OverlapCircle/All/NonAlloc
    OverlapPoint/All/NonAlloc
    OverlapArea/All/NonAlloc

OverlapPoint对应Cast的Line&Ray，因为distance=0
OverlapArea的形状是一个AABB矩形，通过两个vector2定义
Line和Ray的区别在于Line使用两个vector2定义一个线段，Ray使用（原点，方向，长度）定义一条射线，它们原理上都是一个点在世界中移动一定的距离

#### GetRayIntersection方法

GetRayIntersection方法计算3D空间中任何一条射线与2D collider的碰撞，返回发生碰撞的信息RaycastHit2D。这个方法用于从Screen发射ray选中Collider2D。因为碰撞是发生在3D空间中，因此RaycastHit2D中的normal是没有意义，因此被重置为0

    GetRayIntersection/All/NonAlloc

#### GetContacts

int (Collider2D collider, Collider2D[] colliders)

查询与指定collider接触的Colliders2D或者ContactPoint2Ds

如果是查询接触点信息ContactPoint2D，只有碰撞矩阵中那些能触发OnCollision消息的组合才能被GetContacts返回，即【至少有一个Rigidbody & 都不是trigger】

如果是查询碰撞体信息Collider2D，则去掉上面中的trigger条件，即至少有一个rigidbody

其他组合不能再Gettacts中返回

如果查询ContactPoint2D，被设置为Trigger的Collider2D不会被返回，因为Trigger没有接触点的概念

输出支持数组和List

支持ContactFilter2D，但是查询接触点信息时，trigger永不返回，即使filter的useTrigger=true

查询源参数可以是

    一个collider
    一个rigidbody2d：所有collider2d的全部接触点
    两个collider：与两个collider都接触的接触点

#### ClosestPoint

Vector2 (Vector2 position, Collider2D collider)

计算collider边界上距离position最近的位置

任何Collider2D形状

当position在collider内部，或者collider是disable的，直接返回position

#### Distance

ColliderDistance2D (Collider2D, Collider2D)

计算两个collider2d之间的最小距离，用于计算使两个Collider正好发生接触（分离或拉近）需要的方向和长度，以及它们接触时接触点分别在各自图形边界上的位置

#### IsTouching

bool IsTouching(Collider2D collider1, Collider2D collider2)

查询两个Collider2D当前是否接触。查询结果是基于上一次物理系统模拟的结果。如果你在当前FixedUpdate更新了Collider2D，当前物理引擎还没有模拟最新的时间步长。这个方法返回与collision/trigger回调相同的结果。每次物理模拟发送的碰撞结果都保存在全局状态中，就像Event，Input一样可以每帧查询

bool IsTouching(Collider2D collider, ContactFilter2D contactFilter)

检测collider是否与任何filter过滤出来的collider发送碰撞

bool IsTouchingLayers(Collider2D collider1, int layerMask)

检测collider是否与layerMask上任何的collider发送碰撞

### SetLayerCollisionMask

void (int layer, int layerMask)

设置指定layer与其他layer的碰撞掩码

layerMask每一个bit对应场景中的一个layer，它的值（0/1）表示这个layer与参数1指定的layer是否发送碰撞

## Tips

所有的物理查询方法都在Physics，Physics2D中定义

Collider2D提供了基于这个Collider形状的代理查询方法，即利用Collider信息计算相应的参数调用Physics2D中的查询方法

Rigidbody2D则提供了基于所有挂载的Collider的代理查询方法

Rigidbody/Collider只提供了代理的计算ClosestPoint的方法
