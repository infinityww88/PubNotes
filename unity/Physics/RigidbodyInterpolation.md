# Apply interpolation to a Rigidbody

Interpolation 提供一个方式处理 Rigidbody GameObject 运行时运动的抖动现象。

Jitter 可能出现在 physics simulation 更新的频率（由 Fixed Timestep 决定）比 application frame rate 慢的情形。这在 camera 跟踪一个 physics-based 运动的 Rigidbody 时尤其明显。

Unity 的 PhyX 系统提供一种方式实现 interpolation。Rigidbody 上的 Interpolation 设置提供两个选项来平滑 Rigidbody 的运动：Interpolation 和 Extrapolate。

Interpolation 和 Extrapolation 都是在 physics updates 之间计算 Rigidbody 的 pose（position 和 rotation）。应该使用哪个依赖于哪个选项能为你的应用场景提供最好的视觉效果。

你只应该在察觉到 Rigidbody 运动出现 jitter 时使用 Interpolation 或 Extrapolation。默认 Interpolate 为 None。

当开启 Interpolation 或 Extrapolation 时，物理系统控制 Rigidbody 的 transform。由于这个原因，你应该在任何对 transform 的直接改变（non-physics）之后跟随一个 Physics.SyncTransforms 调用。否则，Unity 会忽略任何不是由 physics system 触发的 transform 改变。

pose = position + rotation


内插值 Interpolate：在两个确定值之间计算中间值

外插值 Extrapolate：在两个确定值之外计算后续值

## Interpolate

注意，插值只在 Rigidbody 出现抖动时使用。尤其是物理帧率低于渲染帧率时，这样渲染帧到来时，时而 rigidbody 移动（到达物理帧），时而 rigidbody 静止（物理帧还没有到来）。

要使用内插值，必须首先有两个确定的物理帧数据。因为物理帧率低于渲染帧率，两个物理帧之间包含多个渲染帧。根据两个确定的物理帧，就可以在渲染帧插值得到相应的数据。

但这也意味着渲染系统无法渲染物理系统当前的状态，因为当前的状态需要到下一个物理帧才能确定。因此要使用插值，渲染系统必须比物理系统慢一个物理帧，即计算完上一个物理帧之后，渲染系统开始渲染上个物理帧和上上个物理帧之间的物理系统状态，这样物理系统才能进行插值。这于网络游戏中缓存一定 input 数据，然后稳定输出服务端权威数据是一个原理。通过慢一点换取稳定输出。但是一个物理帧也是很短的，可能只有 1/30 秒，因此这个延迟非常的不起眼，不会被察觉，但是却可以解决抖动的大问题。

Interpolate 使用前两次的 physics updates 的 Rigidbody pose 来计算和应用 Rigidbody GameObject 在当前帧的 pose（transform 的 position + rotation）。

Interpolate 使得 Rigidbody 比它应该在的位置略微落后了。这是因为 interpolation 延迟了 Rigidbody 的 pose 一个 physics update，使得它能够有两个确定的 point 可以用于插值计算，和足够的时间将 Rigidbody 移动到新的 pose。

注意使用插值时，GameObject 的 transform pose 和 Rigidbody 的 pose 可能不同。Rigidbody pose 是最新的 physics update 之后的 pose，是 interpolation 的第二个 point，transform pose 只能之前一个 point 和这个 point 中间的值。

Interpolation 比extrapolation 更精确，但是它有一个 physics update 的时间延迟。

Interpolation 通常最适合 Rigidbody 的速度不断变化，或者有其他物理元素影响 Rigidbody 的移动的情况。

## Extrapolate

当物理帧率比渲染帧率慢，意味着当渲染帧到来时，最新的物理帧还没开始，因此只有上一个物理帧的数据。Extrapolate 就是使用上一个物理帧的 pose，预测 Rigidbody 在下一个物理帧的 pose，然后计算和预测 GameObject 在当前渲染帧应该所处的 pose。

Extrapolate 使得 Rigidbody 看起来比它应该所处的 pose 更前进一点。这是因为 extrapolation 使用 Rigidbody 当前速度预测 Rigidbody 在下一个（还没到来）物理帧的 pose，这样它可以有两个 point 用于插值计算。

Extrapolation 通常不太精确，并且可能轻微穿透 collision 边界（注意，只是 GameObject 的 Mesh 穿透，不是 Collider 穿透，因为物理系统分别控制 GameObject Transform 的 pose 和 Rigidbody 的 Pose），并在下一个物理帧后修复。这是因为 extrapolation 计算不考虑未来 physics force 或计算。

Extrapolate 通常仅适合于精确度不是那么重要的情况。例如 Rigidbody 以一个常量速度运行，并且没有其他物理元素影响 Rigidbody 的运动。
