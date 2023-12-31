# ScrollView

在 UIBuilder 中向 ScrollView 拖放一个元素，元素将被直接添加到 container 子元素内，而不是放到 scrollerview 根元素下面。其他类似包装器元素应该类似。

UITK 和 UGUI 的 ScrollView 在手机上滚动时，都有抖动、视觉残留的问题，总之达不到 App 中那样的平滑的效果。这可能更它们的渲染方式有关。UITK 和 UGUI 的滚动效果一样，里面使用的应该是一样的算法。即使自己实现 Scroll View 也是一样的问题。

在 PC 上问题没有那么明显，但是在 Mobile 上很明显。

EnhancedScroller 并没有改进 ScrollView 的滚动算法，而是基于 ScrollerView 实现可回收的 ListView，并提供很多跳转、对齐相关的功能。

UITK 的 ScrollView == UGUI 的 ScrollView
UITK 的 ListView == EnhancedScroller

它们的效果应该是一样。

一个改善的方法是，不要应用太多文本，文本字体要宽要重（bold），另外增大阻尼系数，decelerationRate，可以减轻抖动效果，能达到可接受的效果。

ScrollView 和 ListView 都是固定大小的，即在固定 size 区域内显示更多的内容。

ScrollView 滚动的元素时 unity-content-container，这也是拖放内容元素到 ScrollView 上时，元素添加到的 parent 元素。unity-content-container 默认是 shrink = 0, grow = 0，因此它默认适应子元素大小。当前 ScrollView 实现中，如果内容子元素的 size 小于 ScrollView 时，也会被滚动，只是保证 content-top > scrollview-top && content-bottom < scrollview-bottom。而 UGUI 的 scrollview 在这种情况下则不会滚动内容区域，即 content-top 总是对齐到 scrollview-top。要使 UITK 的 scrollview 不滚动小于 scrollview size 的内容元素，可以设置 unity-content-container 的 min-height = 100%，即让滚动区域最小也是 scrollview 大小，这样当 content 元素更小时，也不会滚动了，因为 unity-content-container 填满了 scrollview 区域。如果 content 元素大于 scrollview 大小，则正常滚动。

因为 ScrollView 滚动的是 unity-content-container，只有按住并拖放它才会滚动。默认情况下，如果内容元素小于 ScrollView 并且 ScrollView 设置为 elastic 的，内容仍然可以被拖拽，只是放开之后立即回复原位，但是必须按住 unity-content-container 元素。因此拖拽空白区域是没有作用的。如果设置了 unity-content-container 的 min-height = 100%，则可以按住空白区域拖拽内容元素了。

UITK 的 ScrollView & ListView 的效果和 UGUI ScrollView & EnhancedScroller 效果一样。UGUI 能达到什么效果，UITK 就能达到什么效果。

用 DOTween 动画文本也是一样的效果，应该是与动画逻辑无关，而是跟渲染方式有关。

用 Godot 旋转 sprite 也同样有相同的视觉残影效果，这应该是使用游戏引擎渲染动画的通用视觉效果，与一般 GUI 脏区重绘不同。
