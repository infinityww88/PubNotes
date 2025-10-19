# Supported Events

Event System 提供了很多事件，它们可以在用户自定义的的 Input Modules 被定制。

如果你配置了一个有效的 Event System，这些事件将会在正确的时间被调用。

MonoBehavior 自身还有一些事件函数 OnMouseEnter/OnMouseExit/OnMouseDown/OnMouseUp/OnMouseOver等，这些似乎是独立于 Event System 实现的，因为场景中没有 Event System 它们也能正确运行。应该是 Unity 早期提供的一些用于处理输入的事件，现在作为遗留代码。从名字上看，它们也是只针对 Mouse，新的 Event System 统称 Pointer，因为还要处理 touch。从鼠标位置直接向场景发射射线，只检测 Collider。

避免使用这些函数，做一件事有且只有一种方法。

- IPointerEnterHandler - OnPointerEnter - Called when a pointer enters the object
- IPointerExitHandler - OnPointerExit - Called when a pointer exits the object
- IPointerDownHandler - OnPointerDown - Called when a pointer is pressed on the object
- IPointerUpHandler - OnPointerUp - Called when a pointer is released (called on the GameObject that the pointer is clicking)
- IPointerClickHandler - OnPointerClick - Called when a pointer is pressed and released on the same object
- IInitializePotentialDragHandler - OnInitializePotentialDrag - Called when a drag target is found, can be used to initialise values
- IBeginDragHandler - OnBeginDrag - Called on the drag object when dragging is about to begin
- IDragHandler - OnDrag - Called on the drag object when a drag is happening
- IEndDragHandler - OnEndDrag - Called on the drag object when a drag finishes
- IDropHandler - OnDrop - Called on the object where a drag finishes
- IScrollHandler - OnScroll - Called when a mouse wheel scrolls
- IUpdateSelectedHandler - OnUpdateSelected - Called on the selected object each tick
- ISelectHandler - OnSelect - Called when the object becomes the selected object
- IDeselectHandler - OnDeselect - Called on the selected object becomes deselected
- IMoveHandler - OnMove - Called when a move event occurs (left, right, up, down, ect)
- ISubmitHandler - OnSubmit - Called when the submit button is pressed
- ICancelHandler - OnCancel - Called when the cancel button is pressed