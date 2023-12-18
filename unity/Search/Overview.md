# Unity Search

Unity Search 功能可以在 Unity 内搜索各种资源并在结果上执行操作。例如，在 Search Window 中，可以查找 Asset 并打开它们，查找 Unity packages 并安装它们，以及查找 menu 命令并运行它们。

## Search Window

Ctrl + K 组合键或者 Editor > Search All 菜单可以打开 Search 窗口。

可以保存你常用的 search 表达式，并重用它们。

## Search Providers

每种类型的 search 都有它自己的 Search Provider。一个 Search Provider 允许你搜索并过滤它针对的内容。

- Regular Search Providers：当执行一个常规搜索，Search 使用所有常规 Search Providers，除非你排除它们
- Special Search Providers：你必须显示告诉 Search 执行一个特定 search。一次只能使用一个 Special Search Provider

你可以创建自己的 Search Providers。

每个 Search Provider 有一个单独的 search token。search token 是一个文本字符串，你可以在 search field 中使用以便只使用一个特定的 Search Provider 进行搜索。

## Indexes

有 3 种 index 类型：

- Asset：Project 中所有 Assets 的 index。这个 index 在你创建一个 Project 时自动创建，并在你添加或修改新内容时重建。这个 Asset index 包含所有 Assets，包括 Prefabs 和 Scenes，但是它不索引一个 scene 的内容以及一个 Prefab 的嵌套 hierarchy。
- Prefab：只包含作为 Prefabs 一部分的 GameObjects 的 index。
- Scene：任何 scene 中的 Assets 的 index

要使用 Prefab 或 Scene index，你必须在 Index Manager 中创建它们。

## Getting Help

可以以下面几种方式获得帮助：

- 当你第一次启动 Search window，result area 展示基本的快捷键
- 在 search field 输入 ? 对不同类型的 search 展示一个快捷引用
- 在 Search window 顶部点击问号图标打开 Search documentation

## 搜索设置

在 Unity Preferences window 设置 Search  preferences，或者：

- 在 search field 输入 ? 并在结果中选择 Open Search Preferences
- 在 Search window 左上角的 More Options(:) 选择 Preferences
- 点击 Search window 右下角的 gear icon

