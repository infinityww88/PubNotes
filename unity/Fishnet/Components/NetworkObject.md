# NetworkObject

## 描述

- 任何继承自 NetworkBehaviour 的脚本添加到 object 上时，NetworkObject 自动添加
- NetworkObject 组件对任何通过网络 sync、control 的 gameobject 至关重要
- 它作为所有 NetworkBehaviours 的 anchor，就像 GameObject 之于 MonoBehaviour
- 管理所有 NetworkBehaviours 的 identification, ownership
- 管理 networking system 中物体的 lifecycle
- 可以将 NetworkObject 嵌套在其他 NetworkObject 中，放在 Scene 中，放在 Prefab 中
- 这个组件自己不可以在运行时添加到 gameobject 上

## Settings

- IsNetworked
  - 指示 object 是否是 networked 的
  - false：object 不会 network 初始化
  - 适用于你希望 object 有时只本地运行，有时在网络上运行
  - 任何 ServerManager.Spawn 生成的 object，IsNetworked 自动设置为 true
- IsSpawnable
  - 如果 object 可以在运行时 spawn，应设置为 true
  - 对 scene object 应为 false，因为不需要实例化和手动 spawn 它们
  - true：object 的 prefab 将会添加到 DefaultPrefabObjects
- IsGlobal
  - true：使 NetworkObject 在任何时间对所有客户端可见，object 被添加到 Dont Destroy On Load 场景中
  - 这个设置对 scene objects 没有效果
  - 对于实例化 object，它可以在 prefab 中设置，或在实例化后，运行时修改
- InitializeOrder
  - 决定同一个 tick 中 spawn NetworkObjects 的初始化 callbacks 的执行顺序
  - 更小的值具有更高的优先级
  - 默认值为 0，可为负数
- Prevent Despawn On Disconnect
  - 当 owning client 断开连接时，确保 object 不会 destroyed 或 despawned
- Default Despawn Type
  - despawn object 时的默认 behaviour
  - despawn 时 Object 通常销毁
  - 指定 Pool 可以换成 NetworkObject
