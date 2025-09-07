当作为一个 Kinematic Character Controller，CharacterMovement 组件也称为 Motor，可以无缝地执行物理交互，包括推开 rigidbodies 或其他 character，响应外部 forces，处理动态平台。

下面例子展示如何使用 Character LaunchCharacter 函数来实现一个 bouncer。

```C#
public class Bouncer : MonoBehaviour
{
    public float launchImpulse = 15.0f;

    public bool overrideVerticalVelocity;
    public bool overrideLateralVelocity;

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player"))
            return;

        if (!other.TryGetComponent(out Character character))
            return;
        
        character.PauseGroundConstraint();
        character.LaunchCharacter(transform.up * launchImpulse, overrideVerticalVelocity, overrideLateralVelocity);
    }
}
```

需要注意的是PauseGroundConstraint的使用。这会暂时禁用角色的地面约束，使角色能够自由离开可行走的地面。

下面的例子展示如何通过组合扩展 Character，以应用一个 landing force。这使用 Landed 事件：

```C#
public class ApplyLandingForce : MonoBehaviour
{
    public float landingForceScale = 1.0f;
    
    private Character _character;

    private void Awake()
    {
        _character = GetComponent<Character>();
    }

    private void OnEnable()
    {
        _character.Landed += OnLanded;
    }

    private void OnDisable()
    {
        _character.Landed -= OnLanded;
    }

    private void OnLanded(Vector3 landingVelocity)
    {
        Rigidbody groundRigidbody = _character.characterMovement.groundRigidbody;
        if (!groundRigidbody)
            return;
        
        Vector3 force = _character.GetGravityVector() *
                        (_character.mass * landingVelocity.magnitude * landingForceScale);
            
        groundRigidbody.AddForceAtPosition(force, _character.position);
    }
}
```

这里 landing force 的计算公式为：characterMass * characterGravity * landingVelocity * landingForceMag，并沿着 character 的重力方向应用。
