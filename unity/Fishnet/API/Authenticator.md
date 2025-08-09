# Authenticator

## Properties

- bool Initialized

  authenticator 是否被初始化。

## Methods

- void InitializeOnce(NetworkManager networkManager)

  初始化这个 Authenticator。

- void OnRemoteConnection(NetworkConnection connection)

  在 server 上，当 client 连接后立即调用。可以用于向 client 发送认证信息。

## Events

- event Action<NetworkConnection, bool> OnAuthenticationResult

  当 authenticator 得出 connection 的认证结果时调用。如果通过认证，返回 true，否则返回 false。Server 自动监听这个 event。
