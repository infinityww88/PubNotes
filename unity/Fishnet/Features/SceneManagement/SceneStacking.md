Scene Stacking 是 server 或 host 的能力，来在同一个 scene 中同时加载多个 instances，通常每个 scene 有不同的 clients 或 observers。

## General

Stacking Scenes 的好例子是一个 server 上有多个 dungeon instances。

如果两个 clients 进入相同的 dungeon，每个 client 会加载它们自己的 dungeon 的副本，并且拥有独立的 GameObjects，以及那些 scenes 的 state。但是 Server 会同时加载那个 scene 的两个 instances。Server 加载同一个 scene 的两个实例称为 "Scene Stacking"。

Stacked Scenes 通常有不同的 Clients 观察 scene 的每个 instance。

## Stacking Scenes

### Loading Into New Stacked Scene

- 要 stack scene，你必须在 SceneLoadData 选项中设置 AllowStacking 为 true
- 要创建一个 stacked scene 的新实例，SceneLookupData 必须使用 scene name 填充
- Global Scenes 不可 stacked

```C#
//Stacking a new Scene
//Select Connections to load into new stacked scene.
NetworkConnection[] conns = new NetworkConnection[]{connA,ConnB};

//You must use the scene name to stack scenes!
SceneLoadData sld = new SceneLoadData("DungeonScene");

//Set AllowStacking Option to true.
sld.Options.AllowStacking = true;

//Decide if you want seperate Physics for the scene.
sld.Options.LocalPhysics = LocalPhysicsMode.Physics3D;

//load the Scene via connections, you cannot stack global scenes.
base.SceneManager.LoadConnectionScene(conns,sld);
```

### Loading Into Existing Stacked Scene

如果你要用 Scene reference 或 handle 加载两个 connections 到一个 scene，它们会添加到同一个 scene，无论 AllowStacking 是 true 还是 false

## Separating Physics

你可能想要在 stacking scenes 时分离 physics。这确保 stacked scenes physics 不会彼此交互。你会想要在 SceneLoadData 中设置 LocalPhysics 选项。

- LocalPhysicsMode.None

  这是默认选项，Scene Physics 会与其他 scenes 彼此碰撞。

- LocalPhysicsMode.Physics2D

  创建一个 local 2D physics Scene，并被 Scene 所属。

- LocalPhysicsMode.Physics3D

  创建一个 local 3D physics Scene，并被 Scene 所属。

  如果你要使用 separate physics scenes，你还想要在它们中模拟 simulate，必须手动进行。这是有意设计的。

  下面是一个脚本，你可以放在你的 stacked physics scenes，和默认 physics scenes 一起模拟物理。
  
  ```C#
  using FishNet.Object;
  using System.Collections.Generic;
  using UnityEngine;
  
  /// <summary>
  /// Synchronizes scene physics if not the default physics scene.
  /// </summary>
  public class PhysicsSceneSync : NetworkBehaviour
  {
      /// <summary>
      /// True to synchronize physics 2d.
      /// </summary>
      [SerializeField]
      private bool _synchronizePhysics2D;
      /// <summary>
      /// True to synchronize physics 3d.
      /// </summary>
      [SerializeField]
      private bool _synchronizePhysics;
      /// <summary>
      /// Scenes which have physics handled by this script.
      /// </summary>
      private static HashSet<int> _synchronizedScenes = new HashSet<int>();
  
      public override void OnStartNetwork()
      {
          /* If scene is already synchronized do not take action.
           * This means the script was added twice to the same scene. */
          int sceneHandle = gameObject.scene.handle;
          if (_synchronizedScenes.Contains(sceneHandle))
              return;
  
          /* Set to synchronize the scene if either 2d or 3d
           * physics scene differ from the defaults. */
          _synchronizePhysics = (gameObject.scene.GetPhysicsScene() != Physics.defaultPhysicsScene);
          _synchronizePhysics2D = (gameObject.scene.GetPhysicsScene2D() != Physics2D.defaultPhysicsScene);
  
          /* If to synchronize 2d or 3d manually then
           * register to pre physics simulation. */
          if (_synchronizePhysics || _synchronizePhysics2D)
          {
              _synchronizedScenes.Add(sceneHandle);
              base.TimeManager.OnPrePhysicsSimulation += TimeManager_OnPrePhysicsSimulation;
          }
      }
  
      public override void OnStopNetwork()
      {
          //Check to unsubscribe.
          if (_synchronizePhysics || _synchronizePhysics2D)
          {
              _synchronizedScenes.Remove(gameObject.scene.handle);
              base.TimeManager.OnPrePhysicsSimulation -= TimeManager_OnPrePhysicsSimulation;
          }
      }
  
      private void TimeManager_OnPrePhysicsSimulation(float delta)
      {
          /* If to simulate physics then do so on this objects
           * physics scene. If you know the object is not going to change
           * scenes you can cache the physics scenes
           * rather than look them up each time. */
          if (_synchronizePhysics)
              gameObject.scene.GetPhysicsScene().Simulate(delta);
          if (_synchronizePhysics2D)
              gameObject.scene.GetPhysicsScene2D().Simulate(delta);
      }
  }
  ```