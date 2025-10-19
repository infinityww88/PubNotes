# Camera

screen空间以像素定义，左下角是(0, 0)，右上角是(pixelScreenWidth, pixelScreenHeight)，z轴指向屏幕内部，但是单位是世界空间单位

viewport空间screen空间的单位化，除了z轴保持不变，左下角为(0, 0)，右上角为(1, 1)

## 静态属性

- allCameras/allCamerasCount：返回当前scene enable的所有camera
- current：当前用于渲染的camera
- main：第一个具有MainCamera Tag的camera
- onPreRender/onPostRender：摄像机渲染前/后发射的事件

## 静态方法

- Ray ScreenPointToRay(Vector3 pos)

    从屏幕空间指定点创建一条世界空间的射线。射线起点在pos对应的近平面的世界位置。z值被忽略

- Vector3 ScreenToWorldPoint(Vector3 pos)

    将屏幕空间中的点转化为世界空间中的点。pos位于屏幕空间，x是从左向右的屏幕像素位置，y是从下到上的屏幕像素位置，z是从camera近平面向远平面方向的世界距离

    等价于用ScreenPointToRay创建一条世界射线，沿着射线方向移动pos.z个世界单位的点的世界位置就是返回的值
