# 时钟同步 Clock Synchronization

许多算法需要 client 和 server 之间时钟同步。

Mirror 自动为你完成此事。

double now = NetworkTime.time; // 获得当前时间

它在 client 和 server 返回相同 value。当 server starts 时，它从 0 开始。这个时间是一个 double，而且不能被转换为 float，否则在一些时间之后将会丢失精度：
- after 1 day, accuracy goes down to 8 ms
- after 10 days, accuracy is 62 ms
- after 30 days , accuracy is 250 ms
- after 60 days, accuracy is 500 ms

Mirror 还会计算应用程序看见的 RTT 时间：

double rtt = NetworkTime.rtt;

你可以测量精度：

double time_standard_deviation = NetworkTime.timeSd;

deviation（误差）

例如，如果它返回 0.2，意味着 time 测量在 0.2s 上下摇摆。

网络波动通过使用 EMA 平滑波动值被补偿。

你可以配置 ping 的频率：

NetworkTime.PingFrequency = 2.0f;

你还可以配置多少个 ping results 用于计算：

NetworkTime.PingWindowSize = 10;
