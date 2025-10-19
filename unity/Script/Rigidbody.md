# Rigidbody

通过物理引擎控制一个object的位置

为object添加一个Rigidbody组件将使物理引擎控制它的运动（更新transform）

Rigidbody提供了script API可以对object施加force，以物理真实的方式控制它

在script中，规范方式是在FixedUpdate中进行物理操作，例如对object施加力，更新Rigidbody设置，而不是在Update中执行，因为FixedUpdate是以帧独立的方式调用的，并且可以任意设置它fixDeltaTime

FixedUpdate在每个物理更新step前立即调用，因此任何在FixedUpdate中的物理修改将会被立即处理

开始使用Rigidbody时的一个常见问题是游戏物理看起来以慢动作运行。这通常是模型的缩放引起的。默认的重力设置假设一个世界单位对应一米的距离。对于非物理的游戏，即使你的全部模型都放大100倍也没什么问题。但是当使用物理引擎之后，它们会被当作非常大的物体。速度等于距离/时间，想象一下时间不变的情况下距离被缩放的结果。物理引擎总是以1uint=1m的标准模拟。缺少适合大小的参照物无法给出真实的运动感。因此在物理游戏中，保持你的模型接近真实大小

## 运动分解

Rigidbody的运动只有两个独立的运动：位移运动和旋转运动

所有Rigidbody运动属性都可以归纳为这两种运动的属性

rigidbody的mass用来计算如何应用力和力矩到这两种运动

位移运动和旋转运动都是分解在x/y/z轴上正交独立计算的，因此Rigidbody本质上是6个相互独立的运动的合成

    沿x的移动
    绕x的旋转
    沿y的移动
    绕y的旋转
    沿z的移动
    绕z的旋转

这正是Rigidbody的6个自由度DOF，DOF反过来说明Unity就是独立计算这六个运动的，通用关节ConfigurableJoint就是可以分别设置每个DOF的约束的

### 位移运动

- 属性：velocity，drag，position
- 方法：AddForce

### 旋转运动

- 属性：angularVelocity，maxAngularVelocity，angularDrag，rotation
- 方法：AddTorque

## 属性

- velocity

    Vector3，沿着3个轴的移动速度

- drag

    velocity的阻力，减慢物体的移动，drag越大，速度减慢得越快

- angularDrag

    角速度阻力，减慢物体的旋转，drag越大，旋转减慢得速度越快

- angularVelocity

    Vector3，绕3个轴的旋转角速度，弧度每秒

    绝大多数情况下你不应该直接修改它，否则将导致不真实的行为

- maxAngularVelocity

    rigidbody的最大角速度，弧度每秒，默认是7，范围（0，infinity）

    rigidbody在模拟时，角速度被限制到这个上限，以防止不稳定的情况发生。如果这阻止了期望的快速旋转的物体，例如车轮，可以为每个rigidbody独立设置这个限制

- maxDepenetraionVelocity

    rigidbody立刻碰撞侵入状态时的最大速率float。使用这个选项来使得你的物体以比默认方式更平滑地离开碰撞

- centerOfMass

    相对于transform原点的质心位置

    如果不从script中设置质心位置，它将从挂载到rigidbody的所有colliders中自动计算（包括children collider）

    如果在script中设置了质心位置，它将不再自动重新计算，即使添加、移除、移动colliders

    恢复自动计算质心位置，调用Rigidbody.ResetCenterOfMass

    设置质心位置通常在模拟车辆时非常有用，更低的质心，车辆运动更稳定

    质心相对于transform的position和rotation，但是不受transform的scale影响

- collisionDetectionMode

    这个rigidbody的碰撞检测模式

    连续碰撞检测可以防止快速移动的物体穿越其他物体，但是连续碰撞检测只是提高了精度，仍不是无限准确的，对于超级快速的移动物体例如子弹，需要手动执行raycast进行检测

    连续碰撞只支持Sphere/Capusult/Box碰撞体

  - Discrete：离散碰撞检测
  - Continuous：与静态collider碰撞的连续检测
  - ContinuousDynamic：与静态/动态collider碰撞的连续检测
  - ContinuousSpeculative：带预测的与静态/动态collider碰撞的连续检测

- constraints

    控制物理模拟允许的自由度

    2种3轴共有6个自由度DOF：沿着x/y/z平移；绕着x/y/z旋转

    平移约束应用在世界空间，旋转约束应用在自身空间

    默认为None，6个自由度全部允许

    可以使用|组合不同的自由度

    只是禁止物理模拟的自由度，并不禁止script直接控制的transform

- freezeRotation

    控制物理是否修改物体的旋转

    这对实现第一人称射击很有用，因为player需要使用鼠标完全控制旋转

- detectCollisions

    是否开启碰撞检测（默认开启）

    关闭碰撞检测在你setup一个ragdoll并想在它live的时候避免繁重的碰撞检测计算是很有用

    detectCollisions不是序列化属性，不能被保存，也不能在Inspector中显示

- inetiaTensor/inertiaTensorRotation

    相对于质心沿着各轴的惯性涨量，用于计算转动惯性

    移动惯性和转动惯性在物理中是两套相互独立的系统，各自使用不同的物理参数，影响不同物理属性

    移动惯性使用质量，质心，力，速度，加速度来计算，转动惯性使用惯量（惯性质量），惯性涨量，力矩，角速度，角加速度来计算

    惯性涨量描述的是分别绕x/y/z轴抗拒旋转的能力，即沿着3个轴的转动惯量，就像惯性描述的是质量抗拒移动的能力一样

    加速度=力/质量

    角加速度=力矩/转动惯量（针对某个轴）

    速度=加速度*时间

    角速度=角加速度*时间

- interpolation

    interpolation允许你平滑以固定帧率允许的物理引擎的效果

    默认interpolation是关闭的通常rigidbody interpolation被用于player的角色。物理引擎以固定的帧率运行的，而graphics是以可变的帧率允许的。这将导致object看起来都抖动的效果，因为物理引擎和渲染引擎不是完全同步的。这个效果很细微，但是经常在player角色上可见，尤其是当camera跟随这角色当时候。因此建议对于有camera跟随的主角色设置这个选项，对于其他rigidbody关闭这个选项

    timeOfRender = n * Time.fixedDeltaTime + delta, n <- integer

    当图形引擎更新时，如果当前时间正好是物理引擎更新周期的整数倍时，图形显示的就正好是物理引擎的模拟的当前时刻的结果。但是通常情况下，图形引擎的更新的时刻都不是物理引擎的整数倍，两者直接的时间差值为delta。如果delta每次更新时都是固定的，也不会产生抖动，顶多就是图形引擎比物理引擎慢了delta时间进行显示而已；否则图形引擎显示的内容与物理引擎模拟的内容之间的相对时间差总是随着时间或慢或快。delta必定小于fixedDeltaTime，而真正产生抖动对原因是delta的delta，因此物体显示的抖动很细微，通常可以忽略。但是如果camera在跟随一个rigidbody，camera上一个细微的抖动就会导致整个画面尤其是远处场景的剧烈变化

    Camera跟随物体时，更新camera位置的时机应该与物体位置更新的时机相同。如果物体是在FixedUpdate时更新的，camera也应该在FixedUpdate时更新；如果物体是在Update时更新的，camera应该在LateUpdate时更新（因为物体的位置在Update时还不能完全确定，即使物体自己的Update已经执行完，之后其他的物体在Update时仍然可能更新这个物体的位置，因此在LateUpdate时，所有物体的Update都执行完毕，没有脚本在更新物体的位置的时候，再移动camera来跟随物体）

    产生抖动的原因不是因为图形引擎（camera）与运动系统的时机不一致，即使时机不一致，图形引擎有一定的延后，只要延后的差值总是保持不变，图形引擎看起来仍然是流畅的，它只是比运动系统延后了一定时间播放而已。真正导致抖动的是延迟的差值的差值的不同，即图形引擎一会延后了delta1，一会延后了delta2

    默认物理引擎只以fixedDeltaTime周期前进，如果更新整数个fixedDeltaTime后物理引擎的时间仍然没有达到Update时的时间，剩余的时间差delta将在下次Update时补上。完美的解决办法是，每次物理引擎更新来整数个fixedDeltaTime之后，还再模拟一次，以delta为步长，使得物理引擎的时间赶上图形引擎的时间。但是Unity采用来两种不同的但是相似的办法

  - None：不差值
  - Intepolate

    这种方法与完美的解决方案类似，最后一个模拟不模拟整个时间步长fixedDeltaTime，而是可变的。最后这次变动的时间长度使得物理引擎总是提前图形引擎一个步长，这样图形引擎虽然比物理引擎慢来一点，但是延迟的时间总是相同的，即delta的delta为0。例如如果当前物理引擎需要模拟2.3个step达到图形引擎的当前时间，那面它只模拟(1 + 0.3)个step；如果需要模拟2.7个step，它只模拟(1 + 0.7)个。这种方案相对于完美的解决方案的优势在于它每一帧总是少模拟一个step，因此有助于提升性能。而延迟只会在Scene最开始的阶段可见，但是Scene开始几乎可以肯定不会立即开始游戏机制，而是在完成初始化世界，显示UI等任务，而且这个延迟非常小只有fixedDeltaTime的长度，因此几乎肯定是不可见的，因此这种方案是完全可以接受的

  - Extrapolate

    这种方法与完美的解决方案类似，物理引擎仍然只模拟整数个时间步长，最后一个到当前图形引擎时间的差量不通过物理引擎模拟，而是只简单的基于当前物体的速度、角速度向前模拟差量时间，这是一种廉价的模拟，甚至碰撞检测都不会执行，而是等到下一次真正执行物理引擎模拟时再解析

- isKinematic

    物理引擎是否控制rigidbody

    如果开启isKinematic，物理引擎将不会在控制物体，物体就像普通的没有rigidbody的物体一样，只能被脚本移动旋转。

    kinematic物体仍然可以通过碰撞、关节影响其他rigidbody

    kinematic通常在使角色正常情况下被动画系统控制，但是在发生特定事件时快速转化为ragdoll时非常有用，此时将kinematic设为false，使角色被物理引擎接管

- mass

    不同rigidbody mass的巨大差距将导致物理系统不稳定

    物理引擎不是真实世界的机制，它只是提供来按照真实世界规则模拟复杂系统的一种可行方法，但是它的稳定运行是有条件的。就像IMGUI一样，它只是提供了一种实现GUI的可行路径，但不是安全的，这条可行的路径周围充满危险，需要你自己保持谨慎小心

    现实世界中存在各种不同的物理，游戏物理引擎只是模拟牛顿力学物理的简单情况

    电磁物理，流体物理，量子物理，相对论等都不能在这个物理引擎中模拟，因为这个物理引擎只实现了牛顿力学公式，其他的物理现象必须在使用实现相应物理公式的引擎中模拟。游戏物理引擎只能模拟宏观低速的情况，这个宏观低速甚至比牛顿力学的使用情形还要受限，只能在米/分米，千克级别产生稳定的模拟。即使像子弹这样小质量，小尺寸，高速度的物体都只能使用Raycast手动模拟

    因此时刻记得，游戏物理引擎的使用场景是非常受限的

- position/rotation

    rigidbody的位置。因为物理模拟是在世界空间中进行的，因此rigidbody的posiiton/rotation总是相对于世界的

    Rigidbody.position允许你使用物理引擎设置rigidbody的位置。如果你通过这个属性修改rigidbody的位置，transform将会在下一次physics模拟步长中更新。如果是在FixedUpdate中，因为它之后紧随着物理模拟，因此transform会立即更新。这比直接修改transform.position要快，因为后者将导致所有挂载的Collider重新计算它们相对于rigidbody的位置

    如果你想连续地移动一个rigidbody，使用MovePosition，它考虑来interpolation

- sleepThreshold/solverIterations/solverVelocityIterations/maxAngularVelocity

    rigidbody这些属性都对应Physics中的静态属性，后者是为每个生成的rigidbody设置的默认值，而每个rigidbody可以重新设置以采用不同的值，因此Physics静态属性的修改只能影响新生成的rigidbody

- useGravity

    重力是否影响rigidbody

- worldCenterOfMess（RO）

    质心在世界空间中的位置，centerOfMess是在self空间中的

## 方法

### 施加力（影响速度）

- AddExplosionForce

    void (float explosionForce, Vector3 explosionPosition, float explosionRadius, float upwardsModifier, ForceMode mode)

    在世界空间中对rigidbody施加一个力模拟执行中心和半径对球形爆炸效果

    radius=0则无视距离，总是施加爆炸力

    力应用在rigidbody对collider上最接近explosionPosition的点。力对作用方向沿着explosionPosition指向collider上最近的点

    如果explosionPosition在rigidbody内部，或者rigidbody没有有效的collider，则centerOfMess成为作用点

    力的模长依赖于爆炸点和作用点直接的距离，平方反比

    力的垂直方向可以使用upwardsModifier修改。如果这个参数大于0，力的作用点沿着y轴的负方向移动upwardsModifier

- AddForce

    void (Vector3 force, FoceMode mode)

    对rigidbody质心施加一个力，因此只改变rigidbody的位置，而不改变方向

    尽管Rigidbody各种AddForce函数以Force命名，但是可以通过指定ForceMode指定施加其他的物理量，包括加速度，冲量，速度变量

    应用的力只在FixedUpdate和Physics.Simulate方法中模拟一次，如果想连续地应用力的效果，需要连续地调用AddForce

    Force只能被应用于active的rigidbody。如果GameObject是inactive的，AddForce没有效果。此外Rigidbody不能是kinematic

    默认地一旦应用外力，Rigidbody的状态被设置为awake，除非force为Vector3.zero

- AddForceAtPosition

    在世界空间指定位置施加外力，因为外力可以不通过质心，因此将导致对物体的力和力矩同时应用

    对于真实效果，position应该接近rigidbody的表面。通常用于爆炸效果，此时，最后在多个frame中连续调用AddForce而不仅是一个。注意当position离质心非常远时，应用的力矩将不真实的大

- AddRelativeForce

    基于self坐标系调用AddForce

### 施加力矩（影响旋转）

- AddTorque(Vector3 torque, ForceMode mode)

    基于世界坐标系应用绕3个轴的力矩，torque位于世界空间中

- AddRelativeTorque

    基于self坐标系应用绕3个轴力矩，torque位于自身空间中

### 计算

- ClosestPointOnBounds

    代理方法，计算rigidbody上所有colliders上距离一个世界空间位置最近的点。计算rigidbody上所有的colliders

- GetPointVelocity

    计算rigidbody在世界空间中某点的速度，如果rigidbody没有旋转，rigidbody上的任何一点的速度都等于质心的速度。GetPointVelocity考虑力rigidbody的旋转

- GetRelativePointVelocity

    自身坐标系版本的GetPointVelocity

- SweepTest

    代理方法，为rigidbody上所有colliders调用GeometryCast方法

    Box，Sphere，Capsule，ConvexMesh only

- SweepTestAll

    CastAll版本的SweepTest，最多只能返回128个RaycastHit

### 状态查询

- isSleeping

### 手动运动

- MovePosition

    向一个指定的新的位置移动kinematic物体，并遵守interpolation设置。当interpolation开启时，MovePosition在帧之间创建平滑的移动效果。由于interpolation的关系，一次MovePosition调用不一定直接移动到target position，需要在多帧直接保持调用。如果target position保持不变，就使用使用相同的位置调用MovePosition；如果target position以某种方式运动，MovePosition就能是kinematic以平滑的方式追赶target position。MovePosition与target position的差量应该小于一个物理帧的模拟

    如果intepolation关闭，则MovePosition与直接设置Rigidbody.position/Transform.position一样，将kinematic立刻移动到target position

    因此MovePosition的唯一作用就是考虑interpolation来手动移动kinematic物体

- MoveRotation

### 状态设置

- ResetVenterOfMass

    重置rigidbody的质心

    基于rigidbody挂载的所有colliders计算物体的质心位置并存储它。调用这个函数之后，质心位置在rigidbody有任何改变时（质量，colliders）自动更新

- ResetInertiaTensor

    类似ResetCenterOfMass，惯性涨量（绕3个轴的转动惯量Vector3）

- SetDensity

    基于所有Colliders和常量密度设置mass

    这在基于Colliders大小设置mass时非常有用

- Sleep

    强制一个rigidbody sleep至少一个frame

    一个常用情形是在Awake中调用，以使rigidbody在开始时进入sleep状态

    Sleep时，当前物体立刻进入睡眠状态，它的所有运动状态velocity，angularVelocity立刻重置为0，它不再被物理引擎处理，即使当前它正处于悬空状态，调用Sleep之后它将保持悬空。当它受到collision或者force/torque或者调用WakeUp时会再次醒来，但是运动状态velocity，angularVelocity从0开始重新模拟，而不会恢复Sleep之前的状态

- WakeUp

    强制唤醒rigidbody

## 消息

## Force Mode

指定Rigidbody.AddForce应用的是什么物理量

- Force

    施加持续的力（在模拟的时间步长中）到rigidbody，基于它的质量

    应用的力只在下一个FixedUpdate/Simulate模拟连续的时间步长，如果要对rigidbody连续地应用力的效果，就需要连续的AddForce

    在一个时间步长中，力的模拟效果等于

    参数单位计算：

    force = mass \* distance / time^2, time = fixedDeltaTime，千克*米每秒的二次方

- Acceleration

    施加持续的加速度（在模拟的时间步长中）到rigidbody，忽略它的质量

    参数单位计算：

    acceleration = distance / time^2，米每秒的二次方

    => acceleration \* mass = mass * distance / time^2 = force

    => acceleration = force / mass

    相当于在模拟时间中持续施加acceleration * mass的力

- Impulse

    施加一个瞬时冲量到rigidbody，基于它的质量

    参数单位计算：

    impulse = mass \* distance / time，千克*米每秒

    => impulse / time = mass * distance / time^2 = force

    => impulse = force * time

    相当于在模拟时间中持续施加impulse/time的力，time=fixedDeltaTime

- VelocityChange

    施加一个瞬时velocity改变到rigidbody，忽略质量

    这个模式对于控制不同大小的宇宙飞船舰队同时运动非常有用

    参数单位计算

    velocity_change = distance / time，米每秒

### AddForce的应用本质

所有的AddForce最终转化为velocity的change，进而改变position。在Unity中Force、Acceleration、Impulse、VelocityChange是外界施加的物理变化，不是Rigidbody自身的属性。Rigidbody自身属性只包含**velocity，angularVelocity，position，rotation**。因此所有的变化最终转化为velocity的变化以统一计算，唯一区别的是不同ForceMode改变velocity的方式不同而已。这与Box2D不同，Box2D将应用在物体上的作用力作为rigidbody的自身属性，因此对物体设置的力在多次simulate之间是持久的直到下一次修改

一个Simulate的应用过程

    v1 = v0 + velocity_change_by_AddForce
    position = (v0 + v1) * t / 2
    v0 = v1

    VelocityChange -> v1 = v0 + arg_velocity_change
    Acceleration -> v1 = v0 + arg_acceleration * t
    Impulse -> v1 = v0 + arg_impulse / mass
    Force -> v1 = v0 + arg_force / mass * t

    impulse = force * deltaTime = mass * deltaVelocity

AddTorque与AddForce的过程相同，唯一的区别是操作torque，angularVelocity，rotation

    角加速度 = 力矩 / 旋转惯性质量（旋转惯量）
    计算位移的力，加速度，速度，位置都是沿着x/y/z三个坐标轴上正交独立计算的
    力矩，角加速度，角速度，旋转于同样都是绕着x/y/z三个坐标轴正交独立计算的
