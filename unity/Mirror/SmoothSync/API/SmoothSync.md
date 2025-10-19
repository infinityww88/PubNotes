# SmoothSync

在网络上同步 Transform 或 Rigidbody。使用 interpolation 和 extrapolation。

SmoothSync 组件是 NetworkTransform 代替者。NetworkTransform 简单同步 position/rotation/scale，SmoothSync 则通过插值平滑同步 position/rotation/scale。

继承 NetworkBehaviour。

Owned objects 发送 States。Owned objects 首先并主要使用 sendRate 来决定发送 states 的频率。它将延迟 thresholds 来检查是否有任何 State 已经超过 thresholds，如果是这样，它将发送一个 State 到 non-owners 使得它们拥有更新的 Transform 和 Rigidbody 信息。Unowned objects 接受 States，owned objects 发送 States（它直接改变状态，其他客户端插值状态）。Unowned objects 将会试着变成 interpolationBackTime(seconds) 过去的状态，并使用 lerpSpeed 变量来决定当前 transform 多快移动到新 transform。新 transform 通过 received States 之间插值决定。如果没有新的 States 可用（latency spike）object 将开始外插值 extrapolation。

实现完全同步画面是不可能的，也没有意义。即使你前面有两个设备，也没有办法确定是否完全同步：

- 每个设备的网络速度不同，接收的 State 时刻也是不同
- 人眼无法分清轻微的位置、旋转差别
- 看一眼设备1的画面在确定设备2的画面以确定是否同步的过程中也具有时间差，画面也可能已经改变了
- 即使在逻辑完全同步，不同设备的帧率不同，每一帧的渲染时间不同，表现同一个事件的严格时间戳也是不同的。

网络游戏“同步”要保证的是逻辑的同步（重要事件和结果），然后让画面大致和逻辑同步，使人感觉画面和逻辑是“同步”的就可以。Server-Authoritative 架构中，所有重要逻辑是在 server 计算，所有重要事件在 server 发出，因此可以保证所有 clients 都以相同的顺序发生事件，得到相同的游戏逻辑。Clients 的作用是使画面表现大致契合就可以，使得轻微的差别不能被人眼分辨，是人感觉到画面和逻辑是“同步”的就可以。人分辨画面的允许的时间差(1/24s)对于计算机而言远远空闲，因此游戏的逻辑和画面在这个时间差内可以有所差别而人分辨不出。

总而言之，client 的任务不是在所有 clients 之间保证画面一致，而是 server 保证了一个权威的逻辑，clients 尽可能使画面契合这个逻辑，但不需要维护真实有意义的“同步”。Mirror（SmoothSync）中 clients 的 non-owned objects 和 owned objects 不位于同一个时刻。non-owned objects（其他 player 的 objects）在 clients 上总是表示过去（interpolationBackTime）时刻的状态，而不是当前状态，owned objects 表示的则是当前时刻的状态。这样当 client 接收到 non-owned objects 的 State 时，这个 State 的状态是网络传输时间（RTT）之前的状态。但是 client 约定 non-owned objects 只需要表示 interpolationBackTime 之前的状态就可以。因此如果 State 在网络上经历的时间小于 interpolationBackTime，那么它到达 client 时，对于 non-owned object 还属于“未来”的状态，因此只需要向这个状态插值就可以了。如果 State 在网络上经历的时间大于 interpolationBackTime，则 client 想将 non-owned object 移动的 State 中的状态，然后基于 State 向外插值（State 必须包含对 velocity 的同步）。interpolationBackTime 只需要稍大于数据包在网络上传输的时间就可以（clinet0 -> server -> client1）。而且这个时间非常短，因此 client 上画面和逻辑直接的差距不会被人眼识别。

因此客户端上 object 可以平滑地向 server 上的位置平滑插值，但不需要位于当前时间的精确位置。Server 保证逻辑的权威性，Client 只是尽可能快地播放 server 的逻辑，不需要准确，只要足够快，使 player 分辨不出就可以。新的 State 源源不断地到来，画面不断前进，而且逻辑确保时权威的，player 就不会关注到画面和逻辑的差别。

SmoothSync 包含很多选项控制同步的平滑程度和准确程度。这些选项可以在运行时根据网络情况动态调整。由于每个 client 的 latency 的情况都是不同的，因此不同 player 的 SmoothSync 在运行时都可能不同，因此他们的画面也不可能同步。这再一次说明了，在 Server-authoritative 架构中，只需要 server 保证权威逻辑，clients 需要做的只是使画面尽可能接近逻辑而已。

只需要在 clients 保证逻辑一致，不需要在所有 clients 上保证画面甚至时间一致，只要画面大致契合逻辑使 player 分辨不出就可以。

## Public Types

- enum ExtrapolationMode { None, Limited, Unlimited }

  外插值类型。使用已知的过去信息进入未知的外延状态。通常，你想要外插值来帮助填充 latency spikes 期间丢失的信息。

  - None：不使用外插值
  - Limited：使用extrapolation limits 设置
  - Unlimited：允许永久外插值。必须包含 velocity sync 以利用外插值

- enum WhenToUpdateTransform { Update, FixedUpdate }

  在哪里更新 Transform

## Public Member Functions

- void addState(State state)

  添加一个 incoming state 到 non-owned objects（非自己所有的 objects） stateBuffer 中。插值只发生在其他 clients 拥有的 objects，自己拥有过的 objects 可以直接操作（Authority），并发送给其他 clients。

- Awake()

  缓存对组件的引用。

- checkIfOwnerHasChanged()

  在每个接受的 State 上检测 owner 是否改变了。如果改变了，添加一个 包含当前 Transform 的 fake received State 到 State array 中，使得你可以在它和 new owner 的第一个 State 之间进行插值。

- clearBuffer()

  清空 state buffer。如果 object 的 ownership 被改变，必须在所有 non-owned objects 上调用这个函数。

- CmdTeleport(Vector3 position, Vector3 rotation, Vector3 scale, float tempOwnerTime)

  从 Host 到 所有 clients Echo 一个 teleport State。

- forceStateSendNextFixedUpdate()

  强制 State 在 owned objects 下一次 FixedUpdate 中被发送。State 将在下一个 frame 被发送，而无视所有限制。

- GetNetworkChannel: override int

- GetNetworkSendInterval(): override float

- getPosition() / getRotation() / getScale() 

- OnEnable()

  为这个 object 的 OnEnable 自动发送 teleport message。

- OnStartClient()：override void

  在 clients 上注册 network message

- OnStartServer()：override void

  在 server 上注册 network message

- registerClientHandlers()

- RpcNonServerOwnedTeleportFromServer(Vector3 newPosition, Vector3 newRotation, Vector3 newScale)

- RpcTeleport(Vector3 position, Vector3 rotation, Vector3 scale, float tempOwnerTime)

  在 clients 上接收 teleport State 并添加到 State array。

- setPosition(Vector3 position, bool isTeleporting) / setRotation / SetScale

- shouldSendAngualarVelocity() / shouldSendRotation() / shouldSendScale() / shouldSendVelocity()

  检查 angular velocity 是否改变得足够大。

  如果 sendAngularVelocityThreshold 为 0，若当前 angular velocity 和上一次发送的 angular velocity 不同时，返回 true。

  如果 sendAngularVelocityThreshold 大于 0，若当前 angular velocity 和上一次发送的 angular velocity 大于这个 threshold，返回 true。

- stopLerping()

  停止更新 non-owned objects 的状态，使得 object 可以被 teleported。

- teleportAnyObjectFromServer(Vector3 newPosition, Quaternion newRotation, Vector3 newScale)

  Teleport 这个 object，transform 将不会在 non-owners 上插值

- teleportOwnedObjectFromOwner()

  Teleport 这个 object，transform 将不会在 non-owners 上插值

- delegate bool validateStateDelegate(State receivedState, State latestVerifiedState)

  绑定你自己的 validation method。Smooth Sync 在 server 每次收到 State Message 时调用这个方法进行校验。默认它允许每一个接收的 State，但是你可以设置自定义 validateStateMethod 来校验 clients 没有修改它们自己所有的 objects 超出 game 预期的限制。

## Static Public Member Functions

- static bool validateState(State latestReceivedState, State latestValidatedState)

  默认的校验方法，允许所有的 States。返回 false 来 deny 这个 State。State 将不会添加到 server 上并且也不会发送到其他 clients。返回 true 来接受这个 State，存储到 server 上并发送到其他 clients。

## Public Fields

- childObjectSmoothSyncs：SmoothSync[] = new SmoothSync[0]

  对 child objects 的引用，使你可以比较 syncIndex

- childObjectToSync：GameObject

  要同步的 sync child object。

  如果你想同步 SmoothSync 组件所在的 gameobject，使这个 field 为空。要同步一个 child object，你必须添加两个 SmoothSync 到 parent object。在其中一个设置 childObjectToSync 指向你要同步的 child object，并是另一个组件 childObjectToSync 为空来同步 parent。你不能不同步 parent 而只同步 child。

- extrapolationDistanceLimit：float = 20.0f

  一个 non-owned object 允许外插值到 future 的最大距离。

  外插值太远可能导致古怪而且不真实的移动，但是有一点外插值要比 none 更好因为它可以是 non-owned objects 在 latency spikes 期间保持半正确（semi-right）。

- extrapolationTimeLimit = 5.0f

  一个 non-owned object 允许外插值到 future 的最大时间。

  SmoothSync 必须包含对 velocity 的同步以利用外插值。

- extrapolationMode：ExtrapolationMode = ExtrapolationMode.Limited

- forceStateSend：bool = false

  强制 owner 在下一帧发送状态信息

- hasRigidbody：bool = false

  这个 GameObject 是否有 rigidbody

- hasRigidbody2D：bool = false

  这个 GameObject 是否有 rigidbody2D

- interpolationBackTime：float = .1f

  non-owned objects 应该位于过去多少时间。

  interpolationBackTime 是 non-owners 上的 object 将处于的过去的时间。

  如果你遇到一个 latency spike，在开始外插值到未知状态之前，你将仍然拥有一个 interpolationBackTime 的已知 States buffer。

  基本上，对于 ping（RTT) 时间小于 interpolationBackTime 的每个人，这个 object 将会在所有屏幕上出现在相同的位置。

  增加这个值将使得内插值 interpolation 更有可能被使用，意味着 synced position 将更可能是 owner 所在的实际位置。

  减少这个值将使得外插值 extrapolation 更有可能被使用，这会提升响应，但是对于大于 interpolationBackTime 的任何 latency spikes，位置更有可能和 player 实际位置有差距。

  保持大于 1/SendRate 来试图总是使用 interpolate。

  单位时 seconds
  
- isAngularVelocityCompressed：bool = false / isPositionCompressed / isRotationCompressed / isScaleCompressed / isVelocityCompressed

  当在网络上发送 angular velocity 时发送 floats。

  将 angular velocity floats 转换成 Halfs，它只使用一半带宽，精度也只有一半。

  这样 server 或 client 收到的 float 都是丧失精度的。但是不需要保持浮点数精度，因为这是 server-authoritative 架构，总是使用 server 的逻辑为权威，客户端只是使画面靠近逻辑就可以，因此不需要浮点数确定性。Server-authoritative 架构是多人游戏的最佳实现方式。

- isSmoothingAuthorityChanges：bool

  在 authority 改变时平滑改变。

  发送一个带有 owner information 额外的 byte，使得我们可以知道何时 owner 发生改变并相应地平滑改变。

- isSyncingChild：bool

  这个 gameobject 是否有一个 child object 来 sync。相比于检查一个 GameObject 的存在，检查一个 bool 更高效

- lastAngularVelocityWhenStateWasSent：Vector3 / position / rotation / scale / velocity

  上一个 angular velocity State 被发送时 angular velocity owner 所在的状态。

- lastTimeStateWasSent：float

  owner 上一次发送一个 State 的时间

- latestReceivedAngularVelocity：Vector3 / lastestReceivedVelocity

  最新的接收到的 angular velocity。用于 extrapolation。

- maxPositionDifferenceForVelocitySyncing：float = 10

  一个指数度量 scale，用于决定 velocity 可以被设置到多高。

  如果 object 应该所在的位置和它所在的位置超过这个值，则它自动跳到应该在的位置。

  Is on an exponential scale normally。

- netId：NetworkIdentity

  缓存的 NetworkIdentity

- networkChannel：int = Channels.DefaultUnreliable

  用来发送网络更新的 channel

- ownerChangeIndicator：int = 1

  用来指导何时 owner 改变。不是一个 identifier。只从 server 发送。

- positionLerpSpeed：float = 0.85f / rotationLerpSpeed / scaleLerpSpeed

  多快 lerp 到 target state。0 is nerver，1 is instant。

  更低的值意味着更平滑但是更缓慢的运动。更高的值意味着更高的响应，但是可能导致抖动的运行。

- rb：Rigidbody / rb2D

  缓存 Rigidbody 组件

- realObjectToSync：GameObject

  实际同步的 object，这个 object 或者一个 child object（每个组件只有一个 sync object，但是 parent 可以有多个 SmoothSync 组件，一个组件必须同步自己，剩余每个组件可以同步一个 child）

- receivedPositionThreshold：float = 0.0f / receivedRotationThreshold

  这个 position 不会被设置到 non-owned objects，除非它改变地足够大。

  设置为 0 使得有所改变时总是更新 non-owned objects 的位置，并且如果还设置 snapPositionThreshold 为 0，每个 frame 使用 Vector3.Distance() 检查。如果大于 0，一个 synced object 的位置只会在它距离 state target position 大于这个 threshold 才会更新。通常保持这个 threshold 为 0 或者非常低。如果你外插值 extrapolating 到 future 位置，并且想立即停下来而不返回到它当前在 owner 上的位置，可以使用一个更高的值。

- receivedStatesCounter：int

  如果这个数值小于 SendRate，强制 full time adjustment。当第一次进入游戏时使用。

- sendAngularVelocity：bool

  在 Update 的开始设置这个变量，使得我们在一帧中只进行一次检查

- sendAngularVelocityThreshold：float = 0.0f

  angular velocity 不会发送，除非它改变得足够大。

  设置为 0 总是发送 owned objects 的 angular velocity，如果它自上一次发送的 angular velocity 有所改变。如果大于 0，一个 synced object 的 angular velocity 只在和上一次发送的 angular velocity 的差距超过 threshold 时才发送。

- sendPosition：bool / sendPositionThreshold：float

- sendRotation：bool / sendRotationThreshold：float

- sendScale：bool / sendScaleThreshold：float

- sendVelocity：bool / sendVelocityThreshold：float

- sendAtPositionalRestmessage：bool / sendAtRotationalRestMessage

  当两个 frames 的 position 相同时设置为 true，以告诉 non-owners 停止 extrapolating position

- sendRate：float = 30

  每秒多少次发送网络更新。对于 low send rate，尝试降低 lerpSpeeds 如果运动过于抖动。保持你的 interpolationBackTime 大于 send rate interval，这可以很好地进行插值。

- setVelocityInsteadOfPositionOnNonOwners：bool

  在 non-owners 上设置 velocity 而不是 position。

  需要 Rigidbody。使用 synced position 来决定在 non-owned objects 上设置什么 velocity。这对于快速的 speeds 产生更平滑的结果，用于 flying 或 racing（飞行或赛车）游戏。
  
  Is less accurate than default Smooth Sync。

  如果 object 试图到达的 position 被 block，也会导致错误的结果。如果使用这个选项，应该使用一个 SnapPositionThreshold。

- snapPositionThreshold：float / snapRotationThreshold / snapScaleThreshold

  如果一个 synced object 的 position 和 target position 的差距超过 snapPositionThreshold，它将立即跳到 target position 而不是 lerping。

  设置为 0 关闭 snap，如果还有 receivedPositionThreshold = 0，每一帧使用 Vector3.Distance() 检查。

- snapTimeThreshold：float = 3.0f

  在接受一个 State update 时，如果 client 估算的 non-owned objects 的 owner 时间和 State 记录的时间超过这个阈值，立刻将发送更新的 client 的估算时间设置到 State 记录的时间戳，否则仍使用估算时间。

- stateBuffer：State[] / stateCount：int

  Non-owned objects 保持一个在网络上接受的 recent States 列表，用于内插值

  Index 0 是最新的 received State。

  stateCount 是 stateBuffer 中 state 的数量

- syncAngularVelocity：SyncMode = SyncMode.XYZ / syncPosition / syncRotation / syncScale / syncVelocity

  Angular vecocity sync mode。调整 angular velocity 如何同步。

  对于不移动的 objects，使用 SyncMode.NONE

- syncIndex：int

  同步 object 的 index（child index ？）

- timeCorrectionSpeed：float = 0.1f

  修改正 non-owned objects 的估算 owner time 的快慢程度。0 = never，5 = instant

  Estimated owner time 每秒都可能有偏移 shift。Lower values 将会更平滑，但是将在 latency 总需要更长的时间去调整。

  建议小于 .5f，除非你遇到眼中的 latency variance 问题。

- useExtrapolationDistanceLimit：bool / useExtrapolationTimeLimit

  你是否想使用 extrapolationDistanceLimit。

  你可以只使用 extrapolationDistanceLimit 并每一个 extrapolation frame 节省一个 distance 检查。

  必须包含 velocity 同步以利用 extrapolation。

- validateStateMethod：validateStateDelegate

  保存一个方法引用，它被调用以检查 incoming States。你可以设置它为自己的自定义 validation 方法。在 Start 或 Awake 中：

  smoothSync.validateStateMethod = myCoolCustomValidatePlayerMethod

- whenToUpdateTransform：WhenToUpdateTransform
  
  何时在 non-owners 上更新 object 的 Transform。

  Update 将具有更平滑的结果，但是对于物理场景，FixedUpdate 更好。
  
## Properties

- approximateNetworkTimeOnOwner：float

  owner 上的当前估算时间。

  Time 来自 owner 上的每个 sync message。当它被接受时，我们设置 _ownerTime 和 lastTimeOwnerTimeWasSet。

  然后当我们想知道现在是什么时间时，我们添加 elapsed time 到我们接收的最近一个 _ownerTime 上。

- isSyncingXAngularVelocity：bool / isSyncXPosition / isSyncingXRotation / isSyncingXScale / isSyncingXVelocity / isSyncingYZ...
  
  决定相应的分量是否应该同步
