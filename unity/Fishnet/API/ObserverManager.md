# ObserverManager

## 属性

- MaximumTimedObserversDuration

  服务器在负载增加时更新定时观察者条件的最长时间。数值越低，定时条件检查速度越快，但会牺牲性能。

  超过这个时间必须检测一次。

- UpdateHostVisibility

  client：基于它们否是一个 observer 更新 clientHost 的可见性。

## 方法

- void SetMaximumTimedObserversDuration(float value)
- void SetUpdateHostVisibility(bool value, HostVisibilityUpdateTypes updateType)

