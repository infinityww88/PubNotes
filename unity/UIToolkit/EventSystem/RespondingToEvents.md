# Responding to Events

有两种方式使一个 visual element 响应它接收到的事件。

- 注册一个 event callback
- 实现一个默认 action

应该注册回调还是实现默认行为依赖于很多因素。

例如，如果你从一个现有 class 实例化一个 objects，并且想 instance 在它接收事件时以特殊行为响应，唯一的选项是在 instance 上注册回调。

然而，如果你从一个 VisualElement 派生一个新的 class，你想要这个 class 的所有 instance 以相同的方式响应事件，你可以在 class 构造函数中为所有 instance 注册一个回调，或者为 class 实现默认 actions。

Callbacks 和 default actions 的区别是：

- Callbacks 必须在 class 的实例上注册。Default actions 被实现为 class 的 virtual functions
- Callbacks 为传播路径上所有元素执行。Default actions 只为 event target 执行。

你可以阻止执行 default actions，通过调用 event.PreventDefault()。一些 event types 不能被 cancelled，意味着它们的 default actions 不能被 cancelled。

你可以通过调用 event.StopPropagation() 或 event.StopImmediatePropagation() 来阻止执行 callbacks，即使对于那些不能 cancel 的 events。

- PreventDefault -> Default Action

- StopPropagation/StopImmediatePropagation -> Callback

你应该将 default action 视为一个特定类型的元素在接受到 event 时应该执行的行为。例如，一个 checkbox 应该通过 toggling 它的状态响应 click event，否则它就不是一个 checkbox。这个 behavior 应该通过覆盖一个 default action virtual funciton 来实现，而不是为所有 checkboxes 注册 callbacks。Callbacks 是在默认行为基础上实现的一些特殊，附加的行为，它不改变控件的本来功能，只是提供一些额外功能。

通常，你应该倾向于使用 default action 实现你的元素的自然期望的行为。这确保 default element 行为可以在一个 instance 上被 cancelled，通过在 instance 上调用 PreventDefault()。

一个 default action 实现 behavior 的额外好处是它们不需要在 callback registry 查找回调函数，而且没有 callbacks 的 instances 可以为事件传播过程进行优化。

对了更多的灵活性，event target 的 default actions 可以在事件分发过程期间的两个时刻执行：

- 在 trickle down 和 bubble up 传播阶段中间，里 target callbacks 执行之后立即调用，通过覆盖 ExecuteDefaultActionsAtTarget()
- 在事件分发过程的末尾，通过覆盖 ExecuteDefaultActions()

ExecuteDefaultActions / ExecuteDefaultActionsAtTarget 是定义 default action 的地方，二者在事件传播过程的不同时刻执行，选择一个合适的时刻定义 default actions。

如果可能的话，在 ExecuteDefaultActions 中实现 default actions。这个给你的 class 的 user 更多的选项来覆盖它们：它们可以在 trickle down phase 或者 bubble up phase 调用 PreventDefault()。

然而有时，你必须强制执行 default action 的一个 event 停止传播到元素的 parent。例如一个 text field 接收 key down events 来修改它的 value。这些 key down events 不会传播到 parent。在这种情况下，使用 ExecuteDefaultActionAtTarget() 实现你的 default action，并调用 StopPropagation()。这确保在 bubble up 阶段 event 不会被 callbacks 处理。

Default actions 只会对 event target 执行，Callback 被传播路径上每个元素执行。如果你想你的 class 在它们的 children 或 parents 响应事件，你必须在 class 的 instance 上注册一个 callback。有时这是必须的，但是为了更好的性能，尽量避免为你的 class 的每个 instance 注册 callback。

## Registering an event callback

为 instance 注册回调的优势是，它可以让你自定义一个 instance 的行为，劣势是性能损失，因为它需要查找 callback registry。

```C#
// Register a callback on a mouse down event
myElement.RegisterCallback<MouseDownEvent>(MyCallback);
// Same, but also send some user data to the callback
myElement.RegisterCallback<MouseDownEvent, MyType>(MyCallbackWithData, myData);
```

你的 callback 签名看起来应该像这样：

```C#
void MyCallback(MouseDownEvent evt) { /* ... */ }
void MyCallbackWithData(MouseDownEvent evt, MyType data) { /* ... */ }
```

你可以注册任意多个 callbacks。但是 callback registration system 阻止你为给定 event 和 propagation phase 注册同一个 callback 多次。你可以从一个 VisualElement 移除一个 callback，通过调用 myElement.UnregisterCallback() 方法。

传播路径上的每个元素，除了 target，接收到 event 两次：一次在 trickle down phase，一次在 bubble-up phase。要避免执行一个 registered callback 两次，使用 RegisterCallback 来指定 callback 在哪个 phase 执行。

但是默认地，不指定 phase 时，一个 registered callback 只在 target phase 和 bubble up phase 执行（只为第二阶段和第三阶段注册回调），这确保一个 parent element 在它的 children 之后响应。如果想 parent 先响应，显式注册 TrickleDown.TrickleDown callback。

```C#
// Register a callback for the trickle down phase
myElement.RegisterCallback<MouseDownEvent>(MyCallback, TrickleDown.TrickleDown);
```

这指示 dispatcher 在 target phase 和 trickle down phase 执行 callback。即 callback 总是为 target phase 注册，但是可以显式指定另外两个 phase。

## 实现一个 default action

Default action 应用到 class 的所有 instances。

一个实现 default aciton 的 class 还可以有 callbacks 注册在 instances 上。

一个 event class 实现在处理一个 event 之前或之后的被执行的 behavior。Events class 通过覆盖 EventBase 类的 PreDispatch() 或 PostDispatch() 方法来完成。既然 events 是 queued，这些方法可以在事件被处理而不是事件被发射 emitted 时，更新 state 或者执行 tasks。例如，BlurEvent 在它处理 element 之前改变当前 focused element。

实现 default action 需要派生一个新的 VisualElement 子类，然后实现 ExecuteDefaultActionAtTarget() 方法 或 ExecuteDefaultAction() 方法，或者二者都实现。

Default actions 是一个 visual element sub-class 的每个 instance 接收到一个 event 时执行的 action。可以通过覆盖 ExecuteDefaultActionAtTarget() 和 ExecuteDefaultAction() 来定制默认 actions。

```C#
override void ExecuteDefaultActionAtTarget(EventBase evt)
{
    // Do not forget to call the base function.
    base.ExecuteDefaultActionAtTarget(evt);

    if (evt.GetEventTypeId() == MouseDownEvent.TypeId())
    {
        // ...
    }
    else if (evt.GetEventTypeId() == MouseUpEvent.TypeId())
    {
        // ...
    }
    // More event types
}
```

为了更大的灵活性，应该在 ExecuteDefaultAction() 中实现 default aciton。这允许 user 停止或阻止一个 default action 的执行，因为 ExecuteDefaultAction 在整个事件传播的最后执行，因此在之前的任何地方都可以通过调用 PreventDefault 来终止它的执行。

如果想 target default action 在它的 parent callback 之前执行，在 ExecuteDefaultActionAtTarget() 中实现 default actions。

## 事件处理顺序

如果发生一个 event，它沿着 visual element tree 的传播路径发送。假设 event type 在事件传播的所有阶段都执行，event 被发送到每个 visual element，则事件处理顺序是：

1. 从 root element 到 event target 的 parent，执行元素上的 event callbacks，trickle down phase。
2. 执行 event target 上的 callback，target phase
3. 调用 target 的 ExecuteDefaultAcitonAtTarget()
4. 从 event target 的 parent 都 root element 执行 callbacks，bubble-up phase
5. 调用 target 的 ExecuteDefaultAction()。因为它在最后，因此之前阶段的任何一点都可以调用 PreventDefault 来防止它被调用，因此它最灵活。

当 event 沿着传播路径发送时，Event.currentTarget 给更新为当前处理 event 的元素。这意味着，在一个 event callback function 中，Event.currentTarget 是 callback 注册到的 element，而 Event.target 是事件发生的 element。

## 停止事件传播和取消 default actions

可以使用 callbacks 来 stop，prevent，cancel action 的执行。但是你不能阻止 EventBase.PreDispatch() 和 EventBase.PostDispatch() 方法的执行。

一些方法影响事件的传播和 default actions：

- StopImmediatePropagation() 立刻停止事件传播过程。不在为这个 event 执行 callbacks。然而，ExecuteDefaultActionAtTarget() and ExecuteDefaultAction() default actions 仍然被执行
- StopPropagation() 在当前元素的最后一个 callback 之后停止事件传播过程。这确保当前元素上所有的 callbacks 被执行，但是不会有更多的元素响应事件。ExecuteDefaultActionAtTarget() and ExecuteDefaultAction() default actions 仍然被执行
- PreventDefaultAction() 阻止 ExecuteDefaultActionAtTarget() and ExecuteDefaultAction() default actions 被执行。PreventDefaultAction() 不阻止其他 callback 被执行，只影响 ExecuteDefaultActionAtTarget 和 ExecuteDefaultAction。此外，如果在 bubble-up phase 期间调用 PreventDefaultAction()，ExecuteDefaultActionAtTarget default action 不会被阻止，因为它已经执行完了，它在 trickle down 和 bubble up 之间执行。
