# Dispatching Events

Visual elements 和其他支持类，实现一些 events 的默认行为。有时这包含创建和发送额外事件。例如，一个 MouseMoveEvent 可以生成一个额外的 MouseEnterEvent 和 MouseLeaveEvent。这些额外事件被放置在 queue 中，并在当前 event 处理完成后被处理。例如 MouseMoveEvent 在处理 MouseEnterEvent 和 MouseLeaveEvent 事件之前完成。

## Event target

EventDispatcher.DispatchEvent() 的首要任务是发现 event 的 target。

有时这很容易，因为 event target 属性以及被设置好了。然而，对于 operating system 产生的 events 通常不是这样。

Event target 依赖于 event type。对于 mouse events，target 通常是 topmose pickable element，直接在 mouse 下方。对于 keyboard events，target 是当前 focused element。

一旦确认 target，它被存储到 EventBase.target，它在事件分发过程中不会改变。Event.currentTarget 在分发过程中则更新为当前处理 event 的元素。Target 是目的地，currentTarget 是途径的每个元素。

### Picking mode 和 custom shapes

绝大多数 mouse events 使用 picking mode 来确定它的 target。VisualElement.pickingMode：

- PickingMode.Position(default)：基于 position rectangle 执行 picking
- PickingMode.Ignore：阻止 picking 为一个 mouse event 的 result

可以覆盖 VisualElement.ContainsPoint() 方法来执行自定义 intersection 逻辑。

### Capturing the mouse

有时，当一个鼠标按下之后，一个 element 必须捕获 mouse position 以确保之后的所有 mouse events 都发送给它，即使 pointer 已经离开了 element，直到 mouse release。

例如 button，slider，scroll bar。控件在 mouse down 和 mouse up 之间捕获响应所有 mouse move 事件。

要捕获 mouse，调用 element.CaptureMouse() 或 MouseCaptureController.CaptureMouse()。

要是否 mouse，调用 MouseCaptureController.ReleaseMouse()。如果调用 CaptureMouse() 时，另一个元素已经捕获了 mouse，那个元素收到一个 MouseCaptureOutEvent 并失去 capture。

任何时刻，application 中只能有一个元素捕获鼠标。当一个 elements 捕获鼠标时，它成为后续所有 mouse events 的 target，除了 mouse wheel events。

注意：这只应用到没有设置它们的 target 的 mouse events。

### Focus ring 和 tab order

每个 UIElement panel 有一个 focus ring，定义元素的 focus order。默认地，focus order 通过在 visual element tree 上执行一个 depth-first（DFS）来确定，最后一个 focusable 的元素的再次切换回到第一个 focusable 元素。

一些 events 使用 focus order 来确定哪个元素 hold 焦点。例如，一个 keyboard event 的 target 是当前 hold focus 的 element。

使用 focusable 属性来控制元素是否可以具有焦点。默认地，VisualElement 不是 focusable 的，但是一些子类，例如 TextField，默认是可具有焦点的。

使用 tabIndex 属性来控制 focus order（tabIndex 默认为 0）：

- 如果 tabIndex 是 negative，element 不是 tabable 的
- 如果 tabIndex 是 0，element 保持默认的 tab order，即通过 DFS 确认的顺序
- 如果 tabIndex 是 positive，element 被放在任何 tabIndex = 0 或者小于它的 tabIndex 的元素之前

## Event propagation

选择了 event target 之后，dispatcher 计算 event 的传播路径。传播路径是可以接受 event 的 visual elements 的有序列表。

元素列表从 visual element tree 的 root 开始，下降到 target，然后上升到 root。

![UIElementsEvents](../../Image/UIElementsEvents.png)

- 传播的第一个阶段从 root 下降到 target parent，这个过程称为 trickle down phase
- 传播的第二个阶段在 target 上处理事件
- 传播的第三个阶段从 target parent 上升到 root，这个过程称为 bubble-up phase

Event target 在传播路径的中间。

绝大多数事件被发送传播路径上的所有元素。然而，一些 event types 跳过 bubble-up 阶段（上升阶段）。此外，一些 event types 只发送给 event target。

如果一些 element 被 hidden 或 disabled，它将不会接收事件。事件仍然会传播到一个 hidden 或 disabled 元素的 ancestors 或 descendants。

当一个 event 沿着传播路径发送时，Event.currentTarget 被更新为当前处理 event 的元素。这意味着在一个 event callback function 中，Event.currentTarget 是 callback 注册到的 element，而 Event.target 是事件发生的 element。

## Dispatch behavior of event types

每个 event type 拥有它自己的分发行为。下面的 table 总结每个 event 的行为

- Trickles down
- Bubbles up
- Cancellable：这种事件类型可以使它们的默认 action 被 cancelled，stopped，prevented

| Event type | Trickles down | Bubbles up | Cancellable |
| --- | --- | --- | --- |
| MouseCaptureOutEvent          | * | * |   |
| MouseCaptureEvent             | * | * |   |
| ChangeEvent                   | * | * |   |
| ValidateCommandEvent          | * | * | * |
| ExecuteCommandEvent           | * | * | * |
| DragExitedEvent               | * | * |   |
| DragUpdatedEvent              | * | * | * |
| DragPerformEvent              | * | * | * |
| DragEnterEvent                | * |   |   |
| DragLeaveEvent                | * |   |   |
| FocusOutEvent                 | * | * |   |
| BlurEvent                     | * |   |   |
| FocusInEvent                  | * | * |   |
| FocusEvent                    | * |   |   |
| InputEvent                    | * | * |   |
| KeyDownEvent                  | * | * | * |
| KeyUpEvent                    | * | * | * |
| GeometryChangedEvent          |   |   |   |
| MouseDownEvent                | * | * | * |
| MouseUpEvent                  | * | * | * |
| MouseMoveEvent                | * | * | * |
| ContextClickEvent             | * | * | * |
| WheelEvent                    | * | * | * |
| MouseEnterEvent               | * |   |   |
| MouseLeaveEvent               | * |   |   |
| MouseEnterWindowEvent         |   |   | * |
| MouseLeaveWindowEvent         |   |   | * |
| MouseOverEvent                | * | * | * |
| MouseOutEvent                 | * | * | * |
| ContextualMenuPopulateEvent   | * | * | * |
| AttachToPanelEvent            |   |   |   |
| DetachFromPanelEvent          |   |   |   |
| TooltipEvent                  | * | * |   |
| IMGUIEvent                    | * | * | * |

