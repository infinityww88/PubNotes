# ScrollView

在 UIBuilder 中向 ScrollView 拖放一个元素，元素将被直接添加到 container 子元素内，而不是放到 scrollerview 根元素下面。其他类似包装器元素应该类似。

UITK 和 UGUI 的 ScrollView 在手机上滚动时，都有抖动、视觉残留的问题，总之达不到 App 中那样的平滑的效果。这可能更它们的渲染方式有关。UITK 和 UGUI 的滚动效果一样，里面使用的应该是一样的算法。即使自己实现 Scroll View 也是一样的问题。

在 PC 上问题没有那么明显，但是在 Mobile 上很明显。

EnhancedScroller 并没有改进 ScrollView 的滚动算法，而是基于 ScrollerView 实现可回收的 ListView，并提供很多跳转、对齐相关的功能。

UITK 的 ScrollView == UGUI 的 ScrollView
UITK 的 ListView == EnhancedScroller

它们的效果应该是一样。

一个改善的方法是，不要应用太多文本，文本字体要宽要重（bold）。
