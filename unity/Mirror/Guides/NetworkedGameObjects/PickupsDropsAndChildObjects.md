# Pickups, Drops, and Child Objects

经常会出现的问题是，如何处理挂载为 player prefab children 的 objects，那些所有 clients 需要知道和同步的，诸如装备了哪个武器，拾取了哪个 networked scene objects，以及 players 在 scene 中丢弃了 objects。

Mirror 不支持在一个 object hierarchy 上的多个 NetworkIdentity 组件。因为 Player object 必须有一个 NetworkIdentity，因此它的任何子节点都不能有。

注意 item prefab 是 ary only（没有逻辑功能，只是艺术展示）。它们没有 scripts，并且必须没有 networking components。它们可以有 MonoBehavior-based 的脚本，当然，这些脚本可以被应用并且从 player prefab 的 ClientRpc 中调用。

使用 Mirror 支持的类型的 SyncVar 以及 Commands 等通信方式，结合 MonoBehavior 脚本实现物品的装备切换。
