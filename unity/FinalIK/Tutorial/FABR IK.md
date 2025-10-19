FABRIK 和 CCDIK 一样都是集成 IKSolverHeuristic。二者的用法一样，暴露的参数也一样。唯一的区别就是内部 IK Solver 的算法。

CCD 在 rotation space 解析 solver（通过旋转 bones 达到 target），FABR 则是在 position space 解析 solver（通过移动 bones 到达 target）。

看起来 FABR 效果更好一些，尤其是对于更长的骨骼链。

FABR 通常比 CCD 使用更少地迭代到达 target，但是每个迭代中更慢，尤其是应用 rotation limits 时。

FABRIK 中 bone 的长度可以在运行时改变（因为它通过 position 达到 target）。

和 CCD IK 一样，FABR IK 也可以约束在 Root XY 平面上。
