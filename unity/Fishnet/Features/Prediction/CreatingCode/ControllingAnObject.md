# Controlling An Object

如何创建一个 owner 或 server 可以控制的 predicted object。

## Data Structures

实现预测需通过创建​​复制（Replicate）​​和​​调和（Reconcile，校准）​​方法，并按需调用它们：

​​- 复制方法​​ Replicate：接收需在所有者（Owner）、服务器及客户端（若使用状态转发）执行的输入，如跳跃、冲刺、移动方向等控制指令，甚至包含开火等机制。
​​- 调和方法​​ Reconcile：在复制操作后接收对象状态，用于修正可能的数据不同步问题，例如同步生命值、速度、位置及旋转等属性。

此外，若需在结构体中分配资源，建议使用 ​​Dispose 回调​​，该回调会在数据被丢弃时自动执行清理操作。

以下是包含刚体基础机制的两个结构体示例。

```C#
public struct ReplicateData : IReplicateData
{
    public bool Jump;
    public float Horizontal;
    public float Vertical;
    public ReplicateData(bool jump, float horizontal, float vertical) : this()
    {
        Jump = jump;
        Horizontal = horizontal;
        Vertical = vertical;
    }

    private uint _tick;
    public void Dispose() { }
    public uint GetTick() => _tick;
    public void SetTick(uint value) => _tick = value;
}

public struct ReconcileData : IReconcileData
{
    //PredictionRigidbody is used to synchronize rigidbody states
    //and forces. This could be done manually but the PredictionRigidbody
    //type makes this process considerably easier. Velocities, kinematic state,
    //transform properties, pending velocities and more are automatically
    //handled with PredictionRigidbody.
    public PredictionRigidbody PredictionRigidbody;
    
    public ReconcileData(PredictionRigidbody pr) : this()
    {
        PredictionRigidbody = pr;
    }

    private uint _tick;
    public void Dispose() { }
    public uint GetTick() => _tick;
    public void SetTick(uint value) => _tick = value;
}
```

## Preparing To Call Prediction Methods

通常建议在 OnTick 中执行复制（Replicate）或输入处理。是否在 OnPostTick 发送调和（Reconcile）取决于是否使用 Physics Bodies：  

- 使用 physics bodies（如刚体）：需在 OnPostTick 发送调和，以确保在物理模拟完成后同步状态。  
- 非物理控制器：可直接在OnTick发送调和，无需等待物理模拟。  

具体实现可参考 TimeManager API 中关于 Tick 和物理事件回调的说明。

你可能需要根据你的 rigidbody 的 shape，drag，mass 修改 move 和 jump forces。

```C#
//How much force to add to the rigidbody for jumps.
[SerializeField]
private float _jumpForce = 8f;
//How much force to add to the rigidbody for normal movements.
[SerializeField]
private float _moveForce = 15f;
//PredictionRigidbody is set within OnStart/StopNetwork to use our
//caching system. You could simply initialize a new instance in the field
//but for increased performance using the cache is demonstrated.
public PredictionRigidbody PredictionRigidbody;
//True if to jump next replicate.
private bool _jump;

private void Awake()
{
    PredictionRigidbody = ObjectCaches<PredictionRigidbody>.Retrieve();
    PredictionRigidbody.Initialize(GetComponent<Rigidbody>());
}
private void OnDestroy()
{
    ObjectCaches<PredictionRigidbody>.StoreAndDefault(ref PredictionRigidbody);
}
public override void OnStartNetwork()
{
    base.TimeManager.OnTick += TimeManager_OnTick;
    base.TimeManager.OnPostTick += TimeManager_OnPostTick;
}

public override void OnStopNetwork()
{
    base.TimeManager.OnTick -= TimeManager_OnTick;
    base.TimeManager.OnPostTick -= TimeManager_OnPostTick;
}
```

## Calling Prediction Methods

对于这个 demo，下面是如何为 replicate 和 reconcile 收集输入：

Update 用于收集单帧发出的 input（例如按键按下、释放）。Ticks 不会每个 frame 都执行，而是以 TickDelta 时间间隔执行，就像 FixedUpdate 一样。

虽然下面的代码只使用 Update 收集单帧 inputs，但是没有什么阻止你也用它收集 hold inputs（持续按键）。

```C#
private void Update()
{
    if (base.IsOwner)
    {
        if (Input.GetKeyDown(KeyCode.Space))
            _jump = true;
    }
}
```

现在 OnTick 将用来构建 Replicate 数据。不需要一个单独的 CreateReplicateData 方法来创建数据，但是这可以让你的代码更有组织。

当尝试创建 replicate data 时，如果不是 object 的所有者，返回 default。

Server 接收来自 owner 的输入并运行，因此 server 不需要创建数据，而对非 object owner 的客户端，它从 server 接收输入，就像使用 state forwarding 时其他客户端转发的一样。如果不使用 state forwarding，此情景下也会使用 default input，但是 clients 不会在 non-owned objects 上运行 repliates。如果没有 owner，也可以在 server 上运行 inputs，对此，使用 base.HasAuthority 最好。

```C#
private void TimeManager_OnTick()
{
    RunInputs(CreateReplicateData());
}

private ReplicateData CreateReplicateData()
{
    if (!base.IsOwner)
        return default;

    //Build the replicate data with all inputs which affect the prediction.
    float horizontal = Input.GetAxisRaw("Horizontal");
    float vertical = Input.GetAxisRaw("Vertical");
    ReplicateData md = new ReplicateData(_jump, horizontal, vertical);
    _jump = false;

    return md;
}
```

现在实现 replicate 方法。名字可以是任意的，但是参数必须是如下所示的那样。第一个是传递的 input data，其他参数是框架在运行时自动填入。但是你仍然可以改变参数中使用的 default channel，甚至是在运行时。

```C#
[Replicate]
private void RunInputs(ReplicateData data, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
{
    /* ReplicateState 基于 data 是新的设置，例如 replayed 等待。
     * 查看 ReplicateState enum 获取更多信息
     */
    
    /* 确保总是使用 PredictionRigidbody 设置和应用 velocities，
     * 绝不应该使用 rigidbody。这包括从其他脚本访问的情况。
     */
    Vector3 forces = new Vector3(data.Horizontal, 0f, data.Vertical) * _moveRate;
    PredictionRigidbody.AddForce(forces);

    if (data.Jump)
    {
        Vector3 jmpFrc = new Vector3(0f, _jumpForce, 0f);
        PredictionRigidbody.AddForce(jmpFrc, ForceMode.Impulse);
    }

    /* 添加重力让 object 下落更快。当然这是可选的 */
    PredictionRigidbody.AddForce(Physics.gravity * 3f);

    /* 模拟添加的 forces。通常你在 replicate 末尾调用这个 Simulate 方法。
     * 调用 Simulate 最终告诉 PredictionRigidbody 来 iterate 上面添加的 forces。
     */
    PredictionRigidbody.Simulate();
}
```

```
在 non-ownered objects 上，大量 replicates 会以 ReplicateState.Created 到达，但是会包含默认值。这是 PredictionManager.RedundancyCount 功能的工作。
这是正常的，指示 client 或 server 已经 gracefully 停止发送状态，因为没有新的数据发送。如果你使用 Predicting States，这非常有用。
```

现在 reconcile（校准）必须发送给 clients，来执行修正。虽然只有 server 会发送 reconcile，但是无论是 client，server，owner 还是 non-owner，确保调用 CreateReconcile。这是为了给即将推出的功能提供未来兼容性保障。不像 CreateReplicateData 方法，使用 CreateReconcile 不是可选的。

```C#
private void TimeManager_OnPostTick()
{
    CreateReconcile();
}

//Create the reconcile data here and call your reconcile method.
public override void CreateReconcile()
{
    /*
     * 必须将 rigidbody 的 state 发送回去。使用 reconcile data  中的 PredictionRigidbody 字段可以很容易地实现。
     * 更高级的状态，可能需要发送其他的值，后面会介绍。
     */
    ReconcileData rd = new ReconcileData(PredictionRigidbody);

    /* 就像 replicate 一样，你可以指定一个 channel，但是对 reconcile 这通常不会 */
    ReconcileState(rd);
}
```

Reconcile 校准在客户端上执行。

只 Reconciling 一个 rigidbody state 非常简单：

```C#
[Reconcile]
private void ReconcileState(ReconcileData data, Channel channel = Channel.Unreliable)
{
    /* 只需要在 PredictionRigidbody 上调用 reconcile，并传递 data 中的值 */
    PredictionRigidbody.Reconcile(data.PredictionRigidbody);
}
```

这里 ReconcileData 只包含了 PredictionRigidbody，看起来将 PredictionRigidbody 包含在其中有点多余，但真实场景可能包含更多需要 reconcile 的数据。
