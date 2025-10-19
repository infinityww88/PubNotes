# NetworkBehaviour Callbacks

在一个普通的 multiplayer game 过程中会发生大量关于 NetworkBehaviour 的事件。这些事件包括诸如 host starting up，一个 player 加入，或者一个 player 离开。每个这样的事件关联一个 callback，你可以在自己的 code 中实现，在事件发生时执行相应的动作。

当你创建一个自定义 NetworkBehaviour 脚本时，可以编写自己的实现定义当这些事件发生时执行什么动作。

## Server Only

- OnStartServer

  当 Behaviour 在 server 上 start 时调用

- OnStopServer

  当 Behaviour 在 server 上 destroy 或 unspawn 时调用

- OnSerialize

  当 Behaviour 在发送给 client 之前序列化时调用，当覆盖这个函数时，确保调用 base.OnSerialize

## Client Only

- OnStartClient

  当 behaviour 在 client 上生成时调用

- OnStartAuthority

  - 当 behaviour 在生成时具有 authority 时调用（例如 local player）
  - 当 behaviour 被 server 赋予 authority 时调用

- OnStopAuthority

  - 当 authority 从 object 撤销时（例如 local player 被替换，但是没有销毁）

- OnStopClient

  - 当 object 在 client 上被销毁时调用，通过 ObjectDestroyMessage 或 ObjectHideMessage 消息

## Example flows

注意，Start 在第一帧之前被 Unity 调用，这通常在 Mirror 回调之后发生。但是如果你不 instantiate 同一帧调用 NetworkServer.Spawn，则 Start 可能先调用。

注意，OnRebuildObservers 和 OnSetHostVisibility 现在在 NetworkVisibility 而不是 NetworkBehaviour。

## Server mode

当一个 NetworkBehaviour.Spawn 被调用时（例如当一个新的 client connections 和一个 player 被创建时）：

- OnStartServer
- OnRebuildObservers
- Start

## Client mode

当一个 local player 为 client 创建时

- OnStartAuthority
- OnStartClient
- OnStartLocalPlayer
- Start（Start 在 Mirror 回调之后由 Unity 调用）

## Host mode

这些只在一个 client 连接时，在 Player Game Objects 上调用

- OnStartServer
- OnRebuildObservers
- OnStartAuthority
- OnStartClient
- OnSetHostVisibility
- OnStartLocalPlayer
- Start


