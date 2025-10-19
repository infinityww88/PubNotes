# Networked GameObjects

Networked GameObjects 是被 Mirror networking system 控制和同步的 gameobjects。

使用同步的 gameobjects，你可以为所有 players 创建一个共享的体验。它们看见、听到相同的事件和动作——尽管它们可能来自游戏中自己的独特视角。

Mirror Multiplayer games 通常使用包含混合 networked gameobjects 和正常的（non-networked）gameobjects 的 scenes 构建。

Networked gameobjects 是那些在 gameplay 期间需要在所有 players 之间同步的 gameobjects。

Non-networked gameobjects 是那些在 gameplay 期间根本不移动或改变的 gameobjects（例如静态障碍物，石头，围栏），或者是虽然移动和改变，但是不需要在 player 之间同步的 gameobjects（例如不影响游戏结果的视觉元素，平缓摇动的树木，背景中的云彩，特效）。

一个 networked gameobject 是一个具有 NetworkIdentity component 的 gameobject。但是只有一个 NetworkIdentity component 不足以使 gameobject 在 multiplayer game 中工作。NetworkIdentity 组件是同步的起点，它允许 NetworkManager 同步这个 gameobject 的创建和销毁，但是除此以外，它不指定 gameobject 的哪个属性应该同步。

每个 networked gameobject 哪些属性应该同步，依赖于你制作的游戏类型，以及每个 gameobject 的目的是什么。一些你想要同步的示例：

- 移动的 gameobjects 的 position 和 rotation，例如 players 和 non-player 角色
- 一个动画的 gameobject 的 animation state
- 一个 variable 的值，例如当前游戏回合还剩多长时间，或者一个 player 还有多少能量

一些属性可以被 Mirror 自动同步。Networked gameobject 的同步创建和销毁被 NetworkManager 管理，被称为 Spawning。你可以使用 Network Transform 组件来同步 gameobject 的 position 和 rotation，使用 Network Animator component来同步 gameobject 的动画。

要同步一个 networked gameobject 的其他属性，需要使用 scripting。

同步任何属性，使用 NetworkBehaviour，NetworkTransform 和 NetworkAnimator 都是 NetworkBehaviour 的子类。

就像所有组件都是 MonoBehavior 的子类，而一个 gameobject 由很多 MonoBehavior 组件组成，Mirror Multiplayer Game 中，需要同步属性的 GameObject 由许多 NetworkBehaviour 组件构成，每个 NetworkBehaviour 包含可同步的属性，并执行相关的事件回调。
