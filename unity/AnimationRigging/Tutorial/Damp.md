Damp 约束定义一个 target object（constrained object）相对于 source object 延迟阻尼运动，即 source object 的运动以一定地延迟传递给 target object。

这个例子中，包含了一串 object。动画中只定义了 head object 的动画，模型中定义一组 bone，一共 10 个，然后在 rig 下面定义了 9 个 damp 约束，第 i 个约束第 i 个 bone 阻尼地跟随第 i - 1 个 bone。不像其他 demo，rig 下面的 gameobject 只用来定义约束，不用于约束中的 source object。

当动画文件 animate head 时，然后阻尼约束以一定延迟将变化传递给后面的 bone。

Constraint 组件可以放在 rig 下面的任何 GameObject，不仅仅是直接 Child GameObject，可以用来方便组织。
