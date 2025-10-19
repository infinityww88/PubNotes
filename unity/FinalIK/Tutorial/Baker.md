这个 scene 展示了如何使用 AimIK 和 Baker 来克服当添加一个 upper body aiming layer 到运动 locomotion 动画 layer 上时的一个非常常见的问题。这通常导致 aiming 不精确和非常僵硬的 spine，因为来自 locomotion 的 spinal motion 将会在 upper body animation 覆盖过程中丢失。这里表达意思是使用 upper body layer 和 lower body layer 叠加生成瞄准动画，可能不够自然，这里使用 AimIK 调整 bones 可以产生自然的动画，然后用 Baker 将整个动画烘焙成一个完整的单一动画，而不再需要 layer 叠加。

用法就是选择 Bake Mode，选择要 Bake 的 States/Clips，AppendName，Save To Folder，然后播放 scene，点击 Bake Animaiton，Baker 就会在 Scene 中播放动画（加速播放），同时烘焙动画数据。对于 States，指定的是 base layer 的数据。虽然也可以指定更上层 layer 的 states，但是没有意义。因为 Base Layer 中的 states 是基本的 states，更上层的 layer 只是用来 additive override 的。Bake 更上层 Layer 的 states 是可以的，但是 Base Layer 处于哪个状态就是随机的了（看之前停留在哪个状态）。

Baker 的基本原理就是在 scene 中播放动画，然后记录播放过程中的输出的动画数据。而当前输出的数据完全取决于动画系统各个 Layer 当前的状态。因此 Bake 要确保各个 Layer 的 State 处于正确的状态。

Ragdoll 也是后处理，当 EnableRagdoll 之后，Ragdoll 的物理模拟完全覆写动画和 IK 的输出。FinalIK 和 Ragdoll 都是对动画数据的后处理，而不管动画是用什么输出的，无论是 Mecanim 还是 Animancer，这就是隔离的好处。模块之间只使用 pose 数据作为接口，就好像 Unix 管道处理文本一样。

FinalIK 和 PuppetMaster 极为强大，但是大部分功能都是非常高级而且有趣的，对于我们要做的注重游戏性的游戏过于复杂，可以在之后的职业生涯中慢慢研究，通过 Demo 的实例都可以学会，先学会我们当前必需的就可以了。

AnimationClip 静态文件就是记录不同骨骼随时间的不同 Transform（关键帧）。对于 Generic 动画，只能用于骨骼结构相同的模型。对于 Humanoid 动画，可以通过 Unity Avater Retargeting 到其他人物模型上。因此 Baker 的 Humanoid 动画可以用于任何人物模型。

