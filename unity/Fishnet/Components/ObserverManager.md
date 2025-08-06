# ObserverManager

ObserverManager 辅助控制每个客户端可以看见哪些 network objects。

ObserverManager 用于全局定制 observer system。NetworkObserver 用于定制单个 network object 观察条件。

ObserverManager 中的 Observer conditions 会自动添加到 NetworkObjects 的观察条件集合中，除非 NetworkObserver 组件设置忽略 ObserverManager 中的条件。

## 设置

- Update Host Visibility

  这会隐藏对 host client 来说隐藏的 networked objects 的 renderers。

  - true：所有 networked objects 会对 host client 可见，即使这些 objects 正常对 client despawned。

- Maximum Timed Observers

  当 server 负载增加时，server 用于更新 timed observer conditions（限时 observer conditions）的最大 duration。

  更小的值会导致 timed conditions 更快地被检查，但是要付出更多的性能代价。

- Default Conditions

  默认添加到所有 NetworkObjects 的 Observer Conditions 列表。

  几乎所有游戏都应该至少使用 Scene Observer Condition。

## HashGrid

HashGrid 是当使用 Grid Observer Condition 时的管理脚本。

HashGrid 是当使用 Grid Condition 必需的。这个组件负责管理 grid，并为 grid objects 提供信息。虽然 Grids 没有 Distance Condition 精确，但它确实提供了更好的性能。

HashGrid 必须放在 NetworkManager Object 上或它下面的 object。

### 设置

- Grid Axes

  这些是指定网格所基于的坐标轴。被排除的坐标轴，其数值将不会被纳入计算。例如，如果你正在开发一款2D游戏，通常只需考虑XY轴，那么你就选择XY坐标轴。

- Accuracy

  该参数决定了客户端的FirstObject必须与目标（以Unity单位计量）保持多近的距离才会被视为处于有效范围内。需要注意的是，其判定精度不如使用距离条件（Distance Condition）时精确。