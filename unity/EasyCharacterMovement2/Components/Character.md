# Description

Character 作为所有 game avatars 的基础构造块，无论是 player 控制还是 AI 控制。

这个类使用 CharacterMovement 组件作为 Character 控制器/马达，无缝继承典型的移动模式，例如 walking，falling，flying，swimming。此外，它还可以完全配置 jump 和 crouch 机制。

Character 类基于它当前的 mode 指示它的移动，将移动的执行委托给 CharacterMovement 组件，这最终会执行物理运动。

# Character 如何工作

默认，Character 实现一个自动模拟，自动调用它的 Simulation 方法。这个方法负责了角色移动的大部分核心工作，包括更新其当前 movement mode，基于当前 rotation mode 调整 rotation，处理 jump 和 crouch 动作，触发事件，等等。

Auto-simulation 开启时（默认选项），Character 通过 coroutine 实现了一个 LateFixedUpdate。这确保 Character 在 Unity 内部 Physics update 之后模拟，这是实现无缝 physical 交互的关键步骤。

本质上，角色（Character）会解析输入 vectors 和 events（包括用于控制角色的键盘输入），并将这些输入转换为对角色位置和旋转的更新。这一过程在不同的移动模式（如行走、飞行、游泳，或你可能创建的任何自定义模式）中实现，每种模式定义了输入的处理方式，并影响最终的输出结果。

所有这些发生在 Simulate 方法中，并按照以下执行顺序：

```C#
public void Simulate(float deltaTime)
{
    if (isPaused)
        return;
    
    BeforeSimulationUpdate(deltaTime);
    SimulationUpdate(deltaTime);
    AfterSimulationUpdate(deltaTime);
    CharacterMovementUpdate(deltaTime);
}
```

- BeforeSimulationUpdate

  BeforeSimulationUpdate 在任何 movement mode 更新之前调用。它根据 CharacterMovement grounding 状态 自动在 walking 和 falling movement modes 之间切换，并处理 jump 和 crouch 机制。
  
  最后，它触发 OnBeforeSimulationUpdate 事件，允许我们扩展它的功能。
  
  使用 OnBeforeSimulationUpdate 方法/event 在外部更新 character state。

- SimulationUpdate

  它使用给定的 movement direction 向量（SetMovementDirection 设置）来计算一个期望的 velocity vector（方向和大小）。接下来，这个信息基于当前 movement mode 处理，并因此根据它定义的规则，调整 character 的 velocity。

  此外，它根据 current rotation mode 执行 character 的旋转。

- AfterSimulationUpdate

  这个方法负责触发 ReachedJumpApex 和 AfterSimulationUpdated 事件。Apex：最高点，最高峰。此时，character 的 rotation 和 velocity 已经根据它的当前 mode 执行了更新，但是移动 movement 还没有更新，它在稍后的 CharacterMovementUpdate 方法中执行。

- CharacterMovementUpdate

  这个最终模拟方法传递 character 的 velocity 给 CharacterMovement 的 Move 方法，它接下来执行请求的移动。最后，它触发 CharacterMovementUpdated 事件。此时 character 已经完全更新。

# Character Movement Modes

Character 类引入了 Movement Modes 概念，例如 Walking，Falling，Flying，Swimming，和 Custom。

每个 movement mode 有一组预定义的规则和属性，它指示 character 如何在 world 中运动。尽管这个概念一定程度上跟 character states 相关（例如跳跃、攻击、死亡等等逻辑状态），但是它不应该与代码逻辑中的角色状态混淆。Movement Mode 的主要目的是决定角色如何在 world 中移动，可以认为是 Character Movement 的局部专用状态，跟游戏逻辑上角色的状态是两回事。例如角色在移动上处于 Crouch 状态，但是在游戏逻辑中角色可能处于攻击（只是它在潜伏攻击）。

例如，尽管 Flying Movement Mode 暗示角色是在 flying 逻辑状态，但是它是专门定义角色如何 flying 的。例如，它允许 character 移动到空中，不被重力影响，让角色脱离地面束缚，同时保持垂直速度（向上飞行的速度）。

运动状态定义如下：

```C#
public enum MovementMode
{
    /// <summary>
    /// Disables movement clearing velocity and any pending forces / impulsed on Character.
    /// </summary>
    
    None,
    
    /// <summary>
    /// Walking on a surface, under the effects of friction, and able to "step up" barriers.
    /// Vertical velocity is zero.
    /// </summary>
    
    Walking,
    
    /// <summary>
    /// Falling under the effects of gravity, after jumping or walking off the edge of a surface.
    /// </summary>
    
    Falling,
    
    /// <summary>
    /// Flying, ignoring the effects of gravity.
    /// </summary>
    
    Flying,
    
    /// <summary>
    /// Swimming through a fluid volume, under the effects of gravity and buoyancy.
    /// </summary>
    
    Swimming,
    
    /// <summary>
    /// User-defined custom movement mode, including many possible sub-modes.
    /// </summary>
    
    Custom
}
```

你可以通过使用 SetMovementMode 函数改变角色的 movement mode。这个动作自动调用 OnMovementModeChanged 方法，并触发 MovementModeChanged 事件。OnMovementModeChanged 方法专门设计用于处理特定 modes 的初始化，例如开启、关闭 ground constraints，停止跳跃，重置跳跃次数等等。

注意：Walking 和 Falling modes 基于 character 的 grounding 状态自动管理。当 character 被约束到 walk-able 地面上，Walking 运动 mode 被开启。反之，当 character 不在 ground 上，或者在 non-walkable surface，它会切换到 Falling movement mode。

对于 Flying movement mode，你需要根据需要显式开启和关闭它。退出 Flying state 通过过渡到 Falling mode 安全地达成，而这自动会导致 Walking mode。这个原则也适用 Custom movement modes。

```C#
// Enter flying mode
SetMovementMode(MovementMode.Flying);
..

// Exits flying mode
SetMovementMode(MovementMode.Falling);
```

尽管可以手动开启或关闭 Swimming movement mode，当使用 PhysicsVolume 时，这被自动管理。

# Moving a Character

角色（Character）包含一组专门设计的方法，用于简化动作的执行流程，通常是为了响应诸如按下（on-down）、抬起（on-up）等输入事件。

```C#
/// <summary>
/// 设定 Character 的 movement 方向（世界空间）
/// 例如，期望的移动方向向量
/// </summary>
public void SetMovementDirection(Vector3 movementDirection)

/// <summary>
/// 请求 Character 跳跃，请求在下一个 simulation 更新中处理
/// 在一个输入事件中调用这个方法
/// </summary>
public virtual void Jump()

/// <summary>
/// 请求角色角色停止一个跳跃动作
/// 请求在下一个 simulation 更新中处理
/// 在一个输入事件中调用这个方法
/// </summary>
public virtual void StopJumping()

/// <summary>
/// Request the Character to crouch.
/// The request is processed on the next simulation update.
/// Call this from an input event (such as a button 'down' event).
/// </summary>
public virtual void Crouch()

/// <summary>
/// Request the Character to stop crouching.
/// The request is processed on the next simulation update.
/// Call this from an input event (such as a button 'up' event).
/// </summary>
public virtual void UnCrouch()
```

## Movement Relative to Camera

经常需要在 camera orientation（方向）上对齐角色的运动，确保 camera 的观察方向和运动方向一致。要简化这个过程，ECM2 提供了一个有用的 Vector3 扩展方法：

```C#
/// <summary>
/// 相对于给定 transform 变换向量
/// 如果 isPlanar == true，transform 会自动应用在 world up 向量定义的 plane 上
/// </summary>

public static Vector3 relativeTo(this Vector3 vector3, Transform relativeToThis, bool isPlanar = true)
```

这个方法可以被用来对齐运动方向和角色跟随相机的视角：

```C#
// Poll input

Vector2 inputMove = new Vector2()
{
    x = Input.GetAxisRaw("Horizontal"),
    y = Input.GetAxisRaw("Vertical")
};

// World space movement direction

Vector3 movementDirection =  Vector3.zero;

movementDirection += Vector3.right * inputMove.x;
movementDirection += Vector3.forward * inputMove.y;

// Make movement direction relative to a given Transform

movementDirection = movementDirection.relativeTo(_character.cameraTransform);

// Assign camera's relative movement direction to character

_character.SetMovementDirection(movementDirection);
```

注意区别在 relativeTo 扩展方法，它允许在 world-up axis 定义的 plane 上执行变换。当使用自定义 world-up 方向时，这至关重要。

# Character Rotation Modes

尽管 Character 可以通过直接修改其 rotation 属性旋转，它还内置了一组预定义的 Rotation Modes，类似 Movement Modes。

Rotation Modes 定义如下：

```C#
public enum RotationMode
{
    /// <summary>
    /// 关闭 Character 的旋转
    /// </summary>
    None,
    
    /// <summary>
    /// 平滑旋转 Character 朝向移动加速的方向
    /// 使用 rotationRate 作为 rotation 改变的速率
    /// </summary>
    OrientRotationToMovement,
    
    /// <summary>
    /// 平滑旋转 Character 朝向 camera 的 view 方向
    /// 使用 rotationRate 作为 rotation 改变的速率
    /// </summary>
    OrientRotationToViewDirection,
    
    /// <summary>
    /// 让 root motion 处理 Character 旋转
    /// </summary>
    OrientWithRootMotion,
    
    /// <summary>
    /// User-defined custom rotation mode.
    /// </summary>
    Custom
}
```

Character 内置了以下函数用于修改它的旋转。

```C#
/// <summary>
/// 设置 Character 的当前 rotation mode
/// </summary>
public void SetRotationMode(RotationMode rotationMode)

/// <summary>
/// 设置 yaw 值
/// 这会重置当前 pitch 和 roll 值
/// </summary>
public virtual void SetYaw(float value)

/// <summary>
/// Amount to add to Yaw (up axis).
/// </summary>
public virtual void AddYawInput(float value)

/// <summary>
/// Amount to add to Pitch (right axis).
/// </summary>
public virtual void AddPitchInput(float value)

/// <summary>
/// Amount to add to Roll (forward axis).
/// </summary>
public virtual void AddRollInput(float value)
```

这些处理在下一个 simulation update 更新。

# Ground Constraint

CharacterMovement 组件，作为 Character 的控制器/马达，引入 Unity 内置 Character Controller 缺少的一个关键功能 —— GroundConstraint。这个功能对于确保 character 留在 walk-able 表面扮演一个关键角色，阻止 Character 以高速移动时出现不想要的飞起效果。不过，这种增强功能需要​​告知系统角色何时被允许脱离地面​​，例如在进行攀爬、飞行、游泳或跳跃等活动时。

为此，我们使用 CharacterMovement 组件的 contrainToGround 属性来显式开启或关闭它。或者，Character PauseGroundConstraint 方法可以用于在 N 秒内临时暂停 ground constraint，之后恢复。

例如，一个基本的跳跃：

```C#
// 临时关闭 ground constraint 以允许 character 离开地面
PauseGroundConstraint(0.1f);

// 应用一个垂直冲量到 Character 上
LaunchCharacter(Vector3.up * 10.0f);
```

# Events

Character 提供了一组多样的 events 和 event handlers，可以用于在局部上下文（例如一个 Character 的派生类）或全局地响应 actions。

```C#
/// <summary>
/// Event triggered when a character enter or leaves a PhysicsVolume.
/// </summary>
public event PhysicsVolumeChangedEventHandler PhysicsVolumeChanged;

/// <summary>
/// Event triggered when a MovementMode change.
/// </summary>
public event MovementModeChangedEventHandler MovementModeChanged;

/// <summary>
/// Event for implementing custom character movement mode.
/// Called if MovementMode is set to Custom.
/// </summary>
public event CustomMovementModeUpdateEventHandler CustomMovementModeUpdated;

/// <summary>
/// Event for implementing custom character rotation mode.
/// Called when RotationMode is set to Custom.
/// </summary>
public event CustomRotationModeUpdateEventHandler CustomRotationModeUpdated;

/// <summary>
/// Event called before character simulation updates.
/// This 'hook' lets you externally update the character 'state'.
/// </summary>
public event BeforeSimulationUpdateEventHandler BeforeSimulationUpdated;

/// <summary>
/// Event called after character simulation updates.
/// This 'hook' lets you externally update the character 'state'.
/// </summary>
public event AfterSimulationUpdateEventHandler AfterSimulationUpdated;

/// <summary>
/// Event called when CharacterMovement component is updated (ie. Move call).
/// At this point the character movement has completed and its state is current. 
/// This 'hook' lets you externally update the character 'state'.
/// </summary>
public event CharacterMovementUpdateEventHandler CharacterMovementUpdated;

/// <summary>
/// Event triggered when characters collides with other during a Move.
/// Can be called multiple times.
/// </summary>
public event CollidedEventHandler Collided;

/// <summary>
/// Event triggered when a character finds ground (walkable or non-walkable)
/// as a result of a downcast sweep (eg: FindGround method).
/// </summary>
public event FoundGroundEventHandler FoundGround;

/// <summary>
/// Event triggered when a character is falling and finds walkable ground
/// as a result of a downcast sweep (eg: FindGround method).
/// </summary>
public event LandedEventHandled Landed;

/// <summary>
/// Event triggered when Character enters crouching state.
/// </summary>
public event CrouchedEventHandler Crouched;

/// <summary>
/// Event triggered when character exits crouching state.
/// </summary>
public event UnCrouchedEventHandler UnCrouched;

/// <summary>
/// Event triggered when character jumps.
/// </summary>
public event JumpedEventHandler Jumped;

/// <summary>
/// Triggered when Character reaches jump apex (eg: change in vertical speed
/// from positive to negative).
/// Only triggered if notifyJumpApex == true.
/// </summary>
public event ReachedJumpApexEventHandler ReachedJumpApex;
```

发起这些 events 的对应 virtual 方法是：

```C#
/// <summary>
/// Called when this Character's PhysicsVolume has been changed.
/// </summary>
protected virtual void OnPhysicsVolumeChanged(PhysicsVolume newPhysicsVolume)

/// <summary>
/// Called after MovementMode has changed.
/// Does special handling for starting certain modes, eg:
/// enable / disable ground constraint, etc.
/// If overridden, base method MUST be called.
/// </summary>
protected virtual void OnMovementModeChanged(MovementMode prevMovementMode, int prevCustomMode)

/// <summary>
/// Event for implementing custom character movement mode.
/// Called if MovementMode is set to Custom.
/// Derived Character classes should override CustomMovementMode method instead. 
/// </summary>
protected virtual void OnCustomMovementMode(float deltaTime)

/// <summary>
/// Event for implementing custom character rotation mode.
/// Called if RotationMode is set to Custom.
/// Derived Character classes should override CustomRotationMode method instead. 
/// </summary>
protected virtual void OnCustomRotationMode(float deltaTime)

/// <summary>
/// Called at the beginning of the Character Simulation, before current movement mode update.
/// This 'hook' lets you externally update the character 'state'.
/// </summary>
protected virtual void OnBeforeSimulationUpdate(float deltaTime)

/// <summary>
/// Called after current movement mode update.
/// This 'hook' lets you externally update the character 'state'. 
/// </summary>
protected virtual void OnAfterSimulationUpdate(float deltaTime)

/// <summary>
/// Event called when CharacterMovement component is updated (ie. Move call).
/// At this point the character movement has been applied and its state is current. 
/// This 'hook' lets you externally update the character 'state'.
/// </summary>
protected virtual void OnCharacterMovementUpdated(float deltaTime)

/// <summary>
/// Event triggered when characters collides with other during a CharacterMovement Move call.
/// Can be called multiple times.
/// </summary>
protected virtual void OnCollided(ref CollisionResult collisionResult)

/// <summary>
/// Event triggered when a character find ground (walkable or non-walkable)
/// as a result of a downcast sweep (eg: FindGround method).
/// </summary>
protected virtual void OnFoundGround(ref FindGroundResult foundGround)

/// <summary>
/// Event triggered when character enter Walking movement mode
/// (ie: isOnWalkableGround AND isConstrainedToGround).
/// </summary>
protected virtual void OnLanded(Vector3 landingVelocity)

/// <summary>
/// Called when character crouches.
/// </summary>
protected virtual void OnCrouched()

/// <summary>
/// Called when character un crouches.
/// </summary>
protected virtual void OnUnCrouched()

/// <summary>
/// Called when a jump has been successfully triggered.
/// </summary>
protected virtual void OnJumped()

/// <summary>
/// Called when Character reaches jump apex
/// (eg: change in vertical speed from positive to negative).
/// Only triggered if notifyJumpApex == true.
/// </summary>
protected virtual void OnReachedJumpApex()
```

Character 派生类鼓励使用 virtual 方法，而不是注册 event 来处理这些事件。events 用于外界订阅相应事件。

为了接收 ReachedJumpApex 事件，必须提前设置 notifyJumpApex 属性，否则事件不会触发。

```C#
protected override void OnJumped()
{
    // Call base method implementation
    
    base.OnJumped();
    
    // Add your code here...
    
    Debug.Log("Jumped!");
    
    // Enable apex notification event
    
    notifyJumpApex = true;
}

protected override void OnReachedJumpApex()
{
    // Call base method implementation
    
    base.OnReachedJumpApex();
    
    // Add your code here...
    
    Debug.Log($"Apex reached {GetVelocity():F4}");
}
```

# Collisions

尽管你可以灵活地使用 Unity 的 OnTriggerXXX 和 OnEnterXXX 事件，Character 类（就像 Unity 内置的 CharacterController）包含了专用方法和事件，专门设计用于管理角色在最近的 CharacterMovement.Move 调用中的碰撞检测。

```C#
/// <summary>
/// Event triggered when character collides during a Move.
/// Can be called multiple times.
/// </summary>
public event CollidedEventHandler Collided;

/// <summary>
/// Event triggered when character collides during a CharacterMovement Move call.
/// Can be called multiple times.
/// </summary>
protected virtual void OnCollided(ref CollisionResult collisionResult)
```

## Custom Character Class Responding to Collision Event

```C#
public class PlayerCharacter : Character
{
    protected override void OnCollided(ref CollisionResult collisionResult)
    {
        // Call base method implementation
        
        base.OnCollided(ref collisionResult);
        
        // Handle collision here...
        
        Debug.Log($"Collided with {collisionResult.collider.name}");
    }
}
```

更进一步，你可以方便地遍历访问最近一次 movement 期间的所有 collisions：

```C#
for (int i = 0, c = characterMovement.GetCollisionCount(); i < c; i++)
{
    CollisionResult collisionResult = characterMovement.GetCollisionResult(i);
    
    // Handle collision here...
}
```

## Listening to Character Collision Events

Non Character-based 类应该订阅 Character Collided 事件，例如：

```C#
public class OtherClass : MonoBehaviour
{
    public Character character;

    protected void OnCollided(ref CollisionResult collisionResult)
    {
        Debug.Log($"Collided with {collisionResult.collider.name}");
    }

    private void OnEnable()
    {
        // Subscribe to Character events
            
        character.Collided += OnCollided;
    }

    private void OnDisable()
    {
        // Un-subscribe from Character events
        
        character.Collided -= OnCollided;
    }
}
```

## Collision Filtering

很多游戏场景中，有时需要忽略和另一个 Character、特定 collider、甚至要给 rigidbody 上挂载的所有 colliders 的碰撞。为此，CharacterMovement 组件内置了一组函数允许你方便地定义你想要的交互。

```C#
/// <summary>
/// Makes the character's collider (eg: CapsuleCollider) to ignore all collisions
/// vs otherCollider.
/// NOTE: The character can still collide with other during a Move call
/// if otherCollider is in its collisionLayers mask.
/// </summary>

public void CapsuleIgnoreCollision(Collider otherCollider, bool ignore = true)

/// <summary>
/// Makes the character to ignore all collisions vs otherCollider.
/// </summary>

public void IgnoreCollision(Collider otherCollider, bool ignore = true)

/// <summary>
/// Makes the character to ignore collisions vs all colliders attached
/// to the otherRigidbody.
/// </summary>

public void IgnoreCollision(Rigidbody otherRigidbody, bool ignore = true)
```

当需要更精细的控制时，可使用 CharacterMovement ColliderFilterCallback。它允许你基于游戏条件，选择性地忽略特定 colliders。

```C#
/// <summary>
/// Let you define if the character should collide with given collider.
/// Return true to filter (ignore) collider, false otherwise.
/// </summary>

public ColliderFilterCallback colliderFilterCallback { get; set; }
```

例如，要忽略与其他使用 CharacterMovement 组件的的 collisions：

```C#
private bool ColliderFilterCallback(Collider collider)
{
    // If collider is a character (e.g. using CharacterMovement component)
    // ignore collisions with it (e.g. filter it)

    if (collider.TryGetComponent(out CharacterMovement _))
        return true;
        
    return false;
}
```

# Physics Interactions

当开启时，Character 可以和其他 rigidbodies 交互 —— 推开它们或被它们推开，也可以和其他 character 交互，应用 forces，爆炸力，downward forces 等等。这些交互被 CharacterMovement 组件管理，并且默认地，最终行为被 characters 的质量影响。更大质量的会更容易推开质量更小的。

默认行为可以使用 CharacterMovement collisionResponseCallback 函数修改。这允许你调整以任意方式按照游戏需要调整计算后的 collision 的响应冲量。

```C#
/// <summary>
/// Let you modify the collision response vs dynamic objects,
/// eg: compute resultant impulse and / or application point (CollisionResult.point).
/// </summary>

public delegate void CollisionResponseCallback(ref CollisionResult inCollisionResult, ref Vector3 characterImpulse, ref Vector3 otherImpulse);
```

impulses 代表计算后的结果 collision 响应冲量，这可以按需修改。

此外，Character 类包含一组函数来全局地影响角色。这些函数类似 Unity 的 Rigidbody 函数，例如 AddForce，AddExplosionForce，以及一个名为 LaunchCharacter 的自定义函数。

```C#
/// <summary>
/// 为 Character 添加一个 force
/// 这些 forces 会累积，并在 Move 方法调用期间应用
/// </summary>

public void AddForce(Vector3 force, ForceMode forceMode = ForceMode.Force)

/// <summary>
/// 为 Rigidbody 应用一个 force 来模拟爆炸效果
/// 爆炸建模为一个球体，有一个世界空间中的中心位置和半径
/// 正常地，球体之外的任何事情不会被爆炸影响，而球体中被爆炸影响，爆炸力从球体中心随距离按比例衰减
/// 但是，如果为 radius 传递 0，force 全部都会应用到 rigidbody 上，不管它离 center 有多远
/// </summary>
/// 
public void AddExplosionForce(float forceMagnitude, Vector3 origin, float explosionRadius, ForceMode forceMode = ForceMode.Force)
    
/// <summary>
/// 在 Character 设置一个 pending launch 速度。这个速度会在下一个 Move 调用中被处理
/// 如果 overrideVerticalVelocity 为 true，替换 Character 的速度的垂直分量，而不是添加到其上面
/// 如果 overrideLateralVelocity 为 true，替换 Character 的速度的 X、Y 分离（没有 Z 分量），而不是添加到其上面
/// </summary>

public void LaunchCharacter(Vector3 launchVelocity, bool overrideVerticalVelocity = false, bool overrideLateralVelocity = false)
```

# Animating a Character

当动画一个 character，你应该查询 character 的状态，订阅它的各种 events，将 character 的状态信息输入给 AnimationController 的参数，来确保 animation 完美地与 character state 同步，例如它是否落在地面上，是否 falling，jumping 等等。

ECM2 不需要使用动画或任何动画技术。你拥有使用普通 Unity code 或其他想要的方法来自由动画角色的自由。

## Querying Character State

Character 类提供大量方法、事件、委托，你可以利用它们访问 character 的信息，包括 GetPosition、GetRotation、GetVelocity、IsWalking、IsFalling、IsOnWalkableGround 等等。它们应该用于保持和动画系统的同步。

除了这些 Character 提供的信息，你还可以通过 CharacterMovement 组件访问更多详细信息，包括 ground-related 信息，获取和调整角色 capsule collider 的维度，访问碰撞检测函数，甚至计算一组新的 ground-related 细节的能力（例如，is walk-able，is a step，到 ground 的距离等等）。

下面的例子展示如何使用 Character 提供的信息输入给 Animator 参数来动画 UnityCharacter。

```C#
private void Update()
{
    float deltaTime = Time.deltaTime;

    // Get Character animator

    Animator animator = _character.GetAnimator();

    // Compute input move vector in local space

    Vector3 move = transform.InverseTransformDirection(_character.GetMovementDirection());

    // Update the animator parameters

    float forwardAmount = _character.useRootMotion && _character.GetRootMotionController()
        ? move.z
        : Mathf.InverseLerp(0.0f, _character.GetMaxSpeed(), _character.GetSpeed());

    animator.SetFloat(Forward, forwardAmount, 0.1f, deltaTime);
    animator.SetFloat(Turn, Mathf.Atan2(move.x, move.z), 0.1f, deltaTime);

    animator.SetBool(Ground, _character.IsGrounded());
    animator.SetBool(Crouch, _character.IsCrouched());

    if (_character.IsFalling())
        animator.SetFloat(Jump, _character.GetVelocity().y, 0.1f, deltaTime);

    // Calculate which leg is behind, so as to leave that leg trailing in the jump animation
    // (This code is reliant on the specific run cycle offset in our animations,
    // and assumes one leg passes the other at the normalized clip times of 0.0 and 0.5)

    float runCycle = Mathf.Repeat(animator.GetCurrentAnimatorStateInfo(0).normalizedTime + 0.2f, 1.0f);
    float jumpLeg = (runCycle < 0.5f ? 1.0f : -1.0f) * forwardAmount;

    if (_character.IsGrounded())
        animator.SetFloat(JumpLeg, jumpLeg);
}
```

如你所见，它基于 Character 组件提供的信息更新 Animator 参数。

## Utilizing Root Motion

Root motion 引用直接集成在 animation 中的运动，而 animation 自己指示 object 移动了多远，而不是依赖 code。

要在 Character 派生类中内置 root motion，遵循以下步骤：

- 添加 RootMotionController 组件到你的模型的 GameObject 上。这个 RootMotionController 负责提供 animation 的 velocity，rotation 等信息给 Character。
- 在 Character 中开启 useRootMotion 属性。这个属性可以按需 toggled。

一旦 character 使用 root motion 移动，animation 将完全掌控角色的运动逻辑。这将取代所有程序化移动，使得诸如 maxWalkSpeed，maxFallSpeed 等属性变得无关紧要，因为角色完全由动画驱动。

```
一旦角色通过根运动（Root Motion）移动，动画将完全掌控角色的运动逻辑  
在游戏开发中，根运动是一种让动画本身驱动角色位置、旋转等运动的技术。当角色通过根运动移动时，原本由程序代码（如CharacterMovementComponent）控制的运动权限会转移至动画系统——动画中的根骨骼（Root Bone）位移数据会成为角色运动的唯一指令。这意味着，所有程序化的运动控制（如通过transform.Translate()实现的位移、速度调整等）都将失效，动画中的每一个细微移动（如前进、转向、跳跃的轨迹）都会精准传递到角色的Transform组件上，实现“动画驱动运动”的效果。  

这种机制的优势在于彻底解决了“滑步”问题：动画师在DCC工具（如Maya、Blender）中制作的根骨骼位移会被完整保留，角色移动与动画节奏完全同步。例如，角色跑步时，动画中的脚步位移会直接驱动角色向前移动，不会出现“动画做了位移但角色没动”的脱节现象。同时，根运动还能支持复杂动作的精准还原，如格斗游戏中的翻滚、ARPG中的后空翻，动画师制作的根位移能让这些动作在游戏中的表现更加自然。  

需要注意的是，启用根运动后，动画系统会根据根骨骼的位移数据覆盖程序化的运动控制，因此开发者需要在动画制作阶段确保根骨骼包含正确的位移信息（如非原地动画），避免动画中的位移与游戏场景需求冲突。此外，根运动对物理系统的影响也需要关注，例如角色在飞行模式下，根运动中的Z轴位移会被忽略，重力仍会作用于角色，确保运动的合理性。
```

值得注意的是，root motion 开启时，character 的 ground constraint 仍然应用，这暗示你的 motion-based 动画的任何垂直运动都不会工作，除非你显式关闭 ground constraint。这些情形下，建议设定 flying movement mode，因为它自动关闭 ground constraint，并允许全部的 vertical movement。
