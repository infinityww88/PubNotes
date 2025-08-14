# Configuring TimeManager

TimeManager 中用于配置 prediction 的选项非常少。

当使用 prediction 时，使用 Fish-Networking timing 系统非常重要。默认使用的是 Unity 的 timing，但是这可以在 TimeManager 组件中修改。

如果 NetworkManager 上没有 TimeManager，添加一个 TimeManager。然后将 Physics Mode 设置为 Time Manager 即可。
