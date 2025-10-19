# Fallback Transport

FallbackTransport 可以用于 work around transport 平台限制。

例如，Apathy transport 当前只用于 Windows，Mac，和 Linux，而 Telepathy 可以用于所有平台。Apathy 有显著的性能提升，理想地，我们希望 Mirror 使用 Apathy，如果在 Windows/Mac/Linux，并且在其他平台上 fallback 到 Telepathy。

这就是 FallbackTransport 允许我们做的。

用法：

1. 在 scene 中添加一个带有 NetworkManager 的 gameobject
2. 默认地，Unity 添加一个 TelepathyTransport 到 NetworkManager gameobject 上面
3. 添加一个 FallbackTransport 到 gameobject 上面
4. 将 FallbackTransport 赋予到 NetworkManager 的 Transport
5. 添加一个 ApathyTransport 组件到 gameobject
6. 将 ApathyTransport 和 TelepathyTransport 都添加到 FallbackTransport 的 transport property

注意：所有 fallback transport 需要彼此二进制兼容。

![FallbackTransport](../../Image/FallbackTransport.png)
