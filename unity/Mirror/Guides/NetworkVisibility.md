# 网络可见性

Multiplayer 游戏使用网络可见性的概念来决定在 gameplay 期间任何给定时刻，哪些 players 可以看见哪些 gameobjects。在具有移动视角和移动 gameobjects 的游戏中，通常 players 不能看见此刻游戏中发生的所有事情。

如果一个特定 player，在 gameplay 期间的一个特定时间点，不能看见绝大多数其他 players，non-players characters，或者游戏中其他移动的、可交互的东西，对于 server 而言通常没有必要发送这些东西的信息到 player 客户端。这有两点好处：

- 它减少了发送给 players 的数据量。这可以帮助提升你的游戏的响应能力，减少使用的带宽。你的 multiplayer 游戏越大越复杂，这个问题越重要。
- 它还可以帮助防止作弊 cheating。既然一个 player client 没有关于它们能看见的东西的信息，在 player 计算机上的 hack 就不能查看 reveal 这些信息。

网络上下文中 Visibility 的概念不必和 gameobjects 是否在 on-screen 上可见相关。相反，它是关于 gameobject 数据是否应该或不应该发送给一个特定的 client。简单来说，如果一个 client 不能看见一个 gameobject（即使它就在 client player 旁边，但是使用了隐身技能），就不必在网络上发送关于它的信息。理想情况下，你想要限制在网络上传递的数据量，只传输必要的数据。

然而，精确地决定一个 gameobject 对一个给定的 player 是否可见，可能是非常消耗资源的，因此，使用一个简单的计算决定是否想一个 player 发送数据是一个好主意。你需要在计算可见性的复杂性的代价和在网络上发送更多信息的代价直接进行权衡。一个非常简单的方式是近似距离检查，而 Mirror 为这种目的提供了内置的组件。

## Network Proximity Checker Component

Mirror Network Proximity Check 组件，是实现 players 网络可见性的最简单的方式。它和物理系统一起来决定一个 gameobject 是否足够近（即可见，并通过网络发送消息）。

## Network Scene Checker Component

Mirror Network Scene Checker 组件可以用来隔离 players 和 server 上的 networked objects 在 additive scene instances。

## Network Visibility on Remote Clients

当一个 remote client 的 player 加入 networked game，只有对这个 player 可见的 gameobject 才会生成。这意味着即使这个 player 进入到一个拥有很多 networked gameobjects 大 world，游戏也可以快速开始，因为它不需要生成世界中现有的每个 gameobject。

注意这应用于 scene 中的 networked gameobjects，不影响本地加载的 assets。Unity 仍然会花时间加载注册的 Prefabs 的 Assets 和 Scene gameobjects。

当一个 player 在 world 中移动时，network-visible gameobjects 的集合将会改变。发生改变时，player 的 client 将被告知发生的改变。当一个 gameobject 不在 network-visible 时，ObjectHide 消息被发送给 clients。默认地，Mirror 在收到这个消息时销毁不可见的 gameobject。当一个 gameobject 变成可见时，client 接收到一个 ObjectSpawn 消息，就好像 Mirror 第一次生成这个 gameobject。默认地，实例化的 gameobject 就像任何其他生成的 gameobject。

## Network Visibility on the Host

Host 共享相同 Scene 作为 server，因为它对 host 这个游戏的 player 同时扮演 server 和 client。因此，不能销毁对 localplayer 不可见的 gameobjects。

相反，在 NetworkVisibility 类中有一个 virtual 方法 OnSetLocalVisibility 被调用。这个方法在 host 上改变可见性状态的 gameobjects 的继承自 NetworkVisibility 的所有脚本上调用。

OnSetLocalVisibility 默认实现 disable 或 enable gameobject 上的 所有 renderer 组件。如果你想定制这个实现，可以在你的 script 中覆盖这个方法，并为 host（即 local client）在 gameobject 变成 network 可见或不可见时 应该如何响应提供一个新的行为（例如关闭 HUD 元素 或 renderers）。

## Customizing Network Visibility

有时你可能想要其他种类的可见性检查，例如 grid-based rules，视线测试，navigation path 测试，或适合你的游戏的其他类型的测试。

为此，你可以从 script 模板 Mirror/NetworkObserver 创建自己自定义的 Network Observer。

Network Proximity Checker 使用 Mirror HLAPI 的 public visibility 接口实现。

使用相同的接口，你可以实现任何种类的可见性规则。每个 NetworkIdentity 保持对可以看见它的 players 集合的追踪。可以看见一个 NetworkIdentity 的 player 称为 NetworkIdentity 的 ovservers。

Network Proximity Checker 以固定频率调用 NetworkIdentity 组件的 RebuildObservers（在 inspector 中调整 Vis Update Interval），使得每个 player 的 network-visible gameobjects 集合在它们移动时可以更新。

NetworkVisibility 类（自定义 observer 脚本继承自这个类），有一些 virtual functions 来决定 visibility：

- OnCheckObserver

  这个方法在 server 上调用，在一个新的 player 进入 game 时，在每个 networked gameobject 调用。如果返回 true，那个 player 被添加到 object 的 observers。Network Proximity Checker 在它的这个函数实现中执行一个简单的距离检查，并且使用 Physics.OverlapSphereNonAlloc 来发现对这个 object 在可见距离内的 players。

- OnRebuildObservers

  这个方法在 RebuildObservers 时在 server 上调用。这个方法期望 observers 的集合被可以看见这个 object 的 players 填充。NetworkServer 然后给予旧的和新的可见性集合来处理发送 ObjectHide 和 ObjectSpawn 消息。

- OnSetHostVisibility

  这个方法被 visibility system 为 host 上的 objects 在 server 上调用。一个 host （带有一个 local client）上的 Objects 在它们不可见时 不能 disabled 或 destroyed。因此这个函数被调用，以允许自定义 code 隐藏这些 objects。一个典型实现是 disable renderer components。这个函数只对 host 上的 local client 调用。

你可以检查一个给定的 networked gameobject 是否是 player，通过检查它的 NetworkIdentity 是否具有一个有效的 connectionToClient。

```C#
int hitCount = Physics.OverlapSphereNonAlloc(transform.position, visRange, hitsBuffer3D, castLayers);

for (int i = 0; i < hitCount; i++)
{
    Collider hit = hitsBuffer3D[i];

    NetworkIdentity identity = hit.GetComponent<NetworkIdentity>();

    if (identity != null && identity.connectionToClient != null)
        observers.Add(identity.connectionToClient);
}
```
