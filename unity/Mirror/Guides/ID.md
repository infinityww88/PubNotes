# ID

## Asset Id

Mirror 使用 GUID 作为 Asset Ids。每个拥有一个 NetworkIdentity 组件的 prefab 拥有一个 Asset Id，它只是简单地将 AssetDatabase.AssetPathToGUID 转换为 16 bytes。Mirror 需要这个 ID 来知道生成哪个 prefabs（Prefabs 的 Asset ID）。

## Scene Id

Mirror 使用 unit 作为 Scene Ids。Scene（Hierarchy）中的每个拥有一个 NetworkIdentity 的 gameobject 在 OnPostProcessScene 中被赋予一个 scene id。Mirror 需要区分 scene objects，因为 Unity 对 scene 中的不同 gameobject 没有 unique id。

## Network Instance Id (NetId)

Mirror 使用 uint 作为 NetId。每个 NetworkIdentity 在 NetworkIdentity.OnStartServer 或者它被生成之后，被赋予一个 NetId。当在 client 和 servert 之间传递消息时，Mirror 使用这个 id 获知哪个 object 是消息的接受者。

## Connection Id

每个 network connection 具有一个 connection id，它是被 low level Transport layer 赋予的。Connection id 0 被保留为 local connection，当 server 也是一个 client（host）的时候。
