# Network Headless Logger

Network Headless Loger 替换默认 log handler 为一个设置 Console.ForegroundColor 的 handler。

只在运行在 headless 模式下替换 handler。

![NetworkHeadlessLogger](../../Image/NetworkHeadlessLogger.png)

showExceptionStackTrace 将只打印发送给这个 handler 的任何 exceptions 的 stack trace。
