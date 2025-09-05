# 创建要给角色 Character

1. 右键点击 Hierarchy 窗口，选择 ECM2 > Character 选项
2. 这会创建一个空的 character（没有视觉表现，Mesh Filter），名为 Character

   最好将它设置到原点，这会在你 parent model 时免去很多麻烦

3. 将你的 Model 挂载到新创建的 Character GameObject 下面，作为视觉表现

4. 在 CharacterMovement 组件，调整它的 radius 和 height（这会相应地自动配置 character capsule collider）来更好地匹配 character model

# 控制一个角色

创建 Character 之后，还不能移动和控制它。为此创建一个新的脚本 CharacterInput 脚本。

Character 包含一组方法，设计用于使执行 action 更容易。例如，它的 SetMovementDirection 方法可以用于指示 character 向一个特定方向移动（世界空间）。

类似的，Jump 方法发起一个 Jump，而 StopJumping 方法停止正在进行的 Jump，当使用可变 jump 高度时尤其关键。

还有 Crouch 方法用于发起一个下蹲 crouch 动作，UnCrouch 方法用于取消 crouching 状态。

完整的脚本如下：

```C#
using UnityEngine;
using ECM2;

namespace ECM2.Examples
{
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
}
```

最后添加新创建的 CharacterInput 脚本到 Character GameObject。这样就可以移动、跳跃、下蹲了。
