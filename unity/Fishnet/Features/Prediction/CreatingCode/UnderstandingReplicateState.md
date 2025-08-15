# Understanding ReplicateState

理解熟悉每个状态的意义，可以帮助你在关注的 objects 上精细调整 gameplay。

每个状态是一个 flag value，一个 replicate state 可能包含多个 flags。有很多扩展方法可以用来检测一个 state 是否包含特定 flag。

## ReplicateState

这是在 replicate 方法中收到的状体。

- CurrentCreated

  Value 只在 对 object 拥有 ownership 的 server 和 client 上可见。

  Data 在这个 tick 收到。

- CurrentFuture

  Value 只在对 object 没有 ownership 的 client 上可见。

  Tick 在未来，data 还未知。这可以用于及早退出 replicate（不处理 actions 直接退出），或者基于之前的状态创建 actions（即维持之前的 actions）。

- CurrentPredicted

  Value 只在 server 没有 object 的 ownership 时，在 server 上可见。

  Server 没有 object 的控制器，不知道 object 应该如何运动，因此等待 ownership 发送 inputs。

  在这个 tick，server 对其 non-owned object 没有数据但是期望有，期待有数据在这个 tick 到来，但是并没有。

- Invalid

  state 的默认状态值。当运行 replicate 时，这个值应该从不会出现。

- ReplayedCreated

  Value 只能在 clients 上可见。Client 有这个 object 的在这个 tick 的数据。Client 当前在 reconciling 校准。

- ReplayedFuture

  Value 只在对 object 没有 ownership 的 clients 上可见。

  Tick 在未来，data 还未知。这可以用于及早退出 replicate，不处理 actions，或者基于之前的状态创建 actions（即维持之前的 actions）。

- ReplayedPredicted

  Value 只在对 object 没有 ownership 的 clients 上可见。

  Client 没有z这个 tick 的数据，但是期望有，期望有数据到来但是并没有。Client 当前在 reconciling 校准。

以视频流媒体想象多人游戏的 Prediction 和插值技术。客户端不可能物理上每时每刻保持一致状态（例如17:06:12时刻，所有 clients 看到的画面都是一致的），甚至绝大多数情况下不是那么同步的，有的快一点有的慢一点，但是不会差得太多，整体看起来是同步的，人感知不到其中的微小差别。就把多人游戏想象为可交互的流媒体，追求整体效果，而不是一丝一毫的细节，只有 server 端保持关键数据（例如比分、生命值等等）的权威数据即可，至于某个物体在一些 clients 相差几个像素（0.001米的世界距离）不那么重要（更何况本身物理模拟因为浮点数的不确定性，本身在不同的机器上就不同）。

## Future States

当使用 prediction 时，经常看见 in the future 和 future state。

当 in the future 时，不可能知道来自 controller 的数据。这里不是指真实物理意义上的未来，而是对 server 或 client 来说，它们已知的 data 都已经用尽了，再接下来的 tick 中，逻辑上对它来说进入了 future，尽管此时 controller 的数据已经在路上了。

当使用 client-prediction 时，作为 client，你总是实时地移动，即使在知道 server current state 之前。因此，你将不会知道其他 clients 或 server states，知道它们被转发给你，在这个未知的时间段内，object 被认为是 in the future。这是你获得 predict 来自 controller 的 future input 的机会。或者你可以简单地完全阻止移动（直到等到真正的 input 到来），用法完全依赖于你的需求。

对于 objects 的 controller，你从来不会 in the future，这让你只 replay 到你创建的 inputs，从不会超出。

**Replicate 方法和 Reconcile 方法就像 Update 一样，每个 Tick 都会调用，Fishnet 会根据当前状态传递数据和状态值，然后在方法内根据状态值决定做如何处理。**

当没有 create state 时，data 将是 default。这通常让很多开发者措手不及，因为他们可能期望从 controller 看见连续的 input，就像 controller 一直按住一个移动键。

一个常见的用例是仅在 data 已知时更新 objects animator。

```C#
[Replicate]
private void MovePlayer(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{
    //左右移动
    float horizontal = data.Horizontal;
    
    //只在 data 创建时（state 包含 Created）时包含 animator
    //如果 data 不是 created，不更新 animator，因为这会导致 animator 在 having input 和 default 之间来回切换
    //因为 Replicate 每个 tick 都会调用，不管情况如何，当没有来自 controller 的 input 时，会传递 default 值
    //换句话说，在 Created 这个 channel/序列 上（使用 created 过滤 data），才能看见 controller 的 input
    if (state.ContainsCreated())
        _myAnimator.SetFloat("Horizontal", horizontal);
}
```

如果你在 PredictionManager 上使用 State Order -> Inserted，则 Created 将只会在一个 reconcile 期间在 spectated objects 上设置。因为 spectated objects 上的 states 被插入到 replicate history，因此它们在 reconciles 期间运行，而不是 reconciles 之外。

## Preventing Future State Logic and Movement

replayed state 几乎总是用于 predict future（继续运动），或者反之，limit future（阻止运动）。

Limiting future velocities 是 replayed flag 应用最多的地方。这保持 object 不被用来 predict future，这可以限制 object 的实时 reflection，还可以阻止过量的修正或运动吸附snapping。

以下是一个展示跳跃和移动的基本示例，未深入探讨移动速率相关内容。

在未进行 future check 的被观测对象上，随着回放时间推进至未来，replay 时会先跳跃，随后持续向上“吸附”（移动）。

```C#
[Replicate]
private void MovePlayer(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{
    //Exit the method early to prevent going into the future, which would
    //result in the controller snapping upward very fast when replaying a jump.
    if (state.IsFuture())
        return;
        
    //Set vertical velocity to jump up.
    if (data.Jump)
        _verticalVelocity = 10f;

    //Only add vertical movement for this example.
    //Realistically, you would have x and z movement as well.
    Vector3 movement = new(0f, _verticalVelocity, 0f);
    //Reduce vertical velocity to begin falling, but prevent it from going too low.
    _verticalVelocity -= (float)base.TimeManager.TickDelta;
    _verticalVelocity = Mathf.Max(_verticalVelocity, -5f);

    _characterController.Move(movement);
}
```

上述示例展示了在角色控制器上防止 future movement 的简单实现，但刚体（Rigidbody）的情况有所不同。即使提前退出方法阻止新增速度，刚体仍会保持现有速度，因为物理引擎会在每一帧（无论是否回放）模拟其运动，不受复制（replicate）逻辑影响。

以下是一个没有阻止 future movement 的刚体示例：

```C#
[Replicate]
private void MovePlayer(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{       
    float horizontal = data.Horizontal;

    Vector3 movement = new(horizontal, 0f, 0f);

    _predictionRigidbody.AddVelocity(movement);
    _predictionRigidbody.Simulate();
    
    //Nothing in this code prevents the rigidbody from moving into the future.
    //Moving into the future：指的就是 rigidbody 在惯性的作用下在 future 状态（未收到 controller input 时）继续运动，即使在 future 运动。
}
```

阻止在 rigidbodies 上的 future movement 需要额外几行代码，但是非常容易。下面将使用 NetworkObject 上的 RigidbodyPauser 引用，在 future 暂停 rigidbody。

RigidbodyPauser 是 NetworkObject API 上较少提及的部分，绝大多数情况下专门用于 prediction。

```C#
[Replicate]
private void MovePlayer(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{   
    //只有对 objects 的非 ownership（!baseIsOwner）的 clients（!base.IsServerStarted：Server and ServerOnly）
    bool canChangePause = !base.IsOwner && !base.IsServerStarted;

    //如果在 future 状态（未收到 controller 的 input 时），不处理任何逻辑，并暂停 rigidbody。
    //否则，unpause rigidbody。
    //当 RigidbodyPauser 已经在相同状态（暂停时调用暂停，运行时 unpause），调用 pause/unpause 没有任何负面的副作用。
    if (state.IsFuture()
    {
        //这会通过将 rigidbody 标记为 kinematic 来阻止 rigidbody 移动。
        //Pausing rigidbody 还意味着其他 objects 可能潜在穿透它。
        //后面展示另一种方法。
        if (canChangePause)
            base.NetworkObject.RigidbodyPauser.Pause();
    }
    else
    {
        //当不在 future（当前有 controller 的 input 数据）
        //允许 object 再次移动。Unpausing 会恢复 velocities，就像它们暂停之前的那样
        if (canChangePause)
            base.NetworkObject.RigidbodyPauser.Unpause();
            
        float horizontal = data.Horizontal;
    
        Vector3 movement = new(horizontal, 0f, 0f);
    
        _predictionRigidbody.AddVelocity(movement);
        _predictionRigidbody.Simulate();
    }
}
```

就像上面的例子解释的，暂停一个 rigidbody 可能导致其他 objects 穿透它，这是由于 pauser 让 rigidbody 变成 kinematic。

下面是一个不同的技术，简单地在 future（没有 input 数据时，收到 default input 和没有数据不一样，没有数据是没有在这个 tick 收到来自 controller 的数据包，可能是因为网络问题。收到 default input 是明确 controller 在这个 tick 没有 input 数据）将速度设置为 0。绝大多数情况下，下面的新 code 片段是最佳的，但是理解两种方法是最好的。

```C#
[Replicate]
private void MovePlayer(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{   
    //在 future，简单将 velocities 设置为 0 并退出方法，阻止任何 input 检查逻辑。
    //使用这个方法会允许 objects 仍然和这个 rigidbody 碰撞。
    if (state.IsFuture())
    {
        _myPredictionRigidbody.Velocity(Vector3.Zero);
        _myPredictionRigidbody.AngularVelocity(Vector3.Zero);
        return;
    }
    
    float horizontal = data.Horizontal;
    
    Vector3 movement = new(horizontal, 0f, 0f);
    
    _predictionRigidbody.AddVelocity(movement);
    _predictionRigidbody.Simulate();
}
```

## Predicting States In Code

由于 Internet 的不可预测性，inputs 可能丢失或迟到。Predicting states 是补偿这种事件的非常简单的方式。

如果游戏是快节奏和基于 reaction 的，甚至不使用物理的，predicting states 可以用于在你实际从 server 接收到 inputs 之前预测它们。

Server 和 Client 都可以预测 inputs。

Server 可能预测 inputs 来补偿不可靠连接的 clients。Clients 可以预测它们没有 ownership 的 objects 上的 input，通常称之为 “spectated objects”。

通过预测 inputs，你可以在 future 放置 objects，只要你知道它们在哪里，甚至使它们对 client 完全实时的。但是记住，当 predicting future 时，如果你猜错了，在 reconcile 进行修正时，将会有一个 de-synchronization，这可能会看见一个抖动（一个物体突然闪现又消失）。

下面是一个简单的 replicate 方法：

```C#
//What data does is irrelevant in this example.
//We're only interested in how to predict a future state.
[Replicate]
private void RunInputs(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{ 
    float delta = (float)base.TimeManager.TickDelta;
    transform.position += new Vector3(data.Horizontal, 0f, data.Vertical) * _moveRate * delta;
}
```

在更深入之前，你必须理解每个 ReplicateState 是什么。它们基于 input 是否已知、是否 replaying inputs，以及其他信息而改变。

如果你不能完全理解这些状态，后面会变得更清晰。

CurrentCreated 只能在对 object 拥有 ownership 的 clients 上可见。当 inputs 在 spectated objects（没有 ownership 的 objects）上收到时，clients 在 reconcile 运行它们，那里的状态将是 ReplayedCreated。Clients 还会再 spectated objects 上看见 ReplayedFuture 和 CurrentFuture。

以 Future 结尾的 state 基本意味着 input 还没有收到，这些是你可以进行 predict 的状态。

假设你的游戏中玩家有较高概率会定期朝同一方向移动。如果 player 连续 3 个 tick 按着 forward control，input 看起来就像：

```
(data.Vertical == 1)
(data.Vertical == 1)
(data.Vertical == 1)
```

但是如何其中一个 input 没有到达或迟到了怎么办？input 完全不到达的几率几乎不存在，但是因为网络问题迟到则极为常见。如果 input 迟到了，看起来就像这样：

```
(data.Vertical == 1)
(data.Vertical == 1)
(data.Vertical == 0) //Didn't arrive here, but will arrive late next tick. 没有 input 时，使用 default
(data.Vertical == 1) //This was meant to arrive the tick before, but arrived late.
```

因为这些中断，player 可能看见向前移动两次，然后暂停，然后再次向前移动。

为解决上述问题，实际开发中通常会在 NetworkObject 的预测设置下，对 graphic object 启用插值处理，以平衡物体运动。

- 核心逻辑：通过插值算法（如线性插值、样条插值）填补网络延迟或预测误差导致的状态空白，使物体移动看起来连续自然
- 实现方式：
  - 在NetworkObject组件中，找到Prediction Settings（预测设置），启用Interpolation（插值）功能
  - 配置插值参数，例如插值时间间隔、缓动曲线等，以适配游戏的具体需求
- 适用场景：
  - 多人游戏中非本地玩家的移动同步（如队友、NPC的平滑移动）
  - 需要平衡实时性与流畅性的场景，避免因网络抖动导致的“瞬移”或“卡顿”

PredictionManager 还提供了 QueuedInputs，可进一步提供缓冲。但为便于说明，本指南将假设这些功能未满足需求，需自行处理延迟输入。

下面是跟踪和使用已知 inputs 创建 predicted 的一种简单方法。

```C#
private ReplicateData _lastCreatedInput = default;

[Replicate]
private void RunInputs(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{ 
    //如果 inputs 未知，你可以在 CurrentFuture 一直预测。这对 client 将是实时的。
    //尽管你对 future 预测的越多，越容易预测错误
    if (state.IsFuture())
    {
        uint lastCreatedTick = _lastCreatedInput.GetTick();
        //如果距离最后创建的 input 只有 2 个 ticks，将会运行下面的逻辑。
        //这基本意味着如果最后创建的 tick 是 100，这个逻辑将会在小于等于 102 tick 的 future 时间段内运行。
        //这是一个只预测一定数量 inputs 的基本例子。
        uint thisTick = data.GetTick();
        if ((data.GetTick() - lastCreatedTick) <= 2)
        {
            //我们可能不想预测所有状态。
            //例如，在一个 row 内预测多个 jumps 可能没有意义。
            //这个例子中，只有 movement inputs 是预测的。
            data.Vertical = _lastCreatedInput.Vertical;
        }
    }
    //如果 data 是 created 的，将其设置为 lastCreatedInput。
    else if (state == ReplicateState.ReplayedCreated)
    {
        //如果 ReplicateData 包含可能生成 garbage 的 fields，你可能想要在替换 lastCreatedInput 之前 dispose 它
        //这个步骤是可选的
        _lastCreatedInput.Dispose();
        //将 data 设置为 lastCreatedInput
        _lastCreatedInput = data;
    }
    
    float delta = (float)base.TimeManager.TickDelta;
    transform.position += new Vector3(data.Horizontal, 0f, data.Vertical) * _moveRate * delta;
}
```

如果你分配了 ReplicateData，不用忘了在网络停止时 dispose lastCreatedInput。
