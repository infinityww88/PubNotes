# Input Spots

创建一个Spots的集合。手工创建一组Spots。一个Spot包含

- Index
- Position
- Rotation
- Scale

Index告诉CreateGameObject/CreateMesh这个Spot使用输入的VMesh数组/GameObject数组的第几个元素。Volume Spots就是沿着spline根据输入的Bound数组自动生成沿着曲线的Spot。Bound数组应该与后来使用的GameObject数组/VMesh数组一一对应

一个Spot上添加一个GameObject或者一个VMesh

## Slots

- Spots
