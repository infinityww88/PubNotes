# Animancer

## Overview

Unity 的动画系统在底层是 Playable Graph，Animator 就是最终处理这个 Playable Graph 的组件，而 Animancer 是和 AnimatorController 对应的 PlayableGraph 的管理器，这就是为什么 Animancer 需要 Animator 而不需要 AnimatorController 的原因。

Animancer 就是 AnimatorController 的代替品。它们具有非常类似的概念和接口，例如 State，Layer，Mixer 等等。

Ragdoll，IK，AnimationRigging 等后处理约束都是处理 pose 数据，而这些数据最终是从 Animator 输出的，Animancer 和 AnimatorController 和这些后处理由 Animator 隔离了，因此 Animancer 输出动画可以像 Mecanim 动画一样被所有后处理约束。

- Animancer是什么
  - 动画系统
  - Playables API
  - 显式控制每个动画, 脚本直接控制动画片段而不需要额外的设置
  - 整体替换Animator Controller
  - 和character上的animator controllers一起工作
- 快捷播放
  - AnimancerComponent.Play(AnimationClip)
- 等待动画结束
  - 注册一个回调在动画播放完毕时执行
  - 在一个coroutine中yield return一个AnimancerState
  - 直接查看AnimancerState.NormalizedTime(0~1)
- 平滑转换
  - CrossFade: 随时间在两个animations平滑混合。
  - CrossFadeFromStart: 新的animation是同一个，向着同一个animation的开始平滑混合
- 配置简单
  - 在Inspector中管理animations的细节(= Configure Animator State)
  - 作为场景的一部分
  - 使用脚本在运行时动态控制所有事情
  - 设置Fade duration，Speed，Start Time等等
- 结构灵活
  - 使用arrays，ScriptableObjects，或者任何其他结构来组织动画
  - 允许定义诸如DirectionalAnimationSet的通用结构
- Live（实时） Inspector
  - 通过手动控制在Inspector中查看动画的细节，来进行调试和测试
- 有限状态机Finite State Machines
  - 不像Animator Controllers那样强制使用FSM
  - Animancer.FSM非常灵活，并完全从animation系统分离
- 高性能
- 强大的兼容性
  - 绝大多数为常规animator controllers开发的系统都应该可以和Animancer一起工作
  - 支持几乎所有Unity动画系统的其他功能
- 完全控制
  - 对所有动画细节的全部访问，包括speed，time，weight
- Animation Layers
  - 同时管理多个animation集合（通常位于身体的不同部分）
  - 彼此Override或Additive
  - 就像独立动画一样对layers进行fade in/out
- Animator Controllers
- Animation Mixers

## Introduction

### Feature Comparison

- Mecanim
  - Unity的主要动画系统
  - 使用带有一个AnimatorController资源的Animator组件
- Playables API
  - 过于底层不能作为一个动画系统
  - 它可以用来构建类似Mecanim或Animancer的动画系统，但是并不容易
- Workflow
  - Mecanim要求所有可能的动画状态提前定义，作为Animator Controller的一部分
  - 强加一些限制，不能很好地在运行时控制动画
  - 最直接的原因是FSM只适用于提前预知状态的静态逻辑，但是不适用于未知状态的动态逻辑
  - Animancer组件在Inspector中显示它所有的内部状态使得你可以实时查看和修改它们的参数
- Control
  - 使用OnEnd回调函数获得结束通知
  - 在coroutine中，可以yield return一个AnimancerState来等待一个动画的结束
  - Animancer允许动画在Edit模式下播放，就像在Play Mode下一样容易
  - Mecanim只允许访问当前状态和要转换到的下一个状态的细节，Animancer赋予脚本在任何时候对任何动画的细节的全部访问
  - Animancer动态地控制动画细节（转换duration，速度，时间，权重等等）。而Mecanim鼓励你使用Editor基于转换配置参数，而这些在运行时无法修改
  - Animancer可以在Editor和Script中配置动画细节，而Mecanim在Animantor Controller中完成
  - 独立地调整转换的开始时间（在当前动画真正结束之前的一个时间点开始转换，来得到一个平滑的动画转换）。Mecanim在Transition Inspector中配置它，Animancer通过创建一个名为End的Animation Event来实现，End事件将触发任何注册的OnEnd回调函数（因此你可以手动执行一个转换，CrossFade）
  - Mecanim和Animancer支持Unscaled Time模式，对于诸如GUI动画非常有用，它们应该总是按照正常的速度播放，即使game暂停的时候
  - Animancer允许创建自己的state类型，通过继承AnimancerState使得你可以实现自定义行为
- Blending
  - Mecanim同一时间只允许一个Animantor Controller进行混合
  - Animancer的Controller States允许混合多个congtrollers彼此混合，以及和被脚本控制的独立动画直接混合
  - 在animatins之间随时间平滑转换
  - Animation Layers允许同时管理多个动画
  - Blend Tree（Animator Controller）/Animation Mixers（Animancer）
    - Blend Tree允许基于一个参数在两个动画之间进行插值（给予移动的速度在idle，walk和run之间进行插值）
    - Animation Mixers用于同样的目的，但是允许多得多的脚本控制
  - Blend Methods
    - transition：两个连续播放的动画，后面动画的头部和前面动画的尾部重叠，来产生一个平滑转换
    - layer：不同部分的不同动画同时播放构成一个完整的角色动画
    - blend tree：多个角色的整体动画同时播放，通过一个权重控制每个动画对最终动画的贡献（例如idle，walk，run同时混合，通过一个权重在idle到walk，walk到run之间进行平滑变化）
  - Root Motion
    - 传统动画通常在原地保持固定，并依赖其他系统来移动角色，例如物理系统或者角色控制器
    - Root Motion允许动画更加自然的移动角色
  - Linear Root Motion Blending
- Humanoids
  - Animation Retargeting
    - 允许动画从任何humanoid骨骼重定向到任何其他humanoid骨骼
  - Animation Mirroring（on import）
  - Animation Mirroring（per state）
  - 反向动力学和目标匹配
  - Playables API暴露标准IK特性，Mecanim和Animancer都可以使用
- 有限状态机
  - Animancer不再绑定到一个特定的状态机实现，但是它提供了一个通用目的的有限状态机，它完全从动画系统分离，并且对于绝大多数需要足够灵活
  - Animancer.FSM系统完全通过脚本配置和控制，转换可以在运行时确定，而不必像Animator Controller一样提前配置。Animator Controller的全部结构必须在Unity Editor中定义，并不能在运行时改变
  - Animancer.FSM系统可以给予任何你想要的条件改变，不需要所有状态起始时在同一个地方定义或配置
  - 一个class被用作Animancer.FSM系统的一个state的唯一需求是继承IState\<TState>。这意味着它们可以是MonoBehaviour组件来接收updates，collision event，和其他消息，或者ScriptableObject资源，ScriptableObject可以在project的任何地方引用，甚至是完全由脚本构造和管理的常规classes
- 兼容性
  - Animancer是基于Playables API的，这意味着绝大多数为常规Mecanim Animator Controllers开发的系统都可以和它一起工作

### Mecanim vs Animancer

- Animancer使得animation开发管线更加流畅，它移除了创建Animator Controllers和与其交互的脚本的需要，它赋予脚本完全定义全部动画逻辑的能力。
- Animancer允许脚本以任何你觉得对每种情形最适合的逻辑定义动画，而不是强制你全部在一个独立于脚本的地方定义一个状态机结构
- 不再浪费时间查看animator controller的内容以及脚本是如何和它交互的
- Animancer将总是精确按照你脚本告诉它的去做，不再有任何出人意料的意外

#### Why Replace Mecanim

- Mecanim Animator Controller系统被设计用来使没有编程经验的人更加容易访问（防止糟糕的程序员把事件变的更糟，但是却不能帮助优秀的程序员把事件变的更好）
- 游戏是高度复杂和动态的，因此一个所有动画放在一个巨大静态状态机的简易暴力的方式并不适合大量的不同情形
- 它导致重复的effort，因为你定义了角色行为的部分在Animator Controller中，而其他部分在脚本中，还需要花费精力将它们联系起来
- 任何Animator Controller的改变将破坏脚本的逻辑，反过来也一样。但是你无法得到一个清晰的指示哪个脚本使用哪个状态
- 它禁止了分离和封装独立区域为容易管理和重用的groups的尝试。所有东西都扔进一个单独的Animator Controller
- 它极大限制了运行时控制，因为任何事情都需要提前在Unity Editor中提前配置
- Mecanim强制你不需要的额外依赖
- Mecanim使用参数决定合适animation被播放，但是它自己并没有什么用，仍然需要以来脚本来决定何时播放动画，然后相应设置参数为合适的值来触发变换
- Mecanim分离了Scripts和AnimatorController，而它们本应是相互依赖的，还有你没有合适的方法来可视化、校验、或者强制这些依赖
- Animancer不分离本应是一起的东西。脚本决定何时播放动画然后简单地播放他。没有对预定义pre-defined states，transitions或者parameters的依赖
- Animancer让你自由地定义一个character的单独方面，这通常意味着创建你自己的逻辑分组，包装它们，使得多个角色可以共享相同的结构（使用MonoBehaviour或ScriptableObject），在多个prefabs和scene object之中共享动画组
- Animator Controller负责所有的动画，无视哪个系统实际使用这些动画
- 使用Controller状态还可以成为一种为动画分组的有效方式，因为它允许你使用多个小的Animator Controllers而不是一个大而全的
- Animator Controllers需要在UnityEditor中setup，之后它们的结构几乎固定不能在运行时改变

#### Playing

- 每次修改Mecanim动画，都要涉及修改脚本，然后手动查找使用的每个Animator Controller，最后手动作出相应的修改
- Animancer脚本则精确指示所有东西如何工作

#### Waiting

- 当调用Play或者CrossFade，它返回一个AnimancerState（和AnimatorController一样，所有播放的动画都是一个state，即当前Character处于的状态，每个动画都对应角色的一个状态）。在AnimancerState的OnEnd事件注册一个回调函数。OnEnd事件不是在动画结束时自动调用，而是在动画片段中标记一个End事件，Animancer自动处理这个事件并调用OnEnd，这样可以在动画真的结束之前就调用OnEnd，然后可以执行CrossFade到下一个动画
- 在一个Coroutine中，你可以yield return这个state，等待它的结束
- 保持这个状态，并周期地检查它的Time或NormalizedTime。如果担心它被其它脚本停止了，检查它的IsPlaying属性

#### Speed and Time

```C#
var state = animancer.Play(clip);
state.Speed = 2;
state.Time = 1;
state.NormalizedTime = 0.5f;

[SerializeField]
ClipState.Serializable animation = ClipAsset;
animancer.Transition(animation);
```

### Glossary

- State/AnimancerState
  - AnimatorController/AnimancerPlayable graph的一个节点Node
  - 管理当前播放的AnimationClip的细节，例如它的当前时间，混合权重
- Animation Layer
  - 一组共享同一个目的的states（AnimationClips）
  - 每个layer在一个时间可以位于一个状态
  - Additive或Override更低数字的states的效果
- Blend Tree/Mixer
  - 一种特殊的状态类型，使用多个state作为输入，通过一个参数在所有state给出的数据中做混合插值
- Port
  - An array index
  - 每个AnimancerState连接在它Parent节点（一个Layer或一个Mixer）的一个特定PortIndex
