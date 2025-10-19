# Authentication

当你有一个 multiplayer game，你经常需要存储关于你 player 的信息，为之后的游戏过程，保持游戏状态，或者和你的好友通信。对于这些应用场景，你经常需要一个方法来唯一标识一个 player。用来验证和区分 player 的能力称为 authentication。有一些可用的方法，包括：

- 向用户请求 username 和 password
- 使用一个第三方 OAuth2 或 OpenID Identity Provider（身份提供商），例如 Fackbook，Twitter，Google
- 使用一个第三方服务，例如 PlayFab，GameLift 或者 Steam
- 使用一个设备 id，在移动设备上非常流行
- 在 Android 上使用 Google Play
- 在 IOS 上使用 GameCenter
- 使用你的 website 的一个 web service

## Encryption Notice

默认地，Mirror 使用 Telepathy，它不是加密的，因此如果你想通过 Mirror 做 authentication，强烈建议使用一个支持 encryption 的 transport。

## Basic Authenticator

Mirror 在 Mirror/Authenticators 目录上包含一个 Basic Authenticator，它只使用一个简单的 username 和 password。

## Custom Authenticators

Authenticator 从一个 Authenticator 抽象类派生，允许你实现任何你需要的 authentication 模式。

在 Assets menu 中，点击 Create > Mirror > Network Authenticator 从 Script Templates 创建你自己的 Authenticator，并且填充 messages 和 validation code 来满足你的需要。当一个 client 成功验证时，在 server 上 调用 base.OnServerAuthenticated.Invoke(conn)，在 client 上调用 base.OnClientAuthenticated.Invoke(conn)。Mirror is listening for these events to proceed with the connection sequence。订阅 OnServerAuthenticated 和 OnClientAuthenticated 事件，如果你想在 authentication 之后执行附加的步骤。

## Message Registration

默认地，所有注册到 NetworkServer 和 NetworkClient 的所有消息需要 authentication，除非显式指定不这样做。要绕过 authentication 注册消息，你需要指定 false 到 RegisterMessage 的一个 bool 参数：

```C#
NetworkServer.RegisterHandler<AuthenticationRequest>(OnAuthRequestMessage, false);
```

特定内部消息已经被设置为绕过 authentication：

- Server
  - ConnectMessage
  - DisconnectMessage
  - ErrorMessage
  - NetworkPingMessage
- Client
  - ConnectMessage
  - DisconnectMessage
  - ErrorMessage
  - SceneMessage
  - NetworkPongMessage

## Tips

- 在 OnStartServer 和 OnStartClient 中注册 messages 的 handlers。它们分别在 StartServer/StartHost 和 StartClient 中调用
- 如果验证失败，发送一个消息到 client，尤其是如果有它们可以解决的问题
- 当认证失败时，在 server 上调用 NetworkConnection 的 Disconnect() 方法。如果你允许 player 尝试几次使得它们的 credentials 正确，你确实可以这样做，但是 Mirror 不会为你 disconnect，因此需要你自己 disconnect
  - 记住如果你发送了一个失败消息，在 server 上调用 Disconnect 时添加一个小的延迟，使得它有机会在 connection drop 之前被发送
- NetworkConnection 有一个 authenticationData 对象，你可以将任何你需要在 server 上持久的有关于 authentication 的数据放在里面，例如 account id，tokens，character selection，等等

现在你有了一个自定义 Authenticator component 的基础，剩下的就看你的了。你可以在 server 和 client 之间交换任何数量的消息以完成你的 authentication 过程，在核准 client 之前。

Authentication 还可以扩展到 character 选择和自定义，只需要通过精心准备的额外消息，并且在完成 authentication 过程之前和 client 交互它们。这意味着这个过程发生在 client player 实际进入游戏或改变到 Online scene 之前。

## Basic Authenticator

Mirror 包含一个基本的 Authenticator，它只使用一个简单的 username 和 password。

- 拖放 Basic Authenticator 脚本到场景中具有 NetworkManager 组件的 object 的 Inspector 上面
- Basic Authenticator 组件将会自动被赋予到 NetworkManager 的 Authenticator field

注意，你不需要向 event lists 赋值任何东西，除非你想为自己的目的在自己的 code 中订阅这些事件来。Mirror 对于两个 events 都有内部的 listeners。
