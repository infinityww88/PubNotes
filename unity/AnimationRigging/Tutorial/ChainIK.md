ChainIK 类似于 FinalIK 中的 FABRIK，可以用于任意长度的 bone chains 的 IK，同时没有定义弯曲平面。只有 3-joints（或 2-segments）骨骼链才定义了弯曲平面，这就对应的是 FinalIK 的 limbIK 和 AnimationRigging 的 TwoBoneIK，因为 3 个 joints 定义了一个平面，但是 FABRIK 的 chain 可以有很多 joints，因此无法定义一个弯曲平面。

ChainIK 的骨骼链通过指定 chain 的 root 和 tip 来定义，因此不能跳过 bone。末端骨骼 tip 就是 effector，然后指定一个 target。

在这里 ChainIK 定义蝎子的尾巴上，上面有很多骨骼。

注意 ChainIK 的 target 不是 Hierarchy 中的 target GameObject，而是 rig 下面 chainIK 本身，这很容易导致误解。实际上一直是 chainIK gameObject 一直在控制尾巴。尾巴 tip 始终钉在 pinned chainIK 上。而动画中蝎子开始攻击了两次 miss 了，第三次攻击才命中，实际上是被动画控制的。蝎子本身的包含了对 chainIK GameObject 的动画，target GameObject 自身也包含了跳跃动画（它的跳跃不是物理效果，而是动画效果）。在两个动画中实现了两次 miss，最后命中的逻辑，而实际上尾巴 tip 始终在跟随 chainIK。

