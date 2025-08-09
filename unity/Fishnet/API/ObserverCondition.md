# ObserverCondition

## Fields

- NetworkObject

  这个 connection 作用的 NetworkObject.

## Properties

- Order(int)

  conditions 添加到 NetworkObserver 的顺序。

  越小的值越先添加，越先被检查。

  Timed conditions 从不会在 non-timed conditions 之前被检查。

## Methods

- bool ConditionMet(NetworkConnection connection, bool currentlyAdded, out bool notProcessed)

  如果这个 condition 所在的 object 对 connection 应该可见，返回 true。

- void Initialize(NetworkObject networkObject)

  初始化方法，初始化这个条件以使用。

- void Deinitialize(bool destroyed)

  反初始化方法，清理脚本。

- ObserverConditionType GetConditionType()

  ObserverConditionType:

  - Normal：条件只在发生改变时检查
  - Timed：条件需要定时检查

- bool GetIsEnabled()

  获取 condition 的 enabled 状态。

- void SetIsEnabled(bool value)

  设置这个 condition 的 enabled 状态。如果 state 改变，这个 object 的 observers 会重建。