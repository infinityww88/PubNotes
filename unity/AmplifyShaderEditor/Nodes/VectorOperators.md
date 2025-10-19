# Vector Operators

## Append

使用输入的各个channel创建一个Vector。Input Port同时依赖于选择的Output Type以及输入数据。如果Output Type设置为Vector3，节点默认显示3个输入端口。当连接一个Vector2类型数据到Input Port X上，它自动将其命名为XY，下一个端口命名为Z，并移除第三个端口。

## Break To Component

暴露vector/matrix所有可用的channel。

输出

- X, Y, Z, W：Vector
- R, G, B, A：Color
- [0][0] to [2][2]：matrix3x3
- [0][0] to [3][3]：matrix4x4

## Component Mask

输出输入数据被选择的channels子集合。Mask的channel数量依赖于输入数据类型

参数

- X | R: include X | R channel
- Y | G: include Y | G channel
- Z | B: include Z | B channel
- W | A: include W | A channel

## Cross

计算两个向量的叉乘积。输入的两个向量Lhs和Rhs是有顺序的。

## Distance

两个向量的欧几里得距离，Sqrt( Dot( B - A, B - A ))，即向量差的模长

## Dot

计算两个向量的点乘积，等价于两个向量的夹角余弦值与两个向量模长的乘积

## Length

类似Distance，但是直接给出向量，而不是给出两个向量。Sqrt( Dot( Input, Input ))

## Normalize

标准化一个向量

## Reflect

给出入射向量，法向量，计算反射向量。Incident - 2 \* Normal * Dot(Incident•Normal)

法向量应该被标准化，因为这会使反射向量和入射向量具有相同的长度

## Refract

给出入射向量Incident，法向量Normal，表面折射率Eta，计算折射向量。Normal和Incident向量都应该标准化

## Swizzle

允许重组和重复输入数据的channel，Input和Output可以是不同的类型

参数

- Output Type：指定输出数据的类型
  - Float
  - Vector2
  - Vector3
  - Vector4
- Channel：指定输入数据的那个channel被用于哪个新的channel
  - X | R
  - Y | G
  - Z | B
  - W | A

## Transform Direction

在两个空间中转换一个给定的方向向量

参数

- Input：如果没有输入连接，则使用这个默认值
- From：输入向量当前所在的空间
  - Object Space
  - World Space
  - View Space
- To：输出向量要变换到的空间
  - Object Space
  - World Space
  - View Space
- Normalize：将输出向量标准化
