# Events

你经常会需要在一个 animation 中特定时刻做一些事情，例如：

- 在 walk cycle 中，每次 foot 接触 ground 时播放 footstep 声音
- 当回甘经过一个特定的 point 时 hit 一个高尔夫球

你可以使用 coroutines 或其他 timers 使用脚本完成这些事情，但是使用 Unity 的 inbuilt Animaiton Events 或 Animancer 的自定义 event system 允许在配置 events 时预览 animation 使你可以轻易地配置你想要的准确时间。下面的表格总结了两个事件系统的区别。

| Animation Events | Animancer Events |
| --- | --- |
| Unity 内置，有没有 Animancer 工作都是相同的 | End Events，设置一个 custom end time |
| Animation Events 被定义为一个 AnimationClip 的一部分，因此每个使用那个 clip 的 state 会具有相同的 events | Animancer Events 定义为 AnimancerState 的一部分，因此每个 AnimancerState可以具有不同的 events 而不管它们使用的是什么 Animaitonclip. 如果你想共享一个事件集合，你可以简单地在一个共享的位置上定义它们，例如使用一个 Transition Asset |
| 每个 Animation Event 调用一个必须位于同一个 GameObject 上的方法 | 默认地，UnityEvents 用于在 Inspector 中配置 Animancer Events，因此它们可以调用任何它们可以引用的 object 上的方法，并且每个 event 可以调用任意多的方法  |
| 如果你不想其他脚本手动调用事件方法，它可以是 private 的 | UnityEvents 只能调用 public 方法。但是 system 可以被设置使用 UltEvents，它支持 private 升值 static 方法 |
| 方法最多只能有一个参数，类型只能是：float，int，string，UnityEngine.Object，或者 AnimationEvent 它包含每种类型一个字段以及一些其他的细节 | 如果使用 UltEvents，它可以调用任何数量的上面类型以及 Enum，Vector2/3/4，Quaternion，Rect，Color，和 Color32 类型的参数。它们还可以调用一个方法，并使用它的返回值作为另一个方法的参数 |
| Animation Events 不是很高效，因为它们使用类似 GameObject.SendMessage 的机制，并且如果 event 有一个 string 或 AnimationEvent 参数，它每次被触发时还会创建 Garbage，这可能是潜在的性能问题 | Animancer Events 更加高效因为它们使用 C# Delegates。在 Inspector 中使用 UnityEvents 配置的 Animancer Events 不会分配 Garbage。UltEvent 通常也是如此，除了在特定情境下，例如当一个方法返回一个 value type （会触发 boxing）（尽管 UnityEvents 简单地不能调用这样的方法） |
| Animation Events 可以使用 code 添加，但是它们还是具有上面列出的所有限制。如果你正在使用一个 Animator Controller，你甚至不能在一个特定 state 被播放之前访问它的 AnimationClip  | Animancer Events 可以使用 Delegates 被添加，例如 state.Events.Add(0.5f, () => Debug.Log("Event Triggered")); |
| Methods 通过 Magic Strings 引用。新的 Unity versions 使用一个 dropdown menu 来选择这个 method 而不是一个 text field 来手动输入名字，但是一旦选择的 name 仍然存储为 string，因此这个方法被重命名了，Animation Event 不会自动更新为新的名字。 | 当 你在 Inspector 中配置它们，UnityEvents 和 UltEvents 就像 Animation Events 一样使用 strings，但是当使用 code 添加 Animancer Events 时，就不会涉及 strings 了。它甚至可以用于在 Inspector 中配置 event times 因此你可以预览模型在那个时刻模型看起来如何，但是将真实事件保留为空，并使用 code 设置它 |
| Animation Events 系统有一些已知的 Bugs，只能等待 Unity 定位并在新版本修复它们 | 当前 Animancer Events system 没有已知的 bugs，给你钱包含源代码，允许任何 bus 被快速发现并修复，不需要等待 Assset Store 更新 |
|||

- Animation Events

  Unity's inbuilt Animation Event system.

- Animancer Events

  Animancer's custom event system.

- End Events

  你开始一个 animation 之后，你经常想要等待它完成再做一些事情，因此 Animancer 有几种方式来实现它。
  
  