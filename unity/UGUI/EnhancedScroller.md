# Enhanced Scroller

EnhancedScroller 是 UGUI ScrollRect 的扩展，提供：

- 回收 gameobjects，避免 GC
- 无限循环
- 调到指定的 index
- 动态数据驱动，不需要事先准备数据
- Object 数量随着 scroller 的 size 动态增长，必要时自动添加 elements
- 对齐到 scroller view area 中的任意一个位置，以及居中 cell 内的某个位置

EnhancedScroller 需要一个 delegate controller 来告诉它关于 data 和 views 的信息，特别是 controller 中需要 3 个主要 handlers：

EnhancedScroller 使用 MVC 模式。你不需要操作 scroller，只需要操作 controller。

- GetNumberOfCells：告诉 scroller 你需要多少个 cells。Scroller 基于这个 count 计算正确的 bounds 并处理定位
- GetCellViewSize：告诉 scroller 每个 cell 的 size。可以每个 cell 有不同的 size，也可以所有 cells size 相同
- GetCellView：向 scroller 一个 prefab，用于创建 cell。cell 会被回收重用

其他的 handlers：

- cellViewVisibilityChanged：某个 cell 变得可见或不可见
- scrollerScrolled：ScrollRect 改变其 scroll position
- scrollerSnapped：scroller 对齐到你指定的位置
- scrollerScrollingChanged：scroller 开始和停止滚动
- scrollerTweeningChanged：scroller 开始和停止 tweening 动画

## Usage

EnhancedScrolle.ReloadData 加载数据。

当 scroller 请求 controller GetCellView 时，向它传递一个 prefab。可以在 scroller 中使用多个 prefabs。例如，可以将数据分组为 headers，rows 和 footers，这需要 3 个 prefabs。甚至可以为每个 cell 使用不同的 prefab。绝大多数情况下，scroller 只需要一个 prefab。

一旦拥有了一个 scroller 创建的 cell，就可以对它做任何事。通常是当设置 cell 的 view 状态时，基于 data 更新 UI elements。

## Settings

- scrollDirection：设置水平或垂直滚动
- spacing：在 cell view 之间添加 spacing
- padding：从 scroller 的边缘偏移 cell views
- Loop：创建一个无限循环
- ScrollbarVisibility： scrollbar 如何显示。如果没有指定 scrollbar，这个设置被忽略
- onlyIfNeeded：只在需要时显示 scrollbar，除非开启 loop
- Always：总是显示 scrollbar
- Never：从不显示 scrollbar

## Special features

### Looping

TODO

### Snapping

TODO

### Jumping

TODO

## Other properties and methods

- ScrollPositon：当前滚动位置
- Velocity：2D 滚动速度
- LinearVelocity：1D 滚动速度
- IsScrolling：velocity > 0
- IsTweening：如果 scroller 在两个 two positions之间 tweening，返回 true
- StartCellViewIndex：第一个可见的 cell view index
- EndCellViewIndex
- NumberOfCells
- ScrollRect：管理的 ScrollRect component
- ToggleLoop：切换 loop
- GetScrollPositionForCellViewIndex：指定 cell view index 的 scroll poisition
- GetScrollPositionForDataIndex：指定 data index 的 scroll position
- GetCellViewIndexAtPosition：返回指定 scroll position 的 cell view index

  dataIndex = cellViewIndex % numberOfCells

- RefreshActiveCellViews：对 scroller中每个可见的 active cell 调用 RefreshCellView。需要在 cell view 中  override RefreshCellView方法来实际更新 cell UI
