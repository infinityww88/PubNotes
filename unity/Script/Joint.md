# Joint

关节定义了一组应用在Rigidbody上的约束，每次物理引擎模拟时都会应用这些约束，使Rigidbody趋向满足约束定义

约束既可以是位置/旋转，也可以是速度/角速度。Unity物理引擎只使用这4个量表示物体的运动状态

物理引擎是6个独立运动的合成，即6个自由度DOF

    沿x的平移
    沿y的平移
    沿z的平移
    绕x的旋转
    绕y的旋转
    绕z的旋转

关节约束就是在定义这六种独立运动的约束

约束定义分为两种：范围约束Limit和驱动约束Drive（Motor）

范围约束limit定义一个自由度上的运动范围，在这个范围之内rigidbody是可以自由活动的，超过这个范围关节将使用弹簧Spring机制反向约束rigidbody到范围之内

驱动约束drive定义在这个自由度上的自主活动（驱动马达），马达驱动rigidbody运动向指定的target position或达到指定target velocity

和Unity及所有游戏引擎的各种系统一样，这两种约束都是独立的子约束系统，每种约束都不知道对方的存在，最终效果取决于所有子约束系统的合成效果（就像粒子系统，每个子系统都独立模拟，不知道其他的子系统的存在，最终粒子系统效果取决于所有子系统的合成效果）。分解合成是游戏开发的核心模式。你可以只定义一个子系统而忽略其他子系统，从而只是用一个特定子系统的功能。

6个自由度，2种约束类型，共计12种约束

## 关节位置

碰撞解析时碰撞点几乎肯定不会在质心，而且碰撞时的相对冲量也不经过质心，因此会同时导致rigidbody的位置和旋转发生变化。关节约束也是一样，绝大多数的关节约束点都不希望在rigidbody的质心（这就是问什么Unity添加关节时默认的Anchor都是计算在collider的表面而是放置在rigidbody的质心）而是在Rigidbody其他一些自定义的位置，约束方向也可能于rigidbody的方向不同。因此关节约束提供了自定义约束点和约束方向的方法。

约束点称为Anchor（for rigidbody1），Connected Anchor(for rigidbody2)，分别在各自rigidbody的self坐标系中定义。即每个Rigidbody给出一个self空间中的位置，用作关节约束的目标。关节约束所有施加的力和力矩应用在这个点上（AddForceAtPosition）。如果施加在Anchor上的关节约束力不经过rigidbody质心，将会导致rigidbody的旋转。

Joint在一个统一的坐标系计算两个Rigidbody的相对位置和旋转。这个坐标系在关节组件所在的rigidbody的self坐标系中定义。

Joint坐标系的定义是用Axis定义X轴，用Secondary Axis定义Y轴，Y轴通常不一定等于SecondaryAxis，因为X轴的定义是任意的，而手动计算垂直它的Y轴并在Inspector中设置对于Editor来说是不可接受的，因此Unity会根据Secondary Axis自动计算于X轴垂直的Y轴，Secondary Axis相当于lookAt中的hintUpwards向量。确定了X轴和Y轴之后就可以根据左手定则确定Z轴了

    一种左手定则是拇指指向X轴（Axis），食指指向Y轴（Secondary Axis），中指指向的就是Z轴正向
    另一个左手定则是四指沿着从X轴到Y轴的方向弯曲，拇指指向就是Z轴正向

所有针对X/Y/Z定义的运动约束都是基于这个Joint坐标系的

Joint是用来约束两个Rigidbody的相对位置和旋转的，无论Joint两端哪个Rigibody的位置和旋转发生变化，另一个Rigidbody都会因Joint约束而发生相应变化，以使两个Rigidbody的相对位置和旋转满足约束定义

- Rigidbody1 configuration
  - Anchor

    Rigidbody1的约束点在self空间中的位置

  - Axis

    Joint坐标系X轴在Rigidbody1空间中的方向

  - Secondary Axis

    定义Joint坐标系Y轴时使用的upwards向量，Axis相当于LookAt中的forward，Secondary Axis相当于LookAt中的hintUpwards

- Rigidbody2 configuration
  - Connected Body

    Joint连接的另一个Rigidbody2，如果为空，则Joint连接在世界空间中的固定位置

  - Connected Anchor

    Rigidbody2的约束点在self空间中的位置，如果Connected Body为空，则是世界空间

  - Auto Configure Connected Anchor

    Connected Anchor是否自动计算。Connected Anchor是在Rigidbody2d的self坐标系空间定义的。Rigidbody1的Anchor是可以自由定义的，但是很多情况下我们需要让两个Rigidbody的Anchor在世界空间中是重合的，而根据Anchor1来手动计算相同世界空间位置的Anchor2是非常繁琐的。开启这个选项Unity可以自动根据Anchor1在世界空间中的位置计算Anchor2在Rigidbody2 self空间中的位置，使两个Anchor在世界空间中重合

## Configurable Joint

Configurable Joint提供了最全面的关节定义。所有其他类型的关节定义都可以通过Configurable Joint实现（它们只定义几种约束），但是可能需要多个Configurable Joint已经附加脚本来操作Configurable Joint。

### 对6个DOF的约束

X/Y/Z Motion & Angular X/Y/Z Motion

每个DOF指定3种约束类型：

    Free：没有约束，完全自由活动
    Lock：完全锁定，不能自由活动
    Limited：受限活动

- Free

    Limit约束不起作用，Drive起作用

- Limited

    Limit起作用，Drive起作用

- Lock

    Limit和Drive都不起作用

Limit=0时与Lock等效，如果希望Spring在0处震荡，需要将Limit设置为稍大于0的数，例如0.01，这与实际情况也是一致的，一个在0处震荡的关节一定有稍大于0的活动空间才能产生震荡。在Limited Motion模式下使用Drive时记得Limit约束也在生效，如果没有设置Limit的情况下，默认为0，有效的将自由度Lock，Drive无法驱动物体。因此如果只希望使用Drive约束，必须将Motion设置为Free，将Limit约束关闭

Drive通过设置PositionSpring和PositionDamper参数为0可以在开启情况下保持不起作用

Limit约束只在Motion=Limited时才起作用，Drive约束在Limited和Free情况下都起作用

### 平移约束

#### Limit约束

Limit约束不是针对X/Y/Z分别定义的，而是为X/Y/Z统一定义的，至于rigidbody能不能在特定的轴上运动，完全取决于Motion类型（Free、Limited、Lock）。因此Limit对1d定义了一个区间[-limit, limit]，对2d定义了一个半径=limit的圆，对3d定义了一个半径=limit的球。Limit不能定义椭圆或者椭球范围

Limit约束定义分为两部分：

1. 范围定义

    Limit：半径
    Bounciness：rigidbody超过半径时的反弹系数，就像碰撞到刚体一样，等价于物理材质的弹性系数
    ContactDistance：Joint预测接近Limit的距离，如果ContactDistance > 0，Jonit就能提前预测到接近Limit并开始应用约束。如果=0，则从不预测，只能等到超过limit的时候再开始进行约束，容易导致抖动

2. Spring定义

    Spring：定义弹簧弹性系数，当定义了弹性系数>0，Bounciness将被忽略，约束将像弹簧一样运行，而不是像碰撞到刚体上
    Damper：弹簧阻尼系数，定义弹簧震荡衰减的速度

#### Drive约束

    Target Position：马达驱动物体趋向的目标位置
    Target Velocity：马达驱动物体趋向的目标速度

X/Y/Z Drive

    马达驱动力的计算
    force = PositionSpring * (targetPosition - position) + PositionDamper * (targetVelocity - velocity)
    force = Min(force, MaximumForce)

Drive和Limit约束是独立的，它不参考limit定义的范围，但是如果同时定义了Drive和Limit约束，Drive驱动物体超过了Limit，Limit约束会重新把物体拉回，这就是所谓最终效果由所有子系统合成而来

两个约束总是并行执行，但是依赖于其参数配置，它们可能不对物体施加作用。例如如果PositionSpring = 0 & PositionDamper = 0，Drive计算的force总是0，因此对物体没有影响。一旦定义了PositinString、PositionDamper、targetPosition、targetVelocity等参数，使得force不为0，物体就会受到影响。force的计算依赖于（targetPosition - position）和（targetVelocity - velocity），因此物体在处于稳定状态时，position一定不等于targetPosition。因为稳定时velocity=0，而targetVelocity不为0，除非PositionDamper=0，否则，targetPosition于position必须有差量才能补偿targetVelocity与velocity的差量。

force的计算公式是一个依赖于position和velocity的微分控制器，最终在参数不变的情况下最终物体会达到稳定状态，velocity=0，而position不一定等于targetPosition。如果在脚本中动态（FixedUpdate）改变targetPosition，就能得到一个恒定驱动物体运动的马达，而不仅是在targetPosition附近停下来。这就是其他具有恒定马达的高级类型的Joint的实现方法：使用脚本不断更新targetPosition/targetRotation

### 旋转约束

对于旋转，通常我们只需要两种情况：绕着一个轴旋转（1d）；在一个锥形体内旋转（2d）。1d旋转可以模拟铰链，2d旋转可以模拟人体关节，几乎没有3d旋转对需求。因此无论是Limit还是Drive都把旋转约束分为对X的约束（1d）和对YZ对约束（2d）。如果需要1d约束，就将X轴设置为旋转轴的方向，如果需要2d约束，就把YZ平面设置为垂直垂直锥形体方向，X轴为锥形体中心线。

因此Configurable Joint的Angular X约束和Angular YZ约束其实应该称为Angular1d约束和Angular2d约束，因为使用哪个约束与坐标轴无关，而是与使用场景有关，然后将坐标轴设置为相应的方向。

对于Angular YZ约束，Limit Spring和Drive PositionString/PositionDamper是统一设置的，就像平移约束中Limit是对X/Y/Z统一设置的一样。只是Angular Limit对Y、Z是分别设置对，这允许设置一个椭锥体的旋转空间。Angular Limit对于YZ只有一个limit，就像平移中的limit一样，它创建了一个在坐标轴两边对称的区间，YZ锥体旋转空间期望是在Y、Z两个坐标轴上对称的。但是对Angular X约束，它指定了一个下边界和一个上边界，因此可以指定一个不对称的任意的弧形区间作为允许的旋转区间，因为这也是1d旋转约束的常见情形。

Angular Limit YZ最大只能设置到177度，锥体度锥角最大为354度，因此YZ约束旋转总是一个锥体而不是一个球体。

对于旋转约束应该只有两种使用情形，而且Configurable Joint也只支持这两种情形

    绕着一个轴度旋转
    绕着两个轴度旋转（锥体）

如果需要两个rigidbody之间可以无限制地任何旋转，就应该去掉Angular约束（因为不需要Angular约束），只需要两个rigidbody之间的固定距离的约束，即Distance Joint。

就像Transform的旋转一样，既可以以欧拉角的方式旋转，即绕着X/Y/Z轴独立地旋转，也可以绕着空间中任意地一个轴（非坐标轴）旋转。Angular Drive提供了后面一种旋转方式的驱动器，Slerp Drive。Slerp Drive总是在球面上以最短路径将rigidbody旋转到target rotation。

### Joint状态

- breakForce/breakTorque
- currentForce/currentTorque
- massScale/connectedMassScale
