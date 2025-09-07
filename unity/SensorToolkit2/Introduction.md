# 介绍

SensorToolkit 是一个 sensor 组件的集合，它检测周围的 objects，感知 sense 其周围的世界。

它是基本感知 sensing 功能（例如 Physics.Raycast，Physics.OverlapSphrere，TriggerCollider）基础上的强大而便捷的抽象。

**即使在自己平时的开发中也要遵循这种模块化和抽象化的原则，将你需要的功能以抽象的原则实现为一组 building blocks，然后用这些 blocks 打击游戏世界**

Object 检测代码可能变得很复杂，SensorToolkit 极其精巧地管理这个复杂性，使你可以关注到游戏有趣的部分。

Sensor 组件是模块化和独立运行的。简单添加 Sensor 到 GameObject 上，配置它，就可以了。

Widgets 和 Custom Inspectors 可以帮助你快速地调试和定位配置问题。

# Quickstart 

你可以不花任何时间就能将 SensorToolkit 集成到游戏中。假设，你有一个 Enemy GameObject，你想要 Enemy 检测 Player 何时在其附近，并攻击它。你可以这样做：

1. 添加一个 Range Sensor 组件到 Enemy。如果是 2D game，则添加 Range Sensor 2D 组件。
2. 配置 Range Sensor。设置它的 size 和 shape，确保 Detects On Layers 包含 player 所在 physics layer。你可能还想要设置 Detection Mode 为 Rigid Bodies。
3. 添加 Test Button。这会在 Editor Mode Pulse（脉冲）sensor，显示它检测到的所有东西，例如 sensor 是否检测到了 player？
  
   如果 sensor 可以检测到 Player，你就可以安全地继续工作。否则，则查看、修改配置，再次测试。例如，检查 Player 是否有一个 Collider 和 Rigidbody 组件，是否设置了正确的 physics layer。

## 与脚本集成

编写一个 C# 脚本 EmptyBehaviour，实现其 AI 逻辑（如果 player 在 sense range 内，则攻击它），挂载到 Enemy 上。

```C#
using UnityEngine;
using Micosmo.SensorToolkit;

public class EnemyBehaviour : MonoBehaviour {
    Sensor sensor;

    void Awake() {
        sensor = GetComponent<Sensor>(); // RangeSensor extends the base class: Sensor
    }

    void Update() {
        var player = sensor.GetNearestDetection("Player"); // Assuming the player has the 'Player' tag assigned
        if (player != null) {
            // Attack behaviour here...
        }
    }
}
```

使用任何 Sensors 遵循一样的原则：添加你需要的 sensor 组件，配置它，测试它，与游戏逻辑集成。

绝大多数时间，你会使用 Ray Sensor，Range Sensor，Trigger Sensor，或者 Line of Sight Sensor。
