# Description

NavMeshCharacter 组件通过组合扩展了 Character，集成了 NavMesh-based navigation。这可以让 Character 在世界中智能导航。

这个组件替换了之前版本（ECM）的 AgentCharacter。

# Properties

- NavMeshAgent agent：缓存的 NavMeshAgent 组件

- Character character：缓存的 Character 组件

- bool autoBraking：agent 是否自动 brake，以避免在目标 point overshoot

- float brakingDistance：开始 braking 到目标点的距离

- float brakingRatio

  Agent 到目标的剩余距离与开始 braking distance 的百分比，ratio（0-1）。

  如果没有 auto braking，或者 agent 的剩余距离大于 brakingDistance，ratio = 1。

  如果 agent 的剩余距离小于 brakingDistance，ratio 小于 1。

- float stoppingDistance

  距离目标位置的距离小于这个阈值时停止。

# Methods

- virtual bool HasPath()

  Agent 当前是否有一个 path。

- virtual bool IsPathFollowing()

  Agent 是否正在跟随一个 path。

/// <summary>
/// Returns the destination set for this agent.
/// If a destination is set but the path is not yet processed,
/// the returned position will be valid navmesh position that's closest to the previously set position.
/// If the agent has no path or requested path - returns the agents position on the navmesh.
/// If the agent is not mapped to the navmesh (e.g. Scene has no navmesh) - returns a position at infinity.
/// </summary>
        
- virtual Vector3 GetDestination()

  返回为这个 agent 设置的 distination。

  如果设置了 distination，但是没有处理 path，返回的 position 会是一个有效的 navmesh 位置，它接近设置的 postion 的最近 valid position。

  如果 agent 没有 path 或没有请求 path，返回 navmesh 上的 agent 的位置。

  如果 agent 没有映射到 navmesh（例如 Scene 没有 navmesh），返回 infinity position。

- virtual void MoveToDestination(Vector3 destination)

  请求 Character 移动到给定 destination 最近的 navmesh position。

- virtual void PauseMovement(bool pause)

  暂停/恢复 Character path 跟随运动。

  如果为 True，character 的运动会沿着它的当前 path 停止。

  如果 character 停下来之后，设置为 False，则恢复沿着当前 path 移动。

- virtual void StopMovement()

  停止 Character 沿着当前 path 移动。

  这会清空 agent 的当前 path。

# Events

- event DestinationReachedEventHandler DestinationReached;

  当 agent 到达目标位置时，触发的事件。
