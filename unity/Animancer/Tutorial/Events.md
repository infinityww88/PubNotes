End 事件无视 loop，只在第一个 loop 中触发，一旦第一个 loop 经过了 NormalizedEndTime，End 事件就会在之后的每一帧不断触发。

此外， End 事件和普通事件一样，在新的 State 播放时一起被清除。如果新的 State 开始播放时，还没有到 End 事件时间，即第一个 loop 还没有到 NormalizedEndTime，End 事件也会被清除不会调用。
