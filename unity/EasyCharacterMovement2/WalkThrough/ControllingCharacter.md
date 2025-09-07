# Custom Character

Character 包含了一组方法设计用来让 action 执行更便捷。例如 SetMovementDirection 方法指示 character 沿着世界空间中指定的 direction 移动。

类似地，Jump 方法发起一个 Jump，而 StopJumping 方法停止一个正在进行的 Jump，这在使用可变 jump height 时非常重要。

类似的，Crouch 方法发起一个 character 的下蹲动作，UnCrouch 方法用于取消下蹲状态。

# Custom Character

这个例子展示如何在 Character 派生类中控制 player。

```C#
/// <summary>
/// This example shows how to extend a Character (through inheritance)
/// adding input management.
/// </summary>

public class PlayerCharacter : Character
{
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
    }
}
```

# Controlling a Character

这个例子展示如何在 Character 外部控制它。

```C#
using UnityEngine;
using ECM2;

public class CharacterInput : MonoBehaviour
{
    // The controlled Character
    
    private Character _character;

    private void Awake()
    {
        // Cache controlled character
        
        _character = GetComponent<Character>();
    }

    private void Update()
    {
        // Poll movement input
        
        Vector2 inputMove = new Vector2()
        {
            x = Input.GetAxisRaw("Horizontal"),
            y = Input.GetAxisRaw("Vertical")
        };
        
        // Compose a movement direction vector in world space
        
        Vector3 movementDirection =  Vector3.zero;

        movementDirection += Vector3.right * inputMove.x;
        movementDirection += Vector3.forward * inputMove.y;
        
        // If character has a camera assigned,
        // make movement direction relative to this camera view direction
        
        if (_character.camera)
        {               
            movementDirection 
                = movementDirection.relativeTo(_character.cameraTransform);
        }
        
        // Set character's movement direction vector

        _character.SetMovementDirection(movementDirection);
        
        // Crouch input
        
        if (Input.GetKeyDown(KeyCode.LeftControl) || Input.GetKeyDown(KeyCode.C))
            _character.Crouch();
        else if (Input.GetKeyUp(KeyCode.LeftControl) || Input.GetKeyUp(KeyCode.C))
            _character.UnCrouch();
        
        // Jump input
        
        if (Input.GetButtonDown("Jump"))
            _character.Jump();
        else if (Input.GetButtonUp("Jump"))
            _character.StopJumping();
    }
}
```

最后，添加新创建的 CharacterInput 脚本到 Character GameObject。这样 Character 就可以移动、跳跃和下蹲了。

Crouching 和 Uncrouching 仅仅操作 character 的 capsule collider，不会影响 character 的模型。

# Using Input System

下面的例子显示如何使用 InputSystem 控制 character。这里使用了 PlayerInput 组件，它极大简化了 input controls 的设置和管理。

PlayerInput 组件高效地处理 input actions，负责初始化、反初始化、处理输入、事件触发等等。结果就是，我们的主要工作就是简单地为 actions 创建 event handlers。

```C#
using ECM2;
using UnityEngine;
using UnityEngine.InputSystem;

public class CharacterInput : MonoBehaviour
{
    // Cached controlled character
        
    private Character _character;
    
    /// <summary>
    /// Movement InputAction event handler.
    /// </summary>

    public void OnMove(InputAction.CallbackContext context)
    {
        // Read input values

        Vector2 inputMovement = context.ReadValue<Vector2>();

        // Compose a movement direction vector in world space

        Vector3 movementDirection = Vector3.zero;

        movementDirection += Vector3.forward * inputMovement.y;
        movementDirection += Vector3.right * inputMovement.x;

        // If character has a camera assigned,
        // make movement direction relative to this camera view direction

        if (_character.camera)
        {               
            movementDirection 
                = movementDirection.relativeTo(_character.cameraTransform);
        }
    
        // Set character's movement direction vector

        _character.SetMovementDirection(movementDirection);
    }

    /// <summary>
    /// Jump InputAction event handler.
    /// </summary>

    public void OnJump(InputAction.CallbackContext context)
    {
        if (context.started)
            _character.Jump();
        else if (context.canceled)
            _character.StopJumping();
    }

    /// <summary>
    /// Crouch InputAction event handler.
    /// </summary>

    public void OnCrouch(InputAction.CallbackContext context)
    {
        if (context.started)
            _character.Crouch();
        else if (context.canceled)
            _character.UnCrouch();
    }

    private void Awake()
    {
        //
        // Cache controlled character.
        
        _character = GetComponent<Character>();
    }
}
```

之后在 PlayerInput 组件上为 Input Action 设置相应的回调方法。
