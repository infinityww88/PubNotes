# 2D sorting

Unity 根据优先级顺序对渲染器进行排序，而优先级取决于渲染器的类型和用途。

可以通过渲染队列指定渲染器的渲染顺序。

通常由两个主要的渲染队列：不透明队列 和 透明队列。

2D 渲染器主要位于透明队列，包括精灵渲染器（sprite renderer），瓦片地图渲染器（tilemap renderer）和精灵形状渲染器（sprite shape renderer）。

## 透明队列按优先级排序

透明队列中的 2D 渲染器通常遵循以下优先级：

1. sorting layer 和 order in layer
2. 指定的渲染队列 renderer queue
3. 与摄像机的距离
4. sorting group
5. material/shader
6. 当多个渲染器具有完全相同的上面的排序优先级时，有 Tiebreaker（仲裁程序）决定优先级

## Sorting layer 和 Order in layer

可以通过 Inspector 窗口或 Unity Scripting API 为所有 2D 渲染器设置 Sorting Layer 和 Order in Layer。

## 指定渲染队列

可以在渲染器材质或其着色器中指定渲染器的渲染队列。这对于使用不同材质的渲染器的分组和排序很有用。

## 与摄像机的距离

Camera 组件更具其 Projection 设置对渲染器进行排序。两个选项分别是 Perspective 和 Orthographic。

### 透视 Perspective

在此模式下，渲染器的排序距离是渲染器与摄像机的直接距离。

### 正交 Orthographic

渲染器的排序距离是渲染器位置与摄像机沿着摄像机视图方向的距离。默认 2D 设置中，此方向是 (0, 0, 1)。

将 Camera 组件设置为 Perspective 或 Orthographic 时，Unity 会自动设置摄像机的 TransparencySortMode 以匹配所选的模式。

。可以通过两种方式设置透明排序模式（Transparency Sort Mode）：

- 在 Project Settings/Graphics/Camera Settings 下设置 Transparent Sort Mode
- 通过 API 设置相机的 TransparencySortMode

TransparencySortMode：

- Default：根据相机是 Perspective 还是 Orthographic 自动设置 mode 是 Perspective 还是 Orthographic
- Perspective：强制 Perspective mode
- Orthographic：强制 Orthographic mode
- CustomAxis

  根据沿着一个自定义 axis 的距离排序 objects。例如你可以指定 axis 为 (0, 1, 0)。这会有效地使渲染器沿着 Y 轴向上排序（Y 越小越先渲染）。这对 2.5D 游戏很常见。注意这个优先级比 Sorting Layer，Order in layer，Render Queue 低。

当此设置为 Default 时，Camera 组件的 Projection 设置具有更高优先级，否则，Camera 的 Projection 设置保持不变，但是它的 Transparency Sort Mode 将更改为指定的选项。

### 自定义轴排序

这个模式通常用于等距瓦片地图（Isometric Tilemaps）的项目中，以便在瓦片地图（TileMap）上正确排序和渲染瓦片精灵（Tile Sprites）。

### 精灵排序点 Sort Point

默认 Sort Point 设置为 Center，也可以设置为 Pivot。精灵的距离使用这个点来测量。

## 排序组 Sorting Group

Sorting Group 是一个组件，它将具有共同根的渲染器分组到一起进行排序。同一 Sorting Group 中的所有渲染器具有相同的 Sorting Layer，Order in Layer 和 Distance to Camera。

## 材质、着色器

Unity 将具有相同材质设置的渲染器排序到一起，以获得更高效的渲染性能，例如动态批处理。

## TieBreaker

当上面所有优先级都相同时，将由仲裁程序决定 Unity 将渲染器放在渲染队列中的顺序。这是无法控制的内部过程，所以应该使用其他排序选项确保渲染器具有不同的排序优先级。

