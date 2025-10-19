# Metadata

有时你想要存储一些额外的信息到曲线上，例如最大速度，或者跟踪信息，额外的Curvy Generator数据等等

这通过创建你自己的Metadata类并且把它附加在CP上来实现。你可以通过Curvy API来访问这些meta data

## Metadata interpolation

当将一个Metadata赋给一个CP时，元数据的值被应用到CP对应的segment上（直到下一个CP）。如果没有元数据插值，元数据的值会在到达下一个segment时突然改变。有时你希望元数据在两个CP之间平滑插值。这就是interpolatable Metadata类的工作

## 创建Metadata类

创建一个新的MonoBehaviour，继承以下两个类

- CurvyMetadataBase：所有Metadata类的基类
- CurvyInterpolatableMetadataBase\<T>：所有可插值元数据的基类。抽象类，需要实现MetaDataValue getter和Interpolate方法

## 将Metadata赋予Control Points

Metadata本身就是组件

## 获取Metadata

可以从splines和CP获取metadata

- GetMetadata\<T>：获取元数据自身
- GetInterpolateMetadata<T, U>：从Metadata class T获取类型为T的插值数据，一个CP可以附加多个元数据（T），每个元数据包装类型为U的数值类型
- MetaDataSet：属性，获取所有附加的Metadata的集合（CurvySplineSegment only）
