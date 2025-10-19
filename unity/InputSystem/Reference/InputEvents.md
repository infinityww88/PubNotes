# Input events

Input System 是 event-driven 的。所有的 input 传递为 events，你可以通过注入 events 来生成自定义 input。

可以监听所有流过 system 的 events 观察所有 source input。

Events 是一个 advanced 的 Input System 内部功能。如果你想支持自定义 Devices，或者改变现有 Devices 的行为，Event System 的知识非常有用。
