Input System 有很多 workflows，不同的 workflow 有不同的优势。

## 创建并赋值项目范围内 actions

Input System 存储你的 input configuration 在一个 Actions Asset。首次安装 input system package，必须创建这个 Actions Asset。

为此，通过 Edit>Progject Settings>Input System Package>Input Actions 菜单，单机 Create and assign a default project-wide Action Assets 按钮。

## 查看和编辑默认 input settings

一旦 create 和 assign 了一些 project-wide actions，Input Actions Setting window 允许你查看并编辑 input configuration。

## 默认 Action Maps 和 Actions

Action Maps 允许你将 Actions 组织为 groups，它代表一个特定场景，其中一组 actions 放在一起是有意义的。例如 fps 游戏，所有跟枪支相关操作的输入可以放在一个 group，当玩家可以操作坦克时，所有操作坦克相关的输入可以放在一个 group。此外，跟 UI 相关的输入操作可以放在一个 group。这样根据玩家操作枪支、坦克、还是 UI，直接切换 Action Map 就可以了。

Input System 默认的 configuration 带有两个 Action Maps：Player 和 UI。每个包含默认 actions，它们分别用于 gameplay 和 UI 交互。

Play action map 定义了一些游戏相关的 actions，例如 Move，Look，Jump，Attack actions。UI action map 定义了一些 UI 相关的 actions，例如 Navigate，Submit，Cancel。

每个 default action 绑定到一些不同类型的 Control，即一个 action 可以同时绑定到多种设备上，这样可以用不同的设备进行输入，而应用程序则无需了解具体的输入，这样就直接实现了不同类型设备对抽象 action 的映射。例如：

- Move action 绑定到 WSAD 键盘按键和方向键，游戏手柄 gamepad stick，XR 控制器的主 2D 轴
- Jump action 绑定到 Space 键，gamepad 的 south 按钮，XR 控制器的第二按钮

## Read values from default actions

Input System 带有预配置的 default actions，Move、Jump 等等，它们适合很多常见的 app 和 game。它们被配置从最主流的 input controller 读取输入，例如 Keyboard，Mouse，Gamepad，Touchscreen 和 XR。

这意味着，很多情况下，你可以直接使用 Input System 而无需任何配置。

这个 workflow 使用下面的步骤：

- 在脚本顶部添加 using InputSystem 语句
- 创建变量保存 Action 引用
- 在 Start 方法中，查询和存储 Action 引用
- 在 Update 方法中，从 Action references 中读取 values，添加自己的代码响应相应的输入值

```C#
using UnityEngine;
using UnityEngine.InputSystem;  // 1. The Input System "using" statement

public class Example : MonoBehaviour
{
    // 2. These variables are to hold the Action references
    InputAction moveAction;
    InputAction jumpAction;

    private void Start()
    {
        // 3. Find the references to the "Move" and "Jump" actions
        moveAction = InputSystem.actions.FindAction("Move");
        jumpAction = InputSystem.actions.FindAction("Jump");
    }

    void Update()
    {
        // 4. Read the "Move" action value, which is a 2D vector
        // and the "Jump" action state, which is a boolean value

        Vector2 moveValue = moveAction.ReadValue<Vector2>();
        // your movement code here

        if (jumpAction.IsPressed())
        {
            // your jump code here
        }
    }
}
```

不同的 Action 类型有不同的 value 类型（值类型），因此具有不同的方法访问它们的值。例如上面的例子中，对于 Vector2 类型的 action，使用 ReadValue\<Vector2\>() 读取一个 2D 轴的输入，对按键类型的 action，使用 IsPressed() 读取一个 bool 值，表示按键是否按下。

如果在不同的 Action Map 中使用相同的名字创建多个 Action，在使用 FindAction 查找 action 时，必须指定 Action Map 和 Action Name，通过正斜线 / 分割。例如 InputSystem.actions.FindAction("Player/Move")。

