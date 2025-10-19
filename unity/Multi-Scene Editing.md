# Multi-Scene editing

Multi-Scene 让你在 editor 中同时拥有多个 scenes。

每个 scene 只是一组 gameobject 的 prefab。Multi scene 加载只是从加载一个 scene prefab 变成加载多个 scene prefab。对于 runtime 而已，只不过是像 scene 中分组加载了所有预置的 gameobjects 而已。即使是动态加载的 gameobjects，也和预置加载没有区别和明显的分界线，因为所有做的只是实例化 gameobject，调用响应的生命周期回调函数。

就把 scenes 想象为将它包含的所有 gameobjects 作为 children 的 prefab，并在此基础上增加了 scene 管理的功能。

但是在 editor 中打开多个 scenes 允许你创建 large streaming worlds，并改进协作编辑 scene 的 workflow。

## In the editor

要打开一个 scene，并将它添加到 Hierarchy 中的 scenes list：

- 在一个 scene asset 的 context menu 中选择 Open Scene Additive
- 从 Project Window 中拖拽多个 scenes 到 Hierarchy Window 中

每个 scene 在 Hierarchy Window 中分开显式，由 scene 分割线分开。

Scene 添加到 Hierarchy 之后，可以 loaded 或 unloaded 来显式或隐藏它们各自包含的 gameobject（应该类似于 root gameobject 的 enable 和 disable）。

当使用 multiple scens 时，每个被修改的 scene 需要它的 change 被保存，因此同时可能有多个 scene 未保存。未保存 change 的 scene 将会有一个 * 在 scene divider bar 旁边。

每个 scene 通过 divider bar 的 context menu 单独保存。Unity file menu 的 Save Scene 或者 Ctrl/Cmd + S 将会保存所有打开的 scenes。

### Scene divider menu for loaded Scenes

- Set Active Scene

  指定 new GameObjects 在哪个 scene 中创建和实例化。必须总是有一个 scene 被指定为 active scene

- Save Scene

  只保存选择的 scene

- Save Scene As

  将修改的 scene 保存为新的 scene asset

- Save All

  保存所有 scenes 的 changes

- Unload Scene

  Unload scene，但是保持 scene 在 Hierarchy Window（Scene disable）

- Remove Scene

  从 Hierarchy Window unload 并 remove scene

- Select Scene Asset

  在 Project window 选中 scene asset（高亮）

- GameObject

  提供一个和 Unity main GameObject menu 一样的 sub-menu

### Scene divider menu for unloaded Scenes

- Load Scene

  Load scene 内容

- Remove Scene

  从 Hierarchy window 移除 scene

- Select Scene Asset

## Baking Lightmaps with multiple Scenes

为了一次为 multiple scenes bake Lightmap data，应该打开你想 bake 的所有 scenes，关闭 Lighting Window 的 "Auto" mode，点击 Build button 来 build lighting。

Lighting 计算的输入时所有 scenes 中的 static geometry 和 lights。因此 shadows 和 GI light bounces 将会在所有 scens 中工作。然而，lightmaps 和 realtime GI data 被分割为每个 scene 的数据，跟着每个 scene 单独加载和卸载。Lightmaps 和 realtime GI data atlases 在 scenes 之间 split。这意味着 scenes 之间的 lightmaps 从不会 shared，并且它们可以在 unload 一个 scene 时，可以安全地 unload。Lightprobe data 当前总是共享的，并且 baked 到一起的所有 scenes 的所有 lightprobes 同时加载（就是即使加载一个 scene，也会将所有 scene 的所有 Lightprobe 加载）。

或者，你可以在 editor script 中使用 Lightmapping.BakeMultipleScenes 函数自动为 multi-scenes 构建 lightmaps。

## Baking Navmesh data with multiple Scenes

为了一次为 multiple scenes 生成 Navmesh data，同时打开所有想要 bake 的 scenes，点击 Navigation Window 中的 Bake button。NavMesh data 将会 baked 到一个 asset 中，被所有 loaded scenes 共享。Data 匹配到和当前 active scene 名字匹配的目录中（ActiveSceneName/NavMesh.asset）。所有 loaded scenes 将共享这个 navmesh asset。

或者，你可以在 editor script 中使用 NavMeshBuilder.BuildNavMeshForMultipleScenes 函数自动为 multi-scenes 构建 navmesh data。

## Baking Occlusion Culling data with multiple Scenes

Window > Rendering > Occlusion Culling -> Bake。Data 保存到和当前 active scene 名字匹配的目录中一个名为 OcclusionCullingData.asset。

无论何时一个 scene 被增量 loaded，如果它和当前 active scene 引用相同 occlusion data，这个 Scene 的 static renderers 和 portals culling 信息从 occlusion data 初始化。这之后，occlusion culling 的运行就像所有 static renderers 和 portals 被 baked 到一个单一的 Scene 中一样。

## Play mode

在 Play mode，Hierarchy 中除了 multiple scenes，还出现一个称为 DontDestroyOnLoad 的额外 scene。

在 Unity 5.3 之前，在 Playmode 中实例化的标记为 DontDestroyOnLoad 的任何 objects，将会保持出现在 Hierarchy。这些 objects 不被认为任何 scene 的一部分，但是 Unity 仍然会显示这些 objects。使你可以 inspect 它们。现在，这些 objects 显示为一个特殊的 DontDestroyOnLoad scene 的一部分。

你不能访问 DontDestroyOnLoad scene，并且它在运行时不可用。

## Scene-specific settings

许多设置是每个 scene 特定的，即使在运行时它们是在同一个 runtime scene 中，这些是：

- RenderSetting 和 LightmapSetting（Lighting Window）
- NavMesh setting
- Occlusion Culling Window 中的 Scene setting

它可以工作的原因是，每个 scene 会管理它自己的 setting，并且只有和 scene 关联的 setting 才会被保存到 scene 文件中。

如果你打开了多个 scenes，用于 rendering 和 navmesh 的 setting 是来自 active scene 的设置。这意味着，如果你想改变一个 scene 的 setting，你必须或者只打开一个 scene 然后改变设置，或者使指定的 scene 为 active scene 然后改变设置。

如果你在 editor 或 runtime 中切换 active scene，新的 scene 中的所有 setting 将会被应用并替换之前的所有设置。

## Scripting

### Editor scripting

对于 editor scripting，Unity 提供了一个 Scene struct 和 EditorSceneManager API 和 一个 SceneSetup 工具类。

Scene struct 在 editor 和 runtime 中都可用，并且包含有用有关 scene 自身的只读属性，例如它的 name 和 asset path。

EditorSceneManager 类只在 editor 可用。它从 SceneManager 派生，并且拥有大量函数，可以允许你实现上述所有 Multi Scene Editing 功能。

SceneSetup 类是一个小的工具类，存储当前 Hierarchy 中一个 scene 的信息。

Undo 和 PrefabUtility 类已经被扩展以支持 multiple scenes。你现在可以使用 PrefabUtility.InstantiatePrefab 在一个给定 scene 中实例化一个 prefab，并且使用 Undo.MoveGameObjectToScene 移动 objects 到一个 scene 的 root，但是是不可 undo 的。

### Runtime scripting

对于运行时脚本，SceneManager 类中包含 LoadScene 和 UnloadScene 方法可以操作 multiple scenes。

## LocalPhysicsMode

默认，当一个 Scene 创建或加载时，Scene 中一个 GameObject 上的任何 2D 或 3D 物理组件，被添加到 默认 physics Scene。但是每个 Scene 有能力创建并拥有它自己的（local）2D 或 3D 物理 scene。这个选项可以指定，在创建和加载一个 Scene 时，是否应该创建一个 2D 或 3D physics Scene。

当一个 Scene 创建它自己的 2D / 3D physic scene，physics scene 的生命周期和 Scene 相同，例如如果 Scene 被销毁/卸载，则任何创建的 physics Scenes 也是一样。

public static PhysicsScene PhysicsSceneExtensions.GetPhysicsScene(SceneManagement.Scene scene);

返回指定 scene 关联的 PhysicsScene 或者默认的3D physics Scene。

PhysicsScene 方法：

- Raycast
- BoxCast
- CapsuleCast
- SphereCast
- IsEmpty
- IsValid
- OverlapBox
- OverlapCapsule
- OverlapSphere
- Simulate

  模拟这个 PhysicsScene 的 physics。

  调用这个方法导致 physics 被模拟 step time。只有这个 PhysicsScene 关联的 physics 被模拟。如果这个 PhysicsScene 不是默认的 physics scene，则它关联到一个特定 scene，因此只有这个 scene 中的组件被模拟影响。

  如果传递依赖帧率 framerate-dependent 的 step values（例如 Time.deltaTime）到 physics engine，模拟将更不具有确定性，因为帧率时不可预测的。要得到确定的物理结果，你应该每次调用 PhysicsScene.Simulate 时传递一个固定 step value。

  你可以在 Editor 中调用 PhysicsScene.Simulate，在 Editor 中请求物理模拟，实现基于物理效果的关卡设计。当在 play mode 之外的 Editor 模拟时，执行一个 full simulation，包括所有的物理组件（Rigidbody，Collider，Joint），并产生 contacts（碰撞接触），但是 contacts 不会通过标准的 script callbacks 报告。这是一个安全手段，防止回调删除 Scene 中的 objects，并且不可 undo。

## Tips and tricks

可以在拖放时按下 Alt 来添加一个 scene 到 Hierarchy 中，同时保持 unloaded state。这可以让你之后 load scene。

可以通过 GameObject.scene 获得一个 GameObject 属于的 scene。

建议避免使用 DontDestroyOnLoad 来持久化你想在 不同 scene 加载之间持久化 manager GameObject。相反，创建一个 manager scene，它拥有所有的 managers，并使用 SceneManager.LoadScene(<path>, LoadSceneMode.Additive) 和 SceneManager.UnloadScene 来管理你的游戏进程。

SceneManager.LoadScene 用来加载 scene。

```C#
LoadSceneParameters loadSceneParameters = new LoadSceneParameters {
  loadSceneMode = LoadSceneMode.Additive,
  localPhysicsMode = localPhysicsMode
};

SceneManager.LoadScene(sceneName, loadSceneParameters);
```

sceneName 应用的 scene 必须被添加到 Build Setting 中，才能在运行时动态加载（尤其是 Editor 中）。

一个 Multi-Scenes Build 的一个应用是在 Server Build 中同时 hold 多个 gameplay scene（每个 additive 都是一个 subscene），每个用于处理一组 players，每组 players 之间是相互独立的。如果不使用 Physics，一个 Single-Scene Server Build 也可以并行处理多个相互独立的 players group，因为只需要对每个 player 只发送它所在 group 中的 gameobjects 的信息就可以了。但是如果使用了物理，Single-Scene 中的物理物体之间就可能相互影响，尽管可以为每个 group 赋予不同的 layer 进行物理隔离，但是 layer 的本意不是如此，而是用于不同的游戏方面，并且最多只能有 32 个 layer。但是 Multi-Scenes 中，每个 scene 可以有自己单独的 PhysicsScene 进行模拟，这样不同的 subscene 之间就可以完全独立了，并且可以处理任意数量的 subscenes。所有 subscenes 都是在同一个 runtime container scenes 中运行，如果 multi-scenes server build 进行渲染，就可以看见所有 gameobjects 都渲染在同一个画面中，但是通常 server build 是 headless 的，而 client 只从 server 接收自己所在 group subscene 中的 gameobjects 信息，因此也只显示这个 subscene，这样一个 multi-scenes server build 就可以并行处理多个 players group 的 gameplay，每一个在一个单独的 subscene 中，并且相互之间是独立的，互不影响。

Subscene 可以用于在 Scene 中组织 gameobjects，将 gameobject 移动到不同的 subscene 中。此外，一个 scene asset 可以同时 load additive 多次，就像一个 prefab 可以实例化多个 gameobjects 一样。

