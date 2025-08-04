PredictionManager 负责全局预测设置，和其他预测相关信息。

你甚至不需要将它添加到 NetworkManager object 上，但是这样做为你提供了修改默认设置的方法。

![PredictionManager](../../Image/PredictionManager.png)

## Interpolation

内插值是知道两个明确的 state，然后在两个 state 之间插值。外插值是仅知道之前的状态（至少两个状态），然后估计后面的值。
