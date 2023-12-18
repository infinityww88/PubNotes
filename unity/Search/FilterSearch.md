# Filtering Searches

Filtering 缩小 search 的 scope 到特定 providers。你可以以以下方式 filter searches：

- 设置永久 search filters 来控制使用哪些 regular searches
- 在 search field 使用一个 regular 或 special Search Provider 的 search token 来只展示那个 provider 的结果
- 使用 sub-filters 限制搜索结果，并使用 index 的可用 keywords

## Persistent search filters

可以在 Filter pane 中临时 toggle Search Providers。这可以减少 search 返回的 items 的数量。如果你知道你查找的 item 的类型，这可以更便利。

要在当前 Search Session 永久 toggle Search Providers：

- 打开 Search window，选择 More Option(:)
- Mute 或 unmute 任何你想要 include/exclude 的 Search Providers

要为所有 Search Session 永久 toggle Search Providers，在 Search  Preferences 中设置。

## Search tokens

每个 Search Provider 有一个唯一的 text 字符串，称为 search token。当对 search query 使用 search token 前缀，Search 限制搜索的结果到那个 provider。

例如 p: 是 Asset Search Provider 的 search token。当输入 p:Player 时，Search 在 Assets 中搜索匹配 Player 的 Assets（例如，名字中包含 Player 的 assets）。

## 组合 search tokens

可以组合 search tokens 来创建更复杂的 queries。

- queries 写成一行，每个 search token 之间有一个字符的空白
- 每个新 token 之间的 space 是一个 Add 操作，两个 filters 必须都返回 true，结果才会返回。添加其他运算符（or，>，<）来返回不同的结果
- 如果使用 Search Provider filter token，它必须是 query 的第一个分量

| Query | Description |
| --- | --- |
| h: t:meshrenderer p(castshadows)!="Off" | 搜索一个 Scene 中所有投射阴影的 static meshes |
| h: t:light p(color)=#FFFFFF p(intensity)>7.4 | 搜索一个 Scene 中所有具有指定颜色且亮度大于 7.4 的光源 |
| o: t:healthui ref:healthcanvas | 使用 Object Provider 来搜索所有 indexed Prefabs 和 Scenes，查找具有 HealthUI 组件且其引用 healthcanvas Prefab 的 GameObjects |
| h: path:/Collectables t:collectable | 查找位于路径 /Collectables 下带有 Collectable 组件的所有 Objects |
| | |

