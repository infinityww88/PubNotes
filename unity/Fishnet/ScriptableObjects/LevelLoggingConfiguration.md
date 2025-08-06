ScriptableObject 配置 Fishnet 会打印哪些日志内容。

​​Level Logging Configuration（日志级别配置）​​ 是一个可编程资源脚本对象 ScriptableObject，用于自定义 Fish-Networking 的日志输出。创建后，您可以在 NetworkManager 组件中选择该配置。

系统提供四种日志级别，适用于不同的构建类型和编辑器环境：

- ​​Off（关闭）​​：完全禁止日志输出
- ​​Error（错误）​​：仅记录错误级别的日志
- ​​Warning（警告）​​：记录错误和警告级别的日志
- ​​Common（常规）​​：记录所有日志，包括错误、警告和信息性日志

## 设置

- Logging Enabled

  开启/关闭 Fishnet 的 logs。

- Development Logging

  game 是 development build 或 editor 时发送的 logs 等级。

- Gui Logging

  控制常规的游戏 build 的日志等级，对比 headless(Non GUI) 构建。

- Headless Logging

  控制游戏 build 为 headless 的日志等级。
