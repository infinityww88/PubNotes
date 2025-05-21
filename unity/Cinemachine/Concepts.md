## Cinemachine 基本元素

- UnityCamera：捕获 scene 中的场景
- Cinemachine Brain 在 Unity Camera 上开启 Cinemachine 功能
- 一个或多个 Cinemachine Cameras 根据它们的状态接手控制 Unity Camera

一个 Cinemachine 设置只能包含一个 Unity Camera，它时唯一从 Scene 捕获 Images 的 Camera。

Unity Camera GameObject 上挂载 Cinemachine Brain 组件，它负责：

- 监控场景中所有的 Cinemachine Cameras
- 决定哪个 Cinemachine Camera 控制 Unity Camera
- 当另一个 Cinemachine Camera 接手控制 Unity Camera，处理过渡

### Cinemachine Cameras

Cinemachine Cameras，之前称为 Virtual Cameras，是 GameObjects，用作准备好接手控制 Unity Camera 的 camera placeholders。

当 Cinemachine Cameras 控制 Unity Camera，它动态 override 后者的属性和行为，这会影响：

- Unity Camera 在 Scene 中的位置
- Unity Camera 对准哪里
- Unity Camera 随时间流逝的行为

### Cinemachine Camera GameObjects

它是与 Unity Camera 不同的 GameObject

- 它们独立运行，并且不能彼此嵌套
- 它们不包含 Camera 组件
- 必须包含 Cinemachine Camera 组件
- 可以包含额外的 Cinemachine Components，来管理过程化运动，以及添加扩展功能

可以根据需要创建多个 Cinemachine Cameras，但是也可以仅通过一个 Cinemachine Camera 完成全部的功能：

- 如果想要 Unity Camera 跟随一个 character，可以使用一个 Cinemachine Camera，并为它设置一个跟随行为。这样这个 Cinemachine Camera 将会是 Unity Camera 唯一的控制器
- 如果项目中在多个地方需要多个 shots，可以为每个 shot 创建一个 Cinemachine，并带有或不带过程化行为。此时，必须理解 Unity 如何处理 Cinemachine Camera 激活和过渡

Cinemachine 鼓励创建多个 Cinemachine Cameras。Cinemachine 虚拟摄像机的设计旨在降低处理器负载。若场景对性能敏感，建议随时停用非必要的虚拟摄像机，以确保最佳运行效率。

## Camera 的控制和过渡

### Cinemachine Camera 状态

任何时间，每个 Cinemachine Camera 位于三个状态之一：Live，Standby，Disabled。但是一个时间，只有一个是 Live 并且控制 Unity Camera，除非当 Blend 发生时。

- Live：Cinemachine Camera 当前控制一个具有 Cinemachine Brain 的 Unity Camera。当从一个 Cinemachine Camera 到下一个 blend 时，两个 Cinemachine  Cameras 都是 live 的。当 blend 结束后，只有一个 Live Cinemachine Camera。
- Standby：Cinemachine Camera 不控制 Unity Camera。但是，它们仍然跟随和瞄准它们的目标，并且更新。Standby 的 Cinemachine Camera，它的 GameObject 是激活的，并且具有一个等于或低于 live Cinemachine Camera 的优先级。
- Disabled：这个状态的 Cinemachine Camera 不控制 Unity Camera，并且不跟随和瞄准它们的目标。它不消耗处理资源。要 disable 一个 Cinemachine Camera，deactive 它的 GameObject。即使 GameObject 被 deactived，如果它处于 blend 中或者仍然被 Timeline 调用，Cinemachine Camera 仍然控制 Unity Camera。

### Live Cinemachine Camera 选择

默认 Cinemachine Brain 负责处理 live Cinemachine Camera 选择。

- Brain 选择优先级最高的 active Cinemachine Camera，并且使它称为 Live 的。
- 如果多个 active CinemachineCameras 共享最高优先级，则最近 activated 的被选择。
- Deactivated 或低优先级 CinemachineCameras，如果它们处于 blend，它们仍然是 Live 的，知道 blend 完成。
- 如果一个具有 Cinemachine tracks 的 Timeline 激活，它覆盖 Brain 的 优先级系统，并且显式驱动和 blend Live Cameras，无视它们的 Priority 和 active state。

可以通过操作 Cinemachine Camera 优先级或者激活失活 GameObjects，来实时响应动态 game events。这对于 live gameplay 尤其有效，因为 action 不能预测。

可以结合使用 Cinemachine 和 Timeline，来编排 Cinemachine Cameras，在可预期的情景中管理 shots，就像 cutscenes。此时，Timeline 覆盖 Cinemachine Brain 优先级系统，这意味着，当一个 Cinemachine Camera Clip 激活时， Cinemachine Cameras  active state 被忽略。Live Cinemachine Camera 选择基于指定的 Cinemachine Camera clips，可以给你精确地，帧到帧的 camera 控制。

### Cinemachine Camera transitions

当一个 Cinemachine Camera 变成 live 时，你可以管理 Cinemachine Camera 的过渡。

设置 Cinemachine Camera transitions 的方式依赖使用 Cinemachine 的上下文：

- 默认，在 Cinemachine Brain 组件中处理 transition rules
- 当使用 Timeline 创建 shot sequencing，在 Timeline Cinemachine track 中直接处理 transitions

#### Blends

Blends 允许通过组合相对简单的 shots，并根据实时游戏事件在它们之间 blend，或者在 Timeline 中精确编排它们，来创建复杂的 camera motion。

Cinemachine blend 不是 fade，wipe，或 dissolve。相反，Cinemachine 从一个 Cinemachine Camera 到下一个，执行一个 position，rotation 以及 Unity Camera 的其他设置的平滑动画，同时考虑保持 target object 的 view 和 Up direction。

Blend 时，两个 Cinemachine Cameras 同时控制 Unity Camera，在预定义好的时间内平滑地交换全部控制。

#### Cuts

一个 cut 是从一个 shot 到另一个 shot 的突然切换。在 Cinemachine 中，两个 Cinemachine Cameras 之间的 cut 对应一个立即完成的 blend，而没有 Cinemachine Camera 属性之间的平滑过渡。

## Procedural Motin

单独使用时，Cinemachine Camera 是一个 passive GameObject，仅作为摄像机的占位符，你可以：

- 放在一个固定位置，并且静态瞄准一个目标
- Parent 到其他 GameObject 来移动和选择它
- 通过脚本操作来移动和旋转它，以及控制它们的 lens

但是，对于更复杂的结果，可以添加过程化行为和扩展到任何 Cinemachine Camera，使它动态移动、震动、跟踪目标、组合它的 shots，来响应用户输入，沿着预定义 path 移动，响应外部冲量信号 Impulse（模拟突然的爆炸效果），产生 post-processing 效果，以及更多。

### Procedural Behaviors and extensions

Cinemachine Camera 组件可以选择很多 behaviors 和扩展，来驱动 Cinemachine Camera 的位置、旋转、lens。

#### Position 和 Rotation 控制

选择和配置 Position Control 和 Rotation Control behaviors，使 Cinemachine Camera 根据一些 constraints 或 criteria 来 move/aim Unity Camera。

大部分可用 behaviors 被设计用来 track 或 look at 要给 target GameObject。可选地，一些 behaviors 支持 user input 来 orbit 或 rotate camera。

通过这些 behaviors，可以：

- 以一个 fixed offset，in orbital，或作为第一第三人称，跟随一个 target
- 组合 shot 并适应 camera 的 postion 和 rotation，来保持 target 在 camera frame 中
- 应用 target position 和 rotation 到 camera，而不是使 target 在 camera frame 中
- 沿着预定义 Spline 移动 camera，来模拟 dolly camera path
- 沿着配置的 pan and tilt axes 旋转 camera

#### Noise

选择和配置 Noise behavior 可以让 Cinemachine Camera Shake，并为 cinematic effect 模拟真实世界的物理相机质量。

在每帧 update 时，Cinemachine 在相机移动之外单独添加 noise，来跟随要给 target。Noise 不影响 camera 在未来帧的位置。这种分离确保诸如 damping 之类的属性如期望工作。

#### Extensions

添加要给 extension 来改变 Cinemachine Camera 的行为来满足更具体和高级的需求。例如 Deoccluder extension 可以将 camera 离开阻碍 camera view 其 target 的 GameObjects。

### Target GameObject tracking

Target GameObject 跟踪是预定义 procedural motion 中的关键元素。Offsets 和 screen compositions 都是特定于与这些 target 的关系的，因此当 targets 在世界中移动时，cameras 调整它们来保持 shot。

默认，一个 Cinemachine Camera 有一个 Tracking Target 属性，它有两个目的：

- 当你定义一个 position control behavior 时，它为 Cinemachine Camera 定义一个 Transform 来一起移动
- 当你定义一个 rotation control behavior 时，它定义了 LookAt target，Transform 将瞄准它

如果你需要为这些目的使用两个不同的 Transforms，选择 Tracking Target 字段右边的 Use Separate LookAt Target 选项。

Target 还跟 Cinemachine 在两个 shots 之间执行 blends 相关。Cinemachine 试图为 target 维持 shot 的期望位置，如果 target 在 shots 之间改变了，Cinemachine 在两个 target 的 positions 之间进行插值。 

如果没有为 camera blend 指定 target，则 Cinemachine 只会独立地插值 position 和 rotation，这经常会导致 object of interest 以非预期的方式在屏幕上移动。如果 Cinemachine 知道什么是 object of interest，它就可以修正这个问题。

### Behavior and extension selection

当从 Cinemachine Camera 组件中选择 behaviors 或添加 extensions，Unity 会自动添加额外的 Components 到 Cinemachine Camera GameObject 上。要修改 Cinemachine Camera behavior，修改这些额外附加的组件上的属性。

可以通过手动添加组件到 GameObject 上获得相同的效果。

如果没有过程化组件，Cinemachine Camera 控制 Unity Camera 位置和旋转，通过它的 Transform。

还可以通过继承 CinemachineComponentBase 或 CinemachineExtension 类来实现自定义的移动行为或扩展。当创建了这样的 behavior 或 extension，它自动变为可用，可以和现有的那些一起选择。

## Cinemachine and Timeline

如果需要使用 choreographed camera 创建可预期的 shot sequence，可以使用 Timeline 来激活、deactivate、blend CinemachineCameras。

对于简单的 shot sequencers，可以使用 Cinemachine Sequencer Camera，而不需要 Timeline。

当 Timeline 驱动 Cinemachine 时，它覆盖 Cinemachine Brain 的优先级系统。当 Timeline 结束时，或者至少当 Timeline 当前没有驱动 Cinemachine 时，控制权回到 Cinemachine Brain 中。

Timeline 通过 Cinemachine Shot Clips 在 Cinemachine Track 中控制 Cinemachine Cameras。每个 shot clip 指向要给 Cinemachine Camera，来激活 activate 然后 deactivate 它。使用 shot clips 的 sequence 来指定每个 shot 的 order duration。

每个 shot 是一段 Cinemachine Camera 驱动 Unity Camera 的时间。就好像 clip 对于 animation/audio 一样。

要在两个 Cinemachine Cameras 之间创建 cut（duration=0 的 blend，即直接突然地切换），将 clips 一个紧接着一个放置。要创建 blend，将 clips overlap。

可以在 Timeline 中有多个 Cinemachine Tracks。下面的 tracks 覆盖上面任何 track。

通过在更高 track 的 active CinemachineShot clip 下面放置一个 shot，可以用另一个 shot 中断当前 shot。

还可以有多个包含 Cinemachine tracks 的 Timelines。此时包含最近 activated Cinamachine Camera 的 Timeline 覆盖其他的，如果这个 Timeline 没有 active Cinemachine Camera Clips，控制权转回之前的 Timeline。

可以 blend 一个 Cinemachine Shot Clip 和另一个在单独 Cinemachine Track 的 Clip，或者当前被 Brain 标识为 Live 的 Camera。

为此，可以修改 clip 的 Ease In Duration 和 Ease Out Duration。