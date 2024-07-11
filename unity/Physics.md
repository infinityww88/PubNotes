# Physics

GameObject 有两个 bound。一个是 MeshFilter 通过 mesh 计算，一个是通过 MeshCollider 计算。

Bounds 有两个属性构造：center + size，还暴露 min 和 max 两个属性，分别对应 bound 的左下角和右上角。

MeshFilter.sharedMesh 在 local 空间计算的 Bounds，MeshCollider 在 world 空间计算 Bounds。因此：

- 通过 mesh 计算的 Bounds size 和 shape 是固定的（除非 mesh vertices 更新），不能反映 GameObject 在 world 的变化。例如当 GameObject 旋转时，Bounds 也在 world 中旋转（它只在 local 空间是 AABB 的）
- 通过 Collider 计算的 Bounds 会根据 GameObject 在 World 空间中的变化而更新，总是反映 GameObject 在 World 中的实时 AABB。但是 collider.bounds 不会随着 GameObject 的变化而立即更新，而是在多个 frame 中逐渐更新，具有最终一致性

要立即得到 GameObject 在 world 空间的实时 AABB bounds，只能通过 mesh.vertices 和 transform 手动计算。

