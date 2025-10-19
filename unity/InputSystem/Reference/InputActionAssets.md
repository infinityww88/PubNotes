# Input Action Assets

一个 Asset，包含 Input Actions 和它们关联的 Bindings 和 Control Schemes（Gamepad，Keyboard&Mouse，Touch，VR）。存储为 Json 的 .inputactions 文件。

## Creating Action Assets

## Editing Action Assets

### Editing Composite Bindings

有多个部分组成的 Bindings，共同组成一个 Control。例如，一个 2D Vector Composite 使用4个 buttons（left，right，up，down）来模拟一个 2D stick input。

## Using Action Assets

### Auto-generating script code for Actions

使用 .inputactions Asset 最方便的方式是为它们自动生成一个 C# 包装器类。这移除了需要手工使用名字查找 Actions 和 Action Maps，并提供设置 callbacks 的更简单的方式。

在 Asset Inspector 的 importer 属性中点击 Generate C# Class checkbox。

你可以选择一个 path name，class name，一个 namespace，或者保持默认值。

```C#
using UnityEngine;
using UnityEngine.InputSystem;

// IGameplayActions is an interface generated from the "gameplay" action map
// we added (note that if you called the action map differently, the name of
// the interface will be different). This was triggered by the "Generate Interfaces"
// checkbox.
public class MyPlayerScript : MonoBehaviour, IGameplayActions
{
    // MyPlayerControls is the C# class that Unity generated.
    // It encapsulates the data from the .inputactions asset we created
    // and automatically looks up all the maps and actions for us.
    MyPlayerControls controls;

    public void OnEnable()
    {
        if (controls == null)
        {
            controls = new MyPlayerControls();
            // Tell the "gameplay" action map that we want to get told about
            // when actions get triggered.
            controls.gameplay.SetCallbacks(this);
        }
        controls.gameplay.Enable();
    }

    public void OnDisable()
    {
        controls.gameplay.Disable();
    }

    public void OnUse(InputAction.CallbackContext context)
    {
        // 'Use' code here.
    }

    public void OnMove(InputAction.CallbackContext context)
    {
        // 'Move' code here.
    }

}
```

### Using Action Assets with PlayerInput

PlayerInput 组件提供一个方便的方法处理一个或多个 players 的输入。它需要你在一个 Input Action Asset 中设置所有的 Actions，然后你可以将 Asset 赋予 PlayerInput 组件。

PlayerInput 然后自动处理 activating Action Maps 并为你选择 Control Schemes。

![PlayerInput](../../../Image/PlayerInput.png)
