## Inspector

AnimancerComponent 应该被挂载到 Animator 相同的 object 上，使得它们可以同时被 activate 或 deactivate。这还允许 AnimancerComponent 自动获得 Animator 的引用而不必手动在 Inspector 上设置。一旦 reference 被赋值，它还自动收拢 Animantor 的 Inspector，并显示 Animancer 引用相关的字段。

![AnimancerComponent](../../../Image/AnimancerComponent.png)

- Controller 字段没有显示，因为 Animancer 不使用它
- 由于 Unity 的 Bug，在运行时将 Update Mode 改变为 AnimatorUpdateMode.AnimatePhysics 或从其改变，不会有效并且在 Inspector 显示一个 Inspector
- Action On Disable 字段确定当 AnimancerComponent 或它所在的 GameObject 被 disable 时将发生什么

如果找不到 Animator 引用，或丢失，Inspector 将会显示一个 warning，点击它可以快速在 object 的 parents 或 children 搜索 Animator 组件。

## Animation Details

Inspector 会实时以各种控制和 context menu 显示 State 和 Layers 的细节

不像 Animator window 被用来设置 Animator Controllers，Animancer 组件不用来手动配置 states 和 transitions。它们都是通过脚本来完成，因此 panel 只用来调试和测试。

通常它只在 Play Mode 中出现，但是如果脚本在 Edit Mode 中播放动画，它工作起来是一样的。

![live-inspector](../../../Image/live-inspector.png)

1. Weight 指示每个 animation 影响最终 Blending 结果的程度
2. 每个 state 有一个 foldout arrow 可以扩展显示它的细节
3. 一个绿色的 bar 指示每个当前播放的动画的进度。当动画暂停时变成黄色
4. 当细节被扩展显示，精确的播放时间显示为 slider 并让你可以手动控制，一个 multiplier label 指示它循环了多少次，N 按钮在 AnimancerState.Time 和 AnimancerState.NormalizedTime 之间切换显示
5. 细节还包含这个 state 其他各种重要的 values。每个 controls 对应 AnimancerState 中相同名字的属性，可以通过 code 访问它们

## Controls

- Ctrl + Click 一个 animation 来 Cross Fade 到它
- 再按住 Shift 则会 queue 这个 animation，在当前 animation 完成时 fade 它
- 你可以拖放任何 AnimationClip 到 AnimancerComponent Inspector 来为它创建一个 State

## Context Menus

右键点击 Inspector 中的任何 state，将会打开一个 context menu，其中包含各种有用的功能：

- Play 并 Cross Fade 播放 target state。Ctrl + Click 一个 animation 将会触发一个 Cross Fade 而无需打开 menu。这回使用默认的 fade duration(0.25s)
- 如果有 End Event 注册，End Event sub-menu 显示它的细节
- Inverse Kinematics sub-menu 允许你 enable 和 disable Inverse Kinematics
- Toggle Looping 切换 Motion.isLooping flag 为 true 或 false。这个功能为所有 selected animations 一次性应用，这很有用，因为你不能同时编辑多个 AnimationClip
- Toggle Legacy 切换 AnimationClip.legacy 为 true 和 false
- New Locked Inspector and Watch are added by Inspector Gadgets

## Animation Types

- Humanoid

  由于 Unity 的 Humanoid Animation Retargeting 系统，任何 Humanoid animation 可以被播放在 Humanoid character 上

- Generic

  Generic animations 比 Humanoid 更高效，但是不支持 retargeting，并且只能在它们制作的特定 hierarchy 上被播放

- Sprite

  Sprite animations 实际上就是 Generic animations，只是它恰好控制 SpriteRenderer.sprite 而不是旋转 bones
