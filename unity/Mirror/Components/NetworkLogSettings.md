# Network Log Settings

## Network Log Settings component

Network Log Settings 组件允许你配置 logging levels 并且加载 build 中的设置。

当你第一次添加 NetworkLogSetting 时，你必须创建一个存储设置的新的 LogSettings asset。

![NetworkLogSettingsNoSettings](../../Image/NetworkLogSettingsNoSettings.png)

注意：如果 LogSettings asset 以及存在，NetworkLogSettings 组件在添加到一个 gameobject 上时，将会设置 Settings field

## Log Setting

当你第一次设置 LogSettings 时，组件列表可能是空的或不完整的。运行游戏将会导致 Mirror 脚本添加它们各自的 loggers 到这个 list，因此它们的 logging levels 可能会改变。

![NetworkLogSettings](../../Image/NetworkLogSettings.png)

Log settings 还可以使用 “Mirror Log Level” window 改变，它可以从 Window > Analysis > Mirror Log Levels 中打开。

![LogLevelWindow](../../Image/LogLevelWindow.png)

要改变这个设置，在运行时使用 LogFactory。

## Issues

Mirrors Logging api is currently work in progress.
