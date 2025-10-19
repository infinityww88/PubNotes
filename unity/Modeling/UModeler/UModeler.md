# UModeler

- 使用手绘风格折线来实现lowpoly风格的曲线
  - 先绘制粗糙的线条模式，然后调整vertex/edge得到满意的曲线效果
  - 通过extrude获得曲面形状mesh
- 要选中scene或者uv editor的handle，要确保窗口处于选中状态，否则直接点击handle总会导致窗口重新获取焦点而handle消失
- Snap Move Tool通常是和Follow Tool结合使用，但是也可以用于其他合适的场景
  - 选择一个polygon，polygon上面和周围会显示一些控制点
  - 选择其中两个点，这个两个点的连线将作为Y轴将poly竖立起来，注意两个点的顺序，第一个点是原点，第二个点用来确定Y轴的方向
  - 移动鼠标到当前UModeler模型其他任何顶点周围，当前选中的polygon将会对齐到鼠标附近的vertex上，刚才选中的第一个顶点（原点）和对齐的顶点重合，polygon沿着刚才确定的Y轴竖立起来
  - 移动鼠标到其他顶点，来重新对齐polygon，直到满意，polygon并不跟随鼠标，而是保持在初始位置或者刚才对齐的位置，直到鼠标移动到下一个可以对齐的vertex
  - 选中作为section的polygon和作为path的polygon，选择Follow Tool来创建Follow模型
- Follow Tool只能使用polygon作为path，而不能使用线段
- UV只是模型的顶点数据其中之一，只是一个2d向量而已，和position，color，normal等顶点数据没有区别，它记录顶点在texture上的纹理坐标位置。UV editor只是在一个canvas上以可视化的方式编辑每个顶点的uv坐标数值而已
- 当前，UModeler似乎与Archimatix一起使用会导致duplicate gizmos的问题
- UModeler中，移除faces，将保留edge/vertex；移除edge或vertex，则会移除所有元素
