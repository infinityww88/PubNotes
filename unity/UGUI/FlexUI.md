# Unity Flex UI

[Unity Flex UI](https://github.com/gilzoide/unity-flex-ui) 使用 C++ native lib 的 Yoga layout engine 对 Unity UI 支持 Flexbox。

它支持 Windows, Linux, macOS, iOS, tvOS, Android, WebGL, visionOS。

它只使用一个组件：FlexLayout。无论是 Flex Container 还是 Flex Item 都使用这一个组件。

FlexLayout 暴露所有 flexbox layout 属性。

FlexLayout 只布局带有 FlexLayout 组件的 children RectTransform。因此在它上面仍然可以使用 anchors 和其他 Layout Elements。

每个 Root FlexLayout 是一个单独的布局 Context，它内部独立地进行 Layout。

每个 FlexLayout Object 可以设置一个 layout engine 配置，FlexLayoutConfig assets。

Flex UI 支持 edit mode 的 Live Updates。

用法：

1. 添加 FlexLayout 组件到 UI RectTransform 上，它会布局它的 descendants（children/grandchildren）。
2. 为 descentants 元素添加 FlexLayout 组件，它们将会被 Root FlexLayout 布局。
3. 配置必要的 layout properties，并且在 edit mode live 查看 changes
4. Enjoy

所有属性可以被 Inspector 设置，也可以被 code 设置，并且布局会自动刷新，但是在 code 中，layout 每帧只会被计算一次。

要查看 FlexLayout 支持的属性，可以查看 [yoga 的文档](https://yogalayout.dev/docs)。

注意所有 FlexLayout UI 元素的 position 和 size 都被 layout engine 控制。RectTransform 的 position、size 属性都变成 driven 的（不能在 Inspector 中编辑），除了 Root FlexLayout，它的 position、size 被显式设置，因为它为一个独立的 layout context 设置 viewport。尤其是即使 FlexLayout.PositionType = Absolute，元素的位置也不能用 RectTransform 的 position 设置，而是应该用 Position Left/Right/Right/Bottom 控制（即使元素的位置在 SceneView 中用 Gizmos Handle 改变，在 FlexLayout 更新时就会被重置）。

当需要 Unity 的工具时，先在 Github 查看是否有可用的仓库。

在 Unity 中安装 github package 有 3 种方法：

1. 使用命令行 openupm-cli：openupm add com.gilzoide.flex-ui
2. 在 Unity Package Manager 中用 git url 安装：https://github.com/gilzoide/unity-flex-ui.git#1.1.1
3. 从 github 将仓库下载到本地，然后在 Unity Package Manager 选择 Add package from disk，然后选择本地仓库中的 package.json
