SyncStopwatch 是一种高效的服务器与客户端间秒表同步方案。

与 SyncTimer 类似，SyncStopwatch 仅同步启动或停止等状态变更，而非逐帧的细微变化。

```C#
private readonly SyncStopwatch _timePassed = new()
```

修改计时器非常简单，但与其他SyncType一样，**相关操作必须在服务器端完成**。

```C#
//All of the actions below are automatically synchronized.

/* Starts the stopwatch while optionally sending a stop
 * message first if stopwatch was already running.
 * If the stopwatch was previously running the time passed
 * would be reset. */
/* This would invoke callbacks indicating a stopwatch
 * had stopped, then started again. */
_timePassed.StartStopwatch(true);
/* Pauses the stopwatch and optionally sends the current
 * timer value as it is on the server. */
_timePassed.PauseStopwatch(false);
//Unpauses the current stopwatch.
_timePassed.UnpauseStopwatch();
/* Ends the Stopwatch while optionally sends the
* current value to clients, as it was during the stop. */
_timePassed.StopStopwatch(false);
```

更新和读取 timer 的值非常类似常规 normal float value。

```C#
private void Update()
{
    /* Like SyncTimer, SyncStopwatch must be updated
     * with a delta on both server and client. Do not
     * update the delta twice if clientHost. You can update
     * the delta anywhere in your code. */
    _timePassed.Update(Time.deltaTime);

    //Access the current time passed.
    Debug.Log(_timePassed.Elapsed);
    /* You may also see if the stopwatch is paused before
     * accessing elapsed. */
    if (!_timePassedPaused)
        Debug.Log(_timePassed.Elapsed);
}
```

就像 SyncTypes，你可以订阅 SyncStopwatch 的 change events。

```C#
private void Awake()
{
    _timePassed.OnChange += _timePassed_OnChange;
}

private void OnDestroy()
{
    _timePassed.OnChange -= _timePassed_OnChange;
}

private void _timePassed_OnChange(SyncStopwatchOperation op, float prev, bool asServer)
{
    /* Like all SyncType callbacks, asServer is true if the callback
     * is occuring on the server side, false if on the client side. */

    //Operations can be used to be notified of changes to the timer.
    //This is much like other SyncTypes.
    //Here is an example of performing logic only if starting or stopping.
    if (op == SyncStopwatchOperation.Start || op == SyncStopwatchOperation.Stop)
    {
        //Do logic.
    }
    
    /* prev, our float, indicates the value of the stopwatch prior to
     * the operation. Remember that you can get current value using
     * _timePassed.Elapsed */
}
```

## 与 SyncTimer 的区别（AI）

在Unity FishNet中，SyncTimer和SyncStopwatch都是用于时间同步的工具，但它们的用途和工作方式有所不同。

SyncTimer通常用于​​基于tick的时间同步系统​​，它与FishNet的TimeManager配合，处理网络计时、服务器与客户端之间的时间同步，以及对客户端预测计时的支持等功能，主要用于维护整个网络的时间基准，确保不同客户端和服务器的时间一致性，常用于需要严格时间同步的网络操作，如同步游戏中的关键事件、状态更新等。

SyncStopwatch则更侧重于​​测量特定代码段或操作的运行时间​​，例如在处理网络消息、执行同步逻辑或进行性能优化时，用于测量某段代码的执行时长，帮助开发者了解代码的性能瓶颈，以便进行优化，它更关注于局部的时间测量和分析。

