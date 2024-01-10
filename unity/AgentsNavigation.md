# Agents Navigation

Agents Navigation 提供高性能，模块化，大规模的 agent 导航。

它以 DOTS 开发。因此它利用了 Unity 最新的技术，例如 SIMD 数学库，Jobs，Burst 编译器，和 EntityComponentSystem。此外，它还支持 hybrid 模式，用于支持 GameObject 面向对象编程。

Navigation 的一个很大问题时，没有一种解决方案适用于所有游戏。因此这个 package 不提供通用的解决方案，而是提供一个 agent navigation 的基础，用于进一步定制化以满足实际需求。

## GameObjects

因为这个 package 设计为模块化，因此绝大多数 navigation behaviors 跨越很多组件。所有组件只包含 authoring data，没有其他逻辑。Agent 组件内部创建一个 entity 并与它进行数据同步。

### Agent

Agent 是主要组件，它标记 GameObject/Entity 为 Agent。参与 navigation 的所有东西都被认为是一个 Agent，不论它是动态 GameObject，还是仅仅是静态的 obstacle。

Agent type 被设置为 Default Locomotion，它还包含默认的 Locomotion，Seeking，和 Arrival。这会让 agent seek 它的 destination，并向其移动。

### Shape

- Agent Cylinder Shape

  Cylinder shape 指示 agent 应该在 Y 轴向上的 3d 场景模拟。

- Agent Circle Shape

  Circle shape 指示 agent 应该在 Z 轴向上的 2d 场景中模拟。

### Avoidance

Avoidance 是 navigation 的核心。它用于避开障碍物和其他 agents。需要理解的很重要一点是 avoidance 依赖于试探，并且没有完美方案。有可能 agent 完全没法彼此避免，有可能再尝试彼此避免时陷入一个循环。还有，要明白 avoidance 不是 pathing 的替换。相反，它是 pathing 的补充，在 agent 沿着 path 前进同时躲避 obstacles 和 agents。

- Agent Sonar Avoid

  这个组件允许使用 Sonar Avoidance 在接近的 agents 之间进行 avoidance。它实现了 Local Avoidance package。

  这个 behavior 与 RVO 和 ORCA 算法类似，并解决相似的问题。主要区别是 Sonar Avoidance 更关注个体的表现，而不是整个 group 的表现。因此它能体现出包围 target 的行为，这是在 game 中高度追求的效果。

- Agent Separation

  这个组件开启分离行为。它是非常轻量的算法，并对不需要高质量 avoidance 的游戏非常合适。

### Pathing

Pathing 是一个系统，允许在场景中的两个点之间找到一条 path。还被 AI 系统使用，用来找到到 target 的一条路径。

- Agent NavMesh Pathing

  这个组件允许 agents 使用 Unity 内置的 NavMesh 系统。

- Agent Crowd Pathing

  这个组件指定 agent 属于哪个 crowds group，并使用它的 crowd flow 进行 navigation。

### Collider

这个组件在 agents 之间开启 collisions。它是 avoidance 算法非常有用的补充，因为 avoidance 并不总是产生完美结果。它不使用 Unity 的 physics 系统，而是使用自定义的解决办法。

### Smart Stop

这个组件允许 agent 更智能的决策 agents 何时停下。

- Hive Mind Stop

  这个行为是 group-based 的，即在 Group 中的所有 agents 停下来时，agent 尝试停下来。它可以有效地处理一个 group 尝试向一个方向移动的场景。每一帧，agent 会检查它周围的 idle agents 来查看它的目标是否和它自己的相似。如果是，则停下来。

- Give Up Stop

  允许 agent 更智能地决定它是否卡住了。每次 agent 撞到一个站立的 agent，它会 progress 停下来。如果没有撞到，则会从停止恢复。一旦达到 progress value，agent 就会停下来。

## Settings

这个 package 的 setting 在 Project Settings 窗口的 Agents Navigation。

要改变设置，创建一个 scriptable object Agents Navigation Settings。

- Custom Sub Settings

  Agents Navigation settings 可以以 additional sub settings 扩展。

  ```C#
  [Serializable]
  class MySubSettings : ISubSettings
  {
      public int Value = 1;
  }
  
  ...
  
  int myValue = AgentsNavigationSettings.Get<MySubSettings>().Value;
  ```

## Crowds

这是 NavMesh pathing 的代替方案，来自扩展包 Agents Navigation - Crowds。它基于 continuum crowds，agents 使用 flow fields 进行导航。

Flow field 是一个 grid-based graph。一个关键的区别是 agent 的 steering velocity 不是逐 agent 计算的，而是逐 grid cell 计算的：

- 性能消耗与 grid size 乘以 group count 成比例，而不是仅 agent count。这允许 huge crowds，并消耗很少的性能。
- Pathing 和 avoidance 是联合使用的，可以极大减少 agent 由于 local avoidance 而卡住的场景。
- 每个 agent group 必须共享相同的目标，这意味如果有太多的 group 性能会很快地下降（越接近目标，agent 之间的 local avoidance 越频繁）。
- Agents 可以展示非常良好的 huge crowds 效果，但是同时 agents 也失去了独立性，并遵循 group 的 flow 而不是它们自己的。

- Crowd Surface：agents 的 walkable surface
- Crowd Group：特定 particular surface 上的一个 agents group
- Agent Crowd Pathing：agent 从属的 group，指示它应该参与的 crowd flow

### Crowd Surface

### Crowd Group

### Crowd Agent

### Crowd Obstacle

### Crowd Discomfort

## Sonar Avoidance

Agent Sonar Avoid 组件是基于 Local Avoidance 2.0 package 的。

Local avoidance 使用创新的解决方案，称为 SonarAvoidance。它的想法非常简单。Interest point 构造一个 circle 内的 sonar volume，它扫描附件的 obstacles。每个 obstacle cut into 这个 volume。一旦所有的 obstacles 被扫描，则从它计算最佳方向

。这个方案被设计为轻量的，使得它可以移动到任何设计中。这样整个功能被包含到单个 struct，称为 SonarAvoidance。

- Constructor

  Sonar 可以使用简单的构造函数创建：

  ```C#
  var sonar = new SonarAvoidance(position, direction, up, innerRadius, outerRadius, speed);
  ```

- Circular Obstacle

  Circular shape obstacles 通常用于其他 agents。

  ```C#
  bool success = sonar.InsertObstacle(obstaclePosition, obstacleVelocity, obstacleRadius);
  ```

- Directional Obstacle

  Directional shape obstacles 通常用于 vision 受限的 agent。

  ```C#
  bool success = sonar.InsertObstacle(obstacleDirection, obstacleRadius);
  ```

- Cleanup

  如果想下一帧重用 structure，调用 sonar.Clear()，否则直接销毁，调用 sonar.Dispose()。

## Tutorials

### Modify Hybrid Property

因为 hybrid workflow 内部运行 entities 用于模拟，与它的属性的运行时交互和 entity logic 紧密捆绑。每个 authoring components（hybrid mono component）有它们对应的 entity 组件的 getter，setter。通常 property name 以 Entity 前缀开始。

- Speed

  ```C#
  var agent = GetComponent<AgentAuthoring>();
  var locomotion = agent.EntityLocomotion; // Reads locomotion value into a copy
  locomotion.Speed = 10.0f; // Modifies the copy
  agent.EntityLocomotion = locomotion; // Writes back the locomotion value
  ```

### Set Destination

#### GameObjects

- 使用 GameObject > AI > Agent Cylinder 菜单，创建一个 gameobject
- 创建一个脚本，例如 AgentSetDestination.cs，将它挂载到 agent gameobject

  ```C#
  using UnityEngine;
  using ProjectDawn.Navigation.Hybrid;
  
  public class AgentSetDestination : MonoBehaviour
  {
      public Transform Target;
      void Start()
      {
          GetComponent<AgentAuthoring>().SetDestination(Target.position);
      }
  }
  ```

创建另一个 gameobject，用作 target。然后，点击 play，agent 就会向 target 移动。

这种最小 setup 只会包含 steering behavior，不包含任何 avoidance。

#### Other Behaviors

要添加额外行为到 agent，只需要将它们作为组件添加到 gameobject 上即可：

- Agent Collider：这个组件开启 agents 之间的 collisions
- Agent Sonar Avoid：这个组件允许使用 Sonar Avoidance solution 邻近 agents 之间的 avoidance
- Agent Nav Mesh：这个组件允许 agent 使用 Unity Nav Mesh 进行导航

#### Entities Sub-Scene

### NavMesh Setup

- 创建 NavMeshSurface。这是 agent 的 walkable surface area。
- 创建一个 NavMesh Agent，添加 Agent NavMesh Pathing 组件
- 设置 target，GetComponent\<AgentAuthoring\>().SetDestination(Target.position);

### Crowds Setup

### Custom Locomotion

