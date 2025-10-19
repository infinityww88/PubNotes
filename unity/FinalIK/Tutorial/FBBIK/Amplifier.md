相对于 character root 或者另一个身体部分，来增强身体某一部分的运动

## Body

- EffectorLink class：到 effector 的连接
  - FullBodyBipedEffector effector
  - float weight：使用这个 effector 的权重

- Transform transform
- Transform relativeTo
- EffectorLink[] effectorLinks
- float verticalWeight：沿着 character up axis 的增强幅度
- float horizontalWeight
- float speed：增强的速度，0 意味着立刻

增强= effector 旋转加倍 + effector 位移加倍

在 relativeTo 空间读取 tranform 的相对位移变化，然后将变化依次应用到 effectorLinks 中每个 effector 的 positionOffset 上。

## Amplifier

- Body[] bodies：可以在一个 Amplifier 中定义多个增强关系

```C#
// Apply the amplitude to the effector links
for (int i = 0; i < effectorLinks.Length; i++) {
    solver.GetEffector(effectorLinks[i].effector).positionOffset += offset * w * effectorLinks[i].weight;
}
```

Dummy 1 定义了 Pelvis、Left Hand、Right Hand 相对于 Dummy Transform 的增强

Dummy 3 定义了 Pelvis、Left Foot、Right Foot 相对于 Dummy Transform 的增强