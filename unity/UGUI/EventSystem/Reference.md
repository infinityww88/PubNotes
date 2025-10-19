# Reference

## Event System Manager

协调当前 active 的 Input Module，被认为是 选中 的 GameObject，以及一个其他 high level Event System 概念的 host。

每个 Update 中，Event System 检查它的 Input Modules，并指出哪个 Input Module 应该给用在这个 tick 中。然后它将处理传递给这个 module。

因为实在 Update 中执行逻辑，因此帧率会影响 Input 处理。

## Graphic Raycaster

投射 Canvas。查看 Canvas上所有 Graphics 并决定它们中是否有一个被 hit。

可以被配置忽略 backfacing Graphics，还有被前面的 2D 3D objects 阻挡。看起来应该是基于 Physics Raycast 实现的更高级的 Raycaster。

## Physics Raycaster

投射场景中的 3D 物体。这允许消息被发送给实现事件接口的 3D 物理物体。Input Module 检测硬件的信息，并使用Raycaster 投射检测射线碰撞到的物体，至于物体是什么并不关心，UI 元素或者物理物体都是 GameObject，然后向这个物体发送事件。

- Depth：射线投射离开相机的距离
- Event Camera：用于投射射线的相机

## Physics 2D Raycaster

投射场景中的 2D 物体。Physcis Raycaster 附加到 Camera 上，Graph Raycaster 附加到 Canvas 上。

Priority

## Standalone Input Module

## Event Trigger

Event Trigger 组件实现了所有的事件接口，就是可以接受所有的事件消息（当然是在发生在 GameObject 上的），并且调用每个事件注册的函数。

附加 Event Trigger 组件到 GameObject 上将会拦截所有 events，不会再从这个 object 上发生事件冒泡了。

