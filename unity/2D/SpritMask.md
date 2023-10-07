# Sprite Mask 精灵遮罩

精灵遮罩用于隐藏或显示精灵或精灵组的各个部分。精灵遮罩仅影响使用精灵渲染器（sprite renderer）组件的对象。

类似 UGUI 的 image mask 组件。

## 属性

- Sprite：用作 mask 的 sprite
- Alpha Cutoff：如果 Alpha 包含透明区域和不透明区域之间的混合，则可以手动确定显示区域的分界点。通过调整 Alpha Cutoff 滑动条改变 cutoff 的 alpha 阈值
- Range Start：mask 所在的图层位置，即 mask 开始生效（遮罩）所在的图层位置
  - Sorting Layer：mask 所在的排序图层
  - Order in Layer：mask 在排序图层中顺序
- Range End
  - Mask All：默认情况下，此 mask 将影响其后（更低排序顺序）的所有排序图层
  - Custom：Range End 可以设置为自定义 Sorting Layer 和 Order in Layer

## 使用精灵遮罩

精灵遮罩不需要和精灵渲染器在一个 GameObject 上。精灵遮罩可以单独使用，它本身在场景中不可见，只有与精灵产生交互时才可见。可以选择 Scene 菜单中的 Sprite Mask 选项显示场景中的 Sprite Mask。

精灵遮罩始终游戏。受精灵遮罩影响的精灵需要再 Sprite Renderer 中设置 Mask Interaction。

默认情况下，精灵遮罩会影响场景中将 Mask Interaction 设置为 Visible 或 Not Visible Under Mask 的所有精灵。我们通常希望遮罩仅影响特定精灵或一组精灵。

确保遮罩与特定精灵交互的一种方法是使用排序组（Sorting Group）组件。

控制遮罩效果的另一种方法是使用精灵遮罩的自定义范围（Custom Range）设置。

Range Start 和 Range End 可以基于精灵的 Sorting Layer 或 Order in Layer 来选择性遮蔽精灵。

