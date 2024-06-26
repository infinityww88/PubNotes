Unity 的 2d 空间中，Screen 空间和 Viewport 空间都是左下角(0, 0)，右上角(1, 1)/(screenWidth, screenHeight)，UIToolkit 的 UI 空间则是左上角(0, 0), 右下角(1, 1)/(screenWidth, screenHeight)。

Editor Mode 中，Screen.width 和 Screen.height 不是游戏运行时的分辨率(GameView 设定的分辨率)，而是 GameView 的 Editor 中的实际分辨率。要在 editor 中使用 GameView 设定的分辨率，使用 Camera.pixelWidth/pixelHeight 或者 Camera.scalePixelWidth/scalePixelHeight.

Transform 的 3 组 transform 函数:

- 变换位置

  - Transform.TransformPoint
  - Transform.InverseTransformPoint

  考虑4x4矩阵链全部的偏移，旋转，和缩放

- 变换向量

  - Transform.TransformVector
  - Transform.InverseTransformVector

  不考虑矩阵链的偏移，只被旋转和缩放影响。无论是一致缩放还是非一致缩放，单位向量都会被 x, y, z 轴方向上的 scale 相应缩放，变换后不一定还是单位向量。

- 变换方向

  - Transform.TransformDirection
  - Transform.InverseTransformDirection

  不考虑矩阵链的偏移和缩放，只被旋转影响，单位向量变化后仍然是单位向量。

transform.localPosition(localRotation, localScale) 是 transform 在 parent transform 坐标空间的位置（旋转、缩放）。

DOTween.DOPunchPosition(localOffset, duration, vibrato, elasticity) 开始一个到指定位置的敲打动画。其中 localOffset 是针对 transform.localPosition 的，动画时会加到 localPosition 上，因此计算的 localOffset 要相对于 transform 的 parent 坐标空间进行变换，而不是相对于 transform 自身的坐标空间。

Unity 遵循左手坐标系，左手法则，和左乘。

左手坐标系：左手拇指指向 x，食指指向 y，中指指向 z（指向屏幕内部）。

左手法则：拇指伸展，其余四指握拳

- 求两个向量 a 和 b 的叉乘积（垂直两个向量平面的垂直向量），四指握拳沿着从 a 到 b 的方向，拇指方向指向所得结果向量的方向，向量模长是 a b 定义的平行四边形的面积
- 定义 Quaternion 的旋转角度正方向，拇指指向旋转轴 axis 的方向，四指握拳方向就是正角度方向。尤其是当想象沿着坐标系 x/y/z 轴旋转某个欧拉角的结果的时候，让拇指指向坐标轴的方向，四指握拳方向就是正角度方向

Inspector 中展示的 Position、Rotation、Scale 都是 local 的，即现在 parent 坐标系空间下的。

Unity Matrix4x4 Quaternion 都可以链式相乘定义一个变化。链式乘法遵循左乘法则。

```
矩阵的左乘指的是将一个矩阵乘以另一个矩阵时，将要被乘以的矩阵写在左边的操作。这是一种常见的矩阵运算方式，通常用于将一个矩阵作为变换矩阵应用到另一个矩阵上。

具体来说，在Unity中，左乘可以通过使用矩阵的乘法运算符“*”来实现。例如，如果您有两个矩阵A和B，并且您想要将A应用于B上，则可以使用以下代码：

Matrix4x4 result = A * B;

这将使用A作为变换矩阵，将其应用于B矩阵上，得到一个新的矩阵result，其中包含了B被A变换后的结果。

需要注意的是，在矩阵乘法中，左乘顺序非常重要。也就是说，A * B 和 B * A 得到的结果通常是不同的，因为矩阵乘法不满足交换律。
```
Matrix Quaternion 最终都是用来变换一个 point，一个 vector，或一个 direciton 的。Quaternion 变换也可以转换为一个 Matrix。Matrix.Rotate 就是使用一个 Quaternion 产生一个 Matrix。因此 Matrix 是最基本的表示单位，Quaternion 是上层用来简化旋转计算的单位。

```
vr = M0 x M1 x M2 x M3 * v
```

v 是最终变换的顶点。这个顶点可以是一个 object 的 pivot 位置，也可以是 mesh 的每个 vertex。左乘是将最新（最后）要应用的变换矩阵写在左边，因此越是左边的矩阵越晚应用，越接近 Global，越是右边的矩阵越早引用，越接近 Local。因此上面的矩阵链中，v 先应用 M3 变换（变换到 M3 定义的坐标系），变换的结果再应用 M2 变换（变换到 M2 定义的坐标系），结果再应用 M1 变换，最后应用 M0 变换。每个矩阵都定义一个坐标系空间。左边的坐标系影响右边的坐标系，右边的坐标系不影响左边的坐标系。左边的是 parent，右边的是 child。

Quaternion 可以使用一个 axis + angle 定义，亦可以使用 euler angles 定义。无论用那种方式定义，在内部旋转都是使用 Quaternion 来存储的。而最终进行变换的时候，Quaternion 又转换为 Matrix。Matrix 才是最终的存储单位。

Quaternion 也可以像 Matrix 一样链式相乘，结合与 Matrix 一样，因为 Quaternion 本质就是一个 Matrix。

Matrix4x4 可以使用 Matrix4x4.TRS 来生成，分别传入 translation(Vector3)，rotation(Quaternion)，scale(Vector3)。生成的矩阵等价于分别创建三个矩阵 T(ranslation), R(otation), S(cale)，然后按照 T * R * S 结合的结果。因此变化一个 point 时，先应用 scale，然后应用 rotation，最后应用 translation。要改变 T R S 的顺序，可以使用 Matrix4x4 Translate/Rotate/Scale 分别创建 T R S 矩阵，然后手动显式指定结合顺序。

类似的，使用 euler angle 指定旋转的时候，结合的顺序按照 z x y 的顺序，先沿着 z 轴旋转，然后沿着 x 轴旋转，最后沿着 y 轴旋转。记忆方法是：xyz 循环右移一位，变成 zxy，按这个顺序应用。使用欧拉角创建 Quaternion 的时候，Quaternion 的旋转顺序也是如此，等价于定义 3 个 Quaternion x y z（分别沿着 x y z 轴的旋转），然后以 zxy 的顺序乘在一起。要改变这个顺序，手动创建沿着 x y z 的 Quaternion，然后按照想要的顺序结合它们。

transform 中包含 eulerAngles 和 localEulerAngles 属性可以直接用欧拉角指定物体的旋转，但是内部会按照 zxy 的顺序生成相应的 Quaternion。

无论是 Matrix 还是 Quaternion，都是用来变换 Vector 的。Vector 可以是一个 point，一个 vector，或者一个 direction。

使用 transform 的 position，rotation，scale 设置变换时，等价于为 position rotation scale 分别指定相应的 matrix，最终按照 TRS 结合，这个结合顺序是固定的，无论按照何种顺序指定 position rotation scale。transform 的矩阵链从 world 到 local 的结果用来变换这个 transform 下的各种顶点，包括自己的 mesh 的 vertices 以及子物体。localToWorldMatrix 和 worldToLocalMatrix 分别用于在 local 坐标系和 world 坐标系之间变换，这两个矩阵都是只读的。

Matrix4x4 还包含创建 3d 计算中其他常用矩阵的方法：

- Frustum	This function returns a projection matrix with viewing frustum that has a near plane defined by the coordinates that were passed in.
- Inverse3DAffine	Computes the inverse of a 3D affine matrix.
- LookAt	Create a "look at" matrix.
- Ortho	Create an orthogonal projection matrix.
- Perspective	Create a perspective projection matrix.
- Rotate	Creates a rotation matrix.
- Scale	Creates a scaling matrix.
- Translate	Creates a translation matrix.
- TRS

Transform 的 position，rotation，scale 分别具有 world 版本和 local 版本，rotation 还包含 eulerAngles 版本。

但是 scale 的 world 版本叫 lossyScale，而不是 scale，而且是只读的。

当想要创建一个分别沿着两个坐标轴（假设 x y）万向旋转的效果，例如智能导弹发射平台或大炮沿着两个轴旋转，皆可以为两个轴的旋转分别创建一个 GameObject 作为 parents，每个 GameObject 控制一个坐标轴的旋转，也可以只使用一个 GameObject，然后为两个轴的旋转分别创建 Quaternion，然后左乘在一起，作为 GameObject 的 localRotation。这相当于创建了两个虚拟的 GameObject。

## Unity 版本

尽量使用 LTS 版本，不要追求最新版本甚至 beta alpha 版本。不仅仅因为最新版本本身可能存在的问题，还因为很多必须的依赖插件不一定跟着 Unity 最新版本更新。

## CodeLess

努力追求 code less 开发，对游戏开发来说，快速迭代就是一切。使用第三方工具或自己开发插件尽量实现 code less 开发。即使只能通过 code 实现，也要使用 HotReload 或脚本来提升迭代速度。

![IterationIsEverything](IterationIsEverything.jpg)

## UnityWebRequest

拼接路径使用 Uri，而不是 Path.Join，后者使用的平台文件路径分隔符，在 Windows Unity Editor 中分隔符是反斜线，这在 URL 中无效的。

对 request.downloadHandler 使用一个 new DownloadHandlerFile(filePath) 可以将文件自动保存在指定路径，而不必手动写入。

## 静态类与单例模式

其他语言中，使用静态类，静态方法和单例模式没有太大区别。但是在 Unity 中，尽量使用 MonoBehaviour 的单例模式，而不是静态类/属性/方法。因为很多 Code Less 依赖 MonoBehaviour 的序列化和 Inspector。一旦使用静态类就没有办法使用大量 Unity 工具了，静态类没办法引用各种 asset，并且不能利用 Inspector。

## SkinnedMeshRenderer SkinWeight

SkinnedMesh 的 SkinWeight 控制动画随骨骼变形的平滑度。它表示在变形时每个 vertex 最多被多少个 bones 控制。每个模型可以在 import setting 中 Rig > Skin Weights 设置。此外 QualitySettings.skinWeights 还控制整个项目范围内 meshes 的 SkinWeight。

SkinWeight 可以是 OneBone，TwoBone，FourBone，或者 unlimited。通常标准是 4 个骨骼。Bones 越多变形越平滑，但是也需要更多的性能开销，尤其是超过 4 bones。

这个设置不会改变底层 mesh data。它只影响 Unity 使用的 bones 的数量。例如 Mesh 中一个 vertex 包含在 4 个 Vertex Group（每个 bone 一个 Vertex Group）并具有不同的 weight。但是 Unity 可以按照设置只使用两个 bone 来编写。即根据设置一个 mesh 可以有未使用的 weight data。

QualitySettings.skinWeights 可以在运行时修改，并立即生效。可以使用 SkinnedMeshRenderer.quality 为一个特定的 SkinnedMeshRenderer 单独设置 SkinWeight。

在 import setting 中 ModelImporter.maxBonesPerVertex 可以在 Imported 时直接丢弃未使用的 weight 数据。

但是当前 Unity 版本中，Android Build 似乎忽略了 QualitySettings.skinWeights 设置，构建后的应用中 SkinWeight 默认是 TwoBone，即使 QualitySettings.skinWeights 设置为 FourBone。要使用 FourBone，需要在脚本中显式设置 QualitySettings.skinWeights = FourBone

下面显示不同 SkinWeight 设置对应的不同效果：

OneBone

![OneBone](OneBone.jpg)

TwoBone

![TwoBone](TwoBone.jpg)

FourBone

![FourBone](FourBone.jpg)

