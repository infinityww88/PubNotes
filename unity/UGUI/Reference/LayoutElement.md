# LayoutElement

- Ignore Layout：layout system忽略这个layout element，其从layout系统中移除。类似于css定位中的绝对定位，从正常的布局流中移除。
- Min Width/Height：layout element最小具有的size。Layout Controller一定会分配（计算）这么大的size。
- Prefered/ Width/Height：每个元素在Min Size基础上平均分配空间，向着各自Prefered Size发展，直到每个元素都得到各自的Prefered Size。
- Flexible Width/Height：Min/Prefered size都使用绝对单位，Flexible使用相对单位，指定分配额外空间时这个layout element的权重。绝大多数情况下，flexible width/height只设置为0或1.
- Layout Priority：如果一个GameObject具有多个组件提供layout size信息，layout系统使用具有最高priority的组件的信息。如果所有组件的layout priority相同，则对每个属性使用最大值，无论其来自哪个组件。


