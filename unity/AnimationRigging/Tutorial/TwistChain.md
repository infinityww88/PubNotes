Twist Chain Constraint 通过指定 root 和 tip 指定一个 bone chain，然后为 root 和 tip 各指定一个 twist source gameobject。

这个实例中 root 的动画片段只包含 source root 和 tip 的 rotation。没有 RigBuilder 时，source root 和 tip 的旋转不会影响模型上的 Cubes。但是当开启 RigBuilder 之后，source root 和 tip 的旋转被插值到 root 和 tip 之间的每个 bone 上。

