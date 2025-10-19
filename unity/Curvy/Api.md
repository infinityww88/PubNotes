# API

这里只列出最重要的API和属性

## General

应用于CurvySpline

### Refresh()

刷新此曲线。如果有必要，其在Update中自动调用。唯一需要手动调用它的原因是你在code手动更新了曲线，并且想立即读取曲线数据，而不是等等Update之后

Refresh只在必要的时候重建cache，因此调用它多次不会影响性能

## 单位转换

### CurvySpline方法

- TFToDistance()

    从一个曲线的开始处，将一个给定的TF值转换成世界单位距离

- DistanceToTF()

### CurvySplineSegment方法（CP组件）

- LocalFToDistance()

    从一个segment开始处，将一个给定的F值转换为世界单位距离

- DistanceToLocalF()

- LocalFToTF()

## 获取曲线数据

CurvySpline和CurvySplineSegment共有方法

- Interpolate()

    给定TF/F，给出曲线上的点的世界位置

- GetTangent()

    给定TF/F，给出相应点在曲线上的方向（切线方向）

- GetOrientationUpFast()

    给定TF/F，给出相应点在曲线上的向上向量

- GetOrientationFast()

    给定TF/F，给出相应点的rotation，等价于LookRotation(tangent, up)

## Add/Delete Control Points

- Add()

    添加一个或多个CP

- Delete()

    删除一个CP

- Clear()

    移除所有CP

## API Introduction

Curvy所有到Controllers和editor API都是使用到Curvy到API实现到，没有任何隐藏到秘密

## 约定

- 以Fast结尾到方法意味着使用caching数据
- 以INTERNAL结尾的方法应当被认为是私有的并且不应该使用
- 属性通常不必进行缓存。它们或者在内部被缓存，或者足够快到可以实时调用它们。耗时到方法通常都是函数，这就是为什么有的数据通过属性获得，有的则通过函数获得
