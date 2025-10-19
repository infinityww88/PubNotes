# Navmesh Cutting

Navmesh cutting被用于在现有的navmesh/recast graph（navmesh cutting不是针对grid graphs的）上挖出一个洞。Recast/navmesh graphs通常不允许改变现有nodes的参数（例如使一个三角形unwalkable），这样就不够灵活，也不允许重新计算整个tiles，这会非常慢。

使用Navmesh cutting可以移除（cut）navmesh的一部分，这些部分是被obstacles阻塞的区域，例如RTS游戏中一个新建的building。但是不能想navmesh添加新东西或改变nodes的位置。这远比recast graph重新计算tiles更快，而navmesh不能运行时重新计算。

Navmesh cutting通过NavmeshCut组件完成。

NavmeshCut组件使用一个2D形状来cut navmesh。内置的是circle和rectangle形状，但是还可以指定自定义mesh。shape不是3D形状，因此如果旋转NavmeshCut，不会旋转定义的shape。

**如果Navmesh Cut看起来没有正常工作，重新Scan一下**

NavmeshCut看起来就是extruded 2D形状。这是因为navmesh cut还具有高度。它只cut navmesh接触的部分。出于性能原因，它只检查navmesh中triangles的包围盒。因此它可能会cut那些包围盒和它相交但是triangle没有接触的triangles。但是绝大多数情况下，这没有很大的差别。

isDual设置navmesh cut为dual mode。这阻止它在navmesh上cut hole，而是将navmesh沿着hole的border分离为内部区域和外部区域。这可以用于改变一些不能和navmesh triangles对齐的区域的penalty（代价）。Penalty（代价）影响启发函数，使得相应的区域更容易或者更难通过。它通常和GraphUpdateScene组件一起使用（但是当graph更新时，GraphUpdateScene组件将不会自动重新应用跟新的代价）

默认navmeshcut不会考虑GameObject的rotation和scaling。如果要考虑，设置useRotationAndScale=true。这可能会慢一点，但是没有太多影响。Rotation和Scale只考虑XZ平面上的分量。

## 自定义meshes

绝大多数情况下使用内置的shape就足够来。但是一些情况下使用自定义mesh cutting mesh可能很有用。自定义mesh应该是一个flat的2D形状。Script会找到mesh的轮廓并使用这个形状来cut navmesh。确保所有normals都是smooth的，并且mesh不包含UV信息。否则Unity会将一个vertex分离为多个vertex（顶点数据不同），然后script将不能找到正确的轮廓。不应该使用high poly模型因为这将在navmesh graph中创建大量nodes并使pathfinding变得缓慢，甚至可能导致suboptimal path，如果high poly给navmesh引入很多细小的triangles。

## 通过代码控制更新

Navmesh cuts是周期应用的。但有时希望立即应用。

```C#
// 调度pending updates一旦pathfinding threads完成它们当前的工作立即完成
AstarPath.active.navmeshUpdates.ForceUpdate();
// 阻塞线程知道updates完成
AstarPath.active.FlushGraphUpdates();
```

还可以控制script检查navmesh是否改变的频率。如果有大量的cuts，不过于频繁检查cuts有利于性能

```C#
// 每帧进行检查（默认）
AstarPath.active.navmeshUpdates.updateInterval = 0;
// 每0.1秒检查一次
AstarPath.active.navmeshUpdates.updateInterval = 0.1f
// 从不检查，手动调度udpates
AstarPath.active.navmeshUpdates.updateInterval = -1;
AstarPath.active.navmeshUpdates.ForceUpdate();
```

可以在AstarPath inspector上找到这些设置

## Navmesh cutting和tags/penalties

因为navmesh cutting可以任意地修改navmesh triangles，因此不太可能在更新graph时保持tags和penalties。Graph更新时那些保持不变的node的Tags和Penalties将被保持。

如果需要使用tags，唯一稳定保持它们的方式是每次navmesh cut更新完成时应用所有的graph updates。这相对很慢，但至少能工作。
