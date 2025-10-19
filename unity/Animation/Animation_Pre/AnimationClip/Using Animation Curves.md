# Using Animaiton Curves

## 属性列表

在 AnimationClip 中，任何 animatable property 都有一个 Animaiton Curve。这意味这 Animation Clip 控制这个属性如何随着时间改变。

Property <--> Curve

一个动画属性对应一个曲线。

在 Animation View 左边的属性列表区域，所有当前 animated properties 都被列出来。当 Animation View 在 Dope Sheet 模式时，每个属性的 animated values 只作为 linear track 出现，但是当 Animation View 在 Curve 模式时，你可以观察属性值作为曲线随时间而变化。

无论使用哪种模式观察，每个属性的 Curve 都是存在的。Dope Sheet 模式只是将数据作为关键帧呈现。

## 理解 Curves，Keys 和 Keyframes

Keys 是 Curve 的控制点，控制点所在的 frame 称为 Keyframes。

编辑动画就是编辑 Curve 的控制点（Keys），或者编辑 Keyframes 的数据。

## 支持的 Animatable Properties（可动画属性）

Animation View 不仅仅可以 animate 一个 GameObject 的 position，rotation，scale。任何 Component 和 Material 的属性都可以被 animated，甚至是你自己的 script components 的 public variables。

制作具有赋值视觉效果和行为的动画只不过是添加相关属性的 Animation Curves。

Animation System 支持：

- Float
- Color
- Vector2
- Vector3 
- Vector4
- Quaternion
- Boolean

对于 bool 属性，value 0 表示 False，其他值表示 True。

以下是 Animation View 的一些例子：

- Animate 一个光源的 Color 和 Intensity，使它闪烁、摇曳、或浮动
- Animate 一个 looping Audio Source 的 Pitch 和 Volume，模拟呼啸的风，运行的发动机，或流动的水
- Animate 一个 Material 的 Texture Offset，来模拟运动的皮带或履带，流动的水，或者特效
- Animate 多个 Ellipsoid Particle Emitters 的 Emit 状态和 Velocities 来创建精彩的烟花和喷泉
- Animate 你自己脚本的变量使事情随时间行为不同

## Rotation 插值类型

Unity 中 rotation 内部被解释为 Quaternions。

欧拉角通常只用于一个轴的旋转。如果有两个轴的旋转，使用两个 GameObject，parent 控制一个轴，child 控制另一个轴。
