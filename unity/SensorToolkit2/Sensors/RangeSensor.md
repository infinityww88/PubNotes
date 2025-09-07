Range Sensor 检测位于它检测 volume 内部的 objects。它使用 Physics 或 Physics2D 的 Overlap 函数家族。被检测到的 object 有一个或多个 collider 与 sensor 的 detection volume 相交。

# Output Signals

- Object：Collider.gameObject 或 Collider.attachedRigidbody.gameObject（Collider 是 Rigidbody 下面的 GameObject 的组件），依赖于 Detection Mode
- Strength：设置为 1
- Shape：包围 Signal 所有 Collider 的 Bounds（包围盒）

每个 Signal 可能被多个 collider 产生，例如 GameObject 有多个 Collider 组件。另外，如果 sensor 在 Rigid Bodies 模式，可能很多 Collider 是 Rigidbody 的 Child GameObject。

Signals shape 是所有 Collider 的 Bounds。

# Configuration

## Shape

可以选择不同的 Volume Shape。3D sensor：Sphere，Box，Capsule。2D sensor 有等价对应体。选择的形状决定了底层使用的 Physics 函数。例如 Sphere 形状会使用 Physics.OverlapSphereNonAlloc，Cube shape 会使用 Physics.OverlapBoxNonAlloc。

## Layers

Detects On Layers 属性定义 sensor 检测哪些 layers 中的 Colliers。注意没有 ray 中的 obstruction layers。

## Filters

Ignore List 中的 GameObject 不会被 sensor 检测。如果开启 Tag Filter，GameObject 必须具有指定的 tags 中的一个才能被检测。
