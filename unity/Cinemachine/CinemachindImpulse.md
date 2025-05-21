Cinemachind Impulse 在响应游戏事件时产生和管理 camera shake。例如当一个 GameObject 和另一个碰撞时，或当场景中一些东西爆炸时，可以使用 Impulse 使 CinemachineCamera shake。

Impulse 有两部分：

- Impulse Source：一个组件，它发射信号，信号产生于场景中的一个点，并向外传播，非常类似声波或冲击波。这种发射被游戏事件触发。

  信号包含一个方向，一个 curve 指示信号的强度（作为关于时间的函数）。它们一起有效定义了要给沿着特定轴的 shake，持续特定时间。这个 shake 从原点向外传递，当它到达一个 Impulse Listener 的位置，然后 Listener 可以响应它。

- Impulse Listener

  一个 Cinemachine extension 允许 CinemachineCamera 听见一个 impulse，然后通过 shake 来响应它。

  一个 impulse 是一个发射信号的 Impulse Source 的事件。Collisions 和 events 触发 trigger impulses，Impulse Sources 产生 impulses，然后 Impulse Listeners 响应 impulses。

在场景中设置和使用 Impulse：

- 添加 Cinemachine Impulse Source 或 Cinemachine Collision Impulse Source 组件到一个或多个你想要触发 camera shake 的 GameObjects。
- 添加 Cinemachine Impulse Listener extension 到一个或多个 Cinemachine CinemachineCameras，这样它们可以检测和响应 impulses。

### Cinemachine Impulse Sources

Impulse Source 是一个组件，它从场景中的一个位置发射一个震动信号。Game Events 可以让一个 Impulse Source 从事件发生的地点发生一个信号。这个 event 触发 impulses，Impulse Source 产生 impulses。带有 Impulse Listener  extension 的 CinemachineCameras 通过 shaking 响应 impulses。

Cinemachine Collision 提供了两种类型的 Impulse Source 组件：

- Cinemachine Collision Impulse Source：响应 collisions 和 trigger zones 时产生 impulses。
- Cinemachine Impulse Source：响应 collisions 以外的事件时产生 impulses。

场景中可以有多个 Impulse Sources，例如：

- 在巨人的每个脚上有一个 Impulse Source，它 giant 行走时每一步接触地面产生一个 shake
- 当抛射物碰撞到目标爆炸时触发 shake

默认，一个 Impulse Source 影响范围内每个 Impulse Listener，但是可以应用 channel filtering 来使 Sources 只影响一些 Listeners 而不影响其他。

### 关键 Impulse Source 属性

震动信号定义了 camera shake 的基本形状，Impulse Source 控制 impulses 其他一些重要属性。

## 过滤 impulses

Filtering 让你精细调整如何以及何时 Impulse Source 产生 impulses。Cinemachine Impulse 允许两种类型的 filtering：

- 使用 channel filtering，Impulse Listener 只响应特定 Impulse Sources，而无视其他
- 使用 Trigger Object Filtering，只有特定 GameObject 可以触发 impulse

### Filtering with channels

默认每个 Impulse Listener 响应范围内每个 Impulse Source。Channels 允许你精确控制 Impulse Listener 响应哪个 Impulse Sources。

- 设置 channels
- 设置 Impulse Sources 在一个或多个 channels 上广播
- 设置 Impulse Listeners 监听一个或多个 channels

当 Impulse Listener 监听特定 channels，它只响应在那些 channels 广播的 Impulse Sources。

CinemachineImpulseChannels 脚本在场景中创建 channels。默认它只有一个 channel，你可以添加最多 31 个 channels。

### 添加 channels

- Inspect  CinemachineImpulseChannels (Impulse Channel > Edit) 脚本，这可以通过两种方式做到：
  - 在 Cinemachine Impulse Listener inspector 中， 导航到 Channel Mask 下拉菜单，点击它旁边的 Edit 按钮
  - 在 Cinemachine Impulse Source 或 Cinemachine Collision Impulse Source inspector 中，导航到 Impulse Channel 下拉菜单，点击它旁边的 Edit 按钮
- 展开 Impulse Channels 属性 group，设置 Size 属性为 channels 数量。新的 entry 会为每个 channel 创建。
- 重命名 channels

### 设置监听、广播 channels

设置好 channels 后，需要定义你的 Impulse Listeners 和 Impulse Sources 如何使用它们。

- Inspect 每个 Impulse Listener，在 Channel Mask 下拉菜单中选择你想要 listen 的 channel
- Inspect 每个 Impulse Source 或 Collision Impulse Source，在 Impulse Channel 下拉菜单中选择要广播的 channel

可以指定多个 channel，Everything 指定所有 channel，Nothing 清除所有 channel

### 使用 layers 和 tags 过滤

可以使用 Unity 的 Layers 和 Tags 来指定哪些 GameObjects 在碰撞到 Collision Impulse Source 或进入一个 trigger zone 时触发一个 impulse。这称为 Trigger Object Filtering。

Cinemachine Collision Impulse Source 组件有两个 Trigger Object Filter 属性：

- Layer Mask：选择一个或多个 layers，那些 layers 上的 GameObjects 在和 Impulse Source 碰撞时会触发 impulses。Impulse Source 忽略其他 layers 上的 GameObjects 碰撞。
- Ignore Tag：选择一个 tag，带有这个标记的 GameObject 和 Impulse Source 碰撞时不会触发 impulses，即使它们在 Layer Mask 指定的 Layers 中。

