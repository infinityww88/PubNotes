动画是一个 poses 的序列 sequence，poses 被存储为 keyframes。当动画播放时，它在定义的 poses 之间平滑地插值，来创建一个流畅的动作。

Pose Editor 提供了将 GameObject 设置到不同 poses 的所有工具，来为动画创建 key frames。

Clip Editor 提供编辑一个一个 Property 的 frame 和 value 的功能。但是复杂动画 的 keyframe 是以 pose 为单位的。每个 pose 就是一组 bone 的 keyframe 的组合。在 ClipEditor 中手动编辑 pose 的每个 bone 是非常繁琐的。Pose Editor 就是用来方便地设置骨骼的 pose，然后将它们一键添加到关键帧。

Pose Editor 用来方便地编辑一个 pose 的 bones，然后将它们加入到关键帧。Clip Editor 用来调整关键帧的时间（frame）。

## Animated GameObject

Pose Editor 最上面的字段中，应该选择一个被动画的 GameObject。被动画的 GameObject 用于编辑和预览一个动画。

有两种方法为 Pose Editor 指定一个 animated GameObject：

- 从 Unity Hierarchy window 拖拽一个 GameObject 到 Pose Editor 中
- 通过字段旁边的 object selector

Animated GameObject 的 bones 和 transforms 需要匹配当前项目中定义的那些（通过路径名，或者通过 avater）。

当创建一个新的 UMotion project 并首次指定一个 animated GameObject 时，会创建一个用于这个 GameObject 所有 bones/transforms 的默认配置。

这些骨骼配置是 UMotion project 的一部分。

重要：当一个 animated GameObject 被指定给 Pose Editor，就不能通过鼠标点击在 Scene View 中选择任何其他的 GameObject 了。为了选择其他的 GameObject，它们需要在 Unity Hierarchy Window 中选择。Animated GameObject 的 parent 或 child 都不能选择。

点击 Clear 按钮，animated GameObject 将从 Pose Editor 中移除，它的原始值将被恢复。

通过点击 Clear 旁边的 Dropdown 箭头可以从 Pose Editor 中移除 GameObject 但在 scene 中保持当前 pose。

## UMotion Lock

当选择一个 animated GameObject，它自动附加一个 UMotion Lock。这个组件保存 GameObject 的原始状态，并准备将它用于 UMotion。一旦 animated GameObject 从 Pose Editor 中移除，UMotion Lock 被销毁并自动恢复 GameObject 的原始状态。

通过选择 GameObject 并在 UMotion Lock 组件的 Inspector 中点击 Unlock 按钮，GameObject 可以手动 unlock（这在 UMotion crash 时可能有用）

## Edit Modes

Pose Editor 有两个编辑模式（创建 pose & 配置 rig）

- Pose Mode：用于为 clip 创建 poses
- Config Mode：用于配置 animation rig（例如 3D 模型的骨骼）
