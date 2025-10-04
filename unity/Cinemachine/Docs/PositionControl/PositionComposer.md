此 CinemachineCamera 位置控制行为会移动相机，以保持追踪目标在屏幕空间中的期望位置。你还可以指定偏移量、阻尼和构图规则 composition rules。

Position Composer 仅改变相机在空间中的位置，不会旋转相机。若要控制相机的视角，请在相机的变换中设置 CinemachineCamera 的旋转，或者为 CinemachineCamera 添加一个程序化的旋转控制组件。

所谓 Composer 就是使用 Screen Space 约束来控制 CinemachineCamera，而不是 3D 空间中的约束。Composer 是与 Follow、Orbital Follow 一样的过程化算法，一个 CinemachineCamera 只能有一个过程化算法，因此使用了 Follow，就不能再使用 Composer 了。

Position Composer 适用于2D和正交相机，同时也支持透视相机和3D环境。

该算法首先沿相机Z轴移动相机，直至追踪目标与相机XY平面达到期望距离；随后在相机XY平面内移动相机，直至追踪目标到达相机屏幕上的期望位置点。

属性：

- Target Offset
- Lookahead Time

  根据追踪目标的运动动态调整摄影机与目标之间距离的偏移量。Cinemachine会预测目标在未来若干秒后的位置点。该功能对动画噪声较为敏感，可能会放大噪声从而导致不理想的相机抖动。若目标运动时相机抖动明显，可降低此属性数值，或使目标动画更加平滑。

- Lookahead Smoothing

  前瞻算法的平滑度。数值越大，预测结果越平滑（能减少抖动），但预测延迟也会相应增加。

- Lookahead Ignore Y

  若启用此选项， lockahead 计算时将忽略Y轴方向的移动。

- Camera Distance

  沿相机轴线方向与追踪目标之间要保持的距离。

- Dead Zone Depth

  如果 Tracking target 位于这个指定的 camera distance 内，不会沿着 Z 轴移动 camera。

- Damping

  相机在三个相机空间轴向上试图维持期望位置的响应程度。数值越小，相机响应越灵敏；数值越大，相机响应越迟缓。为每个轴设置不同数值可实现丰富多样的相机行为表现。

- Screen Position

  目标在屏幕上的水平与垂直位置。相机会自动调整以将追踪对象放置在此位置。0 表示屏幕中心，-0.5 和 0.5 分别表示屏幕边缘。

- Dead Zone

  如果 target 在 Screen Position 的这个距离内，camera 不会调整。

- Hard Limits

  Camera 不会让 target 位于这个 hard limits 之外。

  - Size：相机可放置目标对象的区域大小，以屏幕尺寸的比例表示。该区域默认以"屏幕位置(Screen Position)"为中心，但可通过"偏移(Offset)"设置进行调整。数值为1时表示占据整个屏幕宽度或高度。
  - Offset：相对 Target Position 水平、垂直偏移 hard limits。

- Center On Active

  当相机激活时，将相机移动以使目标位于死区的中心。


