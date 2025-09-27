non-convex 的 MeshCollider 不能挂载 non-kinematic rigidbody 作为动态刚体使用。除此以外可以和正常 Collider 一样工作，可以和 kinematic rigidbody 一起使用，可以作为 static collider（仅有 collider，没有 rigidbody），可以作为 trigger。



Convex MeshCollider 可以正常用于动态刚体。Non-Convex MeshCollider 可用于静态 collider，和 trigger，可以和其他任意形状的动态刚体正常碰撞。



Mesh Collider 可以精确匹配一个 Mesh 的 shape，用于极为精确的 collision 模拟。



Mesh Collider 构建一个 collision geometry 以匹配 assigned Mesh，包括它的形状，position，scale，以创建精确和真实的碰撞。



Mesh Collider 的精确度，是以比 primitive collider（例如 Sphere，Box，Capsule colliders）更高的处理负载为代价的。因此，最佳实践是只对哪些不需要很高处理性能需求的 collider 使用 Mesh Collider，否则可以使用 Primitive Colliders 的 Compound Collider 更好：



* 物理碰撞体不需要严格匹配 Mesh，只需要大概匹配 Mesh 的形状即可
* 即使复合的 Primitive Colliders，处理性能相对也更低
* 复合的 Primitive Colliders 可以模拟 non-convex MeshCollider，并挂载 non-kinematic rigidbody，模拟动态刚体



绝大多数情况下，Mesh Colliders 提供与 Compound Colliders 类似的解决方案：它们的主要目的是为复杂的形状提供精确的碰撞体。



Mesh Colliders 的主要优势是：



* Mesh Colliders 是极为精确的模拟，因为它完美匹配刚体的形状
* Mesh Colliders 比 Compound Colliders 需要更少的开发时间，因为 Unity 基于 Mesh 的形状自动处理它们的形状
* 一些情况下，Mesh Colliders 比 Compound Collider 需要更少的计算需求，尤其是对于那些非常复杂、需要使用很多 Compound Colliders 近似模拟的形状的情况。一个 Mesh Collider 可能比很多个 primitive colliders 更高效



Mesh Colliders 的显著限制：



* Mesh Colliders 不能提供 concave shapes（凹形状）之间的精确碰撞
* 一些情况下，Compound Colliders 比  Mesh Colliders 需要更少的计算。尤其是只需要几个很简单的 primitive colliders 就能近似模拟的 Mesh 的情况，以及对于不需要精确模拟的形状
* Mesh Colliders 对于运行时会改变的 Meshes 不是好的选项



\# Concave 和 Convex Mesh colliders



根据是标记为 concave 还是 convex，mesh colliders 的行为也不同。默认 PhysX 将 Mesh colliders 标记为 concave。



Concave colliders 有一些限制：Concave Mesh Collides 只能用于静态 collider（不是动态物理刚体），或者 Kinematic ribidbody。Concave Mesh Colliders 只能和 convex colliders 碰撞。如果两个 concave colliders 发生重叠，不会发生碰撞。



如果你有两个 concave Mesh colliders 需要碰撞：



* 如果不需要在 concave 的部分（凹陷的部分）发生精确碰撞，使一个 Mesh Colliders 标记为 Convex。这产生一个称为 hull（包围壳）的新 convex collider
* 如果需要在 concave 的部分发生精确碰撞，使用 primitive convex colliders 构建一个 compound collider



\# 在运行时改变形状的 Meshes



为 Mesh Collider 指定的 Mesh 理想情况下在运行时不应该改变。



每次 Mesh 改变形状，物理引擎需要重新计算 Mesh collider geometry，这会导致显著的性能消耗。出于这个原因，你不应该修改  Mesh Collider 使用的 Mesh 的 geometry。如果一个 Mesh 既需要碰撞，也需要在运行时改变形状，最好使用 Primitive Colliders 或 Compound Primitive Colliders。



Mesh 的碰撞面是单面的，只能在一侧碰撞，另一侧不会碰撞，自由穿越。



