# Synthesizing Events

在你合成 synthesize 并发送自定义事件之前，需要理解 UI Toolkit event system 如何分配和发送 operating system events。

Event system 使用一个 events pool 来避免重复分配 event objects。要合成并发送自己的 events，你应该使用一些步骤分配并发送 events：

1. 从 events pool 获取一个 event object
2. 填充 event 属性
3. 在一个 using block 中 enclose event 来确保它会返回到 event pool
4. 传递 event 到 element.SendEvent()

如果你想发送那些通常由 operating system 发送的事件，例如 keyboard / mosue events，使用 UnityEngine.Event 来初始化 UI Toolkit event。

```C#
void SynthesizeAndSendKeyDownEvent(IPanel panel, KeyCode code,
     char character = '\0', EventModifiers modifiers = EventModifiers.None)
{
    // Create a UnityEngine.Event to hold initialization data.
    // Also, this event will be forwarded to IMGUIContainer.m_OnGUIHandler
    var evt = new Event() {
        type = EventType.KeyDownEvent,
        keyCode = code,
        character = character,
        modifiers = modifiers
    };

    using (KeyDownEvent keyDownEvent = KeyDownEvent.GetPooled(evt))
    {
        panel.SendEvent(keyDownEvent);
    }
}
```
