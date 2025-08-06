Fish-Networking 使用一组预制体来管理网络对象在网络中的生成。

每当你在服务器上实例化并生成一个对象时，FishNet 会使用选定的「可生成预制体」集合来确定该对象的类型，并自动在所有客户端上实例化并关联这些对象。

可生成预制体集合 Spawnable Prefabs 可以在 NetworkManager 组件中进行设置。

## DefaultPrefabObjects

​​默认预制体对象资源（Default Prefab Objects）​​ 是一个动态填充的可生成网络对象集合。

FishNet 会根据你在 Fish-Networking 配置中指定的目录路径，自动在该目录下生成此资源，并从配置好的位置填充网络预制体。

你无需手动填充或更新此集合，FishNet 会自动处理这些操作。

## SinglePrefabObjects

Single Prefab Objects（单预制体对象）​​ 是一个可编程脚本资源，您可以通过继承它来实现自定义功能。

该资源既被 ​​DefaultPrefabObjects 集合​​所使用，也可以直接用于你自定义的集合。

如果选择直接使用它，记得手动将所有可生成的网络对象预制体添加到其集合中。

## DualPrefabObjects

Dual Prefab Objects（双预制体对象）资源​​ 可用于让 Fish-Networking 在客户端生成与服务器不同的预制体。

每当服务器生成选定版本的预制体时，FishNet 会在所有客户端上生成对应的客户端版本。

与上面一样是一个 Prefab 列表，但每个 item 是两个 Prefab，一个用于 server，一个用于 client，但它们可以是同一个 prefab。
