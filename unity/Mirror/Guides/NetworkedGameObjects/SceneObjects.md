# Scene Game Objects

在 Mirror multiplayer 系统中，有两种类型的 networked gameobjects：
- 在运行时动态创建的 networked gameobjects
- 作为 Scene 一部分保存的 networked gameobjects

在运行时动态创建的 Game objects 使用 multiplayer Spawning system，而且实例化它们的 prefabs 必须在 Network Manager 的 networked gameobject prefabs 列表中注册。

然而，保存为 Scene 一部分的 networked gameobjects（因此在 Scene 加载时就已经存在了）以不同的方式处理。这些 gameobjects 作为 scene 的一部分同时在 client 和 server 被加载，并且在运行时在 multiplayer system 发送任何 spawn messages 之前就存在。

当 Scene 被加载时，Scene 中所有 networked gameobjects 在 client 和 server 都是 disable。然后，当 Scene 被完全加载时，Network Manager 自动处理 Scene 的 networked gameobjects，将它们全部注册（因此导致它们在 clients 之前被同步），然后 enabling 它们，就好像它们是在运行时生成的一样。Networked gameobjects 将不会 enabled，直到一个 client 请求一个 Player object。

在 Scene 保存 networked gameobjects（而不是在 scene 加载后自动生成它们）有以下好处：
- 它们和 level 一起加载，因此在运行时没有暂停
- 它们可以有不同于 prefabs 的特定修改
- Scene 中的其他 gameobject instances 可以引用它们，这可以避免你必须在运行时使用 code 来发现这些 gameobjects 并引用它们

当 Network Manager 生成这些 networked Scene gameobjects，这些 gameobjects 的行为就像动态生成的 gameobjects。Mirror 向它们发送更新和 ClientRPC 调用。

如果一个 server 上的 Scene gameobject 在 client 加入游戏之前被销毁，则它从不会在加入游戏的新 clients 上 enable。

当一个 client 连接时，这个 client 对每一个存在于 server 上的 Scene gameobjects 被发送一个 ObjectSpawnScene spawn 消息。这个消息导致这个 gameobject 在 client 上被 enabled，并且拥有那个 gameobject 在 server 的最新状态。这意味着只有那些对 client 可见，并且在 server 上没有被销毁的 gameobjects 才会在 client 上 activate。

就像正常的 non-Scene gameobjects，这些 Scene gameobjects 以 client 加入游戏时的最新状态开始。
