# Event System

Event System 是一种基于输入（keyboard，mouse，touch，或者 custom input）发送事件到应用程序中的 objects 的方法。

Event System 包含一些一起工作来发送事件的组件。

当添加一个 Event System 组件到一个 GameObject，你会注意到它并没有暴露太多功能。因为 Event System 被设计为一个 Event System modules 之间的管理器和服务者。

Event System 的主要角色是：

- 管理（记录）被认为是选中的 GameObject
- 管理（记录）使用哪个 Input Module
- 管理 Raycasting （如果需要）
- 根据需要更新所有 Input Modules

## Input Modules

一个 Input Modules 是你想要 Event System 怎么做的主逻辑所在地

- 处理输入
- 管理 event state
- 发送事件到 scene objects

同一时间 Event System 中只有一个 Input Module 是 active 的。它们必须是 Event System 同一个 GameObject 上的组件。

如果你想要写一个 自定义 Input Module，需要发送 Unity 中现有 UI 组件支持的事件。而如果要扩展和编写自己的事件，参考 Messaging System。

Unity 默认提供了两个 Input Modules，一个用于 Standalone Input，一个用于 Touch Input。每个 module 按照你的配置接受并分发事件。

Input Module 是 Event System 'business logic' 发生的地方。当 Event System enabled，它查看那个 Input Modules 给挂载，并将 Update handling 到指定 module。

Input Module 被设计用来基于你想要支持的 input systems 进行扩展和修改。它们的目的是映射输入硬件（touch，joystick，mouse，motion controller）为通过 messaging system 发送的事件。

内置的 Input Modules 被设计用来支持常见的 game configurations，例如 touch input，controller input，keyboard input，和 mouse input。它们发送发送各种不同的事件来控制应用程序，如果你在 MonoBehavior 上实现特定接口。所有的 UI 组件实现了对于它自己而已合理的事件接口。

## Raycasters

Raycasters 被用来指出 pointer 在什么之上。Input Modules 使用 Scene 中配置的 Raycasters 计算 pointing device 在什么上面是很常见的。

Unity 默认提供了3个 Raycasters

- Graphic Raycaster：用于 UI elements
- Physics 2D Raycaster：用于 2D 物理元素
- Physics Raycaster：用于 3D 物理元素

如果你在 Scene 中有一个 2d/3d Raycaster，你可以很容易地使 non-UI 元素接收来自 Input Module 的事件（和 UI 元素接收的事件完全一样，即场景中的物体也可以像 UI 元素一样响应输入）。简单附加一个实现一个事件接口的脚本到 GameObject 上就可以了。例如，IPointerEnterHandler 和 IPointerClickHandler 接口。

IPointerEnterHandler 和 IPointerClickHandler 等 Unity 内置事件接口，和在 Messaging System 中自定义的事件接口是一样的。它们都是通过 Messaging System 发送消息调用的，只不过前者是由 Event System 的当前 Input Module 发送的消息，后者是应用程序代码自己发送的消息。发送消息时，需要指定一个 GameObject。在 Input Module 中这个 GameObject 就是通过 Raycaster 检测到的 GameObject，而这个 GameObject 被 Event System 记录为当前选中的 GameObject，Input Module 像这个 GameObject 发送各种事件（接口）。在应用程序代码中，这个 GameObject 则可以是想要通知的任何 GameObject。这个功能原来是 SendMessage 来实现的。
