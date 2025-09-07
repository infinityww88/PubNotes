# 核心概念

游戏就是一组规则的集合，设计游戏就是设计一组规则。
游戏就是解决问题的过程，给定一个目标，给出多种工具、路径，让玩家去探索多样化解决问题的过程
或者给定一组相同的工具，每次给定一个不同的目标，让玩家用相同的工具解决不同的问题
本质上都是让玩家探索，无论是探索环境还是探索解决问题的路径
游戏就是玩家调整自己的过程，不断追求更高的能力

所有 sensors 共享一些相同的概念：

- Sensor 是一个组件 Component，它有一个 Signals 列表
- 每个 Signal 存储一个检测到的 GameObject，和一些 objects shape 和 visibility 的数据
- Sensor 可以 Pulse，运行它的检测程序，更新它的 Singles 列表
- 一些 sensors 可以是 Compound 复合的，它们从另一个 sensor 读取 Signals，然后运行更进一步的检测逻辑

有一些边界情形，但是这是一个理解这个 kit 的很好的框架。如果一个 sensor 偏离了这个框架，它会在手册中解释。

## Sensor

几乎所有 sensors 都从一个基类 Sensor 继承。它提供了标准的查询接口，并允许 hook 它的事件。只有 NavMeshSensor 和 SteeringSensor 不是从 Sensor 派生。

## Signal

一个 Signal 是一个 Sensor Pulse（检测，感知）的结果。它是一个小的数据结构，它引用一个 GameObject，保存一点 detection 的信息：

- Object：检测到的 GameObject
- Strength：一个强度值，表示这个 signal 的可见度（例如完全可见 = 1，部分可见，仅一点可见）
- Shape：一个 bounding box，近似 object 的 shape

一个 sensor 对任何 GameObject 最多只有一个 Signal。

Sensor 不是每次只能检测到一个 GameObject，而是能够检测多个，每个 GameObject 对应一个 Signal。

## Pulse

绝大多数 sensors 有一个 Pulse 方法，它运行检测逻辑，产生一个 signals 列表，并与之前的 list 比较，如果有新检测到的 GameObject 或失去之前检测到的 GameObject，发出事件。你可以通过 PulseMode 配置 sensor 何时 pulse。PulseMode 包括：

- Each Frame：sensor 在每个 Update pulse
- FixedInterval：sensor 以固定的时间间隔运行 pulse。这可以优化性能。Intervals 通过一个随机 offset 错开，因此即使 interval 相同的 sensors 也会在多个 frames 中分布
- Manual：sensor 只能通过脚本调用来触发 Pulse()

# Scripting API

所有 class 都在 Micosmo.SensorToolkit 命名空间。一个读取 sensor 的脚本看起来像这样：

```C#
using UnityEngine;
using Micosmo.SensorToolkit;

public class AIBehaviour : MonoBehaviour {
    public Sensor sensor;

    void Update() {
        var pickup = sensor.GetNearestDetection("pickup");
        if (pickup != null) {
            // Collect it...
        }
    }
}
```

当然还可以订阅 OnDetected 和 OnLostDetection 事件，而不是每帧检测。

## Garbage Collector Optimisation

SensorToolkit 设计时特别关注了 GC，使得它从不产生 GC。如果你调用一个返回一个 List 的函数，Kit 实现会每次返回同一个 List 实例（无论是哪个函数）。这使得返回一个检测列表然后迭代它超级方便。

这只对同一个 sensor 而言。不同的 sensor 有各自的全局 List，互不影响。

```C#
List<Signal> enemies = sensor.GetSignals("enemy");  // Get all signals with tag "enemy"
List<Signal> friends = sensor.GetSignals("friend"); // ⚠️ 'enemies' will be overwritten
enemies == friends;  // True
List<Signal> items = sensor.GetSignalsByDistance("item"); // ⚠️ different methods will also overwrite the List
enemies == items; // True

List<Signal> coverLocations = coverSensor.GetSignalsByDistance(); // ✔️ no issue here. Each sensor allocates its own reusable list.
```

要想每次都创建一个新的 List，可以：

```C#
// An optional last parameter let's you provide your own instance of List
List<Signal> enemies = sensor.GetSignals("enemy", new List<Signal>());
List<Signal> friends = sensor.GetSignals("friend", new List<Signal>());
enemies == friends;  // False
```
