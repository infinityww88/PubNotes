# Inverse Kinematics

PuppetMaster 可以想 Final IK 一样和 Unity 内置的 Animator IK 一起使用。后者限制只用于 Humanoids，并可以用于在 PuppetMaster 在读取它用于 following 之前程序化修改 target pose。

Final IK 打开了更多的可能性，例如使用 full body IK 修改 pose，或者在物理模拟上面应用一个 IK pass 用于美化修正或精确瞄准。

## Final IK:

要和 Final IK 一起使用 PuppetMaster，将两个 packages 都导入 project 中，然后导入 Plugins/RootMotion/PuppetMaster/_Integration/Final-IK.unitypackage。Package 所带的 scenes 和 scripts 展示了在 PuppetMaster solver 之前和之后应用 IK。

## IK Before Physics:

我们可能想要因为各种原因使用 IK 来改变 Target pose，例如保持平衡，瞄准，grabbing，从即将到来的碰撞过程化的移动中保护自己。当使用 Unity 内置的 IK solution 时，它将会在 Mechanim update cycle 中自动应用在 animation 上面。Final IK 的组件还会默认地在 PuppetMaster 读取之前更新。如果你需要它们以特定顺序更新，你可以使用 IKBeforePhysics 组件，或者关闭它们并使用 PuppetMaster.OnRead delegate 手动更新它们的 solvers。

```C#
public PuppetMaster puppetMaster;
public IK[] IKComponents;
void Start() {
    // Register to get a call from PuppetMaster
    puppetMaster.OnRead += OnRead;
    // Take control of updating IK solvers
    foreach (IK ik in IKComponents) ik.enabled = false;
}
void OnRead() {
    if (!enabled) return;
    // Solve IK before PuppetMaster reads the pose of the character
    foreach (IK ik in IKComponents) ik.GetIKSolver().Update();
}
// Cleaning up the delegates
void OnDestroy() {
    if (puppetMaster != null) {
        puppetMaster.OnRead -= OnRead;
    }
}
```

## IK After Physics:

每一帧 PuppetMaster 完成 solving 和 mapping Target character 到 ragdoll 之后，我们有一个机会对 character pose 进行一些细微调整（不再改变 physics）。这可以用于例如确保 hands 完美地放在一些位置上，或者使用 AimIK 进行瞄准修正。Unity 内置 IK 不能再 PuppetMaster 将 Target character 映射到 ragdoll pose 之后应用。Final IK 组件可以在任何时候更新，在此情况下我们需要在 PuppetMaster.OnWrite delegate 中完成它。

```C#
public PuppetMaster puppetMaster;
public IK[] IKComponents;
void Start() {
    // Register to get some calls from PuppetMaster
    puppetMaster.OnWrite += OnWrite;
    // Take control of updating IK solvers
    foreach (IK ik in IKComponents) ik.enabled = false;
}
// PuppetMaster calls this when it is done mapping the animated character to the ragdoll so if we can apply our kinematic adjustments to it now
void OnWrite() {
    if (!enabled) return;
    // Solve IK after PuppetMaster writes the solved pose on the animated character.
    foreach (IK ik in IKComponents) ik.GetIKSolver().Update();
}
// Cleaning up the delegates
void OnDestroy() {
    if (puppetMaster != null) {
        puppetMaster.OnWrite -= OnWrite;
    }
}
```
