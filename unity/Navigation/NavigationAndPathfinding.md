# Navigation and Pathfinding

导航系统允许角色在世界中智能地移动，通过使用 navmesh，它基于 scene 中 geometry 自动创建。

动态障碍 允许在运行时修改角色的导航，而 off-mesh links 允许构建特定的动作，例如开门或者从一个 ledge 上跳下。

## 系统组件

- NavMesh：数据结构，描述 game world 的 walkable surfaces，允许从一个 walkable location 到另一个查询路径。NavMesh 从 scene geometry 自动构建
- NavMesh Agent：创建角色，在移动向目标时彼此避免碰撞。Agent 使用 NavMesh 理解世界，并知道如何彼此避免碰撞，以及避开障碍物
- Off-Mesh Link：navigation shortcuts，不能通过 walkable surface 表示。它描述两个 locations，locations 在 NavMesh 是不相连的，但是 Off-Mesh Link 在它们之间创建了一个短路
- NavMesh Obstacle：描述移动的障碍物，agent 在导航时将会避开它们。例如由物理系统控制的木桶或箱子。当 obstacle 移动时，agents 会尽可能避开它们。但是一旦 obstacle 变成静止的，它将在 navmesh 上挖一个洞，因此 agents 在查询路径时就会避开它

## 工作原理

### Walkable Areas

导航系统需要它自己的数据来表示 game world 中的 walkable。就像 物理系统 一样，都是使用不同于渲染的 world 中的 geometry 作为自己的数据来运行。

Walkable Areas 定义 agent 可以站立和移动的区域。Unity 中 agents 描述为胶囊体（两个 sphere 构成）。Walkable Area 通过在 Scene 中的 Geometry 上测试 胶囊体可以站立的位置来构建。这些位置被连接成位于 scene geometry 上的一个 surface。这个 surface 就称为 NavMesh。

NavMesh 以 convex polygons 存储 surface。存储 polygon 的边以及 它们之间的连接信息。

### Finding Paths

先映射开始位置和目标位置对应的最近的 polygons。使用 A* 算法查找最短的 polygons 路径。这组 polygons 序列称为 走廊 corridor。

Agent 通过总是导航到走廊的下一个可见 corner 到达目的地。

当有多个 Agents 时，它们需要偏移原始查找的路径以彼此避开。而试图使修正这样的偏离很快就会变得困难而容易出错。

因为 agent 移动在每一帧都非常小，在我们需要一些迂回绕道时，可以使用 polygons 连接性来修复。然后我们很快会发现导航方向的下一个 corner。

### Avoiding Obstacles

导航逻辑使用下一个 corner 的位置来确定一个方向和速度，以到达目标。使用期望的速度移动 agent 可能导致和其他 agents 的碰撞。

Obstacle avoidance 基于移动的方向和未来将要发生的与其他 agents 和 navmesh 边缘的碰撞 选择一个新的速度。Unity 使用 RVO（reciprocal velocity obstacles）来预测并避免碰撞。

### Moving the Agent

在 steering 和 obstacle avoidance 之后，计算出最终的速度 velocity。Unity 中 agents 使用一个简单的动态模型来模拟，它可以考虑加速并允许更自然和平滑的移动。

在这个阶段，你可以将 simulated agent 的 velocity 传递给 动画系统，来使用 root motion 移动角色，或者让导航系统关心它。

移动 agent 开始移动，simulated agent location 被移动并限制在 NavMesh 上。

### Global and Local

![NavMeshUnderstandingLoop](../Image/NavMeshUnderstandingLoop.svg)

理解 navigation 的最重要的一件事是 global 和 local navigation 的区别。

Global Navigation 用来在 world 中发现走廊（polygons 序列）。在世界中查询路径是非常耗时的操作，需要大量的处理能力和内存。

描述路径的线性 polygons 列表是一个用于 steering 的灵活数据结构，并且它可以在 agents 位置移动时局部地调整。Local Navigation 试图确定如何高效地移动向下一个 corner 而不和其他 agents 或 移动的障碍物 碰撞

### Two Cases for Obstacles

很多导航应用程序需要其他类型的 obstacles 而不仅仅是其他 agents。这可以是射击游戏中的箱子和木桶。障碍物可以使用 local obstacle avoidance 或 global pathfinding 来处理。

当一个 obstacle 移动时，最好使用 local obstacles avoidance 来处理（就像把它当做另一个 agents 一样）。这样 agent 可以预测地避开障碍物。当 obstacle 变成静止时，可以认为阻塞了所有 agents 的路径。障碍物影响了 Global Navigation，即 NavMesh。

修改 NavMesh 称为挖孔 carving。这个过程检测 obstacle 的那个部分接触了 NavMesh 并在 NavMesh 上挖一个洞。这是一个非常消耗计算的操作，这也是为什么移动的 obstacles 应该使用 collision avoidance 来处理的另一个原因。

Local Collision Avoidance 也可以经常被用来在稀疏分布的障碍物周围导航。因为这个算法是 local 的，它只会考虑下一个即将发生的碰撞，而不能全局考虑，不能处理绕开陷阱或障碍物阻塞路径的情况，此时 agent 将被 block。这种情况下就可以使用 carving 来修改 NavMesh 了。

### Describing Off-mesh Links

NavMesh polygons 之间的连接通过 pathfinding 系统内部的 link 描述。但有时需要让 agent 穿越 not walkable 的区域进行导航，例如跳过一个栅栏，或者穿越一道关闭的门。这些情形需要知道穿越动作发生的位置。

这些动作可以使用 Off-Mesh Links 来标注，告诉 pathfinder 在指定 link 之间有一条路径（shortcut）。这个 link 在稍后的 follow path 中可以被访问，并且可以执行一个指定的动作（例如播放攀登或跳跃的动画）。

