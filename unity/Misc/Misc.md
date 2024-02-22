Unity 的 2d 空间中，Screen 空间和 Viewport 空间都是左下角(0, 0)，右上角(1, 1)/(screenWidth, screenHeight)，UIToolkit 的 UI 空间则是右上角(0, 0), 右下角(1, 1)/(screenWidth, screenHeight)。

Editor Mode 中，Screen.width 和 Screen.height 不是游戏运行时的分辨率(GameView 设定的分辨率)，而是 GameView 的 Editor 中的实际分辨率。要在 editor 中使用 GameView 设定的分辨率，使用 Camera.pixelWidth/pixelHeight 或者 Camera.scalePixelWidth/scalePixelHeight.




