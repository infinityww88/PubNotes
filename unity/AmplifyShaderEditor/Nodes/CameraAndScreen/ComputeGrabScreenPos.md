# Compute Grab Screen Pos Node

将一个剪裁空间中的position转换到标准化的屏幕空间纹理坐标，并且考虑了不同图形API垂直方向的不同。输出结果可以直接被用于GrabScreenColor，作为它的uv坐标

## 参数

- Input：剪裁空间中的位置。如果Input端口没有输入则使用这个参数

## Input port

- Input：剪裁空间中的位置
