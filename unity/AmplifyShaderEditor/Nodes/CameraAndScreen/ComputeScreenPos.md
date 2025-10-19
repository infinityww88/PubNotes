# Compute Screen Pos

将剪裁空间中的position转换为屏幕空间纹理坐标。坐标可以直接被应用到TextureSample节点作为它的uv坐标，进行屏幕空间映射纹理采样

## 参数

- Input：剪裁空间位置，如果没有Input port
- Normalize：自动执行透视除法（使用w去除X/Y/Z）

## Input port

- Input：剪裁空间位置

## Misc

- Compute Grab Screen Pos Node等于Normalize=false的Compute Screen Pos Node
- Compute Grab Screen Pos Node就是UnityCG.cginc的ComputeScreenPos()函数
- 不管使用哪种方式, 结果坐标就是屏幕空间标准化坐标, 成为屏幕空间uv坐标
