# Character Controller Creation Walkthrough 

本教程将循序渐进地演示如何基于Kinematic Character Controller系统从零实现完整的角色控制器。你既可以按照步骤顺序学习，也可以将其作为特定功能（如移动/跳跃/碰撞处理）的专项实现参考。

## Player，Character & Camera setup

我们将首先构建输入系统、角色与摄像机协同工作的基础框架。不同于将输入处理和镜头控制直接写入角色控制器，我们会将其独立封装在"MyPlayer"类中——这是因为并非所有角色都需要人工控制（例如AI控制的角色就不应处理输入/镜头逻辑）。通过这种架构设计，我们可以轻松实现：人类玩家控制的角色由"Player"类驱动，AI控制的角色由AI系统驱动。所有这些无需为此开发两套不同的角色控制器。

创建 Character Controller GameObject：

- 在场景中，创建一个空 GameObject
- 添加一个 KinematicCharacterMotor 组件（这会自动创建一个只读的 capsule collider）
- 创建一个脚本，命名为 MyCharacterController，使它继承 Monobehaviour，实现 ICharacterController 接口
- 添加一个 public KinematicCharacterMotor Motor 字段到 class
- 在 MyCharacterController 的 Start 中，编写 Motor.CharacterController = this
- 添加 MyCharacterController 到 character GameObject
- 将 KinematicCharacterMotor 组件赋值给 MyCharacterController 的 Motor 字段
- 添加一个空 GameObject 作为 character GameObject 的 child，命名为 Root。这会作为 character 所有 meshes 的容器。这样在实现下蹲时非常好用
- 将 mesh 作为 child 添加到 Root 上。现在可以使用 Capsule，但是不要忘记移除 Character GameObject 下所有 colliders，否则 character 将会不断下降，因为它会始终尝试从自己分离碰撞。
- 在 KinematicCharacterMotor inspector 中的 Capsule Settings 中设置 character capsule dimensions，以及 physics material。
- 在 Motor Parameters sections，现在可以保留为默认值

创建一个 Player：

- 创建一个空 GameObject，命名为 Player
- 创建一个脚本，命名为 MyPlayer
- 将 MyPlayer 添加到 Player 上面

MyPlayer将负责处理所有角色和摄像头的输入，并建立摄像头与角色之间的连接。目前，我们只需专注于摄像头的控制部分。在Start()函数中，MyPlayer会设置摄像头跟随角色；在Update()函数中，它会计算鼠标移动和滚轮操作的输入数据，并将这些输入传递给其绑定的ExampleCharacterCamera组件。最终实现的效果是：一个始终跟随角色且可自由操控的摄像头系统。

将所有东西链接在一起：

- 将 ExampleCharacterCamera prefab 拖放到 Scene 中
- 将 ExampleCharacterCamera 赋值给 MyPlayer inspector 中的相应字段
- 在 Character GameObject 下面，添加一个空的 GameObject，它会作为 camera orbit point。添加这个 transform 到 MyPlayer inspector 中的 Camera Follow Point 字段
- 添加一个 floor 到场景中（例如 (100, 0, 100) 缩放的 cube primitive）

现在可以按下 play 并注意已经可以控制 camera。初始设置完成了。但是现在还不能移动 character，因为还没有实现任何 movement code。

## Basic movement and Gravity

现在开始编写一些 movement code。

### 在 MyPlayer 和 MyCharacterController 中处理 Movement input

从使 MyPlayer 告诉 MyCharacterController 它需要看哪里和向哪里移动开始。

首先，创建一个 struct，表示 player 可以给它的 character 的 inputs，命名为 PlayerCharacterInputs。

在 MyPlayer 添加一个 HandleCharacterInput，这会在每个 Update 调用。这个方法简单将 input 从 player 传递到 character。

SetInput() 的目标是变换这些 inputs 为 character 可以用于 movement 和 rotation 的信息。这里我们基于 camera orientation 构建一个 movement vector 和一个 look direction vector，以及 character 的 up direction（我们想要在 camera 方向移动，但是只在 character 平面上）。

### Character controller movement code

现在使 character controller 基于来自 Player 的 inputs 移动。

首先，我们将处理移动位移，这部分逻辑会在 MyCharacterController 的 UpdateVelocity 重写方法中实现。该方法由 KinematicCharacterMotor 在每次角色更新时调用，其核心作用是告知角色控制器当前应有的速度。
​必须始终在此方法内处理角色速度，因为它在角色更新循环的精确时机被调用，以确保所有功能正常运行。
你需要修改该方法传入的 currentVelocity 引用参数，以设定目标速度。

接下来，我们将处理角色朝向，这部分逻辑会在 MyCharacterController 的 UpdateRotation 重写方法中实现。该方法由 KinematicCharacterMotor 在每次角色更新时调用，其核心作用是告知角色控制器当前应有的旋转角度。
​必须始终在此方法内处理角色旋转，因为它在角色更新循环的精确时机被调用，以确保所有功能正常运行。
你需要修改该方法传入的 currentRotation 引用参数，以设定目标朝向。

点击播放按钮，测试已实现的移动功能。此时，你可以根据需要向场景中添加更多几何体。

## Jumping

### 简单跳跃

首先需要处理 jump input。在 PlayerCharacterInputs struct 中添加 JumpDown。

请注意，​所有速度计算都必须在 UpdateVelocity 方法中处理，因此我们暂时仅记录跳跃指令，而不会立即以其他方式应用移动效果。

以下是处理跳跃速度的代码实现细节：

- ​跳跃速度应用时机​
  在UpdateVelocity方法末尾处添加的代码负责实际应用跳跃速度。特别注意：每当需要让角色离开地面时，必须调用KinematicCharacterMotor.ForceUnground()方法，否则角色会持续吸附在地面上。
- ​额外跳跃逻辑处理​
  查看MyCharacterController的AfterCharacterUpdate方法中的补充跳跃逻辑，该方法专门用于处理跳跃计时器和状态管理。

JumpPreGroundingGraceTime​（预着陆宽限时间）与 ​JumpPostGroundingGraceTime​（离地后宽限时间）分别表示：

- 在即将落地前仍可输入跳跃指令的额外时间窗口（落地后仍会执行跳跃）
- 离开稳定地面后仍允许跳跃的额外时间

### Double Jumping

要添加 double-jumping，只需要在 jumping requested 时简单添加一个条件，判断是否已经开始了第一次 jump，并且不在 ground，则可以再次跳跃。

### Wall Jumping

要实现蹬墙跳跃功能，我们将采用与常规跳跃类似的机制，但仅当角色贴墙移动时触发。具体实现需要：

​碰撞检测阶段​，在MyCharacterController的OnMovementHit方法中添加代码，用于检测并记录当前是否允许蹬墙跳跃。​速度计算阶段​，在UpdateVelocity方法中读取该状态变量，最终执行实际的蹬墙跳跃动作

## Detecting landing and leaving ground

大多数 character controllers 需要一种方法检测它何时落地，或者它何时离开地面（对 animation，sound effects 等等），这非常容易实现。所需做的就是在 PostGroundingUpdate 中比较当前 KinematicCharacterMotor 的 ground status 和之前的 ground status，PostGroundingUpdate 在 character 已经求值新的 grounding status 后立即调用。

进入 play mode，尝试四处跳跃，查看 debug log messages 何时 land 和 leave ground。

## Adding velocities and impulses

很多时候，需要一种很快很容易的方法，来为 character 添加 forces 和 impulses，例如遇到爆炸冲击波，或者在 wind zones。为此，在 MyCharacterController 中添加一个 AddVelocity 方法，它将维持一个内部 velocity vector 并在 UpdateVelocity 中添加到最终 velocity 上。

为此测试，可以在 MyPlayer 简单添加一些 input，这会添加一个 velocity 到 character。注意，我们在添加 velocity 前调用 ForceUnground。这是因为我们想要强制将 character 发射到空中。否则，character 总会保持在地面上。

## Crouching

要实现 crouching，首先需要处理 input，在 PlayerCharacterInputs strcut 中添加 CrouchDown 和 CrouchUp 字段。在 MyCharacterController.SetInputs() 方法中，记住想要的 crouching state，然后如果进行 crouch 则应用 capsule rescale。

但是 un-crouching 不是在 SetInputs 中处理的。这是因为有时 character 会没有足够的空间进行 uncrouch，因此这是在 MyCharacterController.AfterCharacterUpdate 中处理的。首先尝试确定是否应该 uncrouching，如果是，则临时 resize capsule 来匹配 character 的 standing height，然后使用 KinematicCharacterMotor.CharacterOverlap 执行一个 overlap 测试。之所以这样而不是执行一个简单的 OverlapCapsule 是因为 CharacterOverlap 考虑了 character 所有的 被忽略的 colliders 和特定 collision filtering。如果检测到不能站立，它重置 capsule dimensions 到 crouching 大小。如果能站立，则重置 mesh 的 scale，并且将 IsCrouching 设置为 False。

## Orienting towards arbitary up direction

为展示如何让 charater 沿着任意方向站立，而不是只向下，例如在一个 sphere 上，现在实现一个选项。

在 UpdateRotaion 中，简单告诉 character 从它当前 up 方向旋转到重力方向。UpdateRotation 方法中可以指定你当前希望的 character 的 rotation。然后尝试激活 Orient Towards Gravity，调整 character 的 Gravity vector，查看 reorienting 效果。

简而言之就是通过开启 OrientTowardsGravity 并改变 Gravity 方向，来让 character 沿着任意方向站立。

## Creating a moving platform

现在创建一个可以通过 animations 移动的 moving platform：

- 创建一个 flat cube，命名为 Moving Platform
- 添加一个 PhysicsMover 组件到它上面。必须使用这个组件创建任何 character 可以站立或被 push 的 kinematic moving object
- 创建一个脚本 MyMovingPlatform。这个类必须继承自 BaseMoverController，并实现 UpdateMovement abstract 方法
- 添加 MyMovingPlatform 组件到 MovingPlatform GameObject 上
- 将 MyMovingPlatform 组件赋值给 PhysicsMover 的 MoverController 上
- 使用 PlayableDirector 组件和 Timeline window，创建一个 playable animation，它可以移动和旋转 platform

使用 PhysicsMovers 的方式是，在 BaseMoverController 的 UpdateMovement callback 中精确地告诉它其 position 和 rotation 应该是什么。当你通过这个 callback 处理 movement，所有的 character controller 的 physics 都会被正确地处理，因此关键是不要在其他地方移动 PhysicsMovers。但是如果想要用 animation 移动它，这将是个问题。

我们将通过完全掌控动画的 evaluation 过程来解决此问题，仅在与PhysicsMover的更新（FixedUpdate）同步时才进行动画更新。为此，我们需要确保PlayableDirector的更新模式设置为"Manual"，以便我们可以手动控制其更新。随后，我们将使用Evaluate()方法在任意所需时刻应用动画效果。

首先在 MyMovingPlatform.Start 中停止 animator 的 PlayableGraph。

然后实现 UpdateMovement callback：

- 缓存 evaluation 动画之前的 pose
- evaluate animation，这会立即更新 transform 的 pose
- 告诉 PhysicsMover 下一个 FixedUpdate，它需要在哪里
- 最后，重置 transform 到 evaluate 之前缓存的 pose，让 KCC 来真正移动 Platform，而动画不会影响 physcis

## Custom collision filtering

在游戏开发中，经常需要筛选特定的碰撞检测，而仅靠物理层（Physics Layers）往往无法优雅地实现需求。例如，在网络游戏中，你可能需要让角色穿透友军，但会被敌人阻挡。下面我们将创建一个简单的碰撞过滤示例，帮助你理解如何实现这类功能。

首先向 MyCharacterController 添加一个 public colliders list，其代表想要忽略的 colliders。

实际过滤工作在 IsColliderValidForCollisions 中完成。这个方法向你查询是否可以和这个 colldier 碰撞，返回 true or false。

你可以以任意想要的方式使用这个方法。

## Multiple movement states setup

很快，我们的角色控制器就需要支持多种移动状态了。为了避免代码变得过于混乱，我们现在就花点时间把所有功能重新整理成更易维护的结构——这个前期投入将来一定会带来回报！

- 创建一个 CharacterState enum，代表 character 可以处在的所有 states。现在只有一个 Default。
- 添加一个 CurrentCharacterState 字段到 MyCharacterController，它会记住当前的 state
- 在 MyCharacterController 中所有跟 state 相关的方法中，添加 switch case 语句，根据 character 的当前状态编写不同的 logic
- 在 MyCharacterController 中添加 TransitionToState，OnStateEnter，OnStateExit 方法让 transitions 更容易管理

## Charging state

现在编写一个新的状态：Charging。这个状态下，character 将会以常量速度向前移动，知道撞到墙停下来，或者超过 X 秒。然后它会暂停一段时间并回到默认移动状态。

首先在 CharacterState enum 中添加一个 Charging 状态。然后添加一些 input handle code 在按下某个键时，调用到这个状态的 transition。

- 在 OnStateEnter，对 Charging state 缓存一个 charging velocity，基于 character 的 forward 方向
- 在 UpdateVelocity，对 Charging state，每个 update 保持应用一个 charging velocity，除非处于 charge end 的暂停状态
- 在 OnMovementHit，对 Charging state，查询是否和 wall 碰撞，以便触发进入 charge end
- 在 AfterCharacterUpdate，对 Charging state：
  - 确定 charging time 是否已经过去，应该结束 charge
  - 确定是否应该给回到默认移动状态

## NoClip state



## Swimming state

## Climbing a ladder

## Root motion example

## Frame Prefect rotation

# Tips
