# 第一人称控制器

本示例展示了如何在Unity中使用Cinemachine实现第一人称控制器。它利用Cinemachine虚拟相机的第三人称跟随功能来实现完整的体验。该脚本包含相机设置、鼠标灵敏度的配置，以及管理玩家输入以实现移动、旋转、蹲伏和跳跃的功能。

此外，该示例还无缝集成了事件处理机制，专门用于管理蹲伏和下蹲动作期间的相机过渡效果。总体而言，它为基于Cinemachine的第一人称视角提供了坚实的实现基础，能够有效协调相机控制与玩家交互两大核心功能。

在此设置中，角色将管理偏航旋转（沿角色上轴的旋转），而作为子对象的"Camera Target"游戏对象将处理相机的俯仰旋转。

```C#
public class FirstPersonController : MonoBehaviour
{
    ..

    /// <summary>
    /// Add input (affecting Yaw).
    /// This is applied to the Character's rotation.
    /// </summary>
    
    public void AddControlYawInput(float value)
    {
        _character.AddYawInput(value);
    }
    
    /// <summary>
    /// Add input (affecting Pitch).
    /// This is applied to the cameraTarget's local rotation.
    /// </summary>
    
    public void AddControlPitchInput(float value, float minValue = -80.0f, float maxValue = 80.0f)
    {
        if (value == 0.0f)
            return;
        
        _cameraTargetPitch = MathLib.ClampAngle(_cameraTargetPitch + value, minValue, maxValue);
        cameraTarget.transform.localRotation = Quaternion.Euler(-_cameraTargetPitch, 0.0f, 0.0f);
    }
}
```

关闭 character 的 rotation mode 很重要，因此这里我们自己处理它们：

```C#
private void Start()
{
    Cursor.lockState = CursorLockMode.Locked;
    
    // Disable Character's rotation mode, we'll handle it here
    
    _character.SetRotationMode(Character.RotationMode.None);
}
```

此外，我们使用 Character 的 Crouched 和 UnCrouched 事件来触发 crouch/uncrouch 动画，依赖 Cinemachine 的 transitions。

```C#
private void OnEnable()
{
    // Subscribe to Character events
    
    _character.Crouched += OnCrouched;
    _character.UnCrouched += OnUnCrouched;
}

private void OnDisable()
{
    // Unsubscribe to Character events
    
    _character.Crouched -= OnCrouched;
    _character.UnCrouched -= OnUnCrouched;
}

..

/// <summary>
/// When character crouches, toggle Crouched / UnCrouched cameras.
/// </summary>

private void OnCrouched()
{
    crouchedCamera.SetActive(true);
    unCrouchedCamera.SetActive(false);
}

/// <summary>
/// When character un-crouches, toggle Crouched / UnCrouched cameras.
/// </summary>

private void OnUnCrouched()
{
    crouchedCamera.SetActive(false);
    unCrouchedCamera.SetActive(true);
}
```

最后，我们处理 player input：

```C#
private void Update()
{
    // Movement input
    
    Vector2 moveInput = new Vector2
    {
        x = Input.GetAxisRaw("Horizontal"),
        y = Input.GetAxisRaw("Vertical")
    };
    
    // Movement direction relative to Character's forward

    Vector3 movementDirection = Vector3.zero;

    movementDirection += _character.GetRightVector() * moveInput.x;
    movementDirection += _character.GetForwardVector() * moveInput.y;
    
    // Set Character movement direction

    _character.SetMovementDirection(movementDirection);
    
    // Look input

    Vector2 lookInput = new Vector2
    {
        x = Input.GetAxisRaw("Mouse X"),
        y = Input.GetAxisRaw("Mouse Y")
    };
    
    // Add yaw input, this update character's yaw rotation

    AddControlYawInput(lookInput.x * lookSensitivity.x);
    
    // Add pitch input (look up / look down), this update cameraTarget's local rotation
    
    AddControlPitchInput(lookInput.y * lookSensitivity.y, minPitch, maxPitch);
    
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
```

# 第三人称控制器

以下示例展示了如何在Unity中使用Cinemachine实现第三人称控制器。该方案利用Cinemachine虚拟相机的第三人称跟随功能，提供完整的游戏体验。该控制器包含相机参数配置、鼠标灵敏度设置，以及玩家输入管理（涵盖移动、旋转、蹲伏和跳跃等操作）。

首先，我们实现控制相机旋转和调整其跟随距离的方法：

```C#
/// <summary>
/// Add input (affecting Yaw). 
/// This is applied to the followTarget's yaw rotation.
/// </summary>

public void AddControlYawInput(float value, float minValue = -180.0f, float maxValue = 180.0f)
{
    if (value != 0.0f) _cameraTargetYaw = MathLib.ClampAngle(_cameraTargetYaw + value, minValue, maxValue);
}

/// <summary>
/// Add input (affecting Pitch). 
/// This is applied to the followTarget's pitch rotation.
/// </summary>

public void AddControlPitchInput(float value, float minValue = -80.0f, float maxValue = 80.0f)
{
    if (value == 0.0f)
        return;
    
    if (invertLook)
        value = -value;
    
    _cameraTargetPitch = MathLib.ClampAngle(_cameraTargetPitch + value, minValue, maxValue);
}

/// <summary>
/// Adds input (affecting follow distance).
/// </summary>

public virtual void AddControlZoomInput(float value)
{
    followDistance = Mathf.Clamp(followDistance - value, followMinDistance, followMaxDistance);
}
```

随后，我们同时调整followTarget游戏对象的旋转和Cinemachine虚拟相机的CameraDistance。这本质上意味着我们通过操控followTarget游戏对象来控制Cinemachine相机。

```C#
/// <summary>
/// Update followTarget rotation using _cameraTargetYaw and _cameraTargetPitch values and its follow distance.
/// </summary>

private void UpdateCamera()
{
    followTarget.transform.rotation = Quaternion.Euler(_cameraTargetPitch, _cameraTargetYaw, 0.0f);
    
    _cmThirdPersonFollow.CameraDistance = 
        Mathf.SmoothDamp(_cmThirdPersonFollow.CameraDistance, followDistance, ref _followDistanceSmoothVelocity, 0.1f);
}

private void LateUpdate()
{
    // Update cameraTarget rotation using our yaw and pitch values
    
    UpdateCamera();
}
```

最后，我们处理 player input：

```C#
private void Update()
{
    // Movement input
    
    Vector2 inputMove = new Vector2()
    {
        x = Input.GetAxisRaw("Horizontal"),
        y = Input.GetAxisRaw("Vertical")
    };
    
    // Set Movement direction in world space
    
    Vector3 movementDirection =  Vector3.zero;

    movementDirection += Vector3.right * inputMove.x;
    movementDirection += Vector3.forward * inputMove.y;
    
    // If character has a camera assigned...
    
    if (_character.camera)
    {
        // Make movement direction relative to its camera view direction
        
        movementDirection = movementDirection.relativeTo(_character.cameraTransform);
    }
    
    // Set Character movement direction

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
    
    // Look input

    Vector2 lookInput = new Vector2
    {
        x = Input.GetAxisRaw("Mouse X"),
        y = Input.GetAxisRaw("Mouse Y")
    };
    
    AddControlYawInput(lookInput.x * lookSensitivity.x);
    AddControlPitchInput(lookInput.y * lookSensitivity.y, minPitch, maxPitch);
    
    // Zoom (in / out) input

    float mouseScrollInput = Input.GetAxisRaw("Mouse ScrollWheel");
    AddControlZoomInput(mouseScrollInput);
}
```
