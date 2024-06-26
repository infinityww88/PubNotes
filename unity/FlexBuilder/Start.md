# Start Guide

FlexBuilder 使用带有两种 MonoBehaviour 的 GameObjects：FlexContainer 和 FlexItem。

如果在 Editor 中选择一个带有 FlexContainer/FlexItem 的 GameObject，它会在 Inspector 中有一个（FlexItem）或两个（FlexContainer+FlexItem）sections：

- container 需要配置它们的 contents/children（使用 FlexContainer settings），和它自己（使用 FlexItem settings）。
- Plain UI elements 只需要设置它自己（FlexItem）

FlexContainer 的上半部分 inspector 有一个 FlexTemplates 的可折叠区域，它是一个快速构建 UI 的方法，并且可以扩展。

FlexItem 上半部分 inspector 有一个对 padding/margins/size/shape 的 visual BoxModel previewer。

FlexItem settings 用来控制单独 item。FlexContainer settings 用来控制 layout。

每创建一个 layout 有 4 个步骤：

1. 选择一个 RootFlexContainer 以存储 layout 和控制 shared settings
2. 添加一个初始 FlexContainer 开始配置 layout
3. 添加各种 child FlexContainer 和 FlexItems 创建有趣的 layout
4. 对每个 FlexItem，添加一个 UnityUI element（button，image，text，等等）

可以使用 FlexTemplates（FlexContainer inspector 中的 built-in buttons）的来快捷操作 2-4 步。

FlexContainer 控制 child layout，FlexItem 控制自己的 size/shape/position。UI 元素的表现则仍然是被 UI Component 自己控制（Button，Image，Text 等等）。

直接将 UI Components 挂载到 FlexItem GameObject 是支持的。但是它是一个高级设置，并且对大而复杂的 layouts 会导致问题。因此，只要有可能，建议将 UI Component 作为 direct child 添加到 FlexItem 下面。

每个 FlexItem 应该只有一个 UI 元素。添加多个 UI 元素到 FlexItem 是可能的，但还是高级设置并可能导致问题。

## Flexbox made easy In Unity3D

Flexbox 非常严格遵循 CSS 规范。

在 CSS 中，通常将所有东西都视为 DIV。在 FlexBuilder 中，DIV 的等价物是挂载 FlexItem 和 FlexContaienr 的 GameObject。

当前 FlexBuilder 不支持从 parent objects 继承 values。这个功能在 game/application layouts 中很少用到，并且通常和 Flexbox style layout 不相关。CSS 中继承的属性通常是显示相关的属性，例如颜色，字体等。而布局相关的属性例如 widget/height 继承是没有意义的。

FlexBuilder 支持所有核心 Flexbox 参数（FlexBuilder 只实现了 CSS 的 Flexbox layout，而不是所有的 CSS 属性，UIToolkit 则基本是要实现其他 CSS 样式）。它还支持 Flexbox 依赖的核心 CSS3 参数。可以在 FlexBuilder inspector 中，FlexContainer 和 FlexItem 组件下面，找到每个参数。

| Flexbox 参数 | FlexBuilder 设置 |
| --- | --- |
| direction | FlexContainer |
| grow | FlexContainer |
| shrink | FlexContainer |
| justify | FlexContainer |
| align | FlexContainer |
| padding | FlexItem |
| margins | FlexItem |
| width | FlexItem |
| height | FlexItem |
| min/max width or height | FlexItem |
| | |

## Create Layout with FlexBuilder

1. 选择或创建一个 RootFlexContainer 来保存 layout 信息和控制 shared setting
2. 添加一个初始 FlexContainer 来开始配置 layout
3. 创建和添加嵌套 FlexContainers 和 FlexItems 或者 FlexTemplates，来创建有趣的布局

### RootFlexContainers

首先必须有一个 Root Flex Container。将它放在 Unity Canvas 下面，本质就是一个 RectTransform，可以放在任何 UI 元素上。

RootFlexContainer 有几个作用：

- 在 Unity global layout system（RectTransform/uGUI）和 CSS-Flexbox（FlexBuilder）之间提供一个 gateway
- 控制 Flexbox 的 virtual viewport 的 size（作为 flexbox layout 的容器）
- 提供 global-settings，应用到 Flexbox 的整个 sub-layout

通常会配置 RootFlexContainer 的 RectTransform 扩展填充满整个 Canvas，并将它作为 main object 放置在 Canvas。

当想要有一个或多个 popup windows/modal dialogs，就添加额外的 RFC 到 Canvas 上，在其中创建 dialog 的布局。

每个 RootFlexContainer 是一个 100% 独立的 layout sub-system。它们彼此之间完全独立，layout 只会在它们内部进行。

### FlexContainers

在 RFC（RootFlexContainer）内部，创建一个或多个 FlexContainers。每个 FlexContainer 给定一个 size，然后它设置所有的 child objects 的 size 和 position。它控制 layout-direction，在 left edge 或 right edge 对齐 objects 等等。

FlexContainers 自身不能有 UI elements（Buttons，Labels 等等），但是可以包含他们作为 children。

通常 RFC 自身也是一个 Flex Container，但是它会有一些 overrides 和额外的特殊行为。

### FlexItems

每个 FlexContainer 内部有一个或多个 child FlexItems。它们是独立 UI 元素的 wrappers。

通常会用一个 GameObject 对应一个 UI element，而每个 GameObject 有一个 FlexItem 控制那个 UI element 的 size。

### UI Elements

FlexContainer 和 FlexItem 只负责控制 UI 元素的 layout、size，具体表现还是用 UI Component 自己设置。UI Component 是标准的 UnityUI elements，就像它们往常一样工作，除了它们的 size 和 position 将被 Flexbox/FlexBuilder 控制。

注意：可以联合使用 FlexBuilder 和 RectTransform/uGUI。FlexBuilder 就是 uGUI LayoutController，只是内部使用 Flexbox layout。

有两种方式连接 FlexItem 和 UI Element。

- Direct attachment

  在 Unity 中先创建一个 UI Element，然后挂载一个 FlexItem Component 到那个 GameObject。通常这足够了。这个 Element 将会被 Flexbox 100% 控制 size（Flexbox 完全覆盖 RectTransform）。

- Childing/Parenting

  创建一个 empty GameObject，挂载一个 FlexItem 到它上面。然后将 UI Element 作为 child 添加到它下面。

  这是最强大的方式，并且提供了更精细的控制。通常配置 UI Elements RectTransform expand to fill parent object（FlexItem）。此时 FlexBox 本身的 size 和 position 被 FlexContainer 完全控制，但是 UI 元素作为 child 添加到 FlexItem 下面，它可以基于 FlexItem 的 size 进行 anchor layout，就像普通的 anchor layout 一样。

  这种方法通常用于创建复合 UI，在一个 FlexItem 下挂载多个 UI Elements。基本就是 FlexItem 先获得一个 Flexbox 空间，然后 Anchor Layout 基于这个空间工作。

## Faster workflow

FlexBuilder 已经对性能进行深度优化。通常，如果观察到一个 slow layout updating，它会是 layout 算法的一个 bug。但是可以采用一些手段让 layout 更快。

### Scripts: batch-process changes

每次改变任何 Flex settings，无论是 FlexItem 或 Container，FlexBuilder 会 relayout 整个 layout。这对确保 layout 总是正确的是必要的。但是有时一帧中会有多个 update，你会希望在最后一个 change 之后一起统一 relayout：

```c#
public void MyMethod()
{
    using( new ExperimentalDelayUpdates2() ) // FlexBuilder will wait until the end of this block to re-layout
    {
        // make lots of changes here
        // e.g.:
        foreach( var item in myFlexContainer.FlexItems )
        {
            item.flexGrow = 1;
            item.flexShrink = 1;
            item.flexBasis = 0;
        }
    } // FlexBuilder will now automatically re-layout
}
```

### Layout complexity

CSS Flexbox 非常适合 auto-sizing 几乎所有事情，让你免于手动指定 size 的 time/effort。但这是要消耗 CPU 的 —— 这非常小，并且只会在有 layout 改变时发生，然而在非常复杂的 layout 中，这可能变得显著（超过几个毫秒）。

下面是一些降低 layout 复杂度的方法：

- 选择一些 FlexContainer 作为 layout 的关键部分，它们不会 resize，显式设置它们的 size
- 移动一部分 UI 到单独的 RootFlexContainers。每个 RFC 单独执行它自己的 layout，并且不会和其他 RFC 交互。注意这只在非常极端的情况下是必须的，非常大、非常复杂的 UI！
- 将任何 popups 移动到单独的 RootFlexContainers：这使它们在 code 和 UnityEditor 中更容易管理，并且还能获得额外的性能优势。

注意，百分比指定的 size 比其他方式要略微慢一些，除非它们的 parent object 有一个显式的 size（例如 width = 50 px），因为这需要大量计算来确定最终大小（必须递归 layout tree 并计算所有中间的 items）。
