# NetworkState

SmoothSync 定义的 Mirror Message，用来包装 State，使得可以使用 Mirror 发送它。

继承自 MessageBase。

它只发送在 SmoothSync 组件上 enable 的 State 部分。在 SmoothSync 上可以指定同步哪些信息（position，rotation，scale，velocity，angularVelocity）

## Public Member Functions

- void copyFromSmoothSync(SmoothSync smoothSyncScript)

  从 SmoothSync 组件中复制一个信息到一个 NetworkState

- Serialize(NetworkWriter writer) / Deserialize(NetworkReader reader)：override

- NetworkState()

## Public fields

- smoothSync：SmoothSync

  关联这个 State 的 SmoothSync。

- state：State

  将通过 network 发送的 State。

