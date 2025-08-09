# NetworkTransform

一个 NetworkBehaviour 组件，用于同步 NetworkObject 的 transform 信息。

## Properties

- NetworkBehaiour ParentBehaviour

- bool TakenOwnership

  如果 local client 使用 TakeOwnership 并在等等 ownership 改变，返回 true

## Methods

- void ForceSend()

  重置最后一次 sent 信息，来强制重新发送当前 values。

- void ForceSend(uint ticks)

  重置最后一次 sent 信息，在指定数量的 ticks 后强制重新发送当前 values。

- bool GetSendToOwner()/SetSendToOwner()

- void SetInterval(byte value)

  更新网络上时间间隔。

- void SetPosition{Rotation/Scale}Snapping(NetworkTransform.SnappedAxes axes)

  设置 Position{Rotation/Scale} snap 的 axes。

- void SetSynchronizedProperties(SynchronizedProperty value)
  
  SynchronizedProperty：

  - None
  - Parent
  - Position
  - Rotation
  - Scale

- void SetSynchronizePosition{Rotation/Scale}(bool value)

- void Teleport()

  当被 object 的 controller 调用时，下一个 changed data 将会被 spectators teleports。

## Events

- event NetworkTransform.DataReceivedChanged OnDataReceived

  当新数据到达时调用。提供先前值和后续值。Next data 可以被修改 manipulated。

- event Action OnInterpolationComplete

  当 transform 达到它的 gola 时调用。

- event Action<NetworkTransform.GoalData> OnNextGoal

  当 GoalData 更新时调用。
