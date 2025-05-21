使用一个 Spline 来约束 camera 沿着预定义的 path 移动。

使用一个 Spline 来指示一个固定的路径来定位和动画一个 CinemachineCamera。使用 Spline Dolly behavior 让 CinemachineCamera 沿着 Spline path 移动。

- GameObject > Cinemachine > Dolly Camera With Spline。一个新的 Cinemachine Camera 和 Spline 出现在 Scene 中。
- 在 Spline Inspector 或 Scene View 中添加 waypoints。

任何 Unity Spline 都可以用作 path，只需要将它拖拽到 Spline Dolly Spline 属性中，然后 Cinemachine 立即就会被约束在 Spline 上。

默认 Unity Spline 不包含 rotation 数据。Camera rotation 将会根据 spline 的 tangent 和 world Up 向量得出。要添加 rotation，可以使用 Cinemachine Spline Roll behavior。这可以沿着 spline 为任何一点指定 Roll values。Roll values 用来根据任何一点的 spline tangent 来 rotate camera，提供关于 camera 最终 rotation 更多的控制。

如果 Cinemachine Spline Roll bahavior 添加到 spline，所有使用这个 spline 的 cameras 和 dolly carts 都会看见它。或者，可以添加 Cinemachine Spline Roll behaviour 到 Cinemachine Camera 上，这样 roll 将只会应用到它上面。