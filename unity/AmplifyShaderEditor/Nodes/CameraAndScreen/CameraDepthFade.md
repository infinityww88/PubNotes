# Camera Depth Fade Node

输出表面深度和camera near plane的差值。计算值被设置为[0, 1]之间的线性范围，并且可以使用Length和Offset调整计算值

## 参数

- Length：在观察坐标系（相机坐标系）中定义的距离，value在0-Length之间映射到0-1。参数既可以在节点参数上配置，也可以通过节点输入端口获得。如果没有相应的输入端口，则使用节点参数
- Offset：在观察坐标系（相机坐标系）中定义一个偏移，计算值从这个偏移开始变化

## 输入

- Length

- Offset

## 输出

- float：0-1之间深度值
