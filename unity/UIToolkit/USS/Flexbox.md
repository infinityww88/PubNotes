主轴 main，副轴 cross

方向 column（垂直），row（水平），column-reverse，row-reverse

对齐：

- 主轴对齐：justify content，对齐主轴一行的所有元素（wrap 导致的多行，每一行都单独依次对齐）
- 副轴对齐：Align
  - Align Items 单行内元素对齐（wrap 导致的多行，每一行都单独对齐
  - Align Content 多行在副轴的整体分布
  - Align Self：在 child 元素上覆盖 parent 指定的 Align Items

align-items：控制一行内的元素，在一行的副轴对齐，item 指一行内的元素 item，它与 justify-content 对应，justify-content 控制一行内的元素在主轴方向的对齐
align-content：控制多个行，在父元素的副轴对齐，content 指父元素的内容（多个行）
align-self：自身覆写 align-items，因为 align-content 控制的是 lines，不是 item

align-conent 应该改成 align-lines 更直观。

flex-basis：主轴 main-axis 上自动增长、收缩的基础值，与 flex-shrink、flex-grow 联合使用。设置它会覆盖 size 的 width，但不影响 height。

flex-wrap：主轴元素在超出父元素的 width 是否会折行
