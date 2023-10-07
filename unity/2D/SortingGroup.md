# 排序组 Sorting Group

Sorting Group 将具有精灵渲染器（Sprite Renderer）的游戏对象分组在一起，并控制这些渲染器渲染精灵的顺序。Unity 将同一排序组的精灵渲染器一起渲染，就好像它们是单个游戏对象一样。

## 设置排序组

要将游戏对象添加到排序组中，将 Sorting Group 添加到此游戏对象，Unity 会将同一 Sorting Group 应用与该组件附加的游戏对象的所有子游戏对象。

为了对排序组中的渲染器进行排序，Unity 使用排序组中的渲染器的各个排序设置。

## Sorting Group 属性

Unity 使用 Sorting Group 组件的 Sorting Layer 和 Order in Layer 值来确定排序组在渲染队列内相对于场景中其他排序组和游戏对象的优先级。

## 对排序组中的渲染器进行排序

Unity 按 Sorting Layer 和 Order in Layer 渲染器属性对同一排序组中的所有渲染器进行排序。在此排序过程中，Unity 不会考虑每个渲染器的 Distance to Camera 属性。实际上，Unity 会根据包含 Sorting Group 组件的根游戏对象的位置，为整个排序组（包含其所有子渲染器）设置 Distance to Camera 值。

Unity 相对于场景中其他渲染器和排序组对此排序组进行排序时，排序组的内部排序顺序保持不变。

![SG_diagram1](image/SG_diagram1.png)

Unity 将属于同一排序组的所有渲染器视为单个图层，并且基于未分组渲染器的 Sorting Layer 和 Order in Layer 属性设置对渲染器进行排序。

## 粒子系统

Editor 将一个作为排序组子项的粒子系统视为该排序组内的另一个渲染器，并基于 Sorting Layer 和 Order in Layer 属性设置这个粒子系统与其他渲染器一起进行内部排序。

Unity 对粒子系统与排序组内的其他渲染器一起排序时，会忽略粒子系统的 Sorting Fudge 值。

## 嵌套的排序组

嵌套的排序组是具有父排序组的一种排序组。Unity 首先对嵌套排序组中的渲染器进行排序，然后对其父级进行排序。Unity 确定嵌套排序组的内部排序顺序后，会将嵌套排序组与父排序组中的其他渲染器或嵌套排序组一起进行排序。

嵌套排序组可以具有递归的树形结构。嵌套排序组可以具有子嵌套排序组。Unity 首先对最里面的子排序组进行排序，然后对其各自父级排序。

![SG_diagram2](image/SG_diagram2.png)

## 使用排序组

创建 2D 多精灵角色的最常见方法是在 Hierarchy 窗口中一起排列多个精灵渲染器，并将它们设置为 children，从而形成一个角色。此时可以使用 Sorting Group 来管理这种复杂的多精灵角色。

