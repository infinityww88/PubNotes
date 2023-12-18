# Using Search

使用 Search 的过程：

- 启动 Search
- 进行 Search
- 在结果上执行 actions

## Launch Search

Ctrl + K 快捷键，或 Edit > Search All。

## Searching

要执行常规搜索，在 search field 中输入 query。

对于绝大多数查询，使用 Search All 窗口和 project 默认创建的 Asset index 可以高效地查找你的内容。

### 常规搜索

一个 regular search 使用所有 Search Providers 除非你显式排除它们

- 要执行一个使用全部 active Search Provider 的常规搜索，只需要在 search field 中输入 query
- 要只展示一个特定 Search Provider 的结果，在 search terms 前面加上 Search Provider 的 search token
  
  一个 search token 是一个字符串，在 search field 中指示只使用特定 Search Provider 进行搜索。

  按下 Tab 键展示常规 search provider 前缀。

常规 Serach Providers 和它们的 search tokens：

| Provider | Function | Search token | Example |
| --- | --- | --- | --- |
| Project | 搜索 Project Assets | p: (for "project") | p:Player |
| Hierarch | 搜索 Scene 中的 GameObjects | h: (for "hierarchy") | h:Main Camera |
| Settings | 搜索 Project Settings 和 Preferences | set: | set:VFX |
| Menus | 搜索 Unity main menu | m: | m:TextMesh Pro |
| | | | |

### 特殊搜索

特殊搜索只在你显式指定时才会执行：

- 要执行特殊搜索，在 search terms 前面加上 Provider 的 search token。

  在 More Options(:) 菜单中选择一个特定的 search provider。

Special Search Provider 的 Tokens：

| Provider | Function | Search Token | Example |
| --- | --- | --- | --- |
| Help | 搜索 Quick Search Help | ? | ?aset 搜索 Help 页面中包含 asset 的条目 |
| Calcualtor | 计算数学表达式 | = | =2\*3+29/2 计算表达式的结果 |
| Files | 搜索文件 | find: | find:Paint Mat 搜索所有包含单词 paint 以及单词 mat 的 asset paths |
| Static API | 查找并执行 static API 方法 | # | # mesh 搜索包含 Mesh 的静态 API |
| Packages | 搜索 Unity package 数据库 | pkg: | pkg:vector 搜索 Unity package database 中包含 vector 的 package |
| Asset Store | 搜索 Asset Store | store: | store:texture |
| Saved Queries | 搜索保存的 queries | q: | q: enemies 搜索包含 enemies 的所有保存的 searches |
| Logs | 搜索 Editor.log 文件 | log: | log:cache 搜索 Editor.log 文件中包含 cache 的信息 |
| | | | |

### 在 search results 中导航

使用 Alt 加上下箭头键在 search history 中循环导航，或者在左边的 pane 中选择一个保存的 search。

## 执行操作

每种类型的 item 都有一个 default action。

要执行一个 item 的 default action：

- 双击 item
- 选择 item 按下 Enter

可以在 Preferences 的 Search section 编辑 default actions。

一些 items 支持额外的 action，你可以在 Preview Inspector menu 中访问。要从 item 的 context menu 访问 additional actions，可以：

- 右击 item
- 在 item entry 中，选择 More Options(:)

还可以使用以下 shortcuts 在一个 selected item 上执行 additional actions，而无需打开 contextual menu：

- Alt + Enter：Second action
- Alt + Ctrl + Enter：Third action
- Alt + Ctrl + Shift + Enter：Fourth action

一些 Search Providers（例如 Asset 和 Scene providers）支持 drag 和 drop actions。你可以从 result area 拖拽 item 到 Unity 的任何支持它们的部分，例如 Hierarchy window，Scene view，以及 Inspector。

