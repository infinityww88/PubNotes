# Automatically generating a navmesh

使用RecastGraph自动生成一个navmesh。

Recast graph体素化场景中的所有mesh（不是colliders），使用诸如character height，character radius和其他设置生成walkable navmesh。

直接scan graph通常不会给出任何好的结果。首先点击Recast Graph的Snap bounds to scene按钮，它查找场景中的所有mesh，配置graph的bounds来包围它们，也可以手动使用Center/Size/Rotation设置包围盒。

Width/Depth表示包围盒提诉的分辨率，不可以直接编辑，调整cell size（体素大小）来编辑。

Recast graph使用tiles将graph分割成方形的chunks（体素的group）。可以disable tiles。

使用tile的好处：

- 可以并行scan每个tile，大大加快scan的速度
- 可以在运行时独立更新每个tile，这比更新整个graph快的多
- navmesh cutting在tile基础上操作，而更新一个tile快的多
- 它将非常大大polygons分散，减少出现suboptimal paths大风险

没有最佳tile size，但是常用只大概为64～256

类似状态机和子状态机，A*现在tile之间寻路，然后在每个路径上的tile里面寻路。

默认所有mesh都会参与navmesh大计算，包括character mesh，但这不是我们想要的。将不应计入生成navmesh的gameobject放到一个单独的layer，在Recast Graph的Layer Mask中排除此layer。

一个很大的world的Recast graph可能要花费很多时间scan。可以通过cache result来提高startup的时间

