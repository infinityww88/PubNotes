# ECS concepts

一个 ECS 架构区分 identity（entities，身份，gameobject），data（components），behavior（systems）。

这个架构关注数据。Systems 读取 component data 的 streams，将它们从输入状态转换到输出状态，然后 entities 指向新的 component data 状态。

![ECSBlockDiagram](../Image/ECSBlockDiagram.png)

在这个图中，system 读取 Translation 和 Rotation 组件，将它们相乘然后更新相应的 LocalToWorld 组件（L2W = T * R）。

Entities A 和 B 具有 Renderer 组件的事实不影响 System，因为 System 不关心 Renderer 组件。

ECS 核心技术是将数据组件在内存中以结构体形式连续存储，大大提高游戏循环更新数据时的缓存命中，而面向对象设计中，对象是在内存中随机分布的。

你可以设置一个 System，它需要一个 Renderer 组件，这时 system 将忽略 Entity C 的组件。或者，你可以设置一个 System，排除带有 Renderer 组件的 entities，这将忽略 Entities A 和 B 的组件。

## Archetypes（原型，基模）

一个唯一的 Component Types 的组合成为一个 Archetype。

![ArchetypeDiagram](../Image/ArchetypeDiagram.png)

Entities A B 共享一个 ArcheType M，Entity C 具有单独的 ArcheType N。

Archetypes 类似 C# 的匿名类，尽管没有名字，但是是一个具有特定结构的类定义。

Archetypes 在运行时可以通过添加或移除 components 动态改变。例如移除 B 的 Renderer，它就和 C 一样属于 archetype N。

## Memory Chunks

一个 Entity 的 archetype 决定 ECS 在哪里存储 entity 的 components。

相同类型的 Archetype 的 entity 的 components 在内存中连续排列。改变 Archetype 时，entity 从一个连续数组转移到另一个连续数组。

ECS 以 chunks 分配内存。每个 chunk 表示为一个 ArchetypeChunk 对象。一个 chunk 包含一个 archetype 的一组 entities。当一个 chunk 被填满时，ECS 分配新的 chunk 来填充这个 archetype 的新的 entities。

如果你添加或移除 components，改变了一个 entities 的 archetype，ECS 将这个 entities 转移到相应 archetype 的 chunk 上。

![ArchetypeChunkDiagram](../Image/ArchetypeChunkDiagram.png)

这个组织模式提供了 1:N 的 archetype-chunks 关系。它还意味着查找给定 component 集合的所有 entities 只需要搜索包含这个组件集合的 archetype 的 chunks，它们通常非常少，而不是全部的 entities，后者数量则非常大。

ECS 不以特定顺序存储 entities。当一个 entity 被创建或修改为一个新的 archetype，ECS 将它放在这个 archetype 第一个可以存放它的 chunk。

Chunks 保持紧密存储，当一个 entity 从 archetype 移除时，ECS 将它的最后一个 entity 移动到这个空洞。

Archetype 中共享 components 的 value 也决定哪个 entities 存储到哪个 chunk。一个给定 chunk 的所有 entities 对于任何 shared components 具有相同的 values。如果你改变了一个 shared component 的任何字段，被修改的 entity 移动到另一个 chunk，就像你改变 entity archetype 时的那样。如果需要，分配新的 chunk。Shared Component 例如 Shared Mesh 或 Shared Material。

使用 Shared Components 将一个 archetype 内的 entities 分组，可以更高效的一起处理它们。例如 Hybird Renderer 定义它的 RenderMesh component 来达成此事。

## Entity queries

使用 EntityQuery 来标识一个 System 应该处理哪些 entities。一个 entity query 在现有 archetypes 中搜索具有匹配你的需求的组件的那些。

可以在查询中指定以下 component 需求：

- All：archetype 必须包含 All category 中的所有 component 类型
- Any：archetype 必须包含 Any category 中的至少一个 component 类型
- None：archetype 必须不包含 None category 中的任何 component 类型

一个 entity query 返回一个 chunks 列表，其包含 query 请求的 components 类型。你然后可以使用 IJobChunk 直接在这些 chunks 上的 components 上迭代。

## Jobs

要利用多线程的优势，可以使用 C# Job system。

ECS 提供 SystemBase 类，以及 Entities.ForEach，和 IJobChunk Schedule() 和 ScheduleParallel() 方法，来在主线程之外转换数据。Entities.ForEach 是最简单的方法，通常需要更好的代码来实现。对于Entities.ForEach 不能处理的复杂情况，使用 IJobChunk。

ECS 在主线程中一个你的 Systems 安排的顺序来调度 jobs。当 jobs 被调度时，ECS 保持跟踪哪些 jobs 读取、写入哪些 components。一个读取一个 component 的 job 依赖于任何之前调度的写入相同 component 的 job，反之亦然（一个写入一个 component 的 job 依赖于任何之前调度的读取相同 component 的 job），即读写 component 的 jobs 不会并行执行，会被安排为先后执行，即使是并行调度 job。

Job 调度器使用 job 依赖来决定哪些 jobs 可以并行执行，哪些必须顺序执行。

## System organization

ECS 使用 World 组织系统，然后通过 Group 组织 World。默认地，ECS 使用一个预定义 groups 集合创建一个默认 World。它查找所有可用的 systems，实例化它们，添加它们到默认 world 的预定义的 simulation group（simulation group 是预定义 groups 中的一个）。

你可以指定同一个 group 中的 systems 的更新顺序。一个 group 是一种系统，你可以添加一个 group 到另一个 group，并像其他 system 一样指定顺序。这些形成一个树形组织。一个 group 中的所有 systems 在下一个兄弟 system 或 group 之前更新。如果你不指定顺序，ECS 以一个确定但不依赖创建顺序的顺序将 system 插入更新 order。换句话说，相同的 systems 集合在它们的 group 中总是以一个相同的顺序更新，即使你不显示指定一个顺序。

System 更新发生于 main thread。但是 systems 可以使用 jobs 来将负载卸载到其他线程中。SystemBase 提供了直观的方式来创建和调度 Jobs。

## ECS authoring

当你在 Unity Editor 中创建 game 或 application，你可以使用 GameObjects 和 MonoBehaviors 创建一个转换系统来映射那些 UnityEngine objects 和 components 到 entities。
