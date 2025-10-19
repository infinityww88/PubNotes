# Camera And Screen Nodes

## Grab Screen Position Node

- 输出当前像素的屏幕位置
- 可直接用于Grab Screen Color Node
- Type
  - [0, 0] ~ [ScreenWidth-1, ScreenHeight -1]
  - [0, 0] ~ [1, 1]
- 与ScreenPosition相似，内部额外处理以考虑图形API垂直方向的不同
- GrabScreenPosition + GrabScreenColor总是能正确的得到GrabPass的颜色
- 只有输出（float4）

## Ortho Params Node

- 输出camera的orthographic参数
- 只有输出
- OrthoCamWidth/OrthoCamHeight
- ProjectionMode：0-Perspective，1-Orthographic

## Projection Matrics Node

- 输出camera的投影矩阵或逆矩阵

## Projection Params Node

- 输出camera投影参数
- Flipped：-1-以flipped投影矩阵渲染，1-以正常normal投影矩阵渲染
- NearPlane（float）
- FarPlane，1/FarPlane（float）

## Screen Depth Node

- 输出当前或指定Screen Position的Depth Buffer的值
- [0, 1]或View Space的真实距离
- 如果Camera是orthographic的，ConvertToLinear必须关闭，因为从depth buffer中读取的已是linear scale的值

## Screen Params Node

- 输出屏幕/RenderTarget参数信息
- 通常用于屏幕空间效果
- RT Width
- RT Height
- 1 + 1/Width
- 1 + 1/Height

## Screen Position Node

- 输出当前像素屏幕空间位置
- Type：正常位置或标准化位置

## View Dir Node

- 输出当前camera在Space参数指定的空间的view direction
- Space
  - World
  - Tangent：基于surface tangent plane的坐标空间

## World Space Camera Pos Node

- 输出camera在world的位置

## Z-Buffer Params Node

- 输出基于当前camera投影参数计算的各种值，可以被用于linearize Z-Buffer的值
- 1 - far/near
- far/near
- (1 - far/near)/far
- far/near/far
