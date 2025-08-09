## Properties

- List<ObserverCondition> ObserverConditions
- NetworkObserver.ConditionOverrideType OverrideType
  - AddMissing：保持当前条件，并添加 ObserverManager 的条件
  - IgnoreManager：保持当前条件，忽略 ObserverManager 的条件
  - UseManager：忽略当前条件，使用 ObserverManager 的条件
- bool UpdateHostVisibility：如果为 true，根据其是否为 observer，为 Host client 更新 visibility

## Methods

- ObserverCondition GetObserverCondition<T>()
- SetUpdateHostVisibility(bool)
  - 设置 UpdateHostVisibility
  - 这不会立即更新 renderers
  - 需要和 NetworkObject.SetRenderersVisible(bool) 联合使用
