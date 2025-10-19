# Network Animator

Network Animator 组件允许你同步 networked objects 的 animation states。它同步一个 Animator Controller 的 state 和 parameters。

注意如果你在一个 empty game object 创建一个 Network Animator 组件，Mirror 也会在那个 gameobject 上创建一个 Network Identity 组件以及一个 Animator 组件。

![NetworkAnimatorComponent](../../Image/NetworkAnimatorComponent.png)

- Client Authority

  开启时，使对 animation 参数的修改从 client 发送到 server

- Animator

  定义你想 Network Animator 同步的 Animator 组件。

通常，改变被发送到组件所在的 object 的所有 observers。设置 Sync Mode 为 Owner Only 使得改变在 server 和 object 的 client 之间是私有的。

可以使用 Sync Interval 指定同步的频率（以 seconds 为单位）。

## 细节

Network Animator 确保 gameobject 动画在网络上同步（状态和参数），意味着所有 players 看到动画同时发生。对 networked animation 有两种类型的 authority。

注意：Animator triggers 不是直接同步的。调用 NetworkAnimator.SetTrigger。具有 authority 的 gameobject 可以使用 SetTrigger 函数在其他 client 上发射一个 animation trigger。

- 如果 gameobject 在 client 上具有 authority，你应该在拥有 gameobject 的 client 上 locally 动画它。那个 client 发送 animation state 信息到 server，server 广播它到所有其他 clients。例如，这可能适合具有 client authority 的 player characters
- 如果 gameobject 在 server 上具有 authority，则你应该在 server 上动画它（通过 client 发送 Command 给 server，然后 server 执行动画）。然后 server 向所有 clients 发送状态信息。这对于那些不与特定 client 相关的 animated gameobject 很常见，例如 scene objects，和 non-player characters，或者 server-authoritative clients
