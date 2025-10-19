# State

一个 object 的状态信息（Smooth Sync 可以同步的信息）：timestamp，position，rotation，scale，velocity，angular velocity。

## Public Member Functions

- copyFromSmoothSync(SmoothSync smoothSyncScript)：void

  从一个 SmoothSync 组件复制同步信息（ SmoothSync 组件是 NetworkTransform 组件的代替者，从其中复制状态信息）

- copyState(State state)：State

  复制一个现有 state

- resetTheVariables()：void

  重置状态信息

- State()

  默认构造函数

## Static Public Member Functions

- static State Lerp(State targetTempState, State start, State end, float t)

  返回一个插值的状态 Lerped state，在 start 和 end 之间，使用 time t

## Public Fields

- angularVelocity：Vector3

  state 被发送时，owned object（SmoothSync 组件所在 gameobject）的 angularVelocity。

  State 由 owner client 发送到 server，再从 server 发送到 non-onwer client。State 中的信息记录的是它从 owner client 发送时的状态。

- position：Vector3

- rotation：Quaternion

- scale：Vector3

- velocity：Vector3

- ownerTimestamp：float

  state 被发送时的 owner 的network timestamp

- atPositionalRest：bool

  如果为 true，这个 State 被 tagged 为 位置静止的状态（positional rest State），它应该停止在 non-owners 上extrapolating。

  Transform 变化由 owner client 发出，因此在 owner client 上直接改变，然后发送到 server。Server 应该通过 SmoothSync.validateStateDelegate 校验 owner client 是否作弊。如果 server 接受这个状态变化，将变化发送到所有 non-owners，non-owners 进行状态插值。因此，插值只发生在 non-owners。

- atRotationalRest：bool

- receivedOnServerTimestamp：float

  State 从 owner client 发送到 server 并在 server 进行 validated 时的时间戳。只被 server 用于 latestVerifiedState

- reusableRotationVector：Vector3

  用于 Deserialize，使得我们不需要每次生成一个新的 Vector3

- serverShouldRelayAngularVelocity：bool = false

  relay：转发，中继

  如果 State 中包含需要转发的 angularVelocity（有更新），则设置其为 true，使得 server 将它转发到其他 clients

- serverShouldRelayPosition/Rotation/Scale/Velocity：bool = false

- teleport：bool

  如果为 true，标记 State 是一个 瞬移 teloport State，使得它在其他 clients 上直接改变，而不需要插值

  