# Event System

UI Toolkit 包含一个 event system，在 user interactions 和 visual elements 之间通信。Inspired by HTML events，UI Toolkit event system 共享很多相同的属于和事件名。Event system 由以下事情组成：

- Event dispathcer

  event system 监听来自 operating system 或 script 的事件，并使用 Event dispatcher 分发这些 events。Event dispatcher 还决定用来发送 events 到visual elements 的分发策略。

- Event handler

  当在一个 panel 中发送一个事件时，event 被发送到 panel 中的 VisualElement tree。你可以添加 event handlers 到 visual elements 在它们发生时响应特定事件类型。

- Event synthesizer

  Operating system 不是唯一的事件源。Scripts 也可以通过 dispatcher 创建和分发 events。

- Event types

  不同的事件类型基于 EventBase 组织到一个 hierarchy，并分组为 families。每个 events family 实现一个 interface，其定义同一个 family 的所有 events 的通用特征。例如 MouseUpEvent，MouseDownEvent，和其他实现 mouse events 实现 IMouseEvent 接口。Interface 指定每个 mouse event 有一个 position，一个 pressed button，一组 modifier button，和其他 mouse-related 事件类型。

你还可以使用 events 在 visual elements 和其他消息类型通信，这些消息表达为 events。例如，ContextualMenuManager 使用 ContextualMenuPopulateEvent 在一个 contextual menu 添加 items。

