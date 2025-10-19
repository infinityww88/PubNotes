# Clean up

清理退化geometry，填充mesh的missing区域

## Decimate（十中抽一） Geometry

减少mesh中的vertex/face数量，保持尽可能小的形状改变

- Ratio：减少的triangles的比率

- Vertex Group：使用当前active的vertex group作为影响（指导）
  - Weight：vertex group的强度
  - Invert：反转vertex group

- Symmetry：沿着X/Y/Z保持对称

## Fill Holes

使用很大的selection，检测mesh中的holes，将它们填充

- holes自动检测，无需手动发现并选择围绕它的edges
- 可以限制hole的边缘数量（可以限制只有quad或triangle的hole被填充）
- mesh data（UVs，Vertex Colors，Multi-res，all layers）从周围geometry复制过来，因为手动创建这些data非常耗时

## Make Planar Faces

交互式平坦化faces

- Factor：每次迭代vertices移动的距离
- Interations：迭代的次数

## Split Non-Planar Faces

通过分离超过指定bent限制的non-flat faces来避免geometry上模凌两可的区域

## Split Concave Faces

通过将concave分离为两个或更多convex faces将任何凹面concave faces转换为凸面convex faces

## Delete Loose Geometry

移除未连接的vertices和edges（以及可选的faces）

## Degenerate Dissolve

合并/移除你不想要的geometry

- 没有长度的edge
- 没有面积的faces
- 没有面积的faces角
