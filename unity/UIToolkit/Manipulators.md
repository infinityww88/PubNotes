# Manipulators

使用 manipulator 处理 events，可以将 event 逻辑从 UI code 中分离。

Manipulators 是状态机，它处理 UI 元素的 UI 用户交互。它们存储，注册，反注册 event callbacks。Manipulator 一次性设置用户交互，因此不需要一个一个处理每个回调。要处理 events，使用或继承 UI Toolkit 支持的一 manipulators：

- 定义一个专门的类，继承 UI Toolkit 支持的 manipulator 类。这个类封装 event-handling 逻辑，专门来处理你想要的用户交互
- 在类内部，实现响应相关交互的方法，例如鼠标点击或拖放。这些方法捕获并处理执行期望行为的必须信息。
- 当完成编写 manipulator 类之后，实例化它的实例并附加到 target VisualElement 上。附加让 manipulator 截获并管理特定事件，组织用户交互，同时维持 event code 与 UI code 分离。

## UIToolkit 支持的 Manipulators

- Manipulator：所有 Manipulators 的基类
- KeyboardNavigationManipulator：处理使用键盘的 device-specific input events 到 higher-level navigation operations 的转义
- MouseManipulator：处理 mouse input。具有一个 activation filters 列表
- ContextualManuManipulator：当用户点击鼠标右键，或键盘上的 menu 键，显示一个上下文菜单
- PointerManipulator：处理 pointer input，具有一个 activation filters 列表
- Clickable：在一个 element 上跟踪 mouse events，识别一个点击事件

