# Create Mesh

使用一个或多个VMeshes（CG理论上的mesh数据）创建真正的Unity Meshes。所有mesh都被创建，除非你链接spots（transforms）到这个模块，此时将会迭代提供的spots来创建mesh

这个模块于CreateGameObject模块非常类似，只是CreateGameObject创建一组独立的GameObject，而CreateMesh可以创建合并的Mesh

当CG从两个模块读取不同的数组（Spots[\]，VMesh[\]，Bounds[\]，GameObject[\]）时，以循环的方式从一个数组取的一个元素，然后从另一个数组中取得一个，然后两者进行匹配

Spot似乎不仅仅是Transform，还带有一个索引（0，1，2）。例如在CreateMesh中，会依次迭代输入的Spots[\]中的每个元素，然后使用当前迭代的spot的索引去VMesh[\]中获得对应的Mesh

Volume Spots模块沿着Path创建Spots。输入的Volume/RasterizedPath确定使用path，Volume不是要使用它的体积，而是CG中，Volume也是Path的子类，也是通过Path生成的，因此可以直接使用Volume作为Path的输入，即使用创建Volume时的曲线。Bounds[]包围盒用来确定如何沿着曲线分布物体，因为确定物体的间隔需要确定物体的大小。包围盒是最简单最有效的确定物体的大小的方式。通常Bounds就是Input GameObject模块或VMesh模块，因为GameObject和VMesh都是Bounds的子类。通过GameObject或VMesh的Mesh计算出物体的包围盒。Volume Spots创建的Spots一定是带索引的，子Group中每个Item引用的每个Bound都记录了这个Bound在输入的Bounds[\]中的索引。因此输出给CreateMesh的Spots记录这每个Spot使用第几个元素。因此对于CreateGameObject或CreateMesh来说创建Spots时使用的Bounds[\]和GameObjects[\]（CreateGameObject）/VMesh[\]（CreateMesh）应该是一一对应的，甚至通常就是同一个输入，因此GameObject和VMesh都可以作为Bound输入，尽管它们可以是不同的，只要能确保Bound和对应的GameObject/VMesh匹配的上就没有问题，但这需要额外但关注，因此通常只需要将InputGameObject/InputMesh同时链接到Bounds[\]和GameObjects[\]/VMesh[\]就可以了

Input Spline Path是理论上的曲线，RasterizePath提供了选项将它栅格化

如果不输入Spots，输入的VMesh被原地合并创建，否则沿着Spots依次排列

## Slots

- VMesh[]：VMeshes的数组
- Spots（可选）：用来放置的transforms（沿着transform\[]依次迭代VMesh[]每个元素）（TODO）

## 通用选项

- Combine：Meshes被合并为一个单一mesh。如果VertexCount超过65k，会创建额外的mesh

- Group Meshes：如果提供了Spots，meshes将会按照VMesh index合并为submesh，这样可以为每个submesh赋予单独的材质

- Add Normals

    是否应该计算normals

  - Yes：总是计算normal
  - No：从不计算normal
  - Auto：只在输入的VMesh没有提供normal时才计算

- Add Tangents

    切向量，参加Add Normals

- Add UV2

    创建lightmap的UV

- Make Static

    创建的Mesh具有static flag set

- Layer

    使用的Layer

## Renderer选项

与Unity Renderer选项相同，除了

- Renderer Enabled：创建的mesh将没有enabled的Renderer。通常生成的mesh只用来作为碰撞体

## Collider选项

定义添加给创建的mesh的碰撞体

- Convex：Mesh Collider only。是否创建一个convex MeshCollider。Unity相应的Mesh Collider选项
- Auto Update Colliders：mesh改变时是否自动更新
- Material：赋予MeshCollider的物理材质

## Export选项

- Save To Scene：在Scene中创建独立的GameObject包含Meshes，并移除CG管理相关资源
- Save Mesh Assets：创建包含所有meshes的mesh资源
