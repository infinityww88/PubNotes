# Entities

Entities 表示游戏或程序中一个独立的“thing”。一个 entity 既没有行为，也没有数据。相反，它标识哪些数据片段是属于一起的，即包含一组 components，真正的数据保存在 components。System 提供操作 components 数据的行为。

一个 entity 本质就是一个 ID（身份）。思考它最简单的方式就是将它想象为一个超级轻量的 GameObject，而它甚至连 name 都没有。Entity IDs 是稳定的。你可以使用它们来存储一个到另一个 component 或 entity 的引用。例如，hierarchy 中的一个 child entity 应用它的 parent entity（ID）。

EntityManager 管理一个 World 中的所有 entities。一个 EntityManager 维护 entities 列表，并且组织关联到 entity 的数据以完成优化。

Entities 可以按照它们关联的 data components 类型给分类为 groups。当你创建 entities 并为它们添加 components 时，EntityManager 保持追踪现有 entities components 的唯一组合。每一个唯一的 components 的组合称为 Archetype。当向一个 entity 添加一个 component 时，EntityManager 创建一个 EntityArchetype 结构体。你可以使用现有 EntityArchetype 创建符合这个 archetype 的新 entities（component 数据将是默认值）。你还可以在创建 entities 之前先创建 EntityArchetype。

## Creating entities

创建一个 entities 最简单的方式是使用 Unity Editor。你可以设置 ECS 将放在 Scene 中的 GameObjects 和 Prefabs 在运行时转换为 entities。对于游戏或应用中更多的动态部分，你可创建一个生成系统，它在一个 job 中创建多个 entities。最后，你可以使用一个 EntityManager.CreateEntity 方法一次创建一个 entities。

### Creating entities with an EntityManager

EntityManager.CreateEntity 在 EntityManager 的 world 中创建一个 entity。

你可以以下面的方式一个一个创建 entities

- 使用一个 ComponentType objects 的数组带有相应 Components 的 entity（AddComponent）
- 使用一个 EntityArchetype 创建带有相应 Components 的 entity
- 使用 Instantiate 复制现有 entity，包括它当前的数据
- 创建一个空的 entity，然后再为它添加 Components

你还可以一次创建多个 entities

- 使用 CreateEntity，使用相同 archetype 的新 entities 填充 NativeArray
- 使用 Instanctiate，使用一个现有 entity 的副本填充一个 NativeArray，包括它当前的数据
- 使用 CreateChunk 显式创建 chunks，并填充以给定 archetype 的指定数量 entities

## Adding and removing components

当创建一个 entity 之后，可以添加或移除 components。此时，被修改的 entities 的 archetype 将会改变，EntityManager 必须移动修改的数据到一个新的内存 chunk，并使原来的 chunks 保持紧凑（将最后一个 entity 填充到空出的位置）。

对一个 entity 的修改将导致结构的改变，即改变 SharedComponentData values 的组件添加和移除，以及销毁 entity，不能在一个 job 内部完成，因为这将使 job 正在工作的数据无效。相反，你添加完成这些类型的改变的命令到一个 EntityCommandBuffer，然后在这个 job 完成之后执行这个 command buffer。

EntityManager 提供函数从一个 entity 或一个 NativeArray 的所有 entities 移除一个 component。

## Iterating entities

在匹配一个 components 集合的所有 entities 上进行迭代，是 ECS 架构的核心。
