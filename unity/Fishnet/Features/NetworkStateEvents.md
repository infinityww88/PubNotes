NetworkBehaviour lifecycle 回调是 NetworkObject 生成-销毁 过程中在 server 和 client 发生的 callback。

下面是有关 game/application 全局的网络事件回调，可以认为是 Application 的事件，而不是 NetworkBehaviour 的事件。这可以对比 Unity 的 MonoBehaviour 的事件（Awake, Start, OnEnable, OnDisable, Destroy）和 Application(OnExit) 的事件。

你可以利用很多可用的 events 来实时了解网络当前状态。

下面不是可用 events 的完整列表，只是最常用的一些。

## Server Side Events

- OnAuthenticationResult

  ServerManager.OnAuthenticationResult

  当客户端完成身份验证（无论成功或失败）时，系统将触发此事件。该事件提供两个关键参数：相关的NetworkConnection对象，以及一个布尔值（用于标识该客户端是否验证成功）。

  此事件非常实用，你可以通过它实现以下功能：

  存储成功连接服务器的客户端NetworkConnection；

  向新连接的客户端发送通知消息。

- OnServerConnectionState

  ServerManager.OnServerConnectionState

  当服务器状态发生变化时（即服务器启动或停止运行的瞬间），系统会触发此事件。该事件非常适合用于执行各类服务器端网络操作，例如加载初始场景或生成初始对象。

- OnRemoteConnectionState

  ServerManager.OnRemoteConnectionState

  当客户端到服务器的连接状态发生变化时（即客户端连接或断开服务器的瞬间），系统会触发此事件。该事件具有两大典型应用场景：

  1. 检测客户端断开连接；
  2. 在身份验证脚本中处理数据发送，或在认证前检查服务器是否已满。

## Client Side Events

- OnAuthenticated

  ClientManager.OnAuthenticated

  当本地客户端成功通过FishNet服务器认证时，将触发此事件。此时客户端将获得唯一的Client ID，并被自动添加到ServerManager.Clients和ClientManager.Clients两个集合中。该事件是判断客户端已完全连接服务器并准备好开始游戏的理想时机。

- OnClientConnectionState

  ClientManager.OnClientConnectionState

  当本地客户端状态发生变化时（即客户端与Fish-Networking服务器建立连接或断开连接的瞬间），系统会触发此事件。该事件具有两大典型应用场景：

  1. 检测客户端与服务器的断开连接；
  2. 识别客户端的初始连接动作。

  身份验证脚本通常会利用此事件向服务器发送初始数据，以便服务器完成对客户端的认证流程。

  当这个事件调用时，client 还没有添加到 ClientManager.Clients 集合中。

- OnRemoteConnectionState

  ClientManager.OnRemoteConnectionState

  当远程客户端的状态发生变化时（即远程客户端连接或断开游戏的瞬间），系统会触发此事件。该事件主要用于检测其他玩家的连接或断开行为。

  这个事件只在使用 ServerManager.ShareIds 时可用。

## Shared Events

- OnPreTick

  TimeManager.OnPreTick

  这个事件在 network tick 之前调用，同时也是在数据读取之前。

- OnTick

  这个事件在 network tick 发生时调用，这可以用于以一个设置好的频率发送 data 到 server，防止数据发送频率太频繁导致网络连接的 flooding。

- OnPostTick

  这个事件在 network tick 之后调用。如果使用 PhysicsMode.TimeManager,physics 此时已经模拟完了。

