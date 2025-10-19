# Get Started

## Script Templates

提供常用模板 用于快速创建 Network Behaviours 以及其他脚本。

## NetworkManager set-up

- 添加一个新的 gameobject 到 scene 中，命名为 NetworkManager
- 添加 NetworkManager component 到 NetworkManager gameobject
- 添加 NetworkManagerHUD 组件到这个 gameobject。其提供了管理 network 游戏状态的默认 UI

## Player Prefab

- 查找 game 中 player gameobject 的 Prefab，或者从 player gameobject 创建一个 Prefab
- 添加 NetworkIdentity 组件到 player Prefab
- 在 NetworkManager's Spawn Info section 中设置 playerPrefab 字段为 player 的 prefab
- 从 Scene 中移除 player gameobject instance

## Player movement

- 添加 NetworkTransform 组件到 player Prefab
- 选中组件上的 Client Authority checkbox
- 如果 (NetworkBehaviour) isLocalPlayer 为true，更新 input 和 control 脚本
- 覆盖 OnStartLocalPlayer 为 player 控制场景中的 Main Camera

## Basic player game state

- 使包含重要数据的脚本放在 NetworkBehaviours 中而不是 MonoBehaviours 中
- 使重要的变量放在 SyncVars 中

## Networked actions

- 是执行重要操作的脚本放在 NetworkBehaviours 中而不是 MonoBehaviours 中
- 更新执行重要 player 动作的 functions 为 commands

## Non-player game objects

Fix non-player prefabs，例如 enemies：

- 添加 NetworkIdentity 组件到 non-player prefabs 上
- 添加 NetworkTransform 组件
- 使用 NetworkManager 注册 spawnable Prefabs
- 使用 game state 和 actions 更新脚本

## Spawners

- 可能要修改 spawner scripts 为 NetworkBehaviours
- 改变 spawner 只在 server 上运行（在 OnStartServer() 函数中使用 isServer 属性）
- 调用 NetworkServer.Spawn() 来创建 game objects

## Spawn positions for players

- 添加一个新的 gameobject，并放置在 player 的开始位置上
- 添加 NetworkStartPosition 组件到新的 gameobject 上
