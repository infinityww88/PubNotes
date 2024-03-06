# Misc

Graphic Raycast Target 只能遮挡非 parent 的 Graphic 的交互。一个交互组件的（例如 Button）的 child Image/Text 设置为 Raycast Target 也不会阻挡这个 button 的交互。但是一个设置为 Raycast Target 的 Image/Text 会阻挡非 parent 的交互组件。

交互组件不仅包括内置的 Button 等，还包括带有 Event Trigger 组件的 Graphic。

交互组件会阻挡 Raycast，即使 parent 元素也是交互组件。

# uGUI Events

uGUI 事件系统包括 4 部分：

- EventSystem：处理实际物理设备输入，场景中要包含一个 EventSystem
- InputModule：只需要 Standalone Input Module，不再需要 TouchInputModule，它已经在 Standalone Input Module 中处理了
- Raycaster：包括 GraphicRaycaster，Physics2DRaycaster，PhysicsRaycaster
- EventTrigger

EventTrigger 用于在最终的 GameObject 上接受各种 Pointer 事件。

3 种 Raycaster 分别用于投射 GUI 元素，2D 物理 collider，3D 物理 collider。GraphicRaycaster 需要挂载到 Canvas 上，两个 PhysicsRaycaster 需要挂载到用于投射的 Camera 上。

每次创建 Canvas 时，自动挂载 GraphicRaycaster 组件。用于 uGUI 元素的交互。

- Blocking Objects: None/2D/3D/All，定义哪些 GameObject 可以遮挡 GraphicRaycaster 的投射
- Blocking Mask: Layers，定义哪些 layers 可以遮挡 GraphicRaycaster 的投射

Physic Raycaster(2D) 要挂载到 Camera 上

- Event Mask：Raycaster 的 layers 参数
- Max RayIntersection：Raycast 的 maxRayDistance 参数

任何 uGUI，2D Collider，3D Collider 要接受 pointer 事件，需要挂载实现事件接口的脚步，或者简单地挂载 EventTrigger 组件。每种类型都需要创建相应的 Raycaster，并设置好 layers。

The Raycaster raycasts against 3D objects in the scene. This allows messages to be sent to 3D physics objects that implement event interfaces.

创建一个 Canvas 组件，自动创建必需的 CavasScaler 和 GraphicRaycaster 组件。CanvasScaler 确定 Canvas 的模式和分辨率，Canvas 必处于一种 Canvas Scaler 模式中（Screen Overlay、Screen Camera，World）。GraphicRaycaster 用来处理 UI Pointer 事件。如果场景中没有 EventSystem，还会自动创建一个。

## PixelsPerUnit

对于 Sprite(2D or UI) Texture，需要设定 PixelsPerUnit，其他类型的 texture 没有这个属性。

When importing graphics as Sprites, Unity displays a parameter called Pixels per Unit (PPU). Now that we know all about units, this should be very clear. It's expressing how many pixels from your Sprite fit into a unit in the Unity scene when the GameObject is scaled 1,1,1

PixelsPerUnit 用于确定一个 texture 的多少个像素应该对应一个世界单位（或 uGUI 单位）。它关系图片作为 sprite 或 UI image 显示时的分辨率问题。当越少的像素对应一个世界单位（或 UI 单位），图片显示得就越清晰，反之越越模糊。

这个属性在很多地方都出现，从 Texture 的 import 属性，到 CanvasScaler，到 Image 组件的属性，最终的 PixelsPerUnit 取决于所有这些属性的比例。

这个属性对 Sliced Sprite 尤其重要，因为作为 border 的 sprite 部分是固定的，它因此映射的 世界单位（UI 单位）也是固定的，PixelsPerUnit 确定着 border 在 world/UI 上显示的大小。

例如下面是一个 sliced sprite texture：

![SpriteSliceBorder](SpriteSliceBorder.png)

当 PixelsPerUnit 设置为 50 时，border 非常宽：

![PixelsPerUnit_50](PixelsPerUnit_50.png)

当 PixelsPerUnit 设置为 150 时，border 比较细：

![PixelsPerUnit_150](PixelsPerUnit_150.png)






