# Loading Resources at Runtime

有时使 asset 在 project 可用但是不想将它作为 scene 的一部分加载非常有用。例如动态生成 GameObject 或 Component，并为它指定一个 asset 引用。

Unity 提供 Resource Folders 来支持动态加载的游戏资源。还可以创建 AssetBundles。

## AssetBundles

一个 AssetBundle 是一个外部 assets 的集合。这些文件存在于 Unity Player 外部，通常位于 web server，通过网络动态访问。

## Resource Folders

Resource Folders 是一组包含在 Unity Player 中的，但是不必和任何 GameObject 连接的 assets 的集合。可以认为它是随 Unity Player 一起分发的一个 AssetBundle，更多的 AssetBundles 则需要从网络下载。

要创建 Resources 资源，在 Project 创建 Resources 目录，然后将资源放进去即可。可以在 Project 中很多不同的地方有多个 Resource Folders。无论何时，当你想要从这些目录中加载一个资源，调用 Resources.Load()。


所有 Resources 目录中找到的所有 asses 和它们的依赖都存储在一个名为 Resources.assets 的文件中。如果一个 asset 已经被其他 Level使用，则它存储在那个 Level 的 .sharedAsset 中。

只有存储在 Resources folder 中的 assets 可以通过 Resources.Load() 访问。但是 resources.assets 中可能有很多 assets，因为它们是依赖的（例如 Resources folder 中的一个 material 可能引用外面的一个 Texture）。

## Resource Unloading

可以使用 AssetBundle.Unload() 和 AssetBundle.UnloadAsync(bool) 来卸载一个 AssetBundle 的资源。如果传递 true，AssetBundle 内部保存的 objects 和使用 AssetBundle.LoadAsset() 从 AssetBundle 加载的 objects 都会被销毁，被 bundle 使用的 memory 都会被释放。

有时可能想加载一个 AssetBundle，实例化期望的 objects，并释放被 bundle 使用的 memory，同时保持 object 存在。为此可以 传递 false。当 bundle 被销毁后，将不能从其中再次加载 objects。

要销毁使用 Resources.Load() 加载的 objects，调用 Object.Destory()。要释放 assets，使用 Resources.UnloadUnusedAssets()。

外部数据 => 内部（不被 scene 引用）的 object => 被 scene 使用的 object（实例化，Instantiate）。

销毁的是 scene 应用的 object，卸载的是从磁盘加载到内存不被 scene 引用的 object。

## Resources.Load

加载 Resources folder 中指定 path 指定类型的 asset，找不到返回 null。

path 是大小写不敏感的，并且不能包含文件扩展名。所有 asset names 和 paths 使用正斜线，不能使用反斜线。

path 是相对于任何 Resources 目录的。因为可以有多个 Resources，因此在不同的 Resources 中使用同一个 asset 名字。

例如，project 中可能包含两个 Resources 目录：Asset/Resources 和 Assets/Guns/Resources。path 中不需要包含 Asset 和 Resources 字符串，只需要 Resources 后面的部分。例如加载 Assets/Guns/Resources/Shotgun.prefab 只需要 Shotgun 作为 path。而 Assets/Resources/Guns/Missiles/PlasmaGun.prefab 只需要 Guns/Missiles/PlasmaGun 作为 path。

如果不同类型的 asset 具有相同的名字，因为不能指定扩展名，load 返回的 asset 是不确定的。要加载指定类型的 asset，使用 Resources.Load\<T\>(path)。

