# Advanced Controls

这个 guide 补充基础 prediction guide，展示如何为你的控制引入更多复杂性。

## Guide Goal

为 prediction 实现更多功能，就像你会在单人游戏里那样编码一样，只要记住 reconcile 任何可能 de-synchronzie prediction 的东西。

这个 guide，会添加一个 jump 前的虚拟地面检查，冲刺（sprint）也是一样。

## Sprinting and Ground Checks

首先，ReplicateData 需要更新，以包含 sprint action，这会需要一个耐力机制。只需要添加一个 Sprint bool 变量即可。

```C#
public struct ReplicateData : IReplicateData
{
    public bool Jump;
    public bool Sprint;
    public float Horizontal;
    public float Vertical;
    public ReplicateData(bool jump, bool sprint, float horizontal, float vertical) : this()
    {
        Jump = jump;
        Sprint = sprint;
        Horizontal = horizontal;
        Vertical = vertical;
    }

    private uint _tick;
    public void Dispose() { }
    public uint GetTick() => _tick;
    public void SetTick(uint value) => _tick = value;
}
```

然后，在创建 ReplicateData 时，需要 poll sprint 的值，就像绝大多数游戏那样。

```C#
private ReplicateData CreateReplicateData()
{
    if (!base.IsOwner)
        return default;

    //Build the replicate data with all inputs which affect the prediction.
    float horizontal = Input.GetAxisRaw("Horizontal");
    float vertical = Input.GetAxisRaw("Vertical");

    /* Sprint if left shift is held.
    * You do not necessarily have to perform security checks here.
    * For example, it was mentioned sprint will rely on stamina, we
    * are not checking the stamina requirement here. You certainly could
    * as a precaution but this is only building the replicate data, not where
    * the data is actually executed, which is where we want
    * the check. */
    bool sprint = Input.GetKeyDown(KeyCode.LeftShift);
    
    ReplicateData md = new ReplicateData(_jump, sprint, horizontal, vertical);
    _jump = false;

    return md;
}
```

在类中声明一个 stamina float（耐力）。

```C#
private float _stamina;
```

现在使用新的 Sprint bool 和 stamina 字段，在 replicate 方法中应用 sprinting。

```C#
[Replicate]
private void RunInputs(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{
    float delta = (float)base.TimeManager.TickDelta;
    //以每秒 3f 的速率重新生成 stamina。
    _stamina += (3f * delta);
    //每个 delta 使用 sprint 消耗的 stamina。
    //这会导致 sprint 使用 stamina recharge 速度两倍的 stamina。
    float sprintCost = (6f * delta);
    Vector3 forces = new Vector3(data.Horizontal, 0f, data.Vertical) * _moveRate;
    //如果按下了 sprint，并有足够的 stamina，则倍乘 forces。
    if (data.Sprint && _stamina >= sprintCost)
    {    
        //Reduce stamina by cost.
        _stamina -= sprintCost;
        //Increase forces by 30%.
        forces *= 1.3f;
    }
    
    //你应该在 replicate 中检查任何 changes，就像对 stamina 所做的那样。
    //回忆一下，之前提到在 gather input 时检查耐力（stamina）并不重要，
    //但在 replicate 中进行此操作可赋予服务器权威性，同时确保预测功能在修正和回滚时正常运行。

    //现在检查是否 jump。IsGrounded() 函数并不存在，这里假设它存在，并使用 raycast 或 overlap 检测是否在地面上。
    if (data.Jump && IsGrounded())
    {
        Vector3 jmpFrc = (Vector3.up * _jumpForce);
        PredictionRigidbody.AddForce(jmpFrc, ForceMode.Impulse);
    }
    
    //Rest of the code remains the same.
}
```

如果一个 value 可能影响你的 prediction，不要将它存储在 replicate method 之外，除非你还 reconciling 这个 value。但是如果你在 replicate 方法中设置这个 value，则适用于例外情况。

这是一个非常重要的细节。

只 Reconciling 一个 rigidbody state 非常简单。

```C#
[Reconcile]
private void ReconcileState(ReconcileData data, Channel channel = Channel.Unreliable)
{
    //Call reconcile on your PredictionRigidbody field passing in
    //values from data.
    PredictionRigidbody.Reconcile(data.PredictionRigidbody);
}
```

如果使用了多个 Rigidbody，至少还需要 reconcile 它们的状态。你可以通过为每个 rigidbody 添加一个 RigidbodyState 并将其纳入 reconcile 流程来快速实现这一点。  

如果你还为这些 rigidbody 施加了力，确保使用 PredictionRigidbody 来处理它们，并 reconcile PredictionRigidbody 而非 RigidbodyState。

## Changes To Reconcile

由于对象可能 reconcile 到之前的状态，因此 reconcile 任何存储在 Replicate 方法之外的值也至关重要。

试想：若你拥有 10 点耐力（足够冲刺），且在服务器和本地角色上成功执行了冲刺动作；冲刺后耐力仅剩 1 点，不足以继续冲刺。  

若 reconcile 时未将耐力重置为之前的值，那么 reconcile 后你的耐力仍将停留在 1 点。此时，之前能触发冲刺的输入重放将因耐力不足而无法执行冲刺动作。这将导致不同步现象，通常表现为角色抖动。  

幸运的是，在预测逻辑中纳入更多变量非常简单——你只需更新 reconcile 逻辑，使其包含状态或新增的变量值即可。  

我们在 ReconcileData 结构体中新增了一个 Stamina 浮点数字段。

```C#
public struct ReconcileData : IReconcileData
{
    public PredictionRigidbody PredictionRigidbody;
    public float Stamina;
    
    public ReconcileData(PredictionRigidbody pr, float stamina) : this()
    {
        PredictionRigidbody = pr;
        Stamina = stamina;
    }

    private uint _tick;
    public void Dispose() { }
    public uint GetTick() => _tick;
    public void SetTick(uint value) => _tick = value;
}
```

当然，我们必须在创建的 reconcile data 中包含 stamina 的当前值。

```C#
public override void CreateReconcile()
{
    ReconcileData rd = new ReconcileData(PredictionRigidbody, _stamina);
    ReconcileState(rd);
}
```

最后的最后，你必须使用新的 reconcile data 重置 stamina state。

```C#
[Reconcile]
private void ReconcileState(ReconcileData data, Channel channel = Channel.Unreliable)
{
    PredictionRigidbody.Reconcile(data.PredictionRigidbody);
    _stamina = data.Stamina;
}
```

只需对代码稍作修改，你现在就拥有了一个权威的地面检测机制和基于耐力的冲刺系统。

## Note

Fishnet 中是否：

- 所有客户端保持预测移动等不是那么重要的方面（但只在很少 ticks 内）
- 控制器客户端把重要 input 发送给 server，只有 server 运行，它自己和其他非控制器 clients 同样只向 future 预测，一样等待 server 的权威数据，一样进行 reconcile
- 只要保证控制器客户端发送 input 和 server 返回权威数据的间隔足够短，玩家就感受不到延迟
- 控制器客户端可以预测执行 graphical 动作（例如运动、开火），但是权威数据（子弹数量、是否命中）只等待 server 端返回权威数据 reconcile
- 测试时注意检查，replicate 是否只在 server 执行，还是也会在 clients 执行