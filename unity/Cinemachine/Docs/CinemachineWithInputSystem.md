对于更复杂的输入配置（例如支持多个设备），你需要从 Input System 包提供的 PlayerInput 组件接收输入。以下部分假设你已经知道如何设置该组件。更多信息请参阅 Input System 文档和示例。

# 从 PlayerInput 读取

要从 behaviour 设置为 InvokeCSharpEvents 的 PlayerInput 读取值，你需要创建一个自定义的 InputAxisController，该控制器订阅 onActionTriggered 事件。下面的示例展示了如何接收并相应地连接这些输入。将此脚本添加到你的 CinemachineCamera 上，并分配 PlayerInput 字段。

```C#
using System;
using UnityEngine;
using UnityEngine.InputSystem;
using Unity.Cinemachine;

// This class receives input from a PlayerInput component and disptaches it
// to the appropriate Cinemachine InputAxis.  The playerInput component should
// be on the same GameObject, or specified in the PlayerInput field.
class CustomInputHandler : InputAxisControllerBase<CustomInputHandler.Reader>
{
    [Header("Input Source Override")]
    public PlayerInput PlayerInput;

    void Awake()
    {
        // When the PlayerInput receives an input, send it to all the controllers
        if (PlayerInput == null)
            TryGetComponent(out PlayerInput);
        if (PlayerInput == null)
            Debug.LogError("Cannot find PlayerInput component");
        else
        {
            PlayerInput.notificationBehavior = PlayerNotifications.InvokeCSharpEvents;
            PlayerInput.onActionTriggered += (value) =>
            {
                for (var i = 0; i < Controllers.Count; i++)
                    Controllers[i].Input.ProcessInput(value.action);
            };
        }
    }

    // We process user input on the Update clock
    void Update()
    {
        if (Application.isPlaying)
            UpdateControllers();
    }

    // Controllers will be instances of this class.
    [Serializable]
    public class Reader : IInputAxisReader
    {
        public InputActionReference Input;
        Vector2 m_Value; // the cached value of the input

        public void ProcessInput(InputAction action)
        {
            // If it's my action then cache the new value
            if (Input != null && Input.action.id == action.id)
            {
                if (action.expectedControlType == "Vector2")
                    m_Value = action.ReadValue<Vector2>();
                else
                    m_Value.x = m_Value.y = action.ReadValue<float>();
            }
        }

        // IInputAxisReader interface: Called by the framework to read the input value
        public float GetValue(UnityEngine.Object context, IInputAxisOwner.AxisDescriptor.Hints hint)
        {
            return (hint == IInputAxisOwner.AxisDescriptor.Hints.Y ? m_Value.y : m_Value.x);
        }
    }
}
```
