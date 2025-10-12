# Custom Character（继承）

角色类的显著特性之一，在于它能为所有游戏角色提供高度稳健的基础支撑。借助它，用户能够通过添加贴合自身游戏需求的特定功能与机制，来扩展其功能。

这个例子展示如何使用继承来扩展 Character。在这个场景中，将会添加冲刺 Sprint 能力。

继承相较于组合的优势之一，在于它能够扩展基类中的方法，让我们可以根据自身需求修改这些方法的功能。其中，我们会重点用到GetMaxSpeed方法。顾名思义，该方法会返回角色在特定状态或移动模式下的最大移动速度，这一特性使其非常适合用于实现“冲刺”这类需要临时提升速度的功能。

此外，我们将利用1.4版本中新增的一个方法，即OnBeforeSimulationUpdate。这个方法简化了在角色模拟循环内修改角色状态的过程，从而增强了对角色控制器功能的整体灵活性和控制力。

首先，我们会创建一个名为 SprintableCharacter：

```C#
public class SprintableCharacter : Character
{
    // TODO
}
```

在扩展Character类时，建议遵循该类既定的设计规范，通过创建一组控制新添加能力执行的方法来实现。要确保这些方法遵循角色内置函数的模式，例如Jump（跳跃）、StopJumping（停止跳跃）、Crouch（蹲下）、UnCrouch（取消蹲下）等。在本特定场景中，这些方法专门用于管理冲刺（Sprint）能力。

```C#
public class SprintableCharacter : Character
{
    [Space(15.0f)]
    public float maxSprintSpeed = 10.0f;
        
    private bool _isSprinting;
    private bool _sprintInputPressed;
    
    public void Sprint()
    {
        _sprintInputPressed = true;
    }

    public void StopSprinting()
    {
        _sprintInputPressed = false;
    }

    public bool IsSprinting()
    {
        return _isSprinting;
    }

    private bool CanSprint()
    {
        // A character can only sprint if:
        // A character is in its walking movement mode and not crouched
            
        return IsWalking() && !IsCrouched();
    }

    private void CheckSprintInput()
    {
        if (!_isSprinting && _sprintInputPressed && CanSprint())
        {
            _isSprinting = true;
        }
        else if (_isSprinting && (!_sprintInputPressed || !CanSprint()))
        {
            _isSprinting = false;
        }
    }
}
```

SprintableCharacter 类作为这种方法论的示例。变量 maxSprintSpeed 定义了角色在冲刺时的最高速度，而 _isSprinting 变量则指示角色的持续状态。此外，_sprintInputPressed 变量负责监督能力的激活，通常由输入事件（如按键按下或释放动作）触发。

CheckSprintInput 方法遵循前文提到的模式。像 Sprint 和 StopSprinting 这样的动作执行方法会促使角色执行特定动作。该请求会在 CheckSprintInput 方法中进行处理，其中 CanSprint 方法会判断角色是否具备开始冲刺的条件或者是否应该停止冲刺。

虽然并非强制要求，但在扩展 Character 类时，建议采用类似的方法。Character 类本身在实现其内置的跳跃和蹲伏功能时，就积极运用了这一方法论。

最后一步是修改角色在冲刺时的最大速度。为此，我们扩展了角色的 GetMaxSpeed 方法。通过这种扩展，当角色处于冲刺状态时，我们可以返回 maxSprintSpeed 值。

```C#
public override float GetMaxSpeed()
{
    return _isSprinting ? maxSprintSpeed : base.GetMaxSpeed();
}
```

最后，我们将基于前文提到的 OnBeforeSimulationUpdate 方法进行扩展，以实现对冲刺能力的管理。

```C#
protected override void OnBeforeSimulationUpdate(float deltaTime)
{
    // Call base method implementation
    
    base.OnBeforeSimulationUpdate(deltaTime);
    
    // Handle sprint
    
    CheckSprintInput();
}
```

要开始冲刺，我们使用 Sprint 方法；而响应输入事件（如按键操作）结束冲刺时，则调用 StopSprinting 方法。

```C#
private void Update()
{
    ..

    if (Input.GetKeyDown(KeyCode.LeftShift))
        Sprint();
    else if (Input.GetKeyUp(KeyCode.LeftShift))
        StopSprinting();
}
```

下面是完整的脚本：

```C#
/// <summary>
/// This example shows how to extend a Character (through inheritance) to perform a sprint ability.
/// This uses one of the new methods (introduced in v1.4) OnBeforeSimulationUpdate,
/// to easily modify the character's state within Character's simulation loop. 
/// </summary>

public class SprintableCharacter : Character
{
    [Space(15.0f)]
    public float maxSprintSpeed = 10.0f;
    
    private bool _isSprinting;
    private bool _sprintInputPressed;
    
    /// <summary>
    /// Request the character to start to sprint. 
    /// </summary>

    public void Sprint()
    {
        _sprintInputPressed = true;
    }
    
    /// <summary>
    /// Request the character to stop sprinting. 
    /// </summary>

    public void StopSprinting()
    {
        _sprintInputPressed = false;
    }

    public bool IsSprinting()
    {
        return _isSprinting;
    }
    
    /// <summary>
    /// Determines if the character is able to sprint in its current state.
    /// </summary>

    private bool CanSprint()
    {
        // A character can only sprint if:
        // A character is in its walking movement mode and not crouched
        
        return IsWalking() && !IsCrouched();
    }
    
    /// <summary>
    /// Start / stops a requested sprint.
    /// </summary>

    private void CheckSprintInput()
    {
        if (!_isSprinting && _sprintInputPressed && CanSprint())
        {
            _isSprinting = true;
        }
        else if (_isSprinting && (!_sprintInputPressed || !CanSprint()))
        {
            _isSprinting = false;
        }
    }
    
    /// <summary>
    /// Override GetMaxSpeed method to return maxSprintSpeed while sprinting.
    /// </summary>
    
    public override float GetMaxSpeed()
    {
        return _isSprinting ? maxSprintSpeed : base.GetMaxSpeed();
    }

    protected override void OnBeforeSimulationUpdate(float deltaTime)
    {
        // Call base method implementation
        
        base.OnBeforeSimulationUpdate(deltaTime);
        
        // Handle sprint
        
        CheckSprintInput();
    }
    
    private void Update()
    {
        // Movement input
        
        Vector2 inputMove = new Vector2()
        {
            x = Input.GetAxisRaw("Horizontal"),
            y = Input.GetAxisRaw("Vertical")
        };
        
        Vector3 movementDirection =  Vector3.zero;

        movementDirection += Vector3.right * inputMove.x;
        movementDirection += Vector3.forward * inputMove.y;
        
        // If character has a camera assigned...
        
        if (camera)
        {
            // Make movement direction relative to its camera view direction
            
            movementDirection = movementDirection.relativeTo(cameraTransform);
        }

        SetMovementDirection(movementDirection);
        
        // Crouch input
        
        if (Input.GetKeyDown(KeyCode.LeftControl) || Input.GetKeyDown(KeyCode.C))
            Crouch();
        else if (Input.GetKeyUp(KeyCode.LeftControl) || Input.GetKeyUp(KeyCode.C))
            UnCrouch();
        
        // Jump input
        
        if (Input.GetButtonDown("Jump"))
            Jump();
        else if (Input.GetButtonUp("Jump"))
            StopJumping();
        
        // SPRINT input
        
        if (Input.GetKeyDown(KeyCode.LeftShift))
            Sprint();
        else if (Input.GetKeyUp(KeyCode.LeftShift))
            StopSprinting();
    }
}
```

# Character Extension（组合）

在上节中，我们通过​​继承​​的方式演示了如何扩展现有角色类以添加冲刺功能。接下来，我们将复现相同的冲刺功能添加示例，但采用​​组合​​模式替代继承。

在面向对象编程中，组合指的是通过使用其他类的实例来构建一个类，以实现所需的功能。值得注意的是，与继承相比，组合具有一些优势。利用组合，可以动态地组合组件，从而创建更灵活、更具模块性的设计。这与继承更为僵化的结构形成对比，使得代码更容易修改和扩展。

本质上，组合通过组装更简单、独立的部件来构建复杂结构。这种方法通常能产生更易维护、更具扩展性的代码，从而形成一种优先考虑灵活性和可重用性的设计。

为实现这一目标，我们将利用1.4.0版本中最新引入的"Hooks"（事件）。这些 hooks 使我们能够在无需从Character基类继承的情况下影响角色状态。特别要说明的是，BeforeSimulationUpdated事件本质上与之前使用的OnBeforeSimulationUpdate方法发挥着相同作用。

```C#
/// <summary>
/// Event called before character simulation updates.
/// This 'hook' lets you externally update the character 'state'.
/// </summary>

public event BeforeSimulationUpdateEventHandler BeforeSimulationUpdated;
```

本质上，代码大体保持相似，仅做了一些小的修改。具体来说，CheckSprintInput 方法现在直接修改 Character 的 maxWalkSpeed 属性。之所以需要做出这一调整，是因为与之前的方法（继承）不同，在此情境下扩展 GetMaxSpeed 方法并不可行。

下面是完整的代码。

```C#
/// <summary>
/// This example shows how to extend a Character (through composition) to perform a sprint ability.
/// This one use the new simulation OnBeforeSimulationUpdate event (introduced in v1.4),
/// to easily modify the character's state within Character's simulation loop.
/// </summary>

public class SprintAbility : MonoBehaviour
{
    [Space(15.0f)]
    public float maxSprintSpeed = 10.0f;
    
    private Character _character;

    private bool _isSprinting;
    private bool _sprintInputPressed;

    private float _cachedMaxWalkSpeed;
    
    /// <summary>
    /// Request the character to start to sprint. 
    /// </summary>

    public void Sprint()
    {
        _sprintInputPressed = true;
    }
    
    /// <summary>
    /// Request the character to stop sprinting. 
    /// </summary>

    public void StopSprinting()
    {
        _sprintInputPressed = false;
    }

    public bool IsSprinting()
    {
        return _isSprinting;
    }

    private bool CanSprint()
    {
        return _character.IsWalking() && !_character.IsCrouched();
    }

    private void CheckSprintInput()
    {
        if (!_isSprinting && _sprintInputPressed && CanSprint())
        {
            _isSprinting = true;

            _cachedMaxWalkSpeed = _character.maxWalkSpeed;
            _character.maxWalkSpeed = maxSprintSpeed;

        }
        else if (_isSprinting && (!_sprintInputPressed || !CanSprint()))
        {
            _isSprinting = false;
            
            _character.maxWalkSpeed = _cachedMaxWalkSpeed;
        }
    }
    
    private void OnBeforeSimulationUpdated(float deltaTime)
    {
        // Handle sprinting
        
        CheckSprintInput();
    }

    private void Awake()
    {
        // Cache character
        
        _character = GetComponent<Character>();
    }

    private void OnEnable()
    {
        // Subscribe to Character BeforeSimulationUpdated event
        
        _character.BeforeSimulationUpdated += OnBeforeSimulationUpdated;
    }
    
    private void OnDisable()
    {
        // Un-Subscribe from Character BeforeSimulationUpdated event
        
        _character.BeforeSimulationUpdated -= OnBeforeSimulationUpdated;
    }
}
```

最后，我们使用 Sprint 和 StopSpring 方法来开始或停止 sprinting，以响应输入事件。

```C#
private SprintAbility _sprintAbility;

private void Update()
{
    ..
    
    if (Input.GetKeyDown(KeyCode.LeftShift))
        _sprintAbility.Sprint();
    else if (Input.GetKeyUp(KeyCode.LeftShift))
        _sprintAbility.StopSprinting();
}
```

如你所见，该过程与我们之前看到的非常相似，区别在于现在是由SprintAbility负责启动或停止冲刺。

# 创建一个 Custom Movement Mode

角色类集成了多种移动模式，并支持创建自定义模式。在创建新的移动模式之前，建议先尝试在现有移动模式上实现你所需的机制。例如，跳跃能力是基于下落移动模式构建的，而蹲伏机制则是基于行走移动模式构建的。

采用这种方法是为了充分利用并扩展现有代码的功能，从而更便于维护和扩展。通过基于基础移动模式添加或修改特定机制，可以构建出更加模块化且灵活的系统。

例如，如果已经有一个行走移动模式，那么在此基础上实现蹲伏机制，就可以复用行走逻辑，只需添加蹲伏所需的必要调整即可。

同样地，将跳跃能力构建在坠落移动模式之上，可以让你复用坠落逻辑，同时引入启动和控制跳跃的特定规则。这种模块化方法不仅简化了开发流程，还能确保不同移动模式之间行为的一致性和可预测性。

要创建一个新的 movement mode，首先为它定义一个 ID。例如：

```C#
public enum ECustomMovementMode
{
    None,
    Dashing,
    Climbing
}
```

这个 ID 可以用于使用 SetMovementMode 方法中实现新的 movement mode。

```C#
SetMovementMode(Movement.Custom, (int)ECustomMovementMode.Dashing);
```

在此示例中，创建了一个名为​ ​ECustomMovementMode ​​的枚举（enumeration），其中包含多种移动模式的值，例如​​None​​（无）、​​Dashing​​（冲刺）、​​Climbing​​（攀爬）等。

这个枚举的作用是帮助轻松识别不同移动模式，并在它们之间进行切换。

接下来，需要扩展 ​​CustomMovementMode​​ 方法。根据你是 ​​通过继承（继承自 Character 类）​​ 开发派生类，还是 ​​通过订阅 CustomMovementModeUpdated 事件（采用组合方式）​​ 来实现，你在这个方法中编写新移动模式的逻辑。

- 使用继承

  当从 Character 类继承时，建议扩展它的 CustomMovementMode 方法：
  
  ```C#
  public class CustomCharacter : Character
  {
      protected override void CustomMovementMode(float deltaTime)
      {
          // Call base method implementation
              
          base.CustomMovementMode(deltaTime);
              
          // Update dashing movement mode
  
          if (customMovementMode == (int)ECustomMovementMode.Dashing)
              DashingMovementMode(deltaTime);
      }
  }
  ```

- 使用组合

  另一方面，当使用组合时，你应该订阅 CustomMovementModeUpdated 事件。
  
  ```C#
  protected void OnEnable()
  {
      // Subscribe to Character Event
      
      character.CustomMovementModeUpdated += OnCustomMovementModeUpdated;
  }
  
  protected void OnDisable()
  {
      character.CustomMovementModeUpdated += OnCustomMovementModeUpdated;
  }
  
  private void OnCustomMovementModeUpdated(float deltaTime)
  {
      // Update dashing movement mode
  
      if (customMovementMode == (int)ECustomMovementMode.Dashing)
          DashingMovementMode(deltaTime);
  }
  ```

在这两种情况下，你都需要定制 ​​CustomMovementMode​​ 方法内部的逻辑，以定义角色在“冲刺（Dashing）”“攀爬（Climbing）”或其他自定义移动模式下的具体行为。这种灵活性让你能够根据不同的移动场景，为角色打造量身定制的动态用户体验。

建议使用行走（Walking）或坠落（Falling）移动模式来退出自定义移动模式，因为它们会根据角色的接地状态自动管理。

此外，在配置移动模式的“进入”（enter）或“退出”（exit）设置时，若采用​​继承​​方式开发（即从Character类派生子类），建议使用​​OnMovementModeChanged​​方法；若采用​​组合​​方式（通过订阅MovementModeChanged事件），则应使用其对应的事件处理机制。这些功能的设计目的，是为了让你能在角色进入或离开特定移动模式（如冲刺、攀爬等）时，执行精准的初始化或清理操作。

建议从Character类派生的子类通过扩展OnCustomMovementModeUpdated方法（而非订阅该事件）来实现更强大的自定义功能，并获得更无缝的集成体验。
