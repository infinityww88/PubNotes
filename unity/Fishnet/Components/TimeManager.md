# TimeManager

TimeManager 处理和提供与 network timing 相关的 callbacks。

在 networking framework 中管理 network time 和 tick-based systems。

networked objects 及时刷新，处理 ticks，timing conversions，physics step control。

为 network-related timing events 提供 hooks。

管理 network timing 如何执行，或者使用 fixed ticks 或可变 intervals，并为 sending 和 receiving network data 提供精确时间，确保 server 和 clients 之间的同步

它还控制物理模拟 mode（manual，automatic，disabled），以在网络上维持一致的模拟

## 设置

- Update Order：控制 TimeManager 何时调用它的 Unity callbacks 版本。如果希望在 ​​Tick（网络同步周期）​执行前，通过 ​​OnUpdate（每帧更新）收集输入数据，那么 ​​BeforeTick​​ 会是一个理想的选择

- Timing Type：规定 data 何时发送和接收

  - 设置为 Tick，数据仅在同时触发Tick的网络同步帧中被处理

  - 设置为 Variable，数据将在每帧可用时进行发送与读取

- Allow Tick Dropping：当单帧内出现多次Tick时，将允许客户端跳过部分Tick。这能有效防止客户端每帧执行的模拟次数持续增加，从而避免造成更大的性能损耗

- Maximum Frame Ticks：当启用"允许跳过Tick"（Allow Tick Dropping）功能时，将显示此参数。该数值表示客户端在开始主动跳过Tick以恢复性能之前，每帧最多允许处理的Tick数量上限

- Tick Rate：该数值表示 ​​TimeManager​​ 每秒平均触发 ​​Tick 事件​​ 的频率，以及数据收发的平均频次

- Ping Interval：用户每秒接收Ping更新的频率。较大的Ping值可能导致服务器Tick同步精度略有下降，但这些变化不影响预测功能

- Timing Interval：预测时间更新的间隔秒数。数值越低，时间精度越高，但会占用更多带宽

- Physics Mode：物理模式决定了物理模拟的运行方式。Unity 默认由引擎管理物理模拟，而 TimeManager 则在每个 Tick 周期进行物理模拟。当使用客户端预测（Client-Side Prediction）功能时，必须采用 TimeManager 的物理模拟设置
