# Mixers

Mixers 的作用和 Mecanim Blend Trees 相同，它们允许你基于一个参数 blend 多个动画。例如，你可以基于角色的移动速度（例如 player 推动游戏杆的程度）在 Idle，Walk，和 Run 之间 Blend，使得它们可以以任何速度合适的 animate，而不是只能以特定速度移动。

Linear Blending 例子展示了如何使用 Mixers 和 Blend Trees.

![linear-blending](../../../Image/linear-blending.gif)

Mixers 通常在 Inspector 中使用 Transitions 设置，但是它们也可以被手动创建。

![mixer-inspector](../../../Image/mixer-inspector.png)

## Choosing a Mixer

有很多不同的 mixer 类型，并且你可以继承任何一个创建自己的类型

| Mixer Type | Parameter / Thresholds | Interpolation Algorithm | Equivalent Blend Tree |
| --- | --- | --- | --- |
| ManualMixerState | none | Manual Weights | Direct |
| LinearMixerState | float | Linear O(n) | 1D |
| CartesianMixerState | Vector2 | Gradient Band O(n2) | 2D Freeform Cartesian |
| DirectionalMixerState | Vector2 | Polar Gradient Band O(n2) | 2D Freeform Directional |
| | | | |

ManualMixerStates 允许你简单地手动控制每个 state 的 AnimancerNode.Weight，而没有任何自动的计算。这通常用于 additive animations，以及为面部表情之类的东西 blend shapes。

其他 mixers 有一个 Parameter 属性和 Thresholds 数组，它们被用来为你计算每个 state 的 weight。当 Parameter 完全等于一个特定阈值时，对应的 state 将会具有 weight = 1，当 Parameter values 在 Thresholds 之间时，将会基于使用的插值算法计算一个小数 weights。你可以手动指定这些 thresholds，或者为 MixerState\<T>.CalculateThresholds 提供一个自定义计算 Delegate。对于基于 Vector2 mixers（Cartesian 和 Directional），你还可以使用 AnimancerUtilities.CalculateThresholdsFromAverageVelocityXZ extension 方法。

当选择一个 2D mixer 时，对于那些那些表示方向的动画（forward/back/left/right），Directional 通常比 Cartesian 提供更好的插值。还要注意如果两个 state 之间有 180 度或更大的区域（转向），interpolation 将会是 ill-defined 的，并且将会得到不希望的结果。例如，如果你有 forward，back，left 的 clips，但是没有 right，则如果你设置 parameter 为 right，你将会得到奇怪的结果。

MixerStates 是一种 AnimancerState 类型，具有其他一些与常规 ClipStates 的区别：

- Clip 属性总是返回 null
- MixerState 中的 States 通常不注册在内部的字典（它只用于用户需要访问的 states）中。如果你需要直接访问这些 state，必须通过它们在 mixer 中的 index。所有内置的 mixers 将它们的 states 暴露为 array

## Manual Creation

如果你不想使用一个 Mixer Transition，你可以自己使用 code 创建：

1. 从上面的 table 中选择一个 mixer 类型，并生成一个新的 mixer。例如 new LinearMixerState
2. 调用 mixer 的一个初始化方法：
  - Initialize(portCount) 分配指定数量 states 的空间，其可以单独地使用 CreateChild 或将 mixer 传递给任何 state 类型的构造函数或 SetParent 方法来填充。这甚至让你彼此嵌套 mixers（子树的子树）
  - Initialize(clips, thresholds) 为每个 clips 分配一个 ClipState，并赋值它们各自的 thresholds
3. 确保所有 states 被赋予 thresholds，来确定它们将被使用时的 parameter values 以及它们将会如何相对于其他 states 进行 blend。这可以通过在 Initialize 和 CreateChild 方法中使用可选参数完成，或者通过调用 SetThreshold 或 SetThresholds 完成
4. 可选地调用 SetName 给它一个描述性名字显示在 Inspector 中
5. 存储一个 mixer 的 reference 使你之后可以设置它的 Parameter 来控制它的 blending

下面的 script 使用一个 LinearMixerState 基于一个 Inspector 中的 Movement Speed slider 在 Idle 和 Run 动画之间混合

```C#
using Animancer;
using UnityEngine;

public sealed class LinearMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Idle;
    [SerializeField] private AnimationClip _Run;

    [SerializeField, Range(0, 1)]
    private float _MovementSpeed;

    // Keep the mixer after is is created so we can change the Parameter later.
    private LinearMixerState _MovementMixer;

    private void Awake()
    {
        // 创建一个新的 mixer 并连接它到 default layer
        _MovementMixer = new LinearMixerState();

        // 我们可以在 Initialise 调用中指定自定义的 thresholds
        // 但是既然我们没有这么做，它将会分别使用 0 和 1
        // 其他 overloads 使用 3 个 clips，或者一个任意数量的 clips
        _MovementMixer.Initialise(_Idle, _Run);

        // 通常，synchronisation 非常适合移动，因此你应该为 idle 关闭它
        // 还有因为只有一个其他的 state，因此反正它也没有任何东西可 sync
        // 查看 Optional Synchronisation
        _MovementMixer.DontSynchroniseChildren();

        // 可选地使用一个 key 注册 mixer，使它可以在脚本中使用那个 key 来访问

        // 使用字符串作 key
        _MovementMixer.Key = "Movement Mixer";
        // 其他脚本可以这样访问:
        // var state = _Animancer["Movement Mixer"];
        // _Animancer.Play("Movement Mixer");

        // 或者使用脚本自身作为 key
        _MovementMixer.Key = this;
        // 可以让其他具有这个脚本引用的脚本这样访问:
        // LinearMixerExample example;
        // var state = _Animancer[example];
        // _Animancer.Play(example);

        // 就像一个常规的 clip 一样播放 mixer
        _Animancer.Play(_MovementMixer);
    }

    private void Update()
    {
        // 设置 mixer 的参数来控制它的当前 blending
        _MovementMixer.Parameter = _MovementSpeed;
    }
}
```

![manual-mixer-example](../../../Image/manual-mixer-example.gif)

### Nesting

Mixers 可以拥有任何类型的 state 作为它们的 children，包括其他 mixers（子树）：

1. 使用 mixer.Initialise(portCount) 来指定想要的 state 的数量
2. 将想要的 mixers 放在 mixers.States 数组中形成嵌套的 mixers
3. 使用 mixer.SetThreshold（或者任何其他 threshold 方法）来指定你想它们开始 blend 的 parameter values

例如，如果你有 mixers 用于任何方向的移动，包括正常的移动和受伤时的移动，你可以同时将二者放在另一个 mixer 以允许你 blend 受伤的 level（在正常的移动和受伤的移动之间混合）。

```C#
using Animancer;
using UnityEngine;

public sealed class NestedMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private MixerState.Transition2D _RegularMovement;
    [SerializeField] private MixerState.Transition2D _InjuredMovement;

    [SerializeField, Range(0, 1)]
    private float _InjuryLevel;

    [SerializeField, Range(-1, 1)]
    private float _MovementX;

    [SerializeField, Range(-1, 1)]
    private float _MovementY;

    private LinearMixerState _MovementMixer;

    private void Awake()
    {
        _MovementMixer = new LinearMixerState();

        // 分配 2 个 child states
        _MovementMixer.Initialise(2);
        _MovementMixer.SetName("Movement Mixer");

        // 从 _RegularMovement transition 创建 state 并连接它到 port 0
        var state = _RegularMovement.CreateState();
        state.SetName("Regular Movement");
        _MovementMixer.CreateChild(0, state, 0);

        // 从 _InjuredMovement transition 创建 state 并连接它到 port 1
        var state = _InjuredMovement.CreateState();
        state.SetName("Injured Movement");
        _MovementMixer.CreateChild(0, state, 0);

        _Animancer.Play(_MovementMixer);
    }

    private void Update()
    {
        _MovementMixer.Parameter = _InjuryLevel;

        var movement = new Vector2(_MovementX, _MovementY);
        _RegularMovement.State.Parameter = movement;
        _InjuredMovement.State.Parameter = movement;
    }
}
```

## Smoothing

设置一个 mixer 的 Parameter 将会立即改变它的 blending，但是根据你如何控制它，有几种方式你可以随时间平滑地完成。

### Variable Target

如果 target value 可以常量地改变，则你可以简单地使用 MoveTowards 函数向着 target value 每帧移动 Parameter。例如，如果你正基于来自 joystick 的用户输入控制一个 movement mixer，则你可能想要限制角色可以多块的从一个方向 snap 到另一个方向。

- 1D

  Mathf.MoveTowards

  ```C#
  // How fast the parameter changes.
  [SerializeField] private float _BlendSpeed;
  
  private LinearMixerState _Mixer;
  
  private void Update()
  {
      var input = Input.GetAxisRaw("Vertical");
  
      _Mixer.Parameter = Mathf.MoveTowards(
          _Mixer.Parameter,
          input,
          _BlendSpeed * Time.deltaTime);
  }
  ```
- 2D

  Vector2.MoveTowards

  ```C#
  // How fast the parameter changes.
  [SerializeField] private float _BlendSpeed;
  
  // A Cartesian or Directional Mixer.
  private MixerState<Vector2> _Mixer;
  
  private void Update()
  {
      var input = new Vector2(
          Input.GetAxisRaw("Horizontal"),
          Input.GetAxisRaw("Vertical"));
  
      _Mixer.Parameter = Vector2.MoveTowards(
          _Mixer.Parameter,
          input,
          _BlendSpeed * Time.deltaTime);
  }
  ```

### Fixed Target

如果你只想为 mixer 设置 target value 并靠它自己向 target 移动，则你可以使用 MixerParameterTweenFloat (for 1D Mixers) 或 MixerParameterTweenVector2 (for 2D Mixers):

```C#
[SerializeField] private AnimancerComponent _Animancer;
[SerializeField] private LinearMixerState.Transition _Mixer;

private MixerParameterTweenFloat _MixerTween;

private void Awake()
{
    _Animancer.Play(_Mixer);

    // 使用它将控制的 Mixer 初始化 tween
    _MixerTween = new MixerParameterTweenFloat(_Mixer.State);
}

public void BlendMixerParameter(float parameter, float duration)
{
    // Start interpolating the Mixer parameter.
    _MixerTween.Start(parameter, duration);
}
```

这将会向着指定参数每帧移动 _Mixer.Parameter，然后在 duration 的结束时到达它。你可以再次调用 Start 来中断前面的 target，但是如果你频繁地这样做，则上面描述的 Variable Target 方式（手动 Move 参数）。

## Blend Trees vs. Mixers

Animancer 的 Mixers 和 Mecanim 的 Blend Trees（它可以使用 Parameter Controller States 被播放）用于相同的目的，然而它们的实现有显著的不同：

| Operation | Mixers | Blend Trees |
| --- | --- | --- |
| 创建 | 运行时动态 | 在 Unity Editor 中手动 |
| 修改 | 创建后可以自由修改 | 运行时不可修改 |
| 细节 | 你可以直接访问独立状态的细节 | 你没有对任何内部细节的访问 |
| 同步 Synchronisation | 仅时间同步，并且你可以控制哪些 states 被同步 | Time and Foot Phase Synchronisation, 当时总是用于所有 states |
| 定制 Customisation | 你可以创建自己的 mixer types，继承自任何现有类型来实现自定义 blending 算法，或者其他功能 | None |

## Synchronisation

当 mixing 不同长度的 animations，如果正常播放它们将会不同步。例如，它有可能导致一个 Walk animation 的左脚在地上，而 Run animation 的右脚在地上，此时一个简单地在它们之间插值将会导致一个不真实的结果。这会导致下面示例中当 speed slider 在 75% 时显示的明显的问题（由 Linear Blending 示例调整而来）。这个问题的解决方案是同步每个 states 的时间，使得它们总是在等价的 poses 上。

![synchronisation](../../../Image/synchronisation.gif)

- No Synchronisation

  所有 animations 独立地播放。

  ![unsynced-inspector](../../../Image/unsynced-inspector.gif)

- 同步 Walk and Run

  Walk 和 Run 保持在相同的 NormalizedTime。

  ![synced-inspector](../../../Image/synced-inspector.gif)

为所有 states 开启 time synchronization 将给出和 Blend Tree 相似的效果。

可选的同步

    同步适合于移动，但是通常应该对 Idle 动画关闭

Blend Trees 总是同步它们的 states（动画长度），然而这不总是理想的，因此 Mixers 允许你选择哪些 states 被同步。这个问题可以在上面的动态图中 Blend Tree character 看到，当它 blends Idle 和 Walk(当 slider 在中心的左边)。因为 Idle 动画比 Walk 长的多，同步它们导致 Walk 比它正常慢得非常多，因此角色几乎根本不移动，知道 speed 超过 50%，它开始 blending Walk 和 Run。解决方案是简单地不去同步 Idle 动画，因为它的 poses 没有 Walk 动画中任何时间的相应 poses（这也是为什么 Mixer 角色在低速情况下给出更好的结果）。

当使用一个 Mixer Transition，Inspector 右边的 Sync 开关允许你选择哪些状态被同步。

在 code 中，你可以像这样控制 child 同步：

```C#
// Reference whatever mixer you are using.
// This could be the _MovementMixer from the Manual Creation example above.
MixerState mixer;

// 默认，所有 children 都被同步，但是如果想要你可以阻止这样
// 注意这只影响设置它之后添加到 mixer 的 children
// Note that this only affects children added to a mixer after you set it.
MixerState.AutoSynchroniseChildren = false;

// 为所有 children 关闭同步
mixer.DontSynchroniseChildren();

// 或者关闭一个指定的 child
mixer.DontSynchronise(mixer.GetChild(0));

// 或者为指定的 child 开启它（如果你设置 AutoSynchroniseChildren = false）
mixer.Synchronise(mixer.GetChild(1));
```

### Foot Phase Synchronisation

Blend Trees 还为 Humanoid animations 使用一个更复杂的同步技术，称为 Foot Phase Synchronization。本质上，每个动画被分解成 phases（right foot down，right foot up，等等）使得它可以正确支持具有不规则 walk cycles 的动画，例如一个带有四肢和包含不同数量的 walk cycles 的角色。

有可能在 Mixers 中实现 Foot Phase Synchronization（并且你可以通过继承任何现有 mixer 类型自己实现），但是 Unity 的实现没有公开暴露出来，因此它需要整体从头开始重新实现。它会需要在 Unity Editor 中分析 AnimationClips 来确定它们的 phases，因为它们的曲线不能再运行时访问，然后还会需要更多的逻辑基于那些分析在运行时调整速度。这有可能在将来添加到 Animancer，但是现在已经确定的是需要花费大量的 effort 来得到已经在 Blend Tree 中可以完成的功能。

