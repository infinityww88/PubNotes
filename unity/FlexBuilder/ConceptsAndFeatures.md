# Concepts and Features

## Guide：FlexContainers vs FlexItems

所有 Flexbox layouts 都是使用 FlexContainers 和 FlexItems 创建的。FlexItems 用于描述 layout 中的单个 element，FlexContainers 用于控制 FlexItems 如何 positioned/sized。

为一个 RectTransform GameObject 添加 FlexContainer 脚本将它作为 FlexContainer（相当于 css 的 display: flex）。添加 FlexItem 脚本将它作为 FlexItem 

### One or both

在典型 layout 中，tree 中最高层的 item 是一个 FlexContainer，最底层的 item 是一个 FlexItem，它们中间的任何东西都既是一个 FlexItem（因为它嵌套在一个 parent FlexContainer 中），也是一个 FlexContainer（因为它包含其他 FlexItems）。因此，Flexbox layout 中绝大多数 GameObjects 同时挂载两个组件。

但是一个常见的情景是，有一些 UI 是在运行时生成的，或者通过脚本生成的。此时，典型地会有一个 FlexContainer 在 tree 底部，并且没有 FlexItems（它是挂载点，你可以在此实例化 UI prefabs，然后通过添加一个 FlexItem 或一个 FlexContainer subtree 到它下面）。

另一个常见的情景是：将一些纯粹的 UnityUI 嵌套在 Flexbox layout 中，使用 Flexbox 设置整体 size，然后使用 Unity RectTransform 控制 local UnityUI code。当想要将其他只理解 UnityUI 的 assets 集成时，这非常有用。此时添加一个空 FlexItem 参与 Flexbox 布局，获得 Flexbox 计算的 RectTransform 空间，然后再此基础上应用普通的 anchor layout，children element 上既没有 FlexItem 也没有 FlexContainer。
