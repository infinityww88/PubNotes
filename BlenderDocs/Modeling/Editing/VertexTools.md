# Vertex Tools

## Merging

- Merging Vertices

  合并所有选择的元素到指定的一个，dissolving其他的。可以指定最后合并的顶点的位置

  - At First
  - At Last
  - At Center
  - At Cursor：3D Cursor
  - Collapse：每个选择vertices island（互相连接的vertices）合并到自己的median中心，每个island合并为一个vertex

   在Adjust Last Operation中选择UVs，可以修正uv坐标避免避免image变形

## Merge by Distance

简化mesh的有用工具。将小于指定距离的vertices合并为一个vertex。简化mesh的另一个mesh是Decimate（十中抽一）Modifier

- Merge Distance
- Unsselected：允许selection中的顶点于unselected vertices合并，相当于自动将距离选择的vertices距离小于Merge Distance的unselected vertices也包含进来。否则只merge选择的vertices

## Separating

- Rip Region

  通过创建选择的vertices/edges的副本，副本仍然连接和原来vertices/edges连接的相同的unselected vertices/edges。这样新的edges成为faces的一边，而原来的edges成为faces的另一边

  - Limitations

    Rip只在edges/vertices被选择时有效，并且它们必须是流形mesh（manifold）中间的元素

- Rip Vertices and Fill

  类似Rip Region，但是不是在新edges和旧edges之间留下hole，而是将hold填充fill

## Split

  对于faces，faces与mesh其余部分断开连接，成为独立的一部分

  对于edges/vertices，只是复制它们

  副本分离后仍保留在原地，需要移动它们使其与原来的部分分开

## Rip Edge（使用新vertices rip edge）

  创建选择的vertices的副本，使它们落在距离鼠标最近的edge上，使那些edge被新edge分割为多个edge。可以非常容易地为edge添加更多细节（将大edge分割为多个小edge）

## Separate

  将选择的元素分离到一个新的object中

- Selection：分离选择的元素
- By Material：基于Material ID分离不同的faces到不同的objects
- By loose parts：将每个mesh island分离到一个单独的objects

## Vertex Slide

  将vertex lock在沿着它所在邻接edges上移动，而不是自由移动。使用Shift-V激活这个功能，因为激活时鼠标的位置非常重要，如果有一组顶点被选择，则根据距离鼠标最近的那个vertex确定沿着哪个edges进行移动。即鼠标到最近vertex的相对位置应用到每个vertex上，然后每个vertex基于这个offset判定应该在哪个edge上移动。移动距离也是受限的，最远只能移动到edge的另一端。在Adjuest Last Operation面板中，Factor可以重新调整移动的百分比（0～1）。

- Factor：控制vertex在edge上移动的百分比
- Even（E）：默认每个vertices在各自的edge上移动的距离是edge长度的百分比，将开始时距离鼠标最近的vertex在它的edge上移动的百分比为应用到每个vertex在各自edge的移动。开启这个选项，使得移动按照绝对移动距离应用
- Flipped（F）：在Even模式下，反转Factor的计算方式。默认0是在初始位置，1在edge的另一端位置。Flipped之后0表示在另一端，1表示在原点
- Clamp（Alt/C）：Toggle是否可以在edge的扩展方向slide（默认只能在edge之内slide）。通常用于边界顶顶点，即vertex所在移动的edge的另一侧没有edge，这样默认vertex只能在一侧的edge上移动，而关闭Clamp，则可以沿着edge向相反的方向任意移动。此时运动只限定在初始确定移动的edge，而不能在移动时再切换edge

  Even、Flipped、Clamp都可以在Adjust Last Operation面板上调整，但是也可以在移动时通过快捷键激活，因为Slide进行时会占用鼠标而且没有Adjust Last Operation面板，因此快捷键是非常有用的

## Smooth Vertex

应用一次Smooth Tool

## Convex Hull

将一个point cloud作为input，输出一个包围这些verties的convex hull。如果input包含edges或faces位于convex hull之上，它们也将被作为输出。这个工具也可以用作bridge tool。

- Delete Unused：移除没有作为hull一部分的selected元素，unselected的元素不被删除
- Use Existing Face：如果可能，使用已存在的位于hull上面的input faces。这允许hull包含n-gons而不仅仅是triangles（或quads，如果join triangles选项打开）
- Make Holes：Deleted selected faces that are used by the hull（TODO）
- Join Triangles：将相邻的triangles合并为quads，与Tris To Quad操作相同的参数
  - Max Face Angle
  - Max Shape Angle
  - Compare UVs
  - Compare VCols
  - Compare Seam
  - Compare Sharp
  - Compare Materials

## Add Hook

添加一个Hook Modifier到选择到元素上。Vertex Parent相反到效果。Vertex Parent是让其他object随着vertex移动，而Hook是让vertices随着object移动

Hook Modifier可以在Modifier面板上看见

如果当前object没有关联到hooks，下面到选项只有前两个会出现

- Hook to New Object

  为当前object创建一个hook，创建一个empty object作为target，将选择到vertices赋予这个hook

- Hook to Selected Object

  将选择到Object作为target。在Object Mode下选择target object和要hook的object，进入Edit Mode，选择vertices，在Vertex菜单中选择Hook to Selected Object

- Hook to Selected Object Bone

  类似Hook to New Object，但是它将一个选择的armature中的一个选择的bone作为target

- Assign to Hook

  将选择的vertices赋予一个选择的hook。先清除hook中现有的vertices。一个vertex可以赋予多个hook

- Remove Hook

  从Modifier Stack 中移除选择的Hook

- Select Hook

  选择指定hook中的所有vertices

- Reset Hook

  选择的Hook Modifier中的reset按钮

- Recenter Hook

  选择的Hook Modifier中的Recenter按钮

