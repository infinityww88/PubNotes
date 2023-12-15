# Unity Authentication

App 通常需要知道一个 player 的 identity，以提供各种功能和 services，为开发者和玩家确保安全性、一致性，并安全地进行每个交互。

Unity Authentication 提供匿名和特定平台的 authentication 解决方案，以支持各种平台，包括 mobile 和 PC。

匿名访问不需要 player 来输入 sign-in credentials，或创建一个 player profile，但是通过一个平台访问则需要一个 sign-in credentials。Unity 通过 SDK 和 API calls 提供 authentication，使开发者可以集中精力做他们最擅长的事情：创造游戏。

## Get started

开始使用 Authentication 之前，需要：

- 注册 UGS（Unity Game Service）
- 连接你的 dashboard 到 Unity Editor Project
- 在 game code 中安装 SDK
- 初始化 SDK

### 注册 UGS

