OffsetModifier 是所有 FBBIK effector positionOffset modifiers 的基类。

它们都用来修改 positionOffset.

positionOffset 是 Effector 的属性，用来偏移 Effector 的 position 属性。

每个 Update 之后 Effector 会重置 positionOffset 为 zero。如果 effector positionWeight = 1，这没有效果，因为 hand 的位置完全跟随 effector

## OffsetLimits

限制 effector position offsets

- FullBodyBipedEffector effector：effector 类型，这只是一个 enum
- float spring：Spring 力，如果为 0，则这是一个硬性限制，否则 offset 可以超过这个限制
- bool x, y, z：在哪些轴上限制 offset
- float minX, maxX, minY, maxY, minZ, maxZ：每个轴上的限制
- void Apply(IKEfffector 3, Quaternion rootRotation)：应用 limit 到 effector

## OffsetModifier

- float weight：master weight
- FullBodyBipedIK ik：引用 FBBIK 组件
