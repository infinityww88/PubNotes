# PolyBuild

Poly Build 工具以交互的方式使用多种built operator来添加、删除、移动geometry。这对retopology尤其有用。

Options

- Create Quads：自动分割triangles的edges来维持quad topology

Usage

- Add Geometry（Ctrl-LMB）

通过移动cursor接近一个元素并使用hotkey来添加一个vertex或face

添加Geometry Elements的另种方法。

一种在选择工具下，Ctrl-RMB从当前选择的元素extrude到鼠标当前位置，深度位于3D Cursor在View 空间的深度。vertex extrude 为edge，edge extrude 为face

另一种就是PolyBuild。它只用于边界边即只被一个face使用的edge，以及边界边的vertex。进入PolyBuild之后，如果Mesh没有边界边，则LMB创建独立的vertex。如果存在边界边，则总是高亮于鼠标最近的vertex或者edge

- 如果高亮edge，LMB基于edge和cursor创建一个triangle；Ctrl-LMB将edge分割，插入一个vertex，并且vertex移动到cursor处跟随cursor一起移动，创建n-gons
- 如果高亮vertex，LMB基于使用vertex的edges和新的vertex创建quad；Ctrl-LMB则可以拖拽移动高亮的vertex

无论哪种方式，在LMB之后都可以拖拽移动新创建的vertex，知道抬起LMB确认

开启vertex snapping并使用Merge By Distance对于retopology尤其有用。使用Sculting工具以及任意多个不相连的meshes（作为粘土）雕刻出高清晰度模型，然后使用PolyBuild工具以vertex snapping的方式在外面创建一个包裹的单一连通的mesh

