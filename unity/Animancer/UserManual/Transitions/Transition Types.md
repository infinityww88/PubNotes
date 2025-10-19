# Transition Types

## Transition Assets

每个 transition 类型还有一个关联的具有一个 transition 字段（没有其他）的 ScriptableObject 类型，使得你可以创建它们为 assets 在 project 中共享一个 transition，而不是每个 object 有它自己的 transition。**Transition 只是一个包含 transition 信息的数据结构。这些信息和具体的动画无关，只包含时间、事件、速度等数据。因此 Transition 只是一个数据集合**。它们都遵循相同的命名约定：

| Class | Description |
| --- | --- |
| ClipState | 最常见的 State 类型。管理 AnimationClip 的运行时细节，例如 Time，Speed，Evengts 等等 |
| ClipState.Transition | 一个 serializable class，允许上面的细节在 Inspector 中定义，并在运行时将创建一个 ClipState |
| ClipTransition | 一个 transition asset（ScriptableObject），包含一个 ClipState.Transition 字段 |

- 你可以使用 Assets/Create/Animancer 菜单中的功能创建 transition asset
- Transition.State 属性通常让你访问被 transition 创建的 state，但是重要的一点是因为 transition assets 通常被多个 objects 使用，这个属性将会只保存最近的 played state 的引用

### 常规 Transition：

```C#
using Animancer;
using UnityEngine;

public class TransitionExample : MonoBehaviour
{
    [SerializeField] 
    private ClipState.Transition _Animation;
}
```

![regular-transition](../../../Image/regular-transition.gif)

当使用一个常规的 transition 字段，它是 script 的一部分，使得 script 的每个 instance 将会有自己的 transition 数据。

### Transition Asset

```C#
using Animancer;
using UnityEngine;

public class TransitionExample : MonoBehaviour
{
    [SerializeField] 
    private ClipTransition _Animation; // 包含一个 ClipState.Transition
}
```

![transition-asset](../../../Image/transition-asset.gif)

使用 transition asset，你需要为你应用的字段创建一个单独的 asset，但是之后 project 的任何东西都可以应用这个 asset 以使用相同的 transition settings（Transition 只是包含 transition 的信息的数据结构）。

## Basic Transitions

- AnimancerState.Transition\<TState>

  所有其他 transitions 的抽象基类。只有一个 FadeDuration 字段

- ClipState.Transition

  继承 AnimancerState.Transition\<TState> 并创建一个 ClipState

   ![ClipStateTransition](../../../Image/ClipStateTransition.png)

- PlayableAssetState.Transition

  继承 AnimancerState.Transition\<TState> 并创建一个 PlayableAssetState。具有和 ClipState.Transition 相似的字段，以及一个额外的 Bindings 数组

  ![playable-asset](../../../Image/playable-asset.png)

## Mixer Transitions

这些 transitions 创建各种类型的 Mixer States。它们都使用可重排列 reorderable lists 来配置它们的状态。你可以右键点击任何 transition fields 来打开一个 context menu 使用一些有用的功能。

- ManualMixerState.Transition\<TMixer>

  抽象基类，用于创建派生自 ManualMixerState 的 state 的 transition

- ManualMixerState.Transition

  创建自 ManualMixerState.Transition<ManualMixerState> 并会创建一个 ManualMixerState

  ![manual-mixer](../../../Image/manual-mixer.png)

- MixerState.Transition\<TMixer, TParameter>

  抽象基类，用于创建派生自 MixerState 的 state 的 transition。具有一个 Thresholds 数组和 DefaultParameter 字段

- LinearMixerState.Transition

  继承自 MixerState.Transition\<LinearMixerState,float> 并会创建一个 LinearMixerState.

  ![linear-mixer](../../../Image/linear-mixer.png)

- MixerState.Transition2D

  继承自 MixerState.Transition\<MixerState\<Vector2>, Vector2> 并会根据选择的 Type 创建一个 CartesianMixerState 或 DirectionalMixerState 

  ![mixer-2d](../../../Image/mixer-2d.png)

## Controller Transitions

- ControllerState.Transition\<TState>

  抽象基类，用于创建派生自 ControllerState 的 state 的 transitions

- ControllerState.Transition

  继承 ControllerState.Transition\<ControllerState> 将会创建一个基本的 ControllerState

  ![controller](../../../Image/controller.png)

- Float1/2/3ControllerState.Transition

  派生自 ControllerState.Transition\<Float1ControllerState> 并添加一个 ParameterName 字段，将会创建一个 Float1/2/3ControllerState，它包装这个特定的 parameter。一旦 Animator Controller 被赋值，Parameter Name 字段允许你选择任何 Float parameter 的名字。

  ![float-1-controller](../../../Image/float-1-controller.png)

## Custom Transitions

你可以创建自己的 transitions，通过从开始实现 ITransition，或者从 AnimancerState.Transition 继承。这样做时，你可能想要通过在你继承的 Transition 中创建另一个继承自 Drawer class，或者实现你自己的 PropertyDrawer，来修改它在 Inspector 上绘制的方式，
