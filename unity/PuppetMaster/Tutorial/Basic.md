播放 scene，滑动 Pin Weight 到 zero，来释放 character 到 physical muscle space 动画。

尝试所有其他参数，展开 Muscles 以对每个 muscle 单独地调整 weight multiplier。

要从一个 ragdoll 创建一个 PuppetMaster：

1. 拖拽一个 ragdoll character 到 scene 中。如果 ragdoll 不是使用 ConfigurableJoints 构建，选择它的 root GameObject，并点击 GameObject/Convert to ConfigurableJoints。你还可以使用 BipedRagdollCreator 组件来创建和修改 biped ragdolls

2. 添加 PuppetMaster 组件到 ragdoll character 的 root Transform

3. 指派 Animated Target。它可以被设置为同一个 GameObject，此时，它将被复制并清理所有 ragdoll 组件。它还可以是一个 character 的实例，或者甚至另一个 character，只要 bones 的 positions 匹配。bones 的 rotations 不需要一样。这使得共享 ragdoll 结构成为可能，并且当 feet bones 与地面对齐时非常有用（例如 Mixamo characters）。此时，你可以简单地旋转 ragdoll 的 feet 来对齐 ground，而保持 target 的 feet 在原来的位置

4. 点击 Set Up PuppetMaster

You should now have your character set up in an animated target - ragdoll duality, parented to a root GameObject. 
This dual setup enables you to focus on animating your character, forgetting about the ragdoll part that is managed by the PuppetMaster. It also enables you to disable the PuppetMaster and deactivate the entire ragdoll by simply setting its "Mode" to "Disabled" when you don't need it.

Note that it would be technically possible to set it up as a single ragdoll character, but it would multiply the cost of performance because of having to move GameObjects with colliders back and forth in each update cycle. That price would increase further if you had to solve some IK on those bones. With a dual setup, however, you can do all the procedural kinematic adjustments on the kinematic target character without any extra performance cost from the dynamics side. Add that to the benefits of sharing ragdolls between characters in a future release of PuppetMaster. ;)

All Puppet Behaviours should be parented to this GameObject, the PuppetMaster will automatically find them from here.

All Puppet Behaviours have been designed so that they could be simply copied from one character to another without changing any references.
It is important because they contain a lot of parameters and would be otherwise tedious to set up and tweak.

