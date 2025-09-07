Ray Sensor 检测与一个射线相交的 objects。它使用 Physics 或 Physics2D 内部的 raycast 函数家族。

Sensor 检测沿着它的 path 上的所有 objects，直到 hit 到一个 Obstruction collider。它不会检测超过 obstruction 的 objects。

如果路径上有很多相交的 GameObjects，它们每个都会被检测到（每个对应一个 Signal）。但是如果遇到 Obstruction Layers 中的 GameObject，则检测结束，不会继续向前检测。但是 Obstruction 只起到阻断的作用，它本身不会加入到 Signal List 中。如果没有遇到 Obstruction GameObject，就返回所有能检测到的 GameObjects。

检测 Ray 不仅仅可以是 Line，还可以是 Sphere 等具有体积的 Shape（这通过 SphereCast 之类的物理检测函数）。

# Output Signals

- Object：Collider.gameObject 或 Collider.attachedRigidbody.gameObject，依赖于 Detection Mode
- Strength：设置为 1
- Shape：以相交点为中心的 size=0 的 Bounds（Unity Bounds 结构体）

有两个检测相关的 Layer：

- Detects On Layers：Sensor 检测的 GameObject 必须是这些 Layers 中的 GameObject，其他 Layer 中的 GameObject 不被检测
- Obstructed By Layers：这些 Layers 中的 GameObject 会阻碍终止 Sensor 检测，如果与 Cast 路径相交。它们本身不会加入到 Signal List 中

但是一个 GameObject 可以同时是被检查的物体和 Obstruction。

你可以访问 ray 与每个 object 相交的细节，使用 GetDetectionRayHit() 或 GetObstructionRayHit() 方法。

# Configuration

## Shape

可以选择不同的 casting 形状。3D Sensor 包括 Ray, Sphere, Box, Capsule。2D sensor 对这些形状有 2D 对应体。你选择的形状决定了调用哪个物理方法。例如 Ray 会使用 Physics.RayCast，而 Sphere 会使用 Physics.SphereCast。

## Layers

Detects On Layers 和 Obstructed By Layers 都是 Layer Masks，可以选择一个或多个 physics layers。如果一个 Collider 在其中任意 Layer 中，Ray 会与它相交，但是两个 Mask 的用途不同：

- Detects On Layers：检测这些 layers 中的所有 objects
- Obstructed By Layers：这些 layers 中的任何一个 Collider 如何与 Ray 相交，就会阻断 Sensor 继续检测，并返回，而这个 Collider 不会加入到 Signals List 中，除非它也在 Detects On Layers 中

## Filters

这个属性让你过滤哪些 objects 被 sensor 检测：

- Ignore List

  这个列表中的任何 GameObject 都不会被 sensor 检测，也不会 obstruct sensor。对于它如何 filter obstructions 有一些细微差别。要决定一个 obstructing Collider 是否被忽略，会使用下面的逻辑：

  - 如果 Collider.gameObject 出现在 ignore list 中，则忽略它
  - 如果 Collider.attachedRigidbody.gameObject 出现在 ignore list 中，则忽略它

  如果一个 Signal 的 Object 出现在 ignore list 中，则忽略这个 Signal。

- Tag Filter

  Enable Tag Filter 选项可以激活 tag filtering。Filter 中可以填充一个允许的 tags 列表。一个 object 要被检测到，它的 tag 必须在这个列表中。Obstructions 不会被这个 tag filter 影响。

- Minimum Slope Angle

  Filters detections 和 obstructions 依赖相交点的 slope angle。这个 slope angle 定义为 RaycastHit 的 Normal 和配置的 Up 向量之间的角度。

# Optimisation Considerations

根据配置，sensor 会使用 Physics.RayCast 或者 Physics.RayCastNonAlloc。

- Physics.RayCast：仅计算 ray 路径上的第一个 interaction。这有更佳的性能
- Physics.RayCastNonAlloc：计算 ray 路径上的所有 interaction。不具备更好的性能

Sensor 足够智能，在特定的配置中使用性能更好的 Physics.RayCast：

- Detects On Layers mask 是 Obstructed By Layers 的一个子集。sensor 检测到的任何东西都会阻断它
- Tag Filter 被关闭，Ignore List 是空的，Minimum Slope Angle 设置为 0
