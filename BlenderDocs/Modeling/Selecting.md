# Selecting

Shift-LMB可以同时激活多种选择模式（可以同时选择vertex、edge、face）

切换Select Mode时，当前mode中的选择的元素如果是新的mode中完整元素，切换后这些元素仍然被选择

当从当前模式切换到更高的选择模式时（vertex to edge, edge to face），按住Ctrl，当前元素与所有和当前选择元素接触元素都被选择，即使当前元素在更高的mode中不构成完成的元素

X-Ray不仅影响shading，还影响selection。当开启时，选择元素不会被geometry遮挡

## Selection Menu

- A：Select All
- AA/Alt-A：None
- Ctrl-I：Invert
- Box Select
- Circle Select
- Select Random：based on a percentage value
- Checker Deselect：相对当前active元素交替取消当前选择元素
- Select Sharp Edges：选择所有构成夹角超过指定值的两个faces的edges
- Select Similar：选择和当前current selection类似的元素
- Select All by Trait：通过查询特征选择geometry
  - Non Manifold
  
    选择一个mesh的非流形（non-manifold）的几何。只用于Vertex/Edge selection。Mesh中存在流形元素与非流形元素。这个menu item选择所有非流形元素。一个封闭的mesh是完全流形的。开放的mesh，boundary处的vertices/edges是非流形的。Circle是wire，也是非流形的。Faces相连的边界就是非流形元素

    - Extend：保持当前选择元素，并选择非流形元素添加到当前选择的集合中
    - Wire
    - Boundaries
    - Multiple Faces
    - Non Contiguous
    - Vertices
  - Loose Geometry
  - Interior Faces
  - Faces by Sides
- Select More/Less：扩展选择元素到相邻的选择类型元素
  - Ctrl+NumPlus/NumMinux：More/Less
  - Ctrl+NumMinux：Less
  - Next Active/Previous Active：基于历史选择之前之后的选择
- Select Loops
  - Edge Loops
  - Face Loops
  - Edge Ring
- Select Linked
  - Select Linked：选择所有和当前选择相连接的元素
  - Shortest Path：选择两个选择元素的最短路径
  - Linked Flat Faces：基于一个angle阈值选择相连接的faces。用来选择接近构成平面的faces
- Select Side of Active：选择mesh中和当前active vertex在同一个axis上的所有vertices。只用于vertex selection mode
- Mirror Selection：选择指定axis镜像位置的mesh元素

## Tips

流形就是相连的几何元素构成的形状
