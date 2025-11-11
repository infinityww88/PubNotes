Fishnet 内部机制和 ReplicateState 很复杂，难以理解，只需要记住以下内容：

- Invalid：不应该看见
- Created：这个 Tick 的 Data 是被 Controller 创建的，是有输入数据的（即使 Controller 发送的是 default input data）。
- Ticked：Replicate Data 已经运行过 Replicate 方法中的代码了（根据输入操作 object），基本就是表示这个 Tick 的 Data 已经在 Server 上运行过（确认过）了。

  只有 Ticked 时，表示这个 Tick 凭空过去，Controller 没有发送输入数据过来。

- Replayed：表示这个 Tick 的数据还没有 Server 确认，在这里真正执行预测的逻辑。

Server Repliate 输入数据、Client 执行预测的逻辑都在 Replicate 方法中执行。

客户端收集输入调用 Replicate 方法时，不会执行方法体，而是将输入参数添加到队列中，等待发送给 Server。

输入发送给 Server 并不会立即执行，而是等待几个 Tick（称为 Interpolation）。这是缓存过程。类比流媒体缓存机制。让 Server 有一定量的预存 input data。等到 Interpolation（缓存周期）一过就开始 Replicate 这些输入。这样当 Server 执行这些 Input Data 时，Client 可以同时发送最新的 Input Data 过来。这样的缓存机制可以抹去网络抖动，产生平滑的“回放”。

因此 Server 对 Input Data 的处理是由一定延后的，但是这个延后并不会太多，通常也就几个 tick，只要足够快，玩家是察觉不到的吗，但是对网络却是很大的缓冲时间。

Reconcile 与 Replicate 是两个完全独立、并行的机制。通过它们良好合作，只要网络帧的频率够快，就可以实现流畅的预测回滚。Reconcile 的发送时机与 Replicate 不一定一致。

服务器不会在每个 Tick 都发送 Reconcile，而是按需或定期低频发送。如果每个 Tick 都发一次 ReconcileData，那就意味着：

* 每个对象、每帧都要打包状态
* 网络带宽急剧上升；
* 客户端回滚频繁、性能下降。

FishNet 采用的策略是：

* 只在需要修正预测误差时 或 周期性（例如每隔 N Tick） 才发送 Reconcile。
* FishNet 服务器在模拟预测对象时，会判断是否需要同步给客户端：
* 状态变化超过阈值（位置、旋转、速度等与上次发送的差异大于某个容忍范围）；
* 时间间隔达到同步频率限制（例如每 50ms、100ms 才发一次）；
* 客户端确认滞后太多 Tick（客户端状态明显落后或误差积累大）；
* 其他强制同步事件（如瞬移、被外力撞击等）。

因此 Reconcile 与 Replicate 是平行相互独立的系统，它们发送、执行的时机也是独立的。客户端预测的逻辑也不一定严格按照 server 一样执行。Server 对 Input 进行了一定缓冲（Interpolation），但是客户端却可以立即执行预测，并且每次收到服务端发送回来的 Reconcile，将客户端状态重置到此，然后继续重放这个 Tick 后的 Input Data，往复不断这个循环即可：

```
客户端收集输入，发送到服务端，并在本地也缓冲这些输入 -> 客户端执行立即响应，执行预测逻辑 -> 服务端缓冲周期过后，执行权威逻辑 -> 服务端向客户端发送 Reconcile -> 客户端将 Object 状态重置到这个 reconcile data，然后 replay 这个 tick 之后的 input。
```

Replicate 方法是客户端收集输入、服务器执行 Repliate 逻辑、客户端执行预测共用的方法。

Reconcile 方法是服务端发送 Reconcile data，客户端执行状态重置共用的方法。

Fishnet 用属性 \[Repliate\] 和 \[Reconcile\] 掩盖了这些区别，让你只需要编写一份代码。

总之 Fishnet 内部的实现非常复杂，难以理解。就以黑盒的方式使用它：

- 对于 Networked Controller Object，注册 TimeManager 的 OnTick，每帧调用 replicate 方法和 CreateReconcile 方法

  - Repliate 方法中带 Ticked 的，是 Server 端已经确认的，只需要按照参数 Replicate Data 执行方法体逻辑即可。
  - 仅 Replayed 的 Replicate Data 才是需要预测的部分，可以在这里执行需要的预测逻辑
  - CreateReconcile 是虚拟函数，实现它，在 OnTick 中调用它。这样在 Server 调用时，不会执行里面的方法体，而是检查参数和其他方面，判断是否需要向客户端发送一个 Reconcile Data。客户端调用它时，是将服务端发送过来的 Reconcile Data 在方法体中用其重置客户端状态

- 对于 Networked NonController Object，每个 Tick 只需要 CreateReconcile 方法

**遵循这些约定，就不用管其内部的实现机制、以及是否 state forward 了**。

事实上，只要网络帧足够快，不需要预测也能看到平滑的效果。例如只使用 NetworkTransform 就可以让 object 同步。预测、回滚这些机制是为了遮盖网络延迟和抖动的。

所谓延迟补偿，就是补偿玩家因为网络延迟导致的不公平性。例如，玩家在某个时刻 t0 看见敌人，并瞄准射击，但是在服务器上，可能 t1 时间才收到数据包，如果还有输入缓冲机制，还需要再等一定的 Tick 时间，才能执行，此时敌人的位置已经改变了，如果按照此刻状态判断，对高延迟的玩家是不公平的。因此服务器可以缓存一定时间的游戏状态（尤其是所有玩家的位置）。当服务器开始处理玩家的输入（开火）时，服务器可以向前查找玩家开始时刻 t0 时的游戏状态（敌人位置），然后用那个时刻的敌人位置进行命中判断。这样就补偿了玩家因网络延迟导致的不公平性。这就是所谓的延迟补偿。

如果 t 时刻已经超出了服务器缓存的最早时间，就使用服务器缓存的最早时刻的状态。这就是为什么竞技类游戏的 Interpolation 要尽可能小（通常1-2 tick），而实时性没那么严格的休闲游戏，Interpolation 就可以更大一些的原因。总之网络游戏不是追求完美的实时、准确，这是不现实的。而是允许一定的错误容忍、延迟，只要在玩家可接受、不易察觉的范围内即可。

不要做多人竞技射击游戏，只做合作式、对是实时同步、准确性要求不那么高的娱乐休闲式多人游戏。前者要求太高，技术太复杂。对于娱乐休闲式的游戏，简单的预测就可以，网络好的时候，甚至不需要预测，直接使用 NetworkTransform 同步 Position、Rotation 即可。不做实时竞技类游戏，延迟补偿和复杂的预测回滚都不需要，只需要服务端权威 Replicate 和 Reconcile。