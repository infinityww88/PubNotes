# Transform Orientations

执行各种transform的方向（面向，朝向）

影响Move/Rotate/Scale的行为

在transform时，按下X，transform将约束到Global X上。但是如果按两下X，transform将约束到Local X上

各种orientations可以在3D View header上的Transform Orientation菜单选择

## Orientations

- Global：世界坐标空间

- Local：局部坐标空间

- Normal

  transform gizmo的Z轴将匹配选择的元素的Normal。如果多个元素被选择，它将朝向这些normals的平均值。

  在Object Mode中，等价于Local

- Gimbal：万向坐标系

  使用万向行为，其依赖当前Rotation Mode而改变

- View：3D View空间坐标系，相机空间

## Custom Orientations

使用object或mesh元素自定义orientations

使用object自定义的transform orientations使用它的Local orientation，而使用mesh元素自定义的transform orientations使用selection的Normal orientation

## Align To Transform Orientation

Aligns（旋转）被选择的objects使它们的local orientation匹配当前激活的transform orientation或者Adjust Last Operation里选择的orientation的identity方向
