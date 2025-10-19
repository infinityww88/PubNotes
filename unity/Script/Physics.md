# Physics

全局物理属性和辅助函数

Unity物理系统尽管只能模拟宏观低速的情形，当时依然实现了复杂的物理规则，已经能够绝大多数游戏的物理模拟需求。几乎任何你需要在游戏中手动模拟的牛顿物理公式都已经被包含在了物理引擎中，更不用说物理引擎已经考虑了各种物理模拟中的问题以及提供复杂的关节约束，这些都不是实现几个简单物理公式就能达成的。避免NIH问题，要尽可能利用已经存在的方案，在其基础之上发明新的东西，充分利用软件复利。物理引擎实现的物理公式远比你自己的简易方案更准确更全面，使用起来更简单。因此除了非常简单的不需要物理模拟的平移旋转的游戏需求，可以使用Transform手动实现，任何设计物理公式的Transform变换都要使用物理引擎，这是物理引擎存在的根本意义。当你需要在运动中插入一些非物理的运动效果时，可以通过collider/trigger/kinematic等等方法将自定义运动“插入”到物理引擎模拟过程中

物理引擎本质上就是使用一组物理学公式约束物体运动，这与手动变换物体transform是一样的，只是物理引擎更全面

## 物理引擎接口功能

- 施加影响

    施加力，力矩，速度/角速度，瞬移

- 物理查询

    GeometryCast，Check，Overlay，ClosestPoint，GetContacts

- 刚体配置

    质量，质心，kinematic，trigger，gravity，collider，threshold

- 配置引擎

    碰撞/约束解析因子，查询背面triangles

- 消息通知

    OnCollisionXXX，OnTriggerXXX

## 静态属性

- AllLayers

    包含所有layers的mask，0xffffffff，可以用于Physics.Raycast和任何需要layermask的函数，用来指定所有layers

- autoSimulation

    物理模块是否自动模拟。默认情况下，物理模型在play mode下以Time.fixedDeltaTime周期更新。这作为游戏循环的一部分自动发生。

    但是有些情形需要手动前进physics的模拟。一个特别的粒子就是在edit mode下物理模拟。另一个粒子是联网物理模拟，在从权威服务器收到数据时需要回滚时间以应用所有player输入。

    为了能够手动控制物理模拟，关闭autoSimulation，并使用Physics.Simulate来前进时间。注意MonoBehaviour.FixedUpdate仍然会以Time.fixDeltaTime为周期调用，但是物理模拟不会再自动前进了

- autoSyncTransforms

    当Transform组件发生变换时，是否自动同步transform的修改到physics系统

    当一个Transform组件修改时，它或者它的children上面的任何Rigidbody或者Collider可能需要重新position，rotate或者scale。

    当autoSyncTransform设置为false时，同步只会在FixedUpdate时物理模拟step之前发生。

    你还可以通过Physics.SyncTransforms手动执行transform的同步。

    当autoSyncTransforms设置为true时，不断地修改transform然后执行physics query可能导致性能损失。为了避免影响性能，如果你想连续地执行多个Transform修改和query，设置autoSyncTransforms为false

- bounceThreshold

    两个碰撞物体的相对速度，低于这个速度将不会发生bounce。默认=2（每秒2米）。必须为正

    Edit->Project Setting->Physics

- clothGravity: Vector3

    所有cloth组件的gravity，模拟风力

- defaultContactOffset：float

    新创建的colliders的默认contact offset

    两个collider在它们表面之间的距离小于它们各自的offset总和时就会发生接触。必须为正

    使得物理系统可以在物体的图形表示发生接触之前就强制执行碰撞约束

- defaultMaxAngularSpeed：float

    动态Rigidbody默认最大的角速度（弧度，默认50），物理模拟时rigidbody的角速度强制约束到这个限制

    加速度限制还可以为每个Rigidbody独立设置，Rigidbody.maxAngularVelocity

- defaultPhysicsScene：PhysicsScene

    Unity启动时自动创建的PhysicsScene。它被任何不申请local 3D physics的Scene共用

- DefalultRaycastLayers/IgnoreRaycastLayer

    选取默认raycast layers的layer mask常量，可以用于Physics.Raycast和任何需要选择默认raycast layers的方法

    默认raycast layers包括除了ignore raycast layer的所有layers

    首字母大写，应该是属性，即它在被读取的时候是是实时计算出来的

    IgnoreRaycastLayer和DefaultRaycastLayer互补

- defaultSolverIterations/defaultSolverVelocityIterations

    Rigidbody joints和collision contacts解析的精确程度（defalut 6/1），数值越高解析越精确，但是需要更高的计算量

    Edit->Project Setting->Physics

    solverIterations/solverVelocityIterations是在每个Rigidbody独立设置的属性，这个默认属性只影响新创建的Rigidbody，不会影响已经创建的

- gravity

    Scene中所有rigidbody应用的重力

    每个rigidbody可以通过useGravity属性关闭重力

- interCollisionDistance

    为cloth inter-collision设置最小separation distance

    小于这个距离的属于不同cloth物体的cloth粒子将被分开

- interCollisionStiffness

    控制当两个粒子小于inter-collision distance时如何相互推开当程度

- queriesHitBackfaces

    物理查询是否hit back-face triangles。默认所有物理查询只检测正面三角形

- queriesHitTriggers

    指定物理查询默认（raycasts，spherecasts，overlap tests，etc）是否hit trigger

    这个选项在请求level通过指定QueryTriggerInteraction参数覆盖

- reuseCollisionCallbacks

    垃圾回收器是否应该为所有collision消息函数重用一个collision实例，因为Unity只在主线程执行

    当Collision消息函数触发时（Enter，Stay，Exit），传递给它们的Collision对象在每次函数调用时被创建，而绝大多数情况我们只在函数内部使用它

    如果设置这个选项，只有一个Collision实例被创建，并用于每个collision消息，使得垃圾回收器不必回收大量的Collision进而提供性能

    除非你需要在消息函数之外引用collision对象，此时可以将这个选项关闭。但是你可以通过直接引用collision中你需要的数据而不直接引用collision对象

- sleepThreshold

    质量单位化的能量阈值（每kg多少能量），小于这个阈值的物体将进入sleep状态

## 静态方法

有关Geometry的方法，只有三种基本形状

    Box
    Capsule
    Sphere

各种Cast方法的参数

    基本配置：射线形状和方向
    结果输出：RaycastHit
    高级配置：maxDistance layerMask QueryTriggerInteraction

Cast返回bool，表示是否hit到gameobject

RaycastHit是真正接收hit info的对象，相当于真正的返回

投射长度、layerMask，QueryTriggerInteraction则是更高级的对cast的配置，因此这3个参数如果需要总是以这个顺序放置在返回结果RaycastHint之后

因此各种Cast方法的参数顺序可以这种方法记忆：bool Cast(射线基础配置，返回结果，射线高级配置)

    一个特例是BoxCast，box的旋转应该算是射线基本配置，但是放在了RaycastHit之后

各种CastAll方法对应于各自的Cast方法，但是返回结果类型是RaycastHit\[]，以接收多个hit信息，同时从参数中移除RaycastHit信息：RaycastHit[] CastAll(射线基础配置，射线高级配置)

Box/Capsule/Sphere的Cast查询与物理引擎执行对应形状的碰撞应该执行的是相同的代码，对碰撞位置和法向量等数据的计算也应该是相同的。RaycastHit信息是基于被扫描到的Collider计算的，碰撞点和法向量是在两个Geometry交集中被扫描到的Collider表面上的。碰撞点在交集表面中的位置不像Raycast那样有明确定义。碰撞点和法向量的意义在于，对于解析碰撞来说，通过在碰撞点沿着法向量对侵入物体施加一定的反向力可以使接触分离，对于解析Cast来说，可以用来在接触真正发生前进行回退以避免发生接触

CastNonAlloc方法使得不需要CastAll每次调用都重新分配RaycastHit数组，而是提前创建好RaycastHit数组，并作为参数传递进去，参数位置与RaycastHit位置相同，RaycastHit是结构体。CastNonAlloc返回存储在RaycastHit数组中的元素数量

### Cast方法

#### Geometry cast

- 基于Geometry cast的RaycastHit

- BoxCast/BoxCastAll/BoxCastNonAlloc

    形状参数：Vector3 center，Vector3 halfExtents（size/2） Quaternion orientation

    orientation放在RaycastHit之后

- CapsuleCast/CapsuleCastAll/CapsuleCastNonAlloc

    形状参数：Vector3 point1， Vector3 point2， float radius

    Capsule使用两个sphere定义胶囊体，因为两个sphere已经隐含了Capsule的orientation，因此不需要再传递orientation了

    Unity中通常用两个shere定义的Capsule模拟人体四肢

    CapsuleCollider的hight属性是整个Capsule的高度，即两个sphere中心的距离+两个radius

- SphereCast/SphereCastAll/SphereCastNonAlloc

    形状参数：Vector3 origin，float radius

- LineCast

    线段cast：Vector3 start， Vector3 end，子弹轨迹

#### Raycast

RayCast与GeometryCast一样，参数先定义形状和方向，然后是结果RaycastHit，最后是maxDistance，layerMask，QueryTriggerInteraction

- Raycast
- RaycastAll
- RayNonAlloc

### Overlap方法

Overlap方法是简化版的Cast，maxDistance=0即原地检查Geometry是否与scene中的Geometry有接触，且不接收RaycastHit结果，只返回接触的Collider[]

- OverlapBox/OverlapBoxNonAlloc
- OverlapCapsule/OverlapCapsuleNonAlloc
- OverlapSphere/OverlapSphereNonAlloc

### Check方法

Check方法是简化版的Overlap，甚至不接收发生接触的Collider[]，只返回bool标识是否发生了接触

- CheckBox
- CheckCapsule
- CheckSphere

### Physics system方法

- RebuildBroadphaseRegions
- Simulate

    当automatic simulation关闭时，手动模拟物理。模拟包含自动模拟的全部过程，包括物理回调函数的执行

- SyncTransforms

    将Transform的修改应用到物理引擎中。通常Transform的修改在FixedUpdate中执行物理step之前被应用，因此如果在physics step执行之前，修改transform并不会更新物理引擎中的物体的状态（transform），如果立刻基于修改的transform进行物理查询，将不会得到正确的结果。调用SyncTransform手动将transform数据更新到物理引擎中，使得之后立刻执行的物理查询仍然能得到正确的结果

### 计算方法

- BakeMesh
- Vector3 ClosestPoint(Vector3 point, Collider collider, Vector3 position, Quaternion rotation)

    Collider仅描述形状，描述位置和旋转的是Transform

    将Collider放置在position，旋转到rotation，计算collider上距离point最近的点

    当point位于collider内部或正好位于表面时，直接返回输入的point

    collider只能是BoxCollider，SphereCollider，CapsuleCollider，或者一个MeshCollider

- bool ComputePenetration(Collider colliderA, Vector3 positionA, Quaternion rotationA, Collider colliderB, Vector3 positionB, Quaternion rotationB, out Vector3 direction, out float distance)

    返回：如果两个collider在指定的位置和旋转重叠返回true

    计算将指定位置旋转的collider分离（不接触）需要的最小位移

    direction：最小位移的方向

    distance：最小位移的距离

    如果函数返回true，将第一个collider平移direction*distance将使两个collider分离，否则direction和distance未定义。相反将第二个collider平移-direction\*distance也能将两个collider分离

    其中的一个collider必须是BoxCollider，SphereCollider，CapsuleCollider或者一个convex MeshCollider，另一个可以是任何类型（concave MeshCollider）

    忽略backfaced三角形并且不考虑Physics.queriesHitBackfaces，因为它用于接触分离而不是物理查询

    用于实现自定义物理碰撞相应函数。一个特别的例子是character controller的实现，它需要当character的collider碰撞到周围物理物体时的特殊响应。这种情况下，通常首先调用OverlapSphere查询附近的colliders，然后使用ComputePenetration的返回结果调整character的位置

### 忽略碰撞

- void IgnoreCollision(Collider collider1, Collider collider 2, bool ignore = true)

    在碰撞检测系统中注册是否忽略两个collider之间的所有碰撞

    这可以阻止投射物与发射它们的物体的collider发射碰撞

    碰撞检测系统中实现了collider到collider的碰撞检测标记，而不需要将collider设置为不同的layer才能避免它们之间的碰撞

    这种注册在Edit Mode和Play Mode之间不是持久的，因此需要在Start函数中完成注册

- bool GetIgnoreCollision(Collider collider1, Collider collider2)

    查询碰撞检测系统是否忽略两个collider之间的所有collisions/triggers

- void IgnoreLayCollision(int layer1, int layer2, bool ignore = true)

    在碰撞系统中注册是否忽略两个layer的碰撞检测

    这将重置受影响的colliders的trigger状态，因此有可能收到OnTriggerEnter，OnTriggerExit，OnCollisionEnter，OnCollisionExit

    这与在Physics设置面部中设置layer碰撞矩阵是一样的，但是是在运行时进行的

- bool GetIgnoreLayerCollision(int layer1, int layer2)

    查询碰撞检测系统中是否忽略两个layer的所有碰撞

## RaycastHit

- collider：hit到的collider
- distance：ray原点到接触点的距离
- normal：接触点在collider表面上的法向量
- rigidbody：collider上的rigidbody，如果collider没有挂载到一个rigidbody上，返回null
- textureCoord/textureCoord2/lightmapCoord：接触点在collider的Mesh上的各种uv坐标，需要collider是MeshCollider
- triangleIndex：接触点在collider的Mesh上的三角形索引，需要collider是MeshCollider
- transform：collider的transform

## Collider

所有Collider的基类，具体类包括BoxCollider，SphereCollider，CapsuleCollider，MeshCollider

如果一个带有Collider的object在gameplay时需要移动，你应该在它上面添加一个Rigidbody组件。如果你不想让这个object被物理系统模拟，可以将它设置为kinematic

### 属性

- attachedRigidbody：collider挂载的rigidbody
- bounds：世界空间中的轴对齐包围盒
- contactOffset：计算碰撞时的偏移，使得真实的碰撞发生早于或晚于collider表面，可以认为collider的表面厚度
- enabled：enabled colliders将与其他colliders发生碰撞，disabled collider不会
- isTrigger
- material：应用到collider表面的物理材质
- sharedMaterial：collider共享的物理材质

### 方法

- ClosestPoint

    collider上最接近指定世界位置的点

- ClosestPointOnBounds

    collider的bounding box上最接近指定世界位置的点。可以被用来计算爆炸时的hit point

- Raycast

    判断指定射线是否与本collider碰撞。忽略其他collider

### 消息

- OnCollisionEnter/Stay/Exit

    参数是Collision

- OnTriggerEnter/Stay/Exit

    参数是collider，只是发生碰撞的collider，没有其他信息

    Trigger仅用于触发机制，不关心发生碰撞的位置

## Collision

- contactCount
- GetContact/GetContacts：返回接触信息ContactPoint
- gameObject/collider/rigidbody/transform
- impulse

    用于解析发生这次碰撞应用的全部冲量

    通过将应用到这次碰撞所有contact points的冲量累加到一起计算得到

    要得到对应的解析force，将impulse除以上一帧的fixedDeltaTime

- relativeVelocity

    发生碰撞时两个collider的相对速度

## ContactPoint

- point/normal
- thisCollider/otherCollider
- separation：接触侵入距离，将两个collider分离需要的距离

## 数据结构关系

    rigidbody挂载colliders
    collider碰撞时传递collision对象
    collision对象包含所有接触点信息ContactPoint和两个Collider的相对状态（冲量，相对速度）
    每个ContactPoint包含接触点位置point，法向量normal，接触点两端的collider，接触距离

## 碰撞矩阵

- Collision
  - 都不是Trigger
  - 至少有一个Rigidbody
- Trigger
  - 都不是static
  - 至少有一个Trigger

Static是没有Rigidbody/Kinematicbody的Collider/Trigger

因为发生碰撞需要进行碰撞解析，物理引擎需要修改object的transform来防止侵入以及实现反弹和摩擦。因此只有对Rigidbody进行碰撞解析才有意义，这就是为什么必须至少有一个rigidbody。对两个KinematicBody进行碰撞解析违反了Kinematic的定义，KinematicBody只能被脚本控制。不能有任何一个是trigger，因为trigger只触发消息，不影响物体运动

    collision是阻碍，trigger是穿越
    collision通知碰撞的详细信息，trigger只通知碰撞到的collider

Trigger不需要碰撞解析，只是在两个Geometry发生重叠的时候发送通知即可。因此至少有一个需要配置成trigger。Static Collider/Trigger是用来影响RigidBody和KinematicBody的，Rigidbody和Kinematicbody是角色，Static Collider/Trigger是环境，环境本意是保持静止不变的，在Static之间触发消息对于游戏而言没有意义，这对物理引擎也是一种优化。游戏逻辑存在于Rigidbody/KinematicBody之中

无论Collision还是Trigger消息，都是同时发送给两个物体的。对于Rigidbody/KinematicBody，消息只发送给Rigidbody组件所在的GameObject，对于Static Collider/Trigger则发送给Collider组件所在的GameObject
