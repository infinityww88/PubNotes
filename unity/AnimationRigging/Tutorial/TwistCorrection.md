这个 Rig 和 TwistChain 有点相似。它指定一个 source bone，在指定一组受影响的 bones 列表。Source bone 的旋转将会按照指定的权重分配给相应的 bone。

还可以指定一个分配哪个 Axis 的旋转。

更像是一个分配旋转的 rig，和 Multi-Rotation Rig 很像，但是只应用到一个轴上。但是 M-Rot 是用多个 source 约束一个 target，而 Twist Correction 则是用一个 source 影响多个 target，按照一定权重分配旋转。

