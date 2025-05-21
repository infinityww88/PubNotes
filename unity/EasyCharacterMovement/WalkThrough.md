# Controllers

如先前所述，控制器的核心职责是决定角色移动方式（响应用户输入、AI指令或动画等），并将移动指令传递给CharacterMovement组件执行实际位移。

ECM提供三种可扩展的基础控制器：

- BaseCharacterController：通用角色控制器
- BaseAgentController：NavMeshAgent控制角色的基类
- BaseFirstPersonController：第一人称移动的基类

推荐使用方式是继承某个基础控制器（如BaseCharacterController），通过派生自定义控制器并添加游戏特定逻辑来满足需求——毕竟最了解游戏需求的始终是开发者自己！

需特别说明：虽然建议使用现成基础控制器，但这并非强制要求。您完全可以创建独立控制器，并依赖GroundDetection和CharacterMovement组件处理位移。但继承基础控制器能直接获得大量开箱即用的功能，这通常是更优选择。

# Custom Controllers

使用ECM的推荐方式是：选择内置的基础控制器进行扩展，添加游戏特定功能。这样既能基于现有功能构建游戏基础，也可按需修改甚至完全替换控制器，而无需直接修改ECM源代码。

这种方案的核心优势在于实现游戏代码与资源代码分离——当您更新ECM时，游戏代码将完全不受影响。

创建自定义控制器非常简单：

新建继承自基础控制器（如BaseCharacterController）的类，重写所需方法即可

（以下是最基础的自定义控制器示例，在保留ECM默认功能的同时，仅需添加角色动画相关的代码）

```C#
public sealed class MyCharacterController : BaseCharacterController 
{ 
    protected override void Animate() 
    { 
        // Add animator related code here... 
    } 
} 
```

要使用新创建的自定义控制器（MyCharacterController），您只需执行以下操作：将角色GameObject上的BaseCharacterController组件替换为MyCharacterController即可——由于继承关系，新控制器将完整保留BaseCharacterController的所有功能。

# Custom Input

ECM将所有输入相关逻辑都封装在BaseCharacterController的HandleInput方法中。在您的自定义控制器（继承自某个基础控制器）中，可以通过重写该方法来实现自定义输入方案，例如：

移动端输入支持
Unity新版Input System等

具体实现方式如下：继承BaseCharacterController基类，并重写其HandleInput方法即可。

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
 
        // Replace the above code with your custom input code 
    } 
}
```

# Movement Relative To Main Camera

在游戏中，常见的解决方案是让角色相对于主摄像机（即跟踪角色视角的摄像机）的方向移动。然而，ECM默认是在世界坐标系中处理输入——其moveDirection向量仅由水平输入轴X和垂直输入轴Z直接填充。

随后（在BaseCharacterController的CalcDesiredVelocity方法中），ECM会使用这个moveDirection向量（当前由输入直接填充）来计算角色的期望速度。因此，要实现角色相对于摄像机视角的移动，可采用以下方案：

在您的HandleInput方法中，只需使用内置的扩展辅助方法，将moveDirection输入指令转换到主摄像机相对坐标系即可：

moveDirection = moveDirection.relativeTo(mainCamera.transform);

# Custom Rotaion

ECM默认会将角色朝向给定的移动方向向量（moveDirection）旋转。不过由于ECM的大部分默认功能都可以通过重写对应方法轻松修改，本例中我们需要重写UpdateRotation方法。

在UpdateRotation方法中，通过rotationAmount参数直接修改CharacterMovement组件的偏航旋转（yaw rotation）。若要实现坦克式移动（固定朝向移动），还需修改期望速度（desiredVelocity），因为默认计算仅为：moveDirection * speed。

调用CalcDesiredVelocity方法使角色沿当前正前方向移动。

当需要同时/单独修改以下参数时推荐采用此方案： 角色旋转逻辑 和 期望速度计算方式

# Crouching

当角色进入蹲伏状态时，ECM会自动处理胶囊碰撞体(Capsule Collider)的缩放，并在站立时恢复原始高度。但角色模型的视觉表现需开发者自行实现（例如通过动画系统处理，参考Ethan角色范例）。

此规则不适用于FirstPersonCharacterController，默认在BaseFirstPersonController的AnimateView方法中，它会缩放相机rig的枢轴变换(Pivot Transform)实现基础蹲伏动画。因此要替换它，必须重写AnimateView方法，并实现自定义的相机蹲伏动画。

# Fall Damage

到此，你应该已经很熟悉为了修改扩展默认 ECM 功能应该使用哪些方法了。

这里会展示如何轻易地添加 fall-damage 机制。这里我们保持跟踪 character 的最后 grounded position，当 character 刚落地时（例如 !movement.wasGrounded && movement.isGrounded），我们简单计算坠落高度（最后一次 grounded position 和 character 大当前 position）。

然后就可以使用这个坠落高度确定角色是否应该收到伤害，根据你自己的游戏规则。

这里需要考虑的很重要的一点是对 BaseCharacterController Move 方法的修改。这个方法处理所有角色的移动、跳跃等等。就像之前的方法一样，它可以被扩展，在其上面添加你自己的游戏机制，或者完全替换它的实现。

# Toggle Gravity Direction

新版本一个新的功能是可以修改重力方向，这可以实现独特的游戏机制，并且实际上非常简单。

示例中简单地 toggle gravity 方向为 up 和 down，这会让 rotation 旋转来匹配新的 gravity direction。当 ECM character 旋转后，它所有的移动都将相对其 up vector，这允许 character 在 wall，ceiling 上行走。

要完成 rotation，我们再次 override UpdateRotation 方法，以便将 character 旋转到新的 gravity 方向。

# Orient To Ground

这个示例和上一个相关，但是这里我们简单 orient character 匹配 ground normal，这样 character models 可以 follow terrain orientation。

再次强调，一旦 character 被旋转，它所有的移动都会相对当前的 up vector，例如如果 character 在一个 30° 的 plane 上，一旦旋转并匹配这个 plane 的 normal，在内部，character 会将 plane 视为水平 plane，因为它的新的 up direction 是 plane normal。

# Platforms

默认 ECM character 会自动和 platform 交互，但是 platform 必须是一个 kinematic rigidbody。

Platforms（一个 kinematic rigidbody）可以按你喜欢的方式动画，无论通过脚本还是通过 Animator。如果是 Animator，需要将 Animator update mode 设置为 Animate Physics，以便让 ECM Character 正确地和 Platform 交互。

这个规则同样适用 tweened motion，这个库包含选项设置 Animate Physics，应该使用它来正确地和 ECM Character 交互。

# Wall Grab and Wall Jump

这个例子中，我们依赖 OnCollisionXXX 事件，检测 character 何时跟 grabbable wall（可攀爬墙体）碰撞。当检测到 grabbable wall，character 可以抓住它 grab，并进入 grabbed state。

当 character 处于 grabbed state，我们会限制 character 的 max fall speed，以模拟一个 grabbed drag，并允许角色执行要给 wall jump。Wall jump 是一个 jump 实现。

除了 wall grab，wall jump 机制，这个示例还展示了 one-way platform 的实现方式。

one-way platform 使用实际 platform collider 下面的一个 trigger area，当 character 进入 platform 下面的这个 trigger，one-way platform 脚本将关闭 platform 的 collisons，允许 character 从下面跳上 platform。当 character 离开 trigger area，脚本会再次开启 platform 的 collider，以允许角色站在它上面。

# Flying

这个示例展示了 ECM 的一个重要方面，默认一个 ECM character 会将它所有的移动视为平面移动。这意味着它会丢弃给定 velocity vector 的 Y 分量（相对于 up direction）。为了允许垂直方向的移动（例如攀爬，飞行，游泳等），需要显式告诉 ECM 你想要垂直移动，通过使用 BaseCharacterController allowVerticalMovement。

当把 allowVerticalMovement 设置为 true，在内部，它会关闭 character 的 gravity，允许 character 在空中或水中自由运动。

# Swimming

这个示例跟前面的非常类似，实际上实现也差不多一样，主要不同就是进入和离开 swimming state 的方式不同。

为了检测是否进入 swimming state，这个示例检测整个 capsule volume 是否在 water zone 内部。我们会检测 capsule 的 top 是否在 water zone 是否在 water zone 中，如果是，character 进入 swimming state，否则 character 离开 swimming state。

这个示例使用了阿一个新的功能，OverlapCapsule 方法，它可以很容易进行快速 overlaps 检测，而不需要 OnTrigger events，因此可以很容易地集成到你的 code 中。

此外，这个示例还使用了新的 DisableGroundDetection 和 EnableGroundDection，以便 character 接触到 water zone 的 ground 时，不会被强制约束到 ground 上。值得注意的是，这个功能应该成对使用，因为不像 DisableGrounding，它临时关闭 grounding phase，而 DisableGroundDection 会永久 disable 检测，直到你显式调用 EnableGroundDection。

# Over The Shoulder Camera Movement

在本示例中，我们实现了一种类似于《生化危机4》的移动方式：摄像机位于角色后方，紧密跟随其所有移动。角色的旋转通过鼠标横向移动控制偏航轴（即垂直轴），而摄像机通过鼠标垂直移动控制俯仰旋转（上下移动）。

此示例包含一个基础的肩后摄像机控制器，但需注意，这仅作为演示用途，不建议直接用于实际生产环境。

为实现肩后摄像机移动效果，首先需将输入的移动方向向量（moveDirection）转换为相对于角色视角的方向（通过 Handlesput 方法处理）。这使得角色在沿当前视角方向前后移动时，可同时执行侧向平移动作。

我们替换了默认的ECM旋转实现（UpdateRotation 方法），改为通过鼠标横向移动控制角色绕偏航轴旋转。

最后，在摄像机控制器中，我们处理摄像机的俯仰旋转（上下移动）。

# Mesh Analysis

虽然这不是ECM（高级角色移动）的示例，但它是一个辅助工具，可用于可视化可行走的地面区域。

ECM会根据角色站立或移动目标的地面角度（相对于其向上轴）限制移动范围，同时显示一个地面检测辅助线框，明确标识可移动与不可移动区域。

在不规则网格中，可能难以发现潜在问题，因为某些网格包含微小三角形或“不可行走”区域，导致ECM运行异常。此时，内置的网格分析工具即可发挥作用。

该工具接收网格碰撞体，并以红色高亮显示超过设定角度阈值的不可行走区域。通过脚本右键菜单，还可使用顶点着色（需支持此功能的Shader）完整涂色网格。注意：仅对实际网格（非网格碰撞体）生效，且必须与碰撞体使用同一网格，否则会显示错误结果。

使用方法：将脚本添加至含MeshCollider/网格的游戏对象，设定最大可行走地面角度阈值，并勾选DrawGizmos选项以显示网格碰撞体的法线。

如需涂色网格，通过脚本右键菜单选择PaintMesh，即可用顶点颜色渐变标识从可行走到不可行走的地面区域。
