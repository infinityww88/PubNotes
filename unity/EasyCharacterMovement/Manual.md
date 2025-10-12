# 快速开始

- 右键点击 hierarchy window 打开 creation dialog，选择 ECM，然后选择想要创建的 character type：
  - Character
  - Agent
  - First Person
  这会创建一个名为 ECM_Character/ECM_Agent/ECM_FirstPerson 的空 character（不可见）。确保原点位于 (0, 0, 0)，这会免于之后 parenting 的麻烦。

- 将 character 模型（可视部分）parent 到这个 ECM 上。

- 调整 Capsule Collider 以匹配 model size。

- 完成，现在就可以使用键盘到处移动了。

# Overview

将 ECM 视为 Unity 内置 Character Controller 的高级代替品，更高级的定制需求可以使用 KCC。

ECM 是一个功能丰富的高性能，基于 Rigidbody 的 Character Controller。

它可以用于任何 character，从 Players 到 NPCs 到 Enemies，并可用于很多游戏类型，诸如平台游戏，第一人称，第三人称，冒险，point and click 等等。

ECM 从开始就被设计为高效灵活，在初始化后尽可能 zero allocations。因此它在所有平台都非常高效，包括移动平台。

# 功能

- 基于 rigidbody 的 character controller
- 基于 Capsule 的 character colliders
- 支持 steps，character 可以在最高 89° 的斜面上行走
- 高性能，功能丰富的地面检测组件，可以检测、报告和查询很多 grounding cases
- Flat-base capsule bottom。这可以避免 characters 在 ledge 的边缘缓慢下沉的问题
- 可配置的 ledge offset。这设置了 character 可以站在 ledge 多近/多远 而不坠落
- Groud-Snap。这帮助维持 character 在 ground 上，不管它以多快的速度 running，并且不会在斜坡上飞出
- 在动态平台上移动和旋转
- 在斜面 slopes 上保持站立
- 在平面和斜面上保持相同的速度
- 如果需要，可以在陡峭的斜面上滑落
- Character 的基本控制器
- Agents（NavMeshAgent）的基本控制器
- 第一人称的基本控制器
- 扎实的 Root Motion 支持
- Orient to ground slopes
- 易于整合进现有项目
- 完全注释的 C# code。清晰易读，容易修改
- 移动平台友好
- 垃圾回收友好
- 更多

# 描述

ECM 遵循单一职责原则，一个 class 理想地只负责一个任务。因此一个 ECM 系统有多个针对特定任务的 class 组成。其中最重要的 class 就是 CharacterMovement 组件。

CharacterMovement 组件是 ECM 系统的核心，负责执行所有移动角色相关的复杂工作（又称为 Character Motor），例如应用 forces，impulses，constraints，platforms interaction，等等。这与 Unity 的 Character controller 等同体，但是与后者不同，它使用 Rigidbody physics。

ECM 被设计为简单和灵活，易于使用，但是 CharacterMovement 需要一个 Rigidbody，一个 CapsuleCollider，和 GroundDetection 组件在同一个 GameObject 上。

GroundDetection 执行 ground detection，并将这些信息提供给 CharacterMovement 组件。

最重要的是控制器（例如：BaseCharacterController），它决定了角色应如何移动，比如响应用户输入、AI、动画等，并将这些信息传递给执行移动的CharacterMovement组件。

值得注意的是，CharacterMovement 组件自己不做任何事情，你必须调用它的 Move 方法来移动 character。

# 组件

## Character Movement

CharacterMovement 是 ECM 系统的核心，负责移动一个 character 的所有复杂工作，又称为 Character Motor，例如应用 forces，impulses，constraints，platform interaction 等等。

它是 Unity Character Controller 的对应体，但是与后者不同，它使用 Rigidbody physics。

属性

- Max Lateral Speed：角色可以移动的侧向速度（向左向右侧身走）
- Max Rise Speed：最大上升速度，Y+ 轴，例如跳跃
- Max Fall Speed：最大下降速度，Y- 轴
- User Gravity：开启关闭角色自定义 gravity
- Gravity：应用到角色上的重力 amount
- Slide on Steep Slope：角色是否应该沿着陡坡滑动
- Slope Limit：可行走的 slope 的最大角度
- Slide Gravity Multiplier：当沿着陡坡滑落时应用的 gravity
- Snap to Ground：开启后，会强制 character 落在 ground gemoetry，不会飞离
- Snap Strength：ground 维持 character 的 tolerance 距离。0 == 不 snap，1 == 100% stick 在地面上

## BaseGroundDetection

这是一个抽象类，主要负责执行地面检测，并提供与"地面"相关的信息，例如地面接触点（角色与地面的接触位置）、地面法线等。
若需要，你可以扩展此类以实现自定义的地面检测方法。
我们提供了一个功能强大的GroundDetection类（继承自抽象类BaseGroundDetection），它能够检测并报告完整的地面信息，例如：

- 角色是否站在平台边缘？
- 角色离边缘有多远？
- 角色是否处于台阶上？台阶高度是多少？
- 角色是否位于斜坡上？
- 等等。

如你所见，它提供了一系列有价值的数据，能帮助你更好地将角色动画与周围地形同步。
此外，你可以通过新方法ComputeGroundHit随时查询角色与地面的距离（及其他附加数据），且支持任意指定位置。
还新增了一个辅助方法SweepTest，用于测试角色在场景中移动时是否会与其他物体发生碰撞。
请注意：你不应直接查询/缓存BaseGroundDetection组件，而应通过CharacterMovement组件公开的方法和属性来操作。

## Ground Detection

该组件继承自抽象基类 BaseGroundDetection，并利用角色胶囊体底部的球体来表征角色的"足部"。
这是一个功能完备的强大组件，能够检测并反馈完整的地面信息，包括：

- 角色是否处于平台边缘？
- 角色离边缘距离多远？
- 角色是否站在台阶上？台阶高度多少？
- 角色是否位于斜坡上？
- 等各类地形数据。其主要职责是为 CharacterMovement 组件提供这些关键信息。

属性

- Ground Mask：被认为是 walkable 的 ground 的 Layers
- Ground Limit：被认为 ground 的最大角度，高于这个角度被认为是 wall，不可通过
- Step Offset：一个有效阶梯的最大高度，超过这个高度不可通过
- Ledge Offset：Character 可以站在一个 Ledge 而不滑落的最大水平距离

  指墙壁、悬崖等表面突出的狭窄水平平台​（如窗台、岩架）。如果墙壁上凸出了大于等于 Ledge Offset 长度的平台，那么 Character 是可以在上面站立的，否则不能站立，而直接落下，就像光滑的墙壁一样。通常应该小于 Capsule 的 Radius。因为大于 Radius 不需要指定角色就可以站在上面。这个值最大应该设置到 Radius

  另外 Ledge 还表示悬崖边缘，例如平台边缘。只有当角色 Capsule 底部离开平台边缘一段距离（Ledge Offset）之后，角色才开始坠落。

- Cast Distance：当 character 在 ground 上时，确定 cast 的最大 cast 长度。在内部这被视为一个基于 character grounding state 的动态值，但是当 character 在 ground 上时，这个值被用来将角色约束在地面上

## Grounding Info

新的 ​GroundDetection​ 组件新增了 ​groundLimit​ 属性，用于有效区分可行走的“地面”（ground）和“墙壁”（walls）。因此，在某些情况下，角色的胶囊体（capsule）可能接触到了“地面”，但根据配置参数，该地面属于“无效地面”（invalid ground）。此时，系统会在胶囊体底部显示一个蓝色球体，以标示该“无效地面”。

另一方面，当角色处于有效地面（即任何可行走的"地面"，且地面角度小于指定的 ​groundLimit）​并且​ 接触地面（其胶囊体底部的球体触碰到任何"地面"）时，才会被判定为已着陆（grounded）。
你可以通过 ​CharacterMovement​ 组件的 ​isGrounded​ 属性轻松查询此状态，或结合 ​isOnGround​ 和 ​isValidGround​ 属性进行更精确的判断。

当角色处于着陆状态时，其胶囊体底部会显示一个绿色球体作为视觉提示。
此外，你可以通过 ​CharacterMovement​ 组件的一系列地面状态属性来查询角色当前的"着地"信息，例如：

- ​isGrounded​（是否完全着陆）
- ​isOnGround​（是否接触地面）
- ​isOnPlatform​（是否处于移动平台上）
- ​isOnLedgeSolidSide​（是否处于悬崖实体边缘）
- ​isOnLedgeEmptySide​（是否处于悬崖悬空边缘）

等多项状态检测。

## Steps

ECM v1.6版本新增了台阶攀爬功能，角色最高可攀爬高度为其碰撞体半径值（通过stepOffset属性设置）。

你可以使用CharacterMovement组件的isOnStep属性来检测角色是否处于台阶上，并通过stepHeight属性获取当前台阶的实际高度。

当位于台阶上时，ECM 会显示 step bottom ground point（黑色 point），和 step 高度（黑色 line）。

## Ledges

ECM的一项新特性是其独特的悬崖边缘处理机制：当检测到悬崖边缘时，CharacterMovement组件会自动将角色胶囊体底部视为平面（而非默认的圆弧形状）。这种创新设计有效解决了传统物理模拟中常见的"边缘平衡"问题——即角色胶囊体在悬崖边缘"摇晃平衡"时导致的缓慢滑落现象。

新增的 ledgeOffset 属性允许你精确配置角色在悬崖边缘的最大站立距离 - 超过这个预设阈值时，角色才会开始滑落。这个参数本质上定义了角色胶囊体可以安全悬空延伸的物理容差范围。

你可以通过CharacterMovement组件的isOnLedgeSolidSide属性轻松检测角色是否站在悬崖的"实体支撑侧"。例如，可以利用这个属性触发平衡动画，就像经典游戏《索尼克》中的表现效果一样。

绿色的圆圈表示角色站在 ledge 的 solid 一侧。

其他 ledge 相关属性是：

- isOnLedgeEmptySide：character 是否站在 ledge emtpy 一侧
- ledgeDistance：character bottom position 到 ledge contact point 的水平距离

另一方面当 character 在 ledge empty 一侧时，会在 character 底部显示一个红色圆圈（ledgeOffset radius）。

# Controllers

如前所述，Controller 的职责是确定角色应如何移动（例如响应用户输入、AI指令或动画等），并将这些信息传递给 CharacterMovement 组件，该组件随后会执行具体的移动操作。

ECM（Enhanced Character Movement）提供了三种可扩展的基础控制器：

- ​BaseCharacterController​：通用角色控制器
- ​BaseAgentController​：基于 NavMeshAgent 控制的角色的基类
- ​BaseFirstPersonController​：典型第一人称移动的基类

ECM 的推荐使用方式是：​继承其中一个内置的 Base Controllers​（例如 BaseCharacterController），通过派生基类创建自定义角色控制器，并添加符合游戏需求的代码（可参考附带的示例）。毕竟，没有人比你更了解自己的游戏需求！

需要说明的是，虽然我们建议使用内置的基础控制器，但这并非强制要求。你完全可以（如果更倾向）创建自己的角色控制器，并依赖 ​GroundDetection​ 和 ​CharacterMovement​ 组件来实现角色移动。不过，继承某个「Base」控制器能让你直接获得大量开箱即用的功能，因此通常是更推荐的做法。

## Base Character Controller

这是一个通用型角色控制器，同时也是其他控制器的基类。它默认处理键盘输入，支持以下功能：

- ​基于摩擦力的加速移动​
- ​可调节高度的跳跃​
- ​无限空中跳跃​（按需启用）

不过，这些默认行为很容易被修改或完全替换——只需在派生类中重写相关方法即可。

这是一个功能强大的基础类，主要特性包括：

- ​角色移动控制​
- ​可调节高度的跳跃​
- ​无限空中跳跃​
- ​根运动(root motion)支持​

它能够为你的自定义控制器开发提供坚实基础。

属性：

- Speed：最大移动速度(m/s)
- Angular Speed：最大转向速度(deg/s)
- Acceleration：velocity 改变速率
- Deceleration：characters 减慢的速率
- Ground Friction：该参数用于调节移动控制灵敏度。数值越大，角色转向速度越快。若useBrakingFriction设为false，该参数还将影响制动时的急停能力
- Use Braking Friction：brakingFriction 是否应该被用来减慢 character。如果为 false，则使用 groundFriction
- Braking Friction：制动摩擦系数（在无输入加速时生效）。仅当useBrakingFriction启用时生效，否则将默认使用groundFriction参数
- Air Friction：该参数表示空中摩擦系数​（角色未着地时生效），其作用机制与groundFriction地面摩擦系数类似
- Air Control：该参数用于控制角色空中移动时的横向操控灵敏度​
  - ​0​：完全失控（自由落体）
  - ​1​：完全操控（如地面移动）
  - ​默认值​：0.2
- Base Jump Height：初始 jump 高度(meters)
- Extra Jump Time：额外的 Jump time（例如按住 jump button），in seconds
- Extra Jump Power：当 jump button 按下时的加速度，m/ses^2
- Jump Tolerance Time：该参数用于设置提前跳跃判定窗口​（单位：秒），允许角色在触地前特定时间内按下跳跃键仍可执行跳跃。典型取值范围为0.05至0.5秒
- Max Mid-Air Jumps：最大 mid-air jumps. 0 关闭 mid-air jumps
- Use Root Motion：是否使用 root motion？如果是，animation velocity 将会覆盖 movement velocity。这需要挂载 RootMotionController 到 Animator GameObject 上

## Base Agent Controller

NavMeshAgent 所控制角色的基类。它继承自BaseCharacterController，并扩展了功能以控制NavMeshAgent，智能地响应鼠标点击移动（点击移动）。

与基础角色控制器一样，此默认行为可以在派生类中轻松修改或完全替换。

- Auto Braking

  agent 是否应该自动刹车，来避免超过目标点？如果是，agent 会在接近目标点时就停下来。

- Braking Distance

  agent 靠近目标点开始刹车的距离。

- Stoping Distance

  在距离 target position 这个距离内，agent 可以停下来。

- Ground Mask

  被 agent 认为时 ground（walkable）的 Layers。用于 ground click detection。

## Base First Person Controller

第一人称角色控制器基类。它继承自BaseCharacterController，并扩展以执行经典 FPS 移动。

与基础角色控制器一样，此默认行为可以在派生类中轻松修改或完全替换。

- Forward Speed：向前移动的速度
- Backward Speed：向后移动的速度
- Strafe Speed：侧向移动的速度
- Run Speed Multiplier：奔跑时移动速度提升的因子

# Custom Controllers

如前所述，使用ECM的推荐方式是选择其中一个内置的基础控制器进行扩展，添加游戏特定的功能。这样，你既可以利用现有功能作为坚实基础进行开发，也可以根据需要修改甚至完全替换它，而无需直接改动ECM的源代码。  

这种方法的一大优势在于将游戏代码与资源代码分离。当你需要更新ECM时，你的游戏代码不会受到影响。  

创建自定义控制器非常简单，只需新建一个类来继承某个基础控制器（例如`BaseCharacterController`），然后重写所需的方法即可。

```C#
public sealed class MyCharacterController : BaseCharacterController 
{ 
    protected override void Animate() 
    { 
        // Add animator related code here... 
    } 
}
```

要使用这个新创建的自定义控制器（MyCharacterController），你只需将角色GameObject上的BaseCharacterController组件替换为MyCharacterController即可。

在以下示例中，我们将创建一个自定义控制器，并重写其默认实现，使角色运动相对于主摄像机而非世界坐标系。
与之前一样，我们继承BaseCharacterController并重写其方法，在本例中重写的是HandleInput方法。

```C#
 
public sealed class MyCharacterController : BaseCharacterController 
{ 
    public Transform playerCamera; 
    
    protected override void Animate() 
    { 
        // Add animator related code here... 
    } 
    
    protected override void HandleInput() 
    { 
        // Handle your custom input here... 
    
        moveDirection = new Vector3 
        { 
            x = Input.GetAxisRaw("Horizontal"), 
            y = 0.0f, 
            z = Input.GetAxisRaw("Vertical") 
        }; 
    
        walk = Input.GetButton("Fire3"); 
        jump = Input.GetButton("Jump"); 
    
        // Transform moveDirection vector to be relative to camera view direction 
    
        moveDirection = moveDirection.relativeTo(playerCamera); 
    } 
}
```

# Helpers

## Root Motion Controller

这是一个辅助组件，用于提供Animator的 Root Motion 速度向量(animVelocity)。必须将该组件附加到带有Animator组件的游戏对象上。

## Orient Model to Ground(Optional)

用于调整模型地面朝向的辅助组件。该组件必须附加到带有CharacterMovement组件的游戏对象上，且需要调整朝向的模型必须是其子对象。

- Orient to Ground：决定 model transform 是否会改变它的 up vector 来匹配 ground normal
- Model Transform：约束到地面的 transform，例如 child character model transform
- MinAngle：导致 origientation change 的最小 slope 角度，小于这个角度，up vector 不变，大于这个角度，根据 ground normal 更新 up vector
- Rotation Speed：align ground normal 的最大转向速度（deg/s）

# Prefabs

可以在项目中到一组 prefabs，每个 Controller 一个，你可以使用它们作为开始，也可以在对 character hierarchy 有不明白的地方时查看。

# Code Reference
