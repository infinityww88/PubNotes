# Basic

## Move, Rotate, Scale

G/R/S

Adjust Last Operation Panel：精细调整，限制到特定axes，开启关闭Proportional Editing以及Proportional选项

GG进入Edge Slide或者Vertex Slide模式，依赖于当前选择模式

- Transform Panel
  - Space：global/local
  - Vertex Data
    - Bevel Weight：Bevel Modifier，Only Vertices
  - Edge Data
    - Bevel Weight
    - Crease

## Adding Geometry

### Duplicate or Extrude to Cursor

Vertex Mode下Ctrl+RMB创建新的vertices，新创建的vertices位于相机空间中和3D cursor一样的深度（Z）

Edge Mode下Ctrl+RMB创建新的quad，新创建的quad平行于相机（extrude edge）

Face Mode下Ctrl+RMB创建新的quad，并将原quad和新quad bridge，即extrude效果，但是两个quad在同一个平行相机的平面上，需要手动移动新创建的quad

无论是添加的哪种元素，新创建的元素中心点都位于鼠标下方，并且成为当前active的元素，以便可以连续的添加元素

Edge模式下，新创建的edge会有所旋转

## Deleting & Dissolving

- Delete

    X/Delete

    Vertices/Edges/Faces/Only Edges & Faces/Only Faces

- Dissolve

    可以在Delete menu中访问。移除选择geometry元素，填充周围的geometry（移除产生的hole）

  - Dissovle Vretices：移除vertex，合并周围的faces。如果vertex周围是两个edges，合并为一个edge

    - Face Split：当dissolve vertex为surrounding faces时，经常会得到很大的uneven（不平坦）的n-gons。Face Split选项限制disolve只使用连接到vertex的faces的边角
    - Tear Boundaries：移除Face Split中填充hole产生的边角

  - Dissolve Edges

    移除edges，合并两个faces

  - Dissovle Faces

    合并共享edges的一个region的faces到一个face（F key， fill）

  - Dissolve（Context-Sensitive）

    基于当前选择模式执行相应的dissolve

- Limited Dissolve（受限dissolve）

  通过dissolve分布于平坦区域的vertices/edges来简化mesh

  - Max Angle：使用一个邻接角度阈值减少近于共面、共线的细节
  - All Boundaries：总是dissolve只有两个edge user的vertex（即vertex只被两个edge共享）
  - Delimit（分离）：阻止具有不同属性（例如材质）的faces被合并join（dissolve）
    - Regular：具有face面向（front/back）
    - Material：具有不同材质id
    - Seam：被seam分开
    - Sharp：共享sharp edge
    - UVs：共享vertex具有不同uvs

- Edge Collapse

  将每个edge合并为一个vertex。通常用于将一组ring edge合并为一组vertices

- Edge Loops

  移除一个edge loop如果它在其他两个edge loop之间，然后在其他两个edge loop之间bridge，创建face loop。可以用于取消loop cut创建的过多edge loop

## Make Edge/Face

Context-Sensitive工具，通过填充选择元素创建新的geometry。仅当两个vertices被选择时，创建一个edge，其他情况创建faces

通常情况是选择一组vertices/edges，按F键。当时Blender还支持从不同的selections中创建faces，以辅助快速构建geometry

## Symmetry

- Snap to Symmetry

  Snap一个mesh vertices到它们镜像的邻居。通常用于看起来是对称的mesh，但是从数据上不是严格对称的（大致对称），使得Blender不能检测到它们是对称的

  - Direction：指定snap的axis和direction。可以是X/Y/Z任何一个，可以从负方向到正方向snap，或者从正方向到负方向snap

  - Threshold：指定查询镜像匹配vertices使用半径

  - Factor：指定镜像两端vertex位置混合因子。0.5表示两端移动相同的距离达到镜像位置；0/1表示一端完全固定，完全移动另一端达到镜像位置

  - Center：对于镜像轴指定Threshold范围内的vertices，不再镜像到对称位置，而是直接落在对称轴上

- Symmetrize

  快速创建一个对称的mesh。

  沿着object的pivot将mesh切开，选择其中一个部分，将它镜像到对称轴的另一边，将两个部分合并（如果它们是连接的）。Mesh data也从一边复制到另一边（UVs，vertex colors，vertex weights等等）

  只镜像选择的mesh元素。如果要镜像整个mesh，需要先将mesh的全部faces选中

  - Direction：指定对称的axis和direction
  - Threshold：类似Snap To Symmetry的Threshold，如果有顶点落在对称平面的这个阈值范围之内，则vertices snap到对称平面上
