# TimeManager

## Properties

- float ClientUptime

  local client 已连接的时间。

- bool FrameTicked

  如果本帧中 TimerManager 会或者已经 tick，返回 true。

  网络帧率不一定和 Unity 帧率相同，因此一个 Unity frame 中，不一定执行网络帧。通过这个值判断 Unity 帧中是否会执行网络帧。

  即网络帧与 Unity 帧重叠。

- EstimatedTick LastPacketTick

  最后一个接收的 packet 的 Tick 信息，无论是 server 还是 client。

- uint LocalTick

  这是一个不会同步的计时单位（滴答）。该值只会递增，可用于自定义逻辑的索引或ID生成。
  
  在服务器端调用时返回服务器计时（ServerTick），否则返回本地计时（LocalTick）。
  
  断开连接后该值将重置。

- NetworkManager

- PhysicsMode

  设置如何执行物理。

  - Disabled：关闭 Physics 
  - TimeManager：TimeManager 每个 tick 执行 physics
  - Unity：Unity 每个 FixedUpdate 执行 physics

- byte PingInterval

  多少秒发送一个 connection ping。它还负责近似的 server tick。这个值不影响预测。

- long RoundTripTime（RoundTrip 往返）

  毫秒往返时间。这个值包含来自 tick rate 的延迟。

- float ServerUptime

  local server 已经连接了多长时间（开始监听）

- uint Tick

  当前服务器上的近似网络计时（滴答）。当以客户端模式运行时，此值为服务器计时的估算值。该字段的值可能随时间校准而增减。断开连接后，此值将重置。可通过TicksToTime()函数将Tick转换为服务器时间。如需严格递增的计时值，请使用LocalTick。

- double TickDelta

  对应 TickRate 的 fixed deltaTime。

- ushort TickRate

  server 每秒模拟多少次。这不会限制 server 的 frame rate。

## Methods

- float GetPhysicsTimeScale()

- PreciseTick GetPreciseTick(TickType tickType)

  - TickType
    - LastPacketTick
    - LocalTick
    - Tick
  - PreciseTick

- PreciseTick GetPreciseTick(uint tick)

  tick：返回的 PreciseTick 中设置的 tick。

- byte GetTickPercentAsByte()

  返回 TimeManager 到下一个 tick 的百分比。0-100

- double GetTickPercentAsDouble()

  0d ~ 1d

- uint LocalTickToTick(uint localTick)

  将本地计时（滴答）估算转换为同步 Tick（滴答）。

- void SetPhysicsMode(PhysicsMode mode)

- void SetPhysicsTimeScale(float value)

- void SetTickRate(ushort value)

  设置使用的 TickRate。这个值不会同步，它必须在 client 和 server 上独立设置。

- double TicksToTime(PreciseTick pt)

  将一个 PreciseTick 转换为 Time。

- double TicksToTime(TickType tickType = TickType.LocalTick)

  将当前 ticks 转换为 Time。

- double TicksToTime(uint ticks)

  将一些 ticks 转换为 Time。

- uint TickToLocalTick(uint tick)

  将同步计时（滴答）估算转换为本地计时（滴答）。

- double TimePassed(PreciseTick preciseTick, bool allowNegative = false)

  获取从 Tick 到 preciseTick 经过的时间

- double TimePassed(uint currentTick, uint previousTick)

  获取从 currentTick 到 previousTick 经过的时间

- PreciseTick TimeToPreciseTick(double time)

  将 Time 转换为 PreciseTick

- uint TimeToTicks(double time, TickRounding rounding = TickRounding.RoundNearest)

  将 time 转换为 ticks