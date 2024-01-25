# Navmesh Cutting

Navmesh cutting 用于快速 recast graph updates。它在 recast graph 生成的 navmesh 上切开一个 hole。Recast graphs 通常只允许改变现有 nodes 的参数（例如使整个 triangle unwalkable），这不是很灵活，而重新计算整个 tile 又很慢。使用 navmesh cutting 可以从 navmesh 移除部分（被 obstacle 例如 RTS 游戏中新建筑阻塞的部分），但是不能添加新的 surface 到 navmesh，或改变 nodes 的 position。

NavmeshCut 组件使用 2D shape 来剪切 navmesh。内置的是 rectangle 和 circle，但是还可以指定一个自定义的 mesh。自定义 mesh 应该是一个 flat 2D 形状。脚本会找到 mesh 的轮廓线，并使用这个 shape 来剪切。确保所有 normals 是 smooth 的，并且 mesh 不包含 UV 信息，否则 Unity 可能会分离 vertex，这样脚本就不能找到正确的轮廓线。不要使用非常高面数的 polygon mesh，因为这会在 navmesh 中创建大量 nodes，并使 pathfinding 变得更慢。甚至高面数的 mesh 会因为非常细的 triangles 添加到 navmesh 而导致计算出次优的 paths。

注意 shape 不是 3D 的，因此如果旋转了 cut，会看见 2D shape 旋转然后只是投影在 XZ 平面上。

要在 scene 中使用 Navmesh cut，需要有一个 TileHandleHelper 脚本在 scene 中，并且只应该有一个。这个脚本关心所有的 NavmeshCut 组件来检查它们是否需要更新 navmesh。在 Scene View 中，NavmeshCut 看起来就像一个 extruded 的 2D 形状，因为 navmesh cut 还有一个 height。它只会 cut navmesh 中它接触的那部分。出于性能原因，它只检查 navmesh 中 triangles 的 bounding boxes。因此它可能 cut bounding boxes 和其相交的 triangles 即使那个 triangle 和 extructed shape 并不相交。但是绝大多数情况下这并没有很大区别。还可以设置 navmesh cut 为 dual 模式（设置 isDual field 为 true）。这会防止在 navmesh 中 cut 一个洞，相反它仅仅沿着 border split navmesh，但是仍然保持 interior 和 exterior（即沿着 shape 边界将 navmesh face 切开，同时保留切开后的内外 surface，就像 Blender 中的 Project Knife 工具一样）。如果想改变一些 region 的 penalty，而 region 不完全和 navmesh triangles 对齐，这很有用。它通常和 GraphUpdateScene 组件一起使用（但是注意当 graph 再次更新时，GraphUpdateScene 组件不会自动 reapply penalty）。默认 navmesh cut 不会考虑 rotation 和 scaling。如果想要，可以设置 useRotation 为 true。这会慢一点，但是不会差距太大。

