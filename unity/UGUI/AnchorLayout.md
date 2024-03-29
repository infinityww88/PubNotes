# Anchor Layout

理解一个UI元素如何定位，先确定它使用的坐标系。

Android，iOS，Windows等窗口系统只是简单的父子关系管理。兄弟控件共享相同的父窗口坐标系。坐标系的确定也十分简单，即左上角为原点，x轴向右为正，y轴向下为正。

uGUI中UI元素使用的坐标系的确定：基于父元素的RectTransform的Rect区域，anchor（相对比例，总是在0～1之间）在Parent Rect中划出一块子rect区域，称之为Anchor Rect。uGUI的每个UI元素具有一个Pivot，UI元素的定位、旋转、缩放都是基于这个Pivot。Pivot是按照相对比例在元素自身Rect定义的，但不限定在0～1之间。按照Pivot在Self Rect的比例在Anchor Rect确定一个点，这个点就是UI元素使用的坐标系的原点。X轴向右为正，Y轴向上为正。anchorPosition(3D)就是UI元素的Pivot点在这个坐标系中的位置（偏移）。

Anchor Rect和Self Rect四个角的偏移成为Offset Min/Max。这个Offset Min/Max是锚定系统的核心和目标。当父元素的Rect变化时，UI元素的Anchor Rect也会随着变化，因为它是给予Parent Rect计算的。但是Offset Min/Max保持不变，这样，Self Rect就会随之变化以维持Offset的不变性。这与Css中百分比定位是不同的，子元素随着父元素变化总是保持相对比例不变，但是uGUI中子元素保持的是Offset绝对向量的不变，相对比例肯定是变化的。因此，当Parent Rect小于Offset Min和Max之和，则Self Rect就会成为负的，导致UI元素不被渲染。

不同元素的参考坐标系几乎肯定是不同的，即使是兄弟节点（anchor可以不同，pivot可以不同）具有相同的anchorPosition，两个元素也不一定重合。因为anchorPosition是元素的Pivot在各自参考坐标系中的位置。

RectTransform的rect属性是基于Pivot局部坐标系定义的，即原点是pivot，而不是在参考坐标系中定义的。

两个兄弟元素，基于Parent Rect（在Parent Pivot局部坐标系定义的巨型），各自的Anchor，Pivot，就可以确定它们各自在Parent Rect中坐标系原点的位置，这样转化到同一个空间下，就可以相互参考定位Pivot的anchorPosition了。

Anchor Layout用于固定布局，Auto Layout用于不固定事先不预知的布局（动态添加元素）。

两个UI元素要想相互参考，必须转化到同一个坐标空间下，或者使用Parent坐标空间，或者使用RectTransform的Position（使用的是世界空间）。


Anchor Layout定义相对于Parent Rect的锚定和缩放，可以手动或程序控制position，之后锚定和缩放也随之更新。

自动布局是基于Anchor Layout基础上实现的。它只是一套计算机制，最终还是落实到Anchor Layout的参数实现定位。自动布局对Anchor参数的设置覆盖任何手动和程序的设置，相当于禁止了手动修改Anchor参数，在RectTransform的Inspector也会禁止修改。自动布局应该只看见高级的参数，例如spacing，padding，prefereed size等等。可以通过一个空白的RectTransform实现自动布局和手动布局混合的效果。类似于Css中的relative布局，即在自动布局基础上的手动偏移。

uGUI布局是基于RectTransform之上的一套计算机制，独立于Transform，但最终还是由Transform（Position，Rotate，Scale，Size实现）。

uGUI的UI元素就是普通的GameObject，具有Mesh和Material（Texture）。就像Sprite一样，具有在World中的大小。UI单位和世界单位之间存在一个映射比例，即ScaleFactor。UI单位乘以ScaleFactor就可以得到世界单位。因此可以通过操作RectTransform的position来移动定位UI元素，这是所有UI元素相同的参考空间。但是这种方法只能用于ScreenSpace（Overlay/Camera）模式的Canvas。

World模式Canvas，ScaleFactor参数是没有意义的，因为这个参数用来控制屏幕分辨率和world之间的映射。对于world模式Canvas来说，没有屏幕分辨率了，这个参数也就没有意义了，因为不需要随着屏幕空间调整Canvas大小了。此外，UI元素在World中是可以旋转的，因此UI屏幕可以3D空间的任何平面，而不仅是XY平面，这样就不能通过简单操作position来控制UI元素的位置了，只能通过anchor/auto layout来操作元素。

使用position定位通常是因为需要在两个ui元素之间做参考定位。ScreenSpace模式下，可以通过将Canvas坐标转化为世界空间坐标，然后在世界空间中定位就可以了。World模式下，由于Canvas坐标是在Canvas平面计算，而这个平面可以不和XY平面平行，因此转换很复杂。但是可以通过在要reference的ui元素（RectTransform）上添加一个空白的child元素，将child元素放置在想要的位置上，这样利用Anchor布局自动计算child的世界位置，然后将真正的UI元素的position直接set为child的position就可以了。使用空白元素参考定位是十分重要的技巧。这是css中relative position布局在uGUI中的实现方式。

Screen Space只是Canvas计算UI元素在世界空间中位置的方式，UI元素仍然是世界空间中的GameObject，可以像任何GameObject一样来操作它们。尽管它们显示为2D平面元素，仍然可以沿着3个Axis在3D空间中旋转。但是旋转时在layout之后进行的，围绕着pivot。正是因为UI元素本质上是GameObject，因此uGUI要比Flex布局更灵活，可以更容易地完成不可思议的效果。

UI elements可以保存为prefab，并作为任何RectTransform的child实例化，UI元素anchor就会相对于这个Parent RectTransform Rect进行定位。

RectTransform旋转总是围绕pivot，旋转总是在布局之后，即现在同一个屏幕上按照正常布局完成之后，RectTransform再围绕自己的pivot进行选择，类似于relative布局系统，即先正常layout，layout之后，在基于正常的位置进行偏移。

LayoutGroup的Padding和spacing可以调整留白（margin，可以为负值）和间距。

当有可用空间时，Child force expand控制子控件是否扩张占用可用空间。Control Child Size用来控制扩张的方式，当disable时，元素rect大小不变，只是扩展padding rect；当enable时，元素rect扩展为可用的空间大小。无论是padding扩张，还是rect扩展，都是按照layout elements的Flexible Width/Height用来控制兄弟RT之间的扩展比例的。

Anchor layout比普通的父子关系GUI甚至flex系统更灵活。Flex布局通过重新定义main axis和cross axis和正负方向完成灵活的布局。

Application.targetFrameRate控制渲染速率fps，渲染速率太低也会影响input的处理速度。

自动布局中，layout group给children分配空间时，是根据layout group元素的rect来分配的，但是child的min size是强制的，即无论如何都要分配这么大的空间，不可能更小。即使layout group的rect空间不够children的min size，则children仍然具有min size大小，这样children就会overflow了。如果layout group具有背景图片，就会很明显。perfered size是children理想的大小，当layout group空间大于min size，但是小于perfered size时，每个元素都会平均分配一些空间使得它们向着perfered size变化。当layout group空间超过perfered size时，才会按照flexible size分配额外空间。Control child size时，children最小也要保持min size变化。

Use Child Scale：layout group在计算child layout elements时，是否考虑child的scale。即使用scale之前还是之后的size进行layout计算。

Child Alignment：当有额外空间，而child layout element不扩展时，定义child如何在额外空间中对齐。

Grid Layout Group和其他Layout Group不同，它忽略包含元素的报告的minimum，prefered，flexible size属性，而是将它们统一视为一个固定size，即Cell Size（X & Y）。然后使用这个override的minimum，prefered，flexible size进行Layout计算。

min size强制分配，大于min size，小于等于prefered size时，超出min size的空间为每个元素平均分配，使得每个child元素都想着自己的prefered size grow，直到每个元素都达到自己的prefered size。超出prefered size的空间，按照flexible相对权重分配。

Image/Text这些native的元素的Layout Element size信息无法通过Layout Element组件覆盖。

Selectable组件用于实现normal，highlight，pressed，disable的现实功能，就像普通的按钮外观。例如给一个Image添加Selectable就可以使得Image像Button一样，再加上一个EventTrigger组件，配置PointerClick回调事件，就完全是一个Button了。

Selectable通过AnimatorController来配置UI动画，不仅仅是要使用Unity的动画系统，很多时候更是在使用CrossFade功能。这时，每个动画状态通常都没有多个frame，而是只有一个frame用来定义UI在这个状态下的状态。

```gpt
UGUI 中 gameobject 的 transform 的 x 和 y 的值表示的是什么?

在Unity的UGUI（用户界面图形用户界面）中，游戏对象（GameObject）的Transform组件的x和y值表示该对象在屏幕上的2D位置。这些值表示游戏对象在Canvas上的水平（x）和垂直（y）位置。

Canvas是UGUI中用于绘制2D用户界面元素的容器。游戏对象的Transform的x和y值是相对于Canvas的位置坐标。具体来说：

x值表示游戏对象相对于Canvas左边缘的水平偏移量。如果x为0，则表示游戏对象位于Canvas的左边缘上。
y值表示游戏对象相对于Canvas底边缘的垂直偏移量。如果y为0，则表示游戏对象位于Canvas的底边缘上。
这些值通常用于控制UGUI元素的位置，使其出现在所需的屏幕位置上。通过修改Transform的x和y值，您可以调整游戏对象在用户界面上的位置。这对于创建按钮、文本、图像等UI元素非常有用。
```

基于锚定的布局，改变 anchor，pivot，offsetMin/offsetMax，sizeDelta，以及 RectTransform parent 关系，所有布局数值立即改变，不需要等下一帧。因为它是基于 RectTransform 层级关系和固定的布局公式计算得到的。只有自动布局系统，改变元素大小，添加删除元素，才需要等待下一帧生效（布局位置），因为一帧中可能有很多布局元素的变化，它等到一帧的结束统一进行一次布局计算。

改变 RectTransform 的 parent 层级管线，元素在 Viewport 中的位置、旋转、大小都保持不变，只是各种 RectTransform 参数相应变化，来保持它的不变。

AnchorMin/AnchorMax 只能在 0-1 之间，它在父元素矩形中划出一块矩形空间，即 AnchorRect。PivotMin/PivotMax 可以超过 0-1，它在自身矩形中确定一个位置，作为定位、旋转、缩放的 pivot，然后再 AnchorRect 中按照相同的比例确定一个位置，它就是子元素参考的父坐标系的原点，然后x轴向右，y轴向上，子元素的 pivot 的在这个坐标系的位置就是 anchorPosition。因此即使同一个父元素的两个子元素的坐标系也是不一样的。

上面只是确定了自己的原点和父坐标系的原点，RectTransform 还有一个 rect 面积，它是用 offsetMin 和 offsetMax 用来确定的（它们都是可读写属性）。从 AnchorRect 左下角向右上偏移 offMin 就是 RectTransform 矩形的左下角，从 AnchorRect 右上角向左下偏移 offsetMax 就是 RectTransform 矩形的右上角。

sizeDelta = offsetMax - offMin.

sizeDelta 是 self Rect 与 AnchorRect 之间的 delta 大小（Vector2），大小的差分计算是基于元素的 pivot 的。因此 sizeDelta 和 offsetMin/offsetMax 实际是相互推算的关系。直到 sizeDelta 就能确定 RectTransform 的大小和位置，就能推算出相对于 AnchorRect 的 offsetMin/offsetMax，反之知道 offsetMin/offsetMax 也能确定 RectTransform 矩形的大小和位置，就能推算出 sizeDelta。

因为每个 RectTransform 的坐标系都是不同的，因此在不同元素之间的坐标系之间进行换算非常困难。换算的基础有一个共同的标准（共识）。uGUI 提供了 GetLocalCorners 和 GetWorldCorners 用来将元素矩形在 World 和 Local 进行转换，这样就可以通过 world 位置在不同元素的坐标系之间进行转换了。此外，GetWorldCorners 还可以用来确定 3D canvas 的元素在 world 的位置和大小，来和 world GameObject 进行交互。

The placement of their content is based on 7 RectTransform variables (anchoredPosition, anchorMax, anchorMin, offsetMax, offsetMin, pivot, sizeDelta), it’s actually only 5 variables.

rt.sizeDelta <==> rt.offsetMax - rt.offsetMin;

rt.offsetMin <==> -Vector2.Scale(rt.pivot, rt.sizeDelta) + rt.anchoredPosition;
rt.offsetMax <==> Vector2.Scale(Vector.one - rt.pivot, rt.sizeDelta) + rt.anchoredPosition

rt.anchoredPosition.x <==> Mathf.lerp(rt.offsetMin.x, rt.offsetMax.x, rt.pivot.x);
rt.anchoredPosition.y <==> Mathf.lerp(rt.offsetMin.y, rt.offsetMax.y, rt.pivot.y);

What about calculating the Transform‘s localPosition and world Position? It’s tricky because the localPosition and the RectTransform‘s rectangle is based off the pivot, anchors, and anchoredPosition. Not only that, but it also depends on the parent RectTransform and those issues also apply to the parent’s content and position – and the parent’s parent, and the parent’s parent’s parent, and… While there may be a simple formula, I can’t think of a generic one, and some non-trivial linear algebra and hierarchy traversal will probably be involved.

But, the RectTransform comes with helpful utility functions to get the local and world corners for you!
[RectTransform.GetLocalCorners][RectTransform.GetWorldCorners]

If you have pixel position in world coordinates, also don’t forget you can use the RectTransform’s parent-class’ Transform.InverseTransformPoint function to convert that world position to a local position, which will then should then be compatible with RectTransform.GetLocalCorners().

If you want the results of GetLocalCorners() but don’t care about ordered 3D points, but care about the final local size and position, RectTransform.rect is useful. I don’t find the position that useful, but I find myself getting the rect’s size very often for my procedurally generated GUIs.[example]

If you just need to do collision tests with pixels, the RectTransformUtility class has some helpful functions.


总是使用 Scale With Screen Size，它能指定一个参考 Screen 分辨率，然后在运行时根据实际设备对 Canvas 进行缩放，而设计 uGUI 时，只需要使用相对于参考分辨率的逻辑 UI 单位就可以了，与实际设备屏幕隔离，不用收到它的干扰，可以无所顾虑的使用任何 anchor 方法来定位、缩放元素，而无需担心在实际屏幕上变成乱糟糟的一团。UI Toolkit 也在 PanelSetting 中提供了相同的功能。




