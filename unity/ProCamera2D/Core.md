# Overview

Core 代表 main class —— ProCamera2D.cs。它是一个非常简单的类，专注保持对所有 targets 的追踪，知悉使用哪些坐标轴（XY，XZ，YZ），多快地移动，更重要的，它是所有 extensions 和 triggers 的大脑。

Core 的主要功能：

- Multi-target follow（weighted）

  如果你的游戏有多个角色，或者你就是想跟随一个特定的 missile 但是仍然想保持 player 在视线内，只需要添加另一个 target（或者任意多个）到 camera 就可以了。ProCamera2D 将会找到所有 targets 的平均位置，并考虑它们不同的影响。非常适合 Super Smash Bros（任天堂明星大乱斗）这样的游戏

- Follow smoothness（per axis）

  有时你需要 camera 在一个 axis 上非常快，但是在另一个 axis 则非常平滑。例如对于平台类游戏，你可能想 camera 在跳跃时更少僵硬 rigid。使用 ProCamera2D 你可以定义每个轴上的 follow 速度

- Perspective & Orthographic modes

  所有 ProCamera2D 功能（除了视差 parallax 和 pixel-perfect），在 perspective（3D）或 orthographic（2D）都是相同的。不需要特殊的配置。简单地改变 projection 类型就可以了

- All axes support（XY，XZ，YZ）

  你是否要构建一个平台游戏？一个 top-down 赛车游戏？一个具有疯狂 camera 设置的空间模拟游戏？不要担心，ProCamera2D has got you covered。使用它的 multi-axis 支持，你可以将它用在任何 2D & 2.5D 游戏中

- Dolly zoom

  移动摄影车式 zoom。

  为游戏中最 intense 时刻创建一个令人惊叹的戏剧效果。Get creative！

## Setup

选择你的 camera（默认是 Main Camera），挂载 ProCamera2D 组件

## Editor

![procamera2d_main_editor](../Image/procamera2d_main_editor.png)

### Drop Targets Area

这个区域是你可以拖放 camera targets 的地方。

### Targets List

显式 camera 当前跟随的所有 targets。可以 reorder 它们（但是没有区别），删除或 duplicate target

参数：

- Transform：target GameObject 的 transform 组件
- Offset：水平和垂直偏移 camera 跟随的 target position
- Influence(0-1)：水平和垂直的 float，定义每个轴上对最终 camera position 的影响

### Center Target On Start

如果 checkbox 开启，camera 在游戏开始时立刻移动到 targets position。为此，target 需要提前被添加。要在 centering 运行时添加的 targets，应该使用 Reset 方法。

### Axis

选择游戏要使用的坐标轴。如果是平台游戏，可能限制在 XY 平面，如果是 top-down 游戏，可能想要在 XZ 平面。自由选择最适合你的。所有特性在所有坐标轴上都是一样的。但不要忘记相应地旋转 camera。ProCamera2D 只移动相机，不旋转它。

### Update Type

选择何时更新相机位置。如果使用物理移动 objects，在 FixedUpdate 中更新相机，如果在 physics loop 之外移动 objects，在 LateUpdate 中更新相机。

相机出现抖动是因为相机移动的速率和物体移动的速率有波动。例如在 FixedUpdate 中移动物体，在 Update 中更新相机，每个渲染帧花费的时间不一样，可能 frame1 包含 1.3 个物理 frame，frame2 包含 2.8 个 物理 frame，Unity 只能在一个渲染帧中模拟整数个物理帧，这样 frame1 就剩下 0.3 个 physics frame，frame2 剩下 0.8 个 physics frame。抖动不在于延迟，而在于延迟的抖动。如果所有渲染帧中都延迟相同的物理帧，画面也是没有抖动的。

如果同时使用物理和非物理的移动，必须测试二者，看哪个更合适。

如果你想使用一个自定义 timestep，并需要手动更新 camera 运动，选择 ManualUpdate。这需要调用 core 类的 Move 方法，并传递想要的 timestep。

记住，如果你得到一个抖动的 camera 运动，非常可能是你选择了错误的 update cycle。

### Offset

这个 value 在 targets 和其他 influences 给出的最终 camera position 之上再添加一个整体 offset。使用它给出一个常量 offset camera 位置。记住，每个 target 还可以有它自己的 offset value。

### Zoom With FOV

这个选项只在 perspective camera 中可用。如果开启，相机将通过改变 FOV zoom，而不是真实地移动 camera 接近或远离 objects。在一些情况下可能看起来很好，但是通常它会在一个特定阈值之上导致一些可见的变形。小心使用。

### Extensions

在这个 section 你想要为你的 camera 开启哪个扩展。这个 section 在这里只是用于快速添加/移除组件。你也可以手动添加和移除组件，就像任何组件一样。

### Triggers

这个 section 添加 triggers 并在 scene view 中导航到它们。你还可以查看 scene 中每个类型有多少 triggers。

### Methods

尽管你可以在 ProCamera2D editor 中完成几乎绝大多数事情，但是你可能想要更精确地控制，甚至在运行时改变参数。为此，导入 ProCamera2D 命名空间：

```C#
using Com.LuisPedroFonseca.ProCamera2D;
```

之后，所有需要做的就是在 code 中访问 ProCamera2D static instance：

```C#
ProCamera2D.Instance.AddCameraTarget(myTransform);
```

通过 static ProCamera2D 实例，你可以改变任何 public 参数，并访问下面描述的方法。请注意所有 extensions 和 triggers 也能在运行时被访问运行时配置信息，但是它们不提供 static instances，因此你必须像标准的 Unity 组件一样访问它们。

- Apply Influence

  这个方法被大多数扩展使用。它所做的就是在一帧（调用这个方法的当前帧）中简单地应用给定的 influence 到 camera

  ApplyInfluence(Vector2 influence)

  influence：表示应用的 influence

- Apply Influences Timed

  类似前面的方法，但是可以传递一个不同 influences 的数组，和它们各自的 durations

  ApplyInfluencesTimed(Vector2[] influences, float[] durations)

  durations：每个 influence 应用的 duration。不仅仅在一帧中应用 influence

- Add Camera Target

  在运行时添加 targets。

  AddCameraTarget(Transform targetTransform, float targetInfluenceH = 1f, float targetInfluenceV = 1f, float duration = 0f)

  targetInfluenceH/V：计算所有 targets 的平均位置时 H/V position 的 influence

  duration：target 达到它的 influence 需要的时间。用于一个更 progressive transition

- Remove Camera Target

  RemoveCameraTarget(Transform targetTransform, float duration = 0f)

  duration：target 达到 0 influence 需要的时间。

- Get Camera Target

  从一个 object 的 transform 得到相应的 CameraTarget

  GetCameraTarget(Transform targetTransform)

  targetTransform：target 的 transform 组件

- Adjust Camera Target Influence

  运行时调整一个 target 的 influence。非常适合基于 target 的距离或速度 调整一个 target 的 influence。

  AdjustCameraTargetInfluence(CameraTarget cameraTarget, float targetInfluenceH, float targetInfluenceV, float duration = 0f)

  duration：target 达到它的 influence 需要的时间

- Update Screen Size

  运行时手动更新 camera 的大小

  UpdateScreenSize(float newSize, float duration = 0f)

  newSize：想要的 size 的一半 world units

  duration：达到指定大小需要的时间

- Move Camera Instantly to Position

  手动移动 camera 到指定位置

  MoveCameraInstantlyToPosition(Vector2 cameraPos)

  cameraPos：camera 的最终位置

- Reset

  重置 camera 运动和大小，以及它所有的 extensions 到它们的初始值。这非常有用，例如在角色死亡以及在另一个地方重生时

  Reset(bool centerOnTargets = true, bool resetSize = true, bool resetExtensions = true)

  centerOnTargets：如果为 true，camera 立刻移动到 targets 位置

  resetSize：如果为 true，重置 camera size 到 start value

  resetExtensions：如果为 true，重置所有 active extensions 到它们的初始值

- ResetMovement

  取消任何现有的 camera 移动 easing

  ResetMovement()

- Reset Size

  重置 camera size 到开始值

  ResetSize()

- Reset Extensions

  重置所有 active extensions 到它们的开始值。注意你可以使用 OnReset 方法手动重置每个扩展

  ResetExtensions()

- Center On Targets

  立即移动 camera 到 targets 的位置

  CenterOnTargets()

