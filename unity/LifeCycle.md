# 事件函数的执行顺序

Event functions 是 MonoBehaviour 脚本（是单个组件，不是 GameObject）可以通过实现方法注册的内置事件。

它们对应 Unity core subsystems(physics，rendering，user input)的事件，或者脚本自己 lifecycle 的阶段（creation，activation，frame-dependent-update，frame-independent-update，destruction）。


理解事件的执行顺序很重要，这可以避免在一个 callback 调用另一个还没有调用的 callback 的逻辑。

![flowchart](image/monobehaviour_flowchart.svg)

除了这些内置 event，还有很多其他 events 可以注册。一些主要 classes 例如 Application，SceneManager，和 Camera 提供了可以注册的 delegates。

Method attributes 例如 RuntimeInitializeOnLoadMethodAttribute 也可以在 scene 的特定阶段执行方法。

- Initialization 阶段会连续执行两个 event：Awake，OnEnable。也就是 Awake 和 OnEnable 先后连续执行，中间不会插入其他组件或其他 callback
- Start 在 OnEnable 之后执行。但是 Start 只执行一次，OnEnable 之后可以重复执行多次（与 OnDisable 一起）
- Scene 中 Inactive 的 GameObject 在场景加载后，不会执行 Initialization（Awake + OnEnable），直到第一次 Active。后面的 Active 和 InActive 则只会调用 OnEnable 和 OnDisable
- Unity 会在每个阶段遍历所有 GameObject 依次调用相应事件。这些事件的回调是在每个组件脚本上调用的，而不是对每个 GameObject 执行一次。对于每个 GameObject，遍历所有组件，依次调用每个组件的相应事件
- 不同阶段，GameObject 或组件可以依赖上一个阶段的任何 GameObject/组件 的事件已被执行。但是同一个阶段不同 GameObjects 的执行顺序，同一个 GameObject 的 Components 的执行顺序都是未定义的，不可以依赖这个顺序
- GameObject 和 GameObject，Component 和 Component 之间，同一个阶段的 events 不可以依赖顺序。尤其是 Awake 和 OnEnable 是同一个阶段的 events。即使同一个 GameObject 的组件，一个组件的 OnEnable 也不可以依赖另一个组件的 Awake
- 不同阶段的 events 顺序可以依赖，一个 GameObject 或 Component 的 Start 可以依赖另一个 GameObject 的 Awake/OnEnable 已经执行

## 通用原则

通常，对不同的 GameObjects，你不应该依赖同一个 event function 的执行顺序，除非顺序被显式声明或设置。

如果需要执行顺序由更精细的控制，可以使用 PlayerLoop API。

你无法指定同一个 MonoBehaviour subclass 的不同实例的 event functions 的执行顺序。例如，一个 MonoBehaviour 的 Update function 可能在另一个 GameObject 甚至 Parent 或 Child GameObject 上的相同 MonoBehaviour 实例的 Update 之前或之后执行。

你可以使用 Project Settings 的 Script Excution Order 指定一个 MonoBehaviour subclass 的 event functions 在另一个 subclass 之前或之后执行（这属于明确指定不同组件在响应同一个 event 的执行顺序）。如果加载 multiple scenes additively，配置的脚本顺序在一个 full one scene 中一次执行，而不是部分地跨 scenes 执行。

## First Scene Load

Awake 和 OnEnable 在 scene start 时调用，逐 GameObject 执行，对每个 GameObject 逐 Component 执行。

GameObject is inactive during start up, Awake is not called until it is made active.

作为 Scene asset 一部分的 GameObjects，Awake 和 OnEnable 在 Sttart 之前调用。但是对于运行时 instantiate 的 GameObject，只在 Instantiate 时执行。Instantiate 之后，Awake 和 OnEnable 已经确定执行完。

Awake 只确保在一个 GameObject 的一个 Component 上先于 OnEnable 执行。对于不同的 GameObject，甚至同一个 GameObject 的不同 Component，都不保证顺序。因此不可以依赖一个 GameObject/Component 的 Awake 在另一个 GameObject/Component 的 OnEnable 之前执行。

## Before Scene Load and UnLoad

SceneManager.sceneLoaded 和 SceneManager.sceneUnloaded events 可以让你接收一个 scene 被加载和卸载的 callback。你可以确定在任何 GameObjects 的 OnEnable 之后，Start 之前收到 sceneLoaded 事件。

还可以使用 RuntimeInitializeOnLoadMethod Attribute 和参数 BeforeSceneLoad 和 AfterSceneLoad 来使你的方法在 scene load 之前或之后运行。
