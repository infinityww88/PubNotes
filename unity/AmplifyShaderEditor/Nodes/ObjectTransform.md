# Object Transform

## Object Space View Dir

在物体局部坐标系计算一个局部坐标系中的位置到camera的非标准化方向。如果没有输入的位置，则计算当前game object到camera的方向

## Object To Clip Pos

将一个物体局部坐标系中的位置变换到相机的剪裁空间的其次坐标（未执行齐次除法）

Direct3D和OpenGL的剪裁空间坐标系有所区别

- D3D：剪裁空间在near plane为0，在far plane为1

- OpenGL：剪裁空间在near plane为-1，在far plane为1

## World Space View Dir

类似Object Space View Dir，但是给出局部坐标系位置，计算世界坐标系中的到camera的方向

## World To Object/Object To World

将input指定的position或direction从世界空间转换的局部空间。如果没有input连接，则返回当前物体的pivot位置

## World To Params

The World Transform Params node contains information about the current transform, more specifically W is usually 1.0, or -1.0 for odd-negative scale transforms（TODO）

