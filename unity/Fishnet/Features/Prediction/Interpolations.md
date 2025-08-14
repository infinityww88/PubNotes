# Interpolations

PredictionManager 和 NetworkObject 都有 interpolation values，但是它们有不同的目标。

PredictionManager 的插值与 NetworkObject 的插值不同：

-​​ PredictionManager 插值​​

  在队列中缓存多个状态，逐步执行以实现预测补偿（如处理网络延迟），客户端或服务器均可设置。插值为0时，状态会立即执行，但可能导致不同步，通常建议至少设为1以缓冲延迟。每增加1单位插值，相当于在观察者端增加（插值×TickDelta）的延迟。

- ​​NetworkObject 插值​​

  通过 NetworkTickSmoother 组件控制图形对象的平滑过渡，仅影响视觉表现，与预测逻辑无关。例如，设置观察者插值为2时，图形对象会在状态执行后延迟2帧完成平滑移动。
