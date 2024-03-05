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









