主轴 main，副轴 cross

方向 column（垂直），row（水平），column-reverse，row-reverse

对齐：

- 主轴对齐：justify content，对齐主轴一行的所有元素（wrap 导致的多行，每一行都单独依次对齐）
- 副轴对齐：Align
  - Align Items 单行内元素对齐（wrap 导致的多行，每一行都单独对齐
  - Align Content 多行在副轴的整体分布
  - Align Self：在 child 元素上覆盖 parent 指定的 Align Items

flex-basis：主轴 main-axis 上自动增长、收缩的基础值，与 flex-shrink、flex-grow 联合使用。设置它会覆盖 size 的 width，但不影响 height。

flex-wrap：主轴元素在超出父元素的 width 是否会折行
