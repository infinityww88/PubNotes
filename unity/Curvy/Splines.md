# Spline

Curvy Spline 使用 Curvy Spline 构建，它使用带有 Curvy Spline Segment 组件的 Child GameObject 表示控制点 Control Points(CP)，在其他曲线包中也称为 knots。

可以通过创建 Connection 连接两个 CP。

除非显式声明，Spline 和 CP API 返回的所有 position 和 rotation vectors 都是局部于 Spline GameObject 的。

## ControlPoints vs Segments

CP 和 Segments 的关系就像 vertex 和 edge 的关系。在 Curvy Splines 中，CP 和 Segment 用同一个组件 CurvySplineSegment 表示。因此一个 segment 只不过是跨越曲线到下一个 CP 的 CP 而已。即每个 Segment 是一个 ControlPoint，但反之不然。

## Units

- F：一个 spline segment point 通过在曲线公式中输入一个 time（0-1）值来计算出。因此所有处理 segments 的方法，主要是 CurvySplineSegment 组件的方法，都有一个参数 F（fragment）。不要将它误以为是百分比。F 与 length 不成比例关系（但大约接近），F=0.5 不意味着 curve segment 长度的一半。

  F=0 是 curve segment 的开头（CP 的位置），F=1 是 curve segment 的结尾（下一个 CP 的位置）。

  F 主要出现在处理 Segment 的方法，用来在曲线一个段落上定位某个位置。在 API 中，参数名字通常是 LocalF。就像椭圆一样，相同角度的弧线不一定具有相同的长度，要看弧线在椭圆上的位置，尤其是曲率高的地方，弧形更长，曲率小的地方，弧形更短。这就是为什么 F 与百分比是不同的，0.5 不意味着曲线段的一半。但是只要曲线段不是过于弯曲，还是比较接近的，尤其是直线 Linear，F 就等于百分比。

  每个曲线都有自己古怪的公式。

  F 是 Curvy Segment 的 time。

- TF：和 F（LocalF）类似，它是整个曲线的 time，用来在整个曲线上定位一个点。所有处理整个曲线的 API，尤其是 CurvySpline 组件，都使用 TF（Total Fragment）。TF=0 指示第一个 segment 的 startCP，TF=1 指示最后一个 segment 的 endCP。和 F 一样，TF 不正比于 Length。

- Distance

  尽管 F 和 TF 非常适合用来在 curve 上定位位置，但是绝大多数用户希望使用实际的世界 unit 长度。Curvy Splines 可以在 fragments 和 distances 之间进行转换，因此你可以自由地使用想要的单位。

  和 F-Segment（Segment level 方法），TF-Spline（Curvy level 方法）一样，localDistance-Segment，distance-Spline。

  Curvy Splines 中的所有单位值跨越 curve 的可见部分。不构成 segment 的 CP 不能使用这些单位达到，例如 B-Spline 曲线的控制点，都在曲线外面。

  Curvy Spline 内部只使用 fragment（F 和 TF），因此每个接收 distances 的方法都需要内部转换为 fragments，因为直接根据 time 参数通过曲线公式计算得到位置是最高效的方法。distances 得需要将曲线光栅化为小的直线线段，然后在这些直线段上面计算大致的 fragments，最后再带入公式计算得到 Curvy 上的位置。

  通常可以忽略转换带来的 CPU 消耗。但是如果想要每帧移动上千个物体，应该考虑只使用 fragments，或尽量减少转换。

## Spline

- Interpolation: 曲线类型，Linear，Bezier，Catmull-Rom，B-Spline，TCB。

- Restrict To 2D：将曲线限制在 2D 平面，可以指定 XY, XZ, YZ 平面。

- Closed：曲线是否应该是闭合的，即最后一个 CP 是否应该与第一个 CP 构成一个 segment。

- Auto End Tangents：只用于 Catmull/TCB 曲线，第一个 CP 和最后一个 CP通过曲线方向自动计算。

- Orientation

  如何计算曲线旋转 orientation。

  - None：没有 orientation

  - Static：使用 CP transform rotation

  - Dynamic：计算一个最小的角度，平滑 orientation。这个模式中，direction vector 使用一个最小可能角度在两个 orientation anchors 之间平滑过渡。要控制这个过程，可以在特定 Control Points 开启 Orientation Anchor。注意，第一个 CP 自动被定义为 Orientation Anchor。

### 高级设置

- Show Gizmos：是否在 SceneView 中显示 spline gizmos。

- Color：用于 spline gizmos 的颜色。默认值可以在 Editor Preferences。

- Active Color：曲线被选择时显示的颜色。

- Cache Density：定义 cache 密度。

- Max Points Per Unit：每个 world 单位长度采样点的最大数量。采样被用于 caching，spline rasterization，和 shape extrusion。

- Use Pooling：CP 被缓存，删除时被 disabled 之后重用，而不是销毁再创建它们。这在运行时添加和移除大量 CP 时可以防止帧率跳水。Pooled GameObjects 被 Curvy Global Manager 存储。

- Use Threading：开启时，cache 在多个线程中完成。当前不支持 WebGL 平台。

- Check Transform：只用在 Play Mode。开启时，任何对 CP Transform 的修改都导致 spline 进行相应更新。如果在 Play Mode 不需要修改 Transform，关闭这个选项可以提升性能。

- Check Update：spline 更新的 PlayLoop，Update/LateUpdate/FixedUpdate。

### Events

可以通过添加 handler 到 UnityEvents 响应 spline 相关事件。

- OnInitialized：spline 初始化时调用。
- OnRefresh：每次 spline 刷新时调用，包括它的初始化 Update。
- OnAfterControlPointChanges：添加或删除一个多个 CP 时调用。
- OnBeforeControlPointAdd
- OnAfterControlPointAdd
- OnBeforeControlPointDelete

## Curvy Spline Segment

曲线段组件。

- Bake Orientation（Dynamic orientation only）：开启时自动设置 transform 的 rotation 到计算的 dynamic orientation。要仅设置一次 rotation，关闭这个选项，并使用下面的按钮。
- Orientation Anchor（Dynamic Orientation only）：开启时，CP 被标记为 orientation target。
- Swirl（Orientation Anchor only）：只用于 Orientation Anchor CP。使用这个选项可以添加旋涡到当前的 anchor group。一个 anchor group 的范围是当前 CP 到下一个定义的 Orientation Anchor（或者 End CP）。

第一个 CP 自动定位为 Orientation Anchor。最后一个 CP 不能定义 Orientation Anchor，因为 Anchor Group 可以定位到 End CP，因此也可以认为 End CP 也自动定义为 Orientation Anchor。但是第一个 CP 可以定义 Swirl，End CP 则不能，因为最后一个 CP 不再定义 Segment，最后一个 Segment you End - 1 CP 定义。如果 Spline 是 closed 的，则 End CP 表现的就像其他 CP 一样，因为它和第一个 CP 构成最后一个 Segment。

Swirl 选项：

- Segment：旋涡在每个 segment 上 swirl
- AnchorGroup：以一个常量 F distance 在 Anchor Group 上 swirl
- AnchorGroupAbs：以一个常量 world unit distance 在 Anchor Group 上 swirl

Turns：swirl 应该应用的 360 度旋转数（Swirl only）。

曲线上可以附着很多数值，随着曲线进行插值，插值 time 在 segment 使用 F，在 spline 上使用 TF。最重要的一个插值数据就是旋转方向 Orientation，这样一个物体沿着曲线移动的时候还可以同时进行旋转。因为这个数值太常用，因此直接在 Segment 组件上提供了，其他想要跟着 spline 插值的数据需要手动添加 meta data 到 spline 上。

所有的插值数据只是提供给曲线使用者使用的，必须由使用者自己解释才有实际效果，例如 CurveSplineController，否则它们只是不同的数据而已。例如要使物体沿着曲线移动的时候，还同时旋转，就需要使用 F/TF 插值得到曲线上的位置，将物体平移到这个位置上，然后再计算这个位置的旋转 Quaternion，将它应用到物体上，如果不应用 Orientation，则物体只是移动到曲线上的位置，但是旋转保持不变。

Orientation 数值使用 Segment 的 CP 的 rotation 指定。默认 None 表示没有 orientation 数据，总是得到 Quaternion.identity。Static 表示使用 CP 的 rotation 作为插值锚定点。例如 Segment0 上 F=0 的 Orientation 等于 CP0 的 rotation，F=1 的 Orientation 等于 CP1 的 rotation。内部就是简单在两个 Quaternion 之间使用 F/TF 进行球面插值 SLerp。

插值数据记录在 cache 中。 Max Points Per Unit，

Spline 的 Orientation 定义每个 segment 如何得到它锚定的 rotation：

- None：没有旋转数据
- Static：每个 segment 使用第一个 CP 的 rotation 作为它的锚定数值，每个 segment 在第一个 CP 和最后一个 CP（下一个 Segment 的第一个 CP）的 rotation 之间进行插值。注意 Static Orientation 模式下，Orientation 不会出现螺旋 swirl，整个 spline 的 Orientation 从第一个 CP 旋转到最后一个 CP 的 Orientation，中间的 CP 只是调整这两个值之间的锚点，类似粒子系统中 Gradient Color 中的 Alpha Anchor，即中间 CP 的角度会被限制在 [0-180] 度之间，181 度 被 clamp 为另一个方向的 179 度。
- Dynamic：可以控制曲线进行任意的螺旋。可以在不同的曲线范围设置不同的螺旋数甚至方向。设置范围的单位是 AnchorGroup。AnchorGroup 由两个 Orientation Anchor CP 定义，就像两个 CP 定义一个 segment 一样。但是 AnchorGroup 可以跨越几个 segment。默认第一个 CP 和最后一个 CP 自动定义为 Orientation Anchor。一个常用的设置是让每个 segment 都作为单独的 AnchorGroup，即每个 CP 都被认为是 Orientation Anchor。为此提供了一个单独的 Swirl：Segment，这就不用为每个 CP 都手动定义 Anchor Group 了，直到遇到一个明确定义为 Orientation Anchor 的 CP。

Swirl 是用来定义 Anchor Group 的，它为所在 CP 定义是否是 Orientation Anchor。

Turn 定义当前这个 Anchor Group 从首个 CP 到末尾 CP 旋转多少个 360 度螺旋。每个 Anchor Group 都从首个 CP 的 rotation 开始插值，因此要在两个 AnchorGroup 上得到一致平滑的旋转，turn 需要定义为整数，否则到下一个 Anchro Group 时，就会出现 Orientation 跳跃。

插值的精度还跟采样有关。所有需要插值的数据应该被记录在采样点上，然后再采样点上进行线性插值。因此 Max Points Per Unit 要足够大。它在 SceneView 中的 Gizmos 显示为沿着曲线的 Up 方向的射线。Max Points Per Unit 越大，采样越密集，查看曲线的 Orientation 尤其方便。

最后 spline.GetOrientationFast 只是得到指定 TF 的 Orientation（Quaternion），需要脚本显式使用这个 Quaternion，例如将它应用到物体上。

