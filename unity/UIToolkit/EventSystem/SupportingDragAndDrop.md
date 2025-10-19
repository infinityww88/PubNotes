# Supporting drag and drop

要实现 drag 和 drop 功能，需要确保 drop area VisualElements 和 draggable VisualElement 注册特定 events 的 callback。

## 为 drop areas 注册 callbacks

一个 drop area VisualElement 需要为以下 5 个 event types 注册 callbacks。

- DragEnterEvent

  当 user 拖拽一个 dragable object 并且 pointer 进入一个 VisualElement，DragEnterEvent 被发送。

  当一个 drop area VisualElement 接收一个 DragEnterEvent，它需要提供反馈 feedback，让 user 知道它或者它的一个 child，是潜在的 drop operation 的 target。

  例如，你可以添加一个 USS class 到 target element，并在 mouse pointer 下面显示一个 dragged object 的 ghost

- DragLeaveEvent

  当 user 拖拽一个 dragable object 并且 pointer 离开一个 VisualElement，DragLeaveEvent 被发送。

  当一个 drop area VisualElement 接收到一个 DragLeaveEvent，它需要停止提供 drop feedback。

  例如，你可以移除在 DragEnterEvent 时添加的 USS class，并不在显示 dragged object 的 ghost。

- DragUpdatedEvent

  当 user 拖拽一个 dragable object 并且 pointer 在 VisualElement 上移动时，DragUpdatedEvent 被发送。

  当一个 drop area VisualElement 接收到一个 DragUpdateEvent，它需要提供 drop feedback。

  例如，你可以移动 dragged object 的 ghost 使它保持在 mouse pointer 下面。

  Drop area VisualElement 应该检测 DragAndDrop 属性，并设置 DragAndDrop.visualMode 来指示一个 drop operation 的效果。例如，一个 drop opration 可以创建一个新的 object，移动一个现有 object，拒绝 drop operation，等等。

- DragPerformEvent

  当 user 拖拽一个 dragable object 并在一个 VisualElement 上释放鼠标时，发送 DragPerformEvent。这只有在一个 VisualElement 设置 DragAndDrop.visualMode 为不是 DragAndDropVisualMode.None or DragAndDropVisualMode.Rejected 的值来指示它可以接受 dragged objects 时才发送。

  当一个 drop area VisualElement 接收一个 DragPerformEvent，它需要在存储在 DragAndDrop。objectReference，DragAndDrop.paths，或者 DragAndDrop.GetGenericData() 中的 dragged objects 上执行适当的操作。

  例如，你可以在释放 dragged object 的位置添加一个新的 VisualElement。

- DragExitedEvent

  当 user 拖拽一个 draggable object 到一个 VisualElement 上并释放 mouse pointer 时，发送 DragExitedEvent。这只在没有 VisualElement 指示它可以接受 dragged objects 时发生。

  当一个 drop area VisualElement 接收一个 DragExitedEvent，它需要移除所有 drag and drop feedback。

  注意：当前 UI Toolkit 的一个 bug 阻止 DragExitedEvent 被发送。作为一个变通方法，可以在 DragLeaveEvent 中实现相关功能，它在停止一个 drag and drop operation 时被发送。

## Making VisualElements draggable

要使一个 VisualElement 称为 dragable（可拖放的），必须为以下 3 个事件类型注册 callbacks

- MouseDownEvent

  当一个 draggable VisualElements 接收一个 MouseDownEvent，他需要设置 state 为 ready for dragging。

- MouseUpEvent

  当一个 draggable VisualElements 接收一个 MouseUpEvent，它需要重置它的 state。

- MouseMoveEvent

  当一个 draggable VisualElements 接收一个 MouseMoveEvent 并且它已经准备好 dragging，它需要:

  - 设置它的 state 为 being dragged
  - 添加合适的 state 到 DragAndDrop
  - 调用 DragAndDrop.StartDrag()
  - 提供 visual feedback 来显式它是一个 drag operation 的 object

Drop area VisualElement 在接收到一个 DragPerformEvent 或一个 DragExitedEvent 时应该移除 visual feedback。
