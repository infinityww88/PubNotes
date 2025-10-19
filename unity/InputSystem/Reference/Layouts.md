# Layouts

Layouts 是 Input System 学习 Input Devices 和 Input Controls 的核心机制。每个 layout 表示一个 Input Controls 的特定组合。通过匹配一个设备描述到 layout，Input System 可以创建正确的 Device type 和解释 input data。

和 Events 一样，layout 输入高级知识，在创建自定义设备和改变现有设备行为时才会用到。Input System 已经提供了所有主流的 Device。

一个 layout 描述 input 的内存格式，以便从 Control 读取和写入数据（约定，协议）。Input System 开箱提供了大量常见 Control 和 Devices 的 layout。对于其他 device 类型，system 基于 Device 接口报告的设备描述自动生成 layout。
