Unity 的 2d 空间中，Screen 空间和 Viewport 空间都是左下角(0, 0)，右上角(1, 1)/(screenWidth, screenHeight)，UIToolkit 的 UI 空间则是右上角(0, 0), 右下角(1, 1)/(screenWidth, screenHeight)。

Editor Mode 中，Screen.width 和 Screen.height 不是游戏运行时的分辨率(GameView 设定的分辨率)，而是 GameView 的 Editor 中的实际分辨率。要在 editor 中使用 GameView 设定的分辨率，使用 Camera.pixelWidth/pixelHeight 或者 Camera.scalePixelWidth/scalePixelHeight.

Transform 的 3 组 transform 函数:

- 变换位置

  - Transform.TransformPoint
  - Transform.InverseTransformPoint

  考虑4x4矩阵链全部的偏移，旋转，和缩放

- 变换向量

  - Transform.TransformVector
  - Transform.InverseTransformVector

  不考虑矩阵链的偏移，只被旋转和缩放影响。无论是一致缩放还是非一致缩放，单位向量都会被 x, y, z 轴方向上的 scale 相应缩放，变换后不一定还是单位向量。

- 变换方向

  - Transform.TransformDirection
  - Transform.InverseTransformDirection

  不考虑矩阵链的偏移和缩放，只被旋转影响，单位向量变化后仍然是单位向量。

transform.localPosition(localRotation, localScale) 是 transform 在 parent transform 坐标空间的位置（旋转、缩放）。

DOTween.DOPunchPosition(localOffset, duration, vibrato, elasticity) 开始一个到指定位置的敲打动画。其中 localOffset 是针对 transform.localPosition 的，动画时会加到 localPosition 上，因此计算的 localOffset 要相对于 transform 的 parent 坐标空间进行变换，而不是相对于 transform 自身的坐标空间。

