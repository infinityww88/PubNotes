## 一些猜测

Replicate 用于执行动作，Reconcile 用于校准状态。

例如 Replicate 接收输入，然后执行跳跃、开火等 graphic 视觉动作，但是服务端执行后的状态是权威的，客户端执行的只能是预测。服务端执行 replicate 之后，将权威状态发送给客户端，客户端 reconcile 到权威状态。

ReplicateState：用于 Replicate 重放方法的状态，这些状态都是用在 replicate 方法内的，用于指示 code 如何处理 replicate 方法中的 input 数据。

replicate 方法是处理 input data 的，reconcile 方法是校准 object state 的。

Server 不仅向 clients 发送 reconcile 权威状态数据，还转发其他客户端的 input data，以让这个 client 执行那些 input（例如播放音效、特效、跳跃等等）。

注意 replicate 对于客户端只执行动作，不负责修改权威数据。权威数据只由 server 修改并通知 clients reconcile。但是客户端可以提前预修改，以防止二次跳跃、或不消耗子弹任意开火的情况，但是最终要 reconcile 到 server 的权威数据上。

Replicate：动作
Reconcile：状态

Replciate 方法有两个阶段：

- Current：在 Ownership Client 和 Server 上可直接运行
- Replayed：erver 向其他 clients 转发一个 client 的 input data，在那些 clients 上重放 replicate 方法中的动作，这就是所有的 Replayed 状态

猜测 Fishnet 框架向 Unity Update 或 FixedUpdate 那样，以一定频率时刻调用着 Replicate 方法和 Reconcile 方法。Fishnet 不管你如何处理，它只是以固定频率来调用，你要实现的功能在方法中通过 ReplicateState 来判断分支。但是它们的频率和网络数据包的 tick 频率并不总是完全一致，有可能比网络数据包 tick 频率要快。这就导致在网络数据包到来之间的间隔里会运行有 Replicate 方法和 Reconcile 方法，这些方法里，不会希望有新的 input data 到来（因为还没到下一个网络数据包的 tick），对于这些没有 input data，而且不期望有 input data 的 Replicate 方法，状态就是 Future。

当到达下一个网络数据包的 tick 时和之后，本应该就有新的 input data 了（即使客户端没有操作，也应该时 default values，而不是没有 input data），如果因为网络原因导致在这个网络 tick 没有收到本应收到的 input data（即使没有输入也应该是 default），那后面运行的 replicate 就是 predicted 的，期望有 input data 到来，但是没有。

或者 Fishnet 内部存在某种估算机制，能估计网络数据包的往返时间。在估计的数据包发送时间内，可以假设数据包是在路上的，此期间运行的 replicate 就会传递 future 状态。如果超过了估算时间，数据包还没到来，就传递 predicted 状态，只是 code，此时本应有数据包到来，但是没有收到，看你如何处理。

### 状态分类解释

- invalid

- valid

  - current

    - created：

      ownership server + ownership client：Instance 有 object 在当前 tick 的 input data。

    - future

      non-ownership client：Client 不知道当前 tick 的 input data，可基于之前的 action 继续模拟，或退出模拟（pause rigidbody）等待最新的 input data。

    - predicted

      non-ownership server：Server 不知道当前 tick 的 input data，它期望本应有数据到来，但是并没有。

  - replayed

    - created

      clients：Client 有 object 在这个 tick 的 input 数据。client 当前在 reconciling（即 replay，重放来自服务器发送的 input，后面还会 reconcile 权威状态数据）。

    - future

      non-ownership client：client 没有 object 在这个 tick 的 input data。tick 在 future，data 还未知，client 不期望这个 tick 有数据到来。Clinet 当前正在 reconciling。 Client 可以基于之前的 action 继续模拟，也可以退出模拟（pause rigidbody）等待最新数据。

    - predicted

      non-ownership client：client 没有 object 在这个 tick 的 input data，但是 client 期望这个 tick 本应有数据到来但是并没有，Client 当前在 reconciling。

Replayed 都是 client 的状态，都是 client 正在进行 reconciling。


可见 server 只有两个状态：CurrentCreated 和 CurrentPredicted.

Server 端从不会遇到 Future 状态。

- Server
  - Current Created：server 具有 object 的真实 input data，可以直接运行对应 input 的 action。
  - Current Predicted：Server 没有 non-ownership object 的 input data，object 有 ownership controller，它的真实 input data 可能还在路上。那么在还没有收到真正 input data 时，Server 就是处于 predicted 状态。
- Client
  - Current Created
  - Replayed Created
  - Current Future
  - Replayed Future
  - Replayed Predicted

server 可以直接控制没有任何 ownership 的 object。