**这个组件与 PositionComposer 非常类似，Hard Limit、Soft Limit、Dead Zone 的定义完全一样，作用也完全一样，但是 RotationComposer 更简单，它不需要移动 CC 的位置，只需要旋转相机，让 target 在 Screen 的位置满足 Composer Rule 就可以了**


此 CinemachineCamera 旋转控制行为会使相机面向"注视目标(Look At)"。它同时支持设置偏移量、阻尼值和构图规则（画面构成）。

该功能仅控制相机旋转，不会改变相机位置。典型的注视目标包括：角色的脊椎上部或头部骨骼、载具，或是通过程序控制/动画驱动的虚拟对象。

- Target Offset
 
  相对于注视目标中心的偏移量（以目标本地空间为基准）。当兴趣点并非被追踪对象的中心时，可使用此参数精细调整目标位置。也可通过场景手柄(Scene Handles)修改此属性。

- Lookahead Time

  根据 Look At target 的运动调整相机旋转。该算法会预测目标在未来若干秒后的位置点。此功能对动画噪声较为敏感，可能会放大噪声从而导致相机抖动。若目标运动时相机抖动明显，可降低此属性数值，或使目标动画更加平滑。

- Lookahead Smoothing

  控制前瞻算法的平滑度。数值越大，预测结果越平滑（能减少抖动），但预测延迟也会相应增加。

- Lookahead Ignore Y

  开启这个选项，lookahead 计算时忽略沿着 Y 轴的运动。

- Damping

  相机在水平和垂直方向上追踪目标的响应灵敏度。使用较小数值可使相机更灵敏快速地旋转，从而将目标保持在死区内；使用较大数值则会让相机反应更迟缓沉重。

- Screen Position

  目标在屏幕上的水平与垂直位置。相机会自动调整以将追踪对象放置在此位置。0 表示屏幕中心，-0.5 和 0.5 分别表示屏幕左右/上下边缘。

- Dead Zone：当 target 在 Screen Position 这个范围内，camera 不会调整

  - Size：相机不对目标移动做出响应的区域宽度和高度，以屏幕尺寸的比例表示。该区域以“屏幕位置”为中心。数值为 1 表示占满整个屏幕宽度或高度。

- Hard Limits：相机不会允许 target 移动到 hard limits 之外

  - Size：相机可放置目标对象的区域大小，以屏幕尺寸的比例表示。该区域默认以"屏幕位置"为中心，但可通过"偏移"设置进行调整。数值为1时表示占据整个屏幕宽度或高度。
  - Offset：相对 Target Position 水平、垂直移动 hard limits。

- Center On Activate

  当 camera 变成 live 时，旋转 Camera，将 target 放在 dead zone 中心。

