# Edge Tools

## New Edge/Face From Vertices

F(fill)，从选择的vertices中创建一个edge或者一些faces

## Set Edge Attribute

Edges可以有一些不同的属性，影响其他特定工具如何影响mesh

- Mark Seam and Clear Seam

  Seam是创建分离的UV islands的方法。这个选项选择的edges set或unset seam flag

- Mark Sharp and Clear Sharp

  Split Normals和Edg Split Modifier使用Sharp flag，是smoothing/customized shading的一部分。就像seam，也是edges的一个属性

- Adjust Bevel Weight

  Bevel Modifier使用的（0～1）系数，控制edges的bevel程度。以交互模式（类似transform tool）通过鼠标移动设置edge的bevel weight。如果选择多个edges，修改edges的平均weight

  Vertices也具有可编辑的bevel权重

- Edge Crease

  Subdivision Surface Modifier使用的edge属性（0～1），控制subdivided mesh的edges的sharpness（锐利程度），反smooth。类似Bevel Weight，以交互模式调整（鼠标移动或输入数字）

## Edge Slide

  沿着邻接faces移动一个或多个edges，将edges移动lock在faces上。参见Vertex Slide

## Rotate Edge

  在所在的face上将edge两端vertex沿着顺时针（CW）或逆时针（CCW）各前进一个vertex，重新建立edge

## Edge Split

  参见Rip Vertex

## Bridge Edge Loops

  使用face连接多个edge loops

- Connect Loops
  - Open Loop：不bridge第一个和最后一个edge loop
  - Closed Loop：bridge第一个和最后一个edge loop
  - Loop pairs：每两个loop单独bridge

- Merge：merge edge loops为一个loop，而不是创建新的faces

- Merge Factor：控制最终merged loop的位置，0.5则最终loop将会在所有path中间

- Twist：控制bridge时的扭转。默认没有扭转，一个loop的vertex0对应相邻loop的vertex0。Twist 控制vertex对应关系的位移。1意味着loop0的vertex0连接loop1的vertex1，loop1的vertex1连接loop2的vertex2，以此类推，因此创建一种扭曲效果

- Number of Cuts：每个bridge face loop两个edge loops之间创建的loop cut数量

- Interpolation：中间loop cut的edge loop如何bevel

- Smoothness：Profile Shape的Falloff指数

- Profile Factor：bevel的系数，凹陷还是凸出

- Profile Shape：bevel的曲线形状

vertices数量不相同的edge loops之间也可以bridge

如果选择的是一组face loop，则等价于将每个face loop的face去掉，留下相应的edge loop，然后对edge loop进行bridge，相当于cut出两个hole，然后将两个hole进行bridge

根据edge loop之间的距离自动确定edge loop bridge的路径（次序）

Subdivision选项自动计算uv
