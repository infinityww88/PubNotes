# Layers

当播放一个动画时，它停止所有其他动画（或者 Fade out 它们）。更具体地说，它停止指定 layers 上所有的 animations，而不影响其他 layers 上的动画。

一个 layers 就是一个 playable graph 的 node 子树，停止一个 layer 就是将子树 root node 的 weight 变为 0.

这允许你同时播放多个分离的动画，每个 layer 控制身体的不同部分，使用 layers 来决定它们如何形成最终的 output。

大多数涉及 layers 的操作通过 AnimancerComponent.Layers 属性访问。

```C#
AnimancerComponent animancer;
AnimationClip clip;

// 在默认的 layer 0 创建一个 state 并播放它
// 如果那个 animation 的 state 以及存在，将它保留在当前 layer
animancer.Play(clip);

// 在 layer 1 上创建一个 state 并播放它
// 如果那个 animation 的 state 以及存在，将它移动到 layher 1
// 如果 layer 1 还不存在，访问 Layers[1] 将会创建它
animancer.Layers[1].Play(clip);
```

下面的例子显示了这个功能。如果 Action 在 character 是 idle 时被执行，它在默认的 layer 上被播放使得它可以控制整个身体。但是如果它是在 Run animation 播放时被执行，则 Action 在另一个 layer 上被播放，layer 被 masked 使得只影响 upper body（只输出 upper body 的数据），使得 legs 继续运行而 upper body 独立地运动。

![layers](../../../Image/layers.gif)

细节

- Max Layer Count：如果你指定一个不存在的 layer，它将会自动创建（以及它之前的每个 layer，就是 graph 中一个连接到 output 的子树，不过每个子树都是空的）。默认地，如果试图创建超过 4 个 layer，Animancer 将会抛出一个 ArgumentOutOfRangeException。但是这只是一个一般的安全措施，因为绝大多数情况下不需要这么多的 layer（通常只是上下身两个 layer）。如果你真的需要更多 layers，你可以简单地设置 AnimancerCmponent.Layers.Capacity 为一个更高的值（或者考虑设置 static AnimancerPlayable.LayerList.defaultCapacity 或使用 SetMinDefaultCapacity）
- Changing Layers：如果一个 animation 的 AnimancerState 已经存在，而你指定了一个不同的 layer，这个 state 将会移动到那个 layer（子树）中。还可以通过直接设置 AnimancerState.LayerIndex 属性将 state 移动到一个不同的 layer
- Names：可以在一个 Layer 上调用 SetName 来给它一个展示在 Inspector 上的名字，但是这些名字不存在于运行时，因此任何对这个方法的调用在运行时都会被排除编译
- 如果想要在多个 layers 上同时播放一个动画，需要为这个动画创建多个 states，并使用不同的 dictionary keys 注册它们（或者根本不注册它们，只是简单地引用它们）

Animancer 创建一个 state 时，state 就会存在 playable graph 中，但是 Animancer 可选地在内部用字典引用这些状态，也可以不依赖字典引用，而是使用脚本自己去引用，但是无论如何 state 都存在于 playable graph 上。

## Blending

有一些因素可以决定每个 layer 的 output 如何组合形成最终的 result：

- Weight：每个 layer 有一个 Weight，就像 AnimancerState，而且你可以使用 StartFade 方法（指定一个 target weight 和一个 duration）来 fade in/out 它们
  - StartFade 只影响你调用时所在的 layer 上，而且对于 layers 没有 CrossFade，因为通常不使用这种方法交互它们，但是你可以简单地 fade in 一个 layer，同时 fade out 其他的 layers
  - Layers 默认以 Weight = 0 开始。然而，对 0 layer 调用 AnimancerComponent.Play（播放动画） 会自动设置它的 Weight = 1. 类似的，Cross Fading 会自动地立即以 Weight = 1 播放 animation，并且 fade in 这个 layer 而不是 fading 这个动画
  - 如果你想要一个 layer 停止影响最终的 output，可以简单地 fade 它的 weight 为 0（或者直接设置 Weight = 0，立即完成）
- Masks：每个 layer 可以被赋予一个 AvatarMask，来确定它影响哪些 bones。可以使用 Assets/Create/Avatar Mask menu 函数创建一个 mask，然后使用 AnimancerComponent.Layers.SetMask 将它赋予一个 layer，使得那个 layer 上的动画只影响模型中被 mask 包含的部分
- Additive Blending：默认地，每个 layer 将会覆盖之前的 layer，完全替换它的 output。但是使用 AnimancerComponent.Layers.IsAdditive 你可以使一个 layer 添加它的动画到之前 layer 的上面。
