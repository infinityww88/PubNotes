# Architecture

新的 Input System 有一个层次的架构 layered architecture，由一个 low-level layer 和 一个 high-level layer 组成。

## Native backend

Input System 的基础是 native backend code。这是平台特定的 code，它收集有关可用设备的信息，和来自设备的输入数据。这些 code 不是 Input System package 的一部分，而是包含在 Unity 自身中。它包含对每一个 Unity 支持的平台的实现。

Input System 使用 native backend 发送的 events 和 native backend 交互。这些 events 通知系统 Input Devices 的创建和移除，以及任何 Device 状态的更新。

Input System 还可以反向发送 data 到 native backend，以发送到 Devices 的 commands 的形式。这些命令对不同的 Device 类型和平台具有不同的意义。

## Input System（low-level)

Low-level Input System code 处理和解释 native backend 提供的 event stream，并分发独立的 events。

Input System 为在 event stream 中任何新发现的 Device 创建一个 Device 表示。Low-level code 将这个 Device 视为一个 raw，unmanaged memory block。如果它接受一个 Device 的一个 state event，它将 state event 中的数据写入内存中的 Device state representation，使得 state 总是包含一个 up-to-date（最新）的设备和它所有的 Controls 的 representation（例如键盘和它的每个键）。

一个 Device 表示是一块内存，包含 设备和它的 Control 的状态表示，每个设备事件都覆盖内存中的数据，因此其中的数据总是最新的。

Low-level system code 还包含结构体描述常见已知 Devices 的 data layout。

## Input System（high-level）

High-level Input System code 使用 layouts 解释 Device 的 state buffers 中的数据。

基于 layout 的信息（例如 keyboard 包含哪些 keys，gamepad 包含哪些 buttons），Input System 为创建每个 Device controls 创建 Control 表示，它让你读取设备每个 Control 的状态。

作为 high-level system 的一部分，你还可以构建另一个抽象层来映射 Input Controls 到你的应用中。使用 Actions 来 bind 一个或多个 Controls 到你的应用中的一个 input。然后 Input System 监控这些 Controls 的状态改变，并使用 callbacks 通知你的游戏逻辑。你还可以使用 Processors 和 Interactions为你的 Actions 指定更复杂的行为。Processors 在将数据发送给你之前对 input data 进行处理。Interactions 让你在一个 Control 上指定监听的模式，例如 multi-taps。

