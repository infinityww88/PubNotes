# Non-Controlled Object

一个非常简单的脚本，使用 Prediction System 保持 non-controlled objects 同步。

很多游戏需要 physics bodies 联网（在网络上保持同步），即使不是被 player 或 server 控制的那些。这些 objects 也可以和新的 state system 一起工作，通过添加一个基础的 prediction script 到它们上面。

值得注意的是你还可以通过使用 base.HasAuthority 控制 server 上的 non-owned objects。

因为 rigidbody 是仅响应的 reactive-only，因此不需要 polling input。否则你会发现数据结构几乎与采集 input 的数据结果一模一样。

```C#
public class RigidbodySync : NetworkBehaviour
{
    //Replicate structure.
    public struct ReplicateData : IReplicateData
    {
        //The uint isn't used but Unity C# version does not
        //allow parameter-less constructors we something
        //must be set as a parameter.
        public ReplicateData(uint unused) : this() {}
        private uint _tick;
        public void Dispose() { }
        public uint GetTick() => _tick;
        public void SetTick(uint value) => _tick = value;
    }
    //Reconcile structure.
    public struct ReconcileData : IReconcileData
    {
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

    //Forces are not applied in this example but you
    //could definitely still apply forces to the PredictionRigidbody
    //even with no controller, such as if you wanted to bump it
    //with a player.
    private PredictionRigidbody PredictionRigidbody;
    
    private void Awake()
    {
        PredictionRigidbody = ResettableObjectCaches<PredictionRigidbody>.Retrieve();
        PredictionRigidbody.Initialize(GetComponent<Rigidbody>());
    }
    private void OnDestroy()
    {
        ResettableObjectCaches<PredictionRigidbody>.StoreAndDefault(ref PredictionRigidbody);
    }

    //In this example we do not need to use OnTick, only OnPostTick.
    //Because input is not processed on this object you only
    //need to pass in default for RunInputs, which can safely
    //be done in OnPostTick.
    public override void OnStartNetwork()
    {
        base.TimeManager.OnPostTick += TimeManager_OnPostTick;
    }

    public override void OnStopNetwork()
    {
        base.TimeManager.OnPostTick -= TimeManager_OnPostTick;
    }

    private void TimeManager_OnPostTick()
    {
        RunInputs(default);
        CreateReconcile();
    }

    [Replicate]
    private void RunInputs(ReplicateData md, ReplicateState state = ReplicateState.Invalid, Channel channel = Channel.Unreliable)
    {
        //If this object is free-moving and uncontrolled then there is no logic.
        //Just let physics do it's thing.	
    }

    //Create the reconcile data here and call your reconcile method.
    public override void CreateReconcile()
    {
        ReconcileData rd = new ReconcileData(PredictionRigidbody);
        ReconcileState(rd);
    }

    [Reconcile]
    private void ReconcileState(ReconcileData data, Channel channel = Channel.Unreliable)
    {
        //Call reconcile on your PredictionRigidbody field passing in
        //values from data.
        PredictionRigidbody.Reconcile(data.PredictionRigidbody);
    }
}
```