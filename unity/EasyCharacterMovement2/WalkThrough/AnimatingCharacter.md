# Root Motion

当动画一个 Character，你应该查询 character 的 state 并订阅它的各种 events，将这些信息输入给 AnimationController 参数，以确保动画完美地与 Character 状态同步，无论它是 Grounded，Falling，Jumping 还是其他状态。

ECM2 不需要使用 animation，或任何动画技术。你可以自由地使用 plain Unity code 或其他喜欢的方法来控制 Character。

```C#
/// <summary>
/// This example shows how to animate a Character,
/// using the Character data (movement direction, velocity, is jumping, etc) to feed your Animator.
/// </summary>

public class AnimationController : MonoBehaviour
{
    // Cache Animator parameters
    
    private static readonly int Forward = Animator.StringToHash("Forward");
    private static readonly int Turn = Animator.StringToHash("Turn");
    private static readonly int Ground = Animator.StringToHash("OnGround");
    private static readonly int Crouch = Animator.StringToHash("Crouch");
    private static readonly int Jump = Animator.StringToHash("Jump");
    private static readonly int JumpLeg = Animator.StringToHash("JumpLeg");
    
    // Cached Character
    
    private Character _character;

    private void Awake()
    {
        // Cache our Character
        
        _character = GetComponentInParent<Character>();
    }

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
}
```

如你所见，这是标准的 Unity code，它使用 character 的状态信息控制 animator。

# Root Motion

Character 类内置对 root motion 支持。

# Utilizing Root Motion

要开启 root motion，使用以下步骤：

1. 添加 RootMotionController 组件到模型的 GameObject。RootMotionController 负责为 Character 提供动画中的 velocity，rotation 等等。
2. 在 Character 中开启 useRootMotion 属性。这个属性可以按需 toggle。

一旦 character 通过 root motion 移动，动画完全控制 character 的运动。这替换所有的过程化运动，以及诸如 maxWalkSpeed，maxFallSpeed 等无关的渲染属性。

值得注意的是，character 的 ground constraint 在 root motion 开启时仍然应用。这暗示基于 root motion 的动画中的任何垂直速度，都不会工作，除非你显式关闭它。在此场景中，建议设置 Flying movement mode，因为它自动关闭 ground constraint，并且允许垂直运动。

要开启 vertical root motion movement，Character 的 movement mode 必须设置为 Flying。

# Toggling Root Motion

这个例子展示如何在运行时 toggle root motion。这里只在 character 在 walking movement mode 时开启 root motion。

```C#
public class RootMotionToggle : MonoBehaviour
{
    private Character _character;
    
    private void OnMovementModeChanged(Character.MovementMode prevMovementMode, int prevCustomMovementMode)
    {
        // Allow root motion only while walking
        
        _character.useRootMotion = _character.IsWalking();
    }

    private void Awake()
    {
        _character = GetComponent<Character>();
    }

    private void OnEnable()
    {
        // Subscribe to Character events
        
        _character.MovementModeChanged += OnMovementModeChanged;
    }

    private void OnDisable()
    {
        // Un-Subscribe from Character events
        
        _character.MovementModeChanged -= OnMovementModeChanged;
    }
}
```

这个例子中，使用 MovementModeChange 事件，每次 character 改变它的 movement mode 时触发，非常适合这个用例。
