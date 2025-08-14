# PredictionManager

## Properties

- uint ClientReplayTick

  local client replay 权威 inputs 所在的当前 tick。

- uint ClientStateTick

  最近执行 reconcile 的 local tick。

- bool IsReconciling

  如果 prediction 当前在 reconciling，返回 true。当 reconciling 运行 replicates 将是 replays。

- uint ServerReplayTick

  local client replay 非权威 inputs 所在的当前 tick。

- uint ServerStateTick

  最近执行 reconcile 的 server tick。

- ReplicateStateOrder StateOrder

  state 运行所在的 order。Future 模式优先考虑性能且不依赖回滚机制，而 Past（历史）模式则侧重精确性但要求客户端每帧都进行回滚处理。

  由此可见不要求所有客户端完全与 server 模拟一直，只要大致准确即可，关键的核心是：至关重要的数据（生命值、比分、子弹数量等待）完全由服务器权威控制同步。

  - Appended

    在客户端上，状态仍会被置于历史时间点，而不是等待一个 reconcile 才执行，这些状态还会被加入队列并在它们被接收时运行。这会导致状态最初以错位的帧时序执行（后续在 reconcile 时进行修正）。但由于状态不再依赖 reconcile 才会执行，系统可以减少 reconcile 指令的发送频率，客户端也能降低 reconcile 执行的频次——这一机制尤其能为基于物理模拟的游戏带来显著的性能提升。

  - Inserted

    在客户端，状态会被置于历史时间点，然后在 reconcile 发生时执行。这确保了本地客户端与服务器在相同时间点运行状态，从而实现最佳的预测准确性。然而，为保证正常运行，客户端需定期 reconcile 以处理历史输入，这可能会对低端客户端设备的性能造成一定影响。

## Methods

- byte GetMaximumServerReplicates()

  server 每个 object 可以 queue 的 replicates 的最大数量。更高的值会导致 server 上更多的负载，并对 client 增加 replicate 延迟。

- void SetMaximumServerReplicates(byte value)

- uint GetReconcileStateTick(bool clientTick)

  当前 reconcile 的 client 或 server 的 tick。

- void SetStateOrder(ReplicateStateOrder stateOrder)

  设置当前 ReplicateStateOrder。这可以在 runtime 改变。改变这个值只影响修改它的 client。

## Events

- event PredictionManager.PostPhysicsSyncTransformDel OnPostPhysicsTransformSync

  在通过 TimeManager 进行时间管理时，若物理系统设置为使用TimeManager，该操作会在每次 reconcile 后、物理引擎执行 SyncTransforms（同步变换）后被调用。

- event PredictionManager.PrePhysicsSyncTransformDel OnPrePhysicsTransformSync

  在通过 TimeManager 进行时间管理时，若物理系统设置为使用TimeManager，该操作会在每次 reconcile 后、物理引擎执行 SyncTransforms（同步变换）前被调用。

- event PredictionManager.PostReconcileDel OnPostReconcile

  在 reconcile 执行之后调用。包含 reconcile 所在的 client 和 server tick。

- event PredictionManager.PreReplicateReplayDel OnPreReplicateReplay

  在 reconcile 执行之前调用。包含 reconcile 所在的 client 和 server tick。

- event PredictionManager.PostReplicateReplayDel OnPostReplicateReplay

  当 replay 一个 replicate 方法时，physics 模拟之后调用。

- event PredictionManager.PreReplicateReplayDel OnPreReplicateReplay

  当 replay 一个 replicate 方法时，physics 模拟之前调用。

- event PredictionManager.ReconcileDel OnReconcile

  当执行 reconcile 时调用。这在内部用来 reconcile objects，并不保证你的订阅在 internal components 之前或之后被处理。
