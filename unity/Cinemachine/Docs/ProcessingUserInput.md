Cinemachine 相机并不直接处理用户输入。相反，它们会暴露出一些轴（axes），这些轴可以由脚本、动画或用户输入来驱动。Cinemachine尽可能保持对输入来源的中立性，这样它就能兼容Unity的Input System、Unity的旧版输入管理器或其他第三方输入系统。

Cinemachine 自带 CinemachineInputAxisController 组件。当将其添加到 CinemachineCamera 上时，它会自动检测所有可由用户输入驱动的轴（axes），并暴露相关设置，让你能够控制这些轴的数值。

它同时兼容 Unity 的 Input 包和 Unity 的旧版输入管理器。您也可以将其作为模板，用于编写自定义的输入处理器。

输入轴控制器不仅将输入映射到已公开的轴上，还为每个轴提供设置以通过加速/减速和增益来调整响应性。

如果你愿意，你也可以将 CinemachineInputAxisController 与自己的脚本一起使用来驱动输入轴，例如在实现玩家运动的脚本中。

该组件可以轻松地让你在单人游戏环境中使用鼠标和键盘或手柄来控制CinemachineCamera。

# 属性

- Player Index

  要查询哪个玩家的输入控制。对于单人游戏，请将此值保留为默认值 -1。否则，这应该是 UnityEngine.Input.InputUser.all 列表中该玩家的索引。仅当安装了 Unity 的 Input 包时，才会显示此设置。

- Auto Enable Inputs

  如果安装了 Unity 的 Input 包，则此选项可用。它将在启动时自动启用任何已映射的输入操作。

- Scan Recursively

  如果设置，将执行对 IInputAxisOwners 行为的递归搜索。否则，只会考虑直接附加到此 GameObject 上的行为，而子对象将被忽略。

- Suppress Input While Blending

  如果设置，并且此组件附加到了一个 CinemachineCamera 上，则在相机参与混合（blend）期间，将不会处理输入。防止输入操作影响 blend 的结果。

- Enabled

  当此值为 true 时，控制器将驱动输入轴。如果为 false，则该轴将不会被控制器驱动。

- Legacy Input

  如果使用的是旧版输入管理器，则在此处指定要查询的输入轴名称。
  
- Legacy Gain

  如果使用的是旧版输入管理器，则读取的输入值将乘以该数值。

- Input Action

  如果使用 Input 包，驱动 axis 的 Input Action 的引用。 

- Gain

  如果使用 Input 包，读取的 input value 乘以这个数值。

- Input Value

  这帧读取的 input value。

- Accel Time

  Input value 加速到更大值花费的时间。

- Decel Time

  Input value 减速到更小值花费的时间。

- Cancel Delta Time

  这将取消输入轴内置的 deltaTime 补偿。如果输入值本身依赖于帧时间，则启用此选项。例如，鼠标增量在较长的帧中自然会更大，因此在这种情况下应取消默认的 deltaTime 缩放。

# 创建你自己的 Input Axis Controller

CinemachineInputAxisController 的默认实现可以处理来自 Input 包和 Unity 旧版输入系统的输入源。

对于更复杂的场景（例如移动设备控制），你可以扩展此默认功能，并通过脚本创建自己的输入轴控制器。

以下示例展示了如何使用自定义输入控制器脚本通过滑块来控制移动设备的摄像机。该示例代码可作为模板使用，并可轻松修改以适用于其他对象。

```C#
using UnityEngine;
using Unity.Cinemachine;
using System;
using UnityEngine.UI;
using Object = UnityEngine.Object;

//The component that you will add to your CinemachineCamera.
public class SliderInputController : InputAxisControllerBase<SliderInputController.SliderReader>
{
    void Update()
    {
        if (Application.isPlaying)
            UpdateControllers();
    }

    [Serializable]
    public class SliderReader : IInputAxisReader
    {
        
        public Slider m_Slider;

        public float GetValue(Object context, IInputAxisOwner.AxisDescriptor.Hints hint)
        {
            if (m_Slider is not null)
                return m_Slider.value;

            return 0;
        }
    }
}
```
