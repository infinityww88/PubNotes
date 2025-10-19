# Deploying for mobile

iPhone相对受限，因此需要一些额外的注意

在iPhone上，如果使用stripping（Assembly or bytecode），需要找到Assets/AstarPathfindingProject/link.xml，并将它放在Assets/link.xml。这个文件指示AOT（ahead-of-time）编译器不要剥离文件中提到的classes。否则，在一些情况下可能得到一些errors，例如当试图使用caching时

如果使用Fast But No Exceptions选项，需要开启ASTAR_FAST_NO_EXCEPTIONS（A* Inspector）。

## Optimize for mobile

当开发iPhone时，Caching Startup是个好主意，尤其是使用Recast graphs。
