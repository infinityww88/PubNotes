# Using Physical Cameras

Camera 组件的 Physical Camera 属性模拟真实世界的相机。这对从 3D 建模程序导入也是模拟真实世界的 cameras 信息非常有用。

![InspectorCameraPhysCam](../Image/InspectorCameraPhysCam.png)

Unity 提供了和大多数 3D 建模软件物理相机设置相同的设置。

有两个主要的属性控制相机可以看见什么：Focal Length（焦距）和 Sensor Size（传感器/底片 尺寸）。

![PhysCamAttributes](../Image/PhysCamAttributes.png)

- Focal Length：sensor 和 lens 的距离。这决定了垂直视野。当 Unity camera 处于 Physical Camera mode，改变 Focal Length 还相应地改变 field of view。小的 focal length 导致更大的 field of view，反之亦然
- Sensor Size：捕获 image 的 sensor 的 width 和 height。这决定物理相机的 aspect ratio。你可以选择一些对应真实世界的 camera formats sensor sizes preset，或者可以设置一些自定义 size。当 sensor aspect ratio 和 rendered aspect ratio（Game view）不一致时，你可以控制 Unity 如何适配 fit camera image 到 rendered image

sensor：光电传感器，底片

lens：镜头

focal：焦点

## Lens Shifts

Lens Shift 水平地或垂直地偏移 camera 的镜头（镜头不是沿着相机中心线，而是绕着中心旋转镜头）。这允许你改变焦点中心，在 rendered frame reposition subject，没有或很少失真 distortion。

这通常用于建筑摄影。例如，如果你想捕捉一个很高的建筑，你可以向上旋转 camera（中心线想上旋转）。但是这样会使 image 失真，使下图中红色的 parallel lines（平行线）看起来收敛 converge。

平行线收敛就是透视投影的灭点效果。

![LensShift_VRot](../Image/LensShift_VRot.png)

如果你向上（旋转）偏移镜头（相机不动，即传感器 sensor 保持垂直），你可以改变图像的构图来包含建筑的 top，但是平行线 parallel lines 仍然保持垂直。

![LensShift_VShift](../Image/LensShift_VShift.png)

类似地，你可以使用一个水平镜头偏移（旋转）来捕获很宽的物体，而不会得到你旋转整个相机导致的失真。

![LensShift_HRot](../Image/LensShift_HRot.png)

![LensShift_HShift](../Image/LensShift_HShift.png)

### Lens shifts and frustum obliqueness

镜头偏移的副作用是使得 view frustum 倾斜。这意味着 camera 中心线一侧的视椎体角度比另一侧小。

![ObliqueFrustum_LensShift](../Image/ObliqueFrustum_LensShift.png)

你可以使用这个功能创建基于透视的视觉效果。例如，在赛车游戏中，你可能想要保持透 perspective low to ground。一个 lens shift 是不使用 scripting 达成倾斜视椎体的方法。

## Gate Fit

Camera 组件 Gate Fit 属性决定当 GameView 和 Physical Camera sensor 具有不同的 aspect ratios 将会发生什么。

在 Physical Camera 模式，一个 camera 有两个 gates。

- GameView 中的渲染的区域，根据你在 Aspect drop-down 菜单设置的 resolution，称为 resolution gate
- Camera 实际看见的区域，被 Sensor Size 属性定义，称为 film gate

![GateFitGates](../Image/GateFitGates.png)

当两个 gates 具有不同的 aspect ratios，Unity 适配 fits resolution gate 到 film gate。有几种 fit modes，但是它们最终都产生下面3种结果中的一个：

- Cropping（剪裁）：当 fitting 之后 film gate 超过 resolution gate，Game View 渲染尽可能多的 fits 到它 aspect ratio 的 camera 图像，然后剪裁剩下的
- Overscanning（超扫描）：当 fitting 之后 film gates 超过 resolution gte，Game View 还会对落到 camera field of view 之外的 scene 执行渲染 rendering 计算（即 camera field of view 之外的 scene 一样执行渲染）
- Stretching（拉伸）：GameView 选择全部 camera 图像，水平或垂直拉伸来适配它的 aspect ratio

要在 Scene View 中查看 gates，并观察它们是如何 fit 在一起的，选择 camera 并观察它的 view frustum。Resolution gate 是 camera 的 far clipping plane。film gate 是 frustum base 上的第二个 rectangle。

![GateFitUI](../Image/GateFitUI.png)

Camera view frustum base（far clipping plane）上外面的 A rectangle 是 resolution gate。内部的 B rectangle 是 film gate。

### Gate Fit Modes

Gate Fit mode 确定 Unity 如何 resize resolution gate。Film gate 总是保持相同尺寸。

无论如何，相机 view frustum（远近平面）会被完整映射到 screen 上（即 game view）。因此 view frustum 的远屏幕就是对应 game view。相机组件是没办法设置 ratio 的，对于 Prespective 相机，只能调整 Field of View，对于 Orthographic 相机，只能调整 size（相机一半高度），而相机 view frustum 总是和 GameView aspect 保持相同的，调整 GameView 的 aspect ratio，Camera 就相应调整 view frustum 的 aspect ratio。

对于物理相机，Focal Length 和 Sensor Size 都是逻辑上的，不和 View Frustum 对应。Unity 使用这两个真实相机的参数来建立一个逻辑相机，然后在逻辑相机的 Sensor Size 和 Camera View Frustum 的 base 进行 fit（适应）。

Unity 应该是基于物理相机参数真正建立了一个匹配的相机（变化矩阵）。这个相机的 View Frustum 的 aspect ratio 是与 Sensor 相同的。然后渲染时，Unity 使用这个相机渲染。但是渲染之后，将得到的 rendered image（底片）和游戏中看到的相机的 View Frustum 进行适配 fit。这就是为什么可以 Overscanning。

- Vertical

  当 Gate Fit 设置为 Vertical，Unity 调整 fit resolution gate（因此就是调整 camera view frustum） 到 film gate 的高度（Y 轴）。任何对 sensor width（Sensor Size > X）的改变对 rendered image 没有影响。

  如果 sensor aspect ratio 比 game view aspect ratio 更大（aspect ratio = width / height，ratio 更大，就是更宽），Unity 剪裁调两侧的 rendered image。

  ![GateFitV_600x900_16mm](../Image/GateFitV_600x900_16mm.png)

  View Frustum 被 Sensor 更窄，两侧多出来的 Sensor Image 被剪裁调。

  ![GateFitV_16-9_16mm](../Image/GateFitV_16-9_16mm.png)

  Sensor 更窄，绿色区域指示 Unity overscan image 的部分。Overscans 即物理相机实际上渲染了更大的区域，使得它覆盖不够的区域，然后将多余的区域剪裁掉。

- Horizontal

  和 Vertical 类似，只是 fit resolution gate 到 film gate 的宽度（X 轴）

  Crop

  ![GateFitH_600x900_16mm](../Image/GateFitH_600x900_16mm.png)

  Overscan

  ![GateFitH_16-9_16mm](../Image/GateFitH_16-9_16mm.png)

- None

  拉伸 rendered image（sensor）来适配到 GameView aspect ratio。

  ![GateFitF_16mm](../Image/GateFitF_16mm.png)

- Fill or Overscan

  Unity 依据 resolution gate 和 film gate aspect ratios 自动执行 Vertical 或 Horizontal fit。

  - Fill：fit resolution gate 到 film gate 的 smaller axis，剪裁掉剩余的 sensor image
  - Overscan：fit resolution gate 到 film gate 的 larger axis，overscans sensor image 边界外的区域
  
