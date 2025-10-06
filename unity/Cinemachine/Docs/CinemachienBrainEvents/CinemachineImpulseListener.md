脉冲信号与脉冲源本身并不直接产生作用效果，没有 Impulse Listener 不会发生任何失去。

脉冲监听器是Cinemachine的一个扩展功能，它使Cinemachine虚拟摄像机能够“感知”脉冲振动信号并作出响应。

Cinemachine内置的默认实现方式是将接收到的信号直接应用于监听器的变换位置，使其随信号产生震动效果。此外，还可指定次级响应——通常表现为所有位置和旋转轴向上的随机振动——从而为监听器的运动赋予个性特征。这类似于将监听器置于弹簧支架上，然后通过脉冲信号进行触发：除了冲击本身产生的推力外，弹簧还会引发随机抖动。

当为Cinemachine Camear 添加脉冲监听器扩展时，Camera 便会根据脉冲源发出的信号产生震动响应。最简单的应用场景是，脉冲监听器将信号直接映射到 Camera 的 transform 上，使其产生抖动效果。

如下图所示，角色脚部被设置为脉冲源。当双脚与地面碰撞时（A），会生成脉冲信号。Camera 作为脉冲监听器，通过震动（B）对脉冲作出反应，最终导致游戏视图中的画面产生抖动（C）。

![ImpulseOverview](../../Images/ImpulseOverview.png)

在实际拍摄中，不同摄像机的固定稳固程度存在差异，稳固性较低的设备往往会产生更明显的晃动。脉冲监听器的增益属性正是通过放大或衰减脉冲振动信号来模拟这一特性：数值设置越高，摄像机产生的晃动幅度就越大。

你可以创建自己的 Impulse Listener 来以任何想要的方式解释 vibration signals。

要为不是 CinemachineCameras 的 GameObjects 添加监听 impulse 的能力，可以使用 CinemachineExternalImpulseListener behaviour。

默认，一个 Impulse Listener 响应范围内的每个 Impulse Source，但是可以使用 Channel Filtering 让 Listener 只响应部分 Impulse Source。

# 属性

- Apply After

- Channel Mask

- Gain

  此数值决定了接收到的脉冲信号在触发反应时的放大倍数。它作为一个简单的乘数作用于输入信号，默认值为1。

- Use 2D Distance

  启用此设置后，在计算摄像机与脉冲源的距离时将忽略Z轴。此属性适用于2D游戏。

- Use Camera Space

  此选项将脉冲信号解析为 camera 局部空间坐标而非世界坐标系。例如当脉冲Y轴产生振动时，监听器将沿其自身局部坐标系的Y轴进行上下运动。

- Reaction Settings

  允许设置由脉冲信号触发的次级噪声。通过选择噪声预设并调整振幅与频率增益进行微调。持续时间用于设置次级噪声的淡出时长（时间为近似值），该值会根据脉冲强度自动按比例调整。

  监听器会将原始脉冲信号与反应信号叠加，并作用于其附着的对象（可以是摄像机、虚拟摄像机或其他任意对象）。通过编写自定义监听器，能够以非标准方式应用信号（例如将Z轴运动转换为焦距变化）。





