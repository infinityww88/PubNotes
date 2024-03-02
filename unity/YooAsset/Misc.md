# YooAsset

文档中的资源包指的是 bundle，而不是 package。bundle 之间有依赖关系，package 之间完全是独立的，没有任何关系。

package 打包后是就是一组 bundles + 元数据。

bundle 打包策略关系 bundle 大小。可以一个 asset 一个 bundle，也可以一组 asset 一个 bundle。一个 package 只下载有更新的 bundle，并缓存到本地。如果所有资源打包到一个 bundle，则一个 asset 有更新，整个 bundle 就要更新，就需要下载整个 bundle。如果每个 asset 一个 bundle，只会下载更新的 asset 的 bundle。

整个 package 有版本，里面的 bundle 也有版本。任何一个 bundle 更新 package 版本也会更新，但是里面的 bundle 如果没有新版本的话，也不会更新，只使用本地的缓存版本。

package 是一个管理单元，它是一组资源的集合。为这组资源执行一系列相同的操作：打包后到同一个目录；包含一个 manifest（更新列表）；具有一个 copy option（builtin 或 remote）；每次 build 也是一次 build 一个 package。代码中也是一个 package 以单位进行下载更新（打补丁）。

每次 build，YooAsset 会删除 ${Platform} 目录下所有的之前生成的结果，然后创建新的目录。但是新的构建结果中没有更新的资源版本号还是不变，不会被下载，只有更新的 asset 的 bundle 才有新版本。目录名字就是 build version 的名字。每次 build 会自动生成一个版本名，也可以在对话框中自己设置。

使用 YooAsset 的远程更新过程是：

1. 初始化 YooAsset
2. 初始化 code 中 package 对象
3. 更新 package 版本号
4. 更新 package manifest，让本地知道本次更新的列表
5. 下载更新的资源（补丁）。这里可以下载全部更新，也可以通过 tags 下载部分资源，甚至不下载。
6. 加载资源。因为上一步下载时可能只下载部分资源，甚至可以不下载。因此如果加载资源时，它的依赖本地还没有，会自动下载它们。本地已经缓存的资源不会再下载。这就是文档中所说的自动下载依赖资源包（bundle）

下载更新资源（补丁）是可选的，因为如果加载 asset 时，如果 bundle 在本地不存在，会自动取下载（包括下载依赖资源）。完全下载更新可以在 loading 界面时完成，免去在游戏中再下载。

Package 是相互独立的隔离的，两个 package 之间没有任何关系，单独使用。在一个 package 中 yooasset 会自动管理资源之间的依赖，以及自动下载依赖，但是不会对两个 package 进行任何管理，完全取决于自己如何使用。

build 后生成的目录就是本次更新的全部资源，部署时就部署这个目录下的内容。下载资源的地址就指向这个目录。

加载资源 LoadAssetAsync 返回的 handle 还包含的资源的引用计数。YooAsset 资源系统单独维护资源引用计数系统，和 C# 内存管理的引用计数无关，因此要注意防止资源泄露。每次资源加载时，该资源的引用计数加一，handle.Release() 将计数减一。资源可以被 load 多次。当引用计数降为 0 的时候，资源就可以被回收了。因此注意维护 handle 的计数。

每次加载一个资源，引用计数都加 1，返回一个 handle。可以加载多次，得到多个 handle。只有所有 handle 都 Release，资源才可以被 unload。也可以强制 unload 所有资源（例如在切换场景的时候）。

Package.UnloadUnusedAssets 释放所有引用计数为 0 的资源。Package.TryUnloadUnusedAsset 尝试卸载指定资源，如果它的计数为 0 则卸载，否则无作用。UnloadUnusedAssets 就是为每个资源调用 TryUnloadUnusedAsset。

如果加载了一个 Texture，然后将它赋予一个 Material，然后调用 handle.Release() 和 Package.UnloadUnusedAssets，Texture 就会被释放，material 的 texture 变成 missing。

- 不调用 handle.Release() 而调用 UnloadUnusedAsset 或 TryUnloadUnusedAsset，资源不会被卸载
- 调用 handle.Release() 而不调用 UnloadUnusedAsset 或 TryUnloadUnusedAsset，资源不会被卸载
- 如果加载完资源立即调用 handle release 和 unload，资源会被立即卸载，引用它的地方立即变成 missing

Group 中的 collector 包含 3 中类型

- MainAssetCollector
- StaticAssetCollector
- DependAssetCollector

MainAssetCollector 收集的资源对外暴露（接口资源），写入 Manifest 的 AssetList，可以通过代码加载。

StaticAssetCollector 和 DependAssetCollector 收集的资源不对外暴露，打包但是不写入 Manifest 的 AssetList，但是可以被任何其他的资源依赖。

StaticAssetCollector 收集的资源不论是否被其他资源引用，都会被打包。DependAssetCollector 的资源只有被依赖才会打包到 bundle 中，否则剔除。

StaticAssetCollector 和 DependAssetCollector 收集的资源没有 address，因此设置 Address 策略没有意义，只是 YooAsset 没有对 Address UI 做处理，无需设置，此外它下面的 MainAsset 也不显示任何内容，同时是 UI 没有进行特殊处理而已。但是 pack 策略和其他 Collect 策略是有意义的，设置它收集的资源如何打包。

每个收集的资源都被打包到 package 内的一个 bundle 中。

一个资源只能被一个 Collector 收集到，无论是 collector 是 MainAssetCollector，StaticAssetCollector，还是 DependAssetCollector，无论是在一个 group 中，还是在多个 group 中。因为每个 collector 关系到 asset 的打包策略（以及 address name 策略）。如果两个 collector（无论是同一个 group 还是多个 group）收集到同一个资源，YooAsset 会报错，asset 已经存在。

这里针对的是 Collector 显式收集到的资源。YooAsset 收集的策略是先分析所有 Group 的所有 Collector 收集的资源，检查是否有重复（一个资源被多个 collector 收集到），有则报错。没有的话，在分析每个资源的依赖资源，是否在某个已经收集到的 bundle 中，在的话，则这个 bundle 依赖那个 bundle，设置依赖关系，否则将依赖资源打包到自己的 bundle 中（但不暴露）。

因为 collector 显式收集的资源不能重复，因此 group 应该是作为 package 内资源打包划分的逻辑单元来使用，这样就可以天然地隔离资源，最小化资源冲突（被多个 collector 收集）的可能性。

- 如果按照资源类型划分，则可以一个 group 是 material，一个 group 是 texture，一个 group 是 audioClip 等等
- 如果按照应用逻辑划分，则可以一个 group 是 environment，一个 group 是 character，一个 group 是 enemy

尽管一个 group 可以设置多个 collector，但这只是因为 group 可以设置 3 中类型的 collector 而已，不是为了设置多个 MainAssetCollector 或另外两种 collector。group 通常只作为一个资源划分单元，通常只需要一个 MainAssetCollector（暴露的资源）即可，按需要设置一个 depend 或 static asset collector。depend 和 static 都设计较高级的用法。

group 是 package 内部的逻辑组织单元，没有物理实体，为一组资源赋予一个 tags，或 address name 策略。

两个 package 之间完全没有关系和依赖，即使设置相同的 group collector 也会打包两个完全一样的 package。

因为 package 用于给程序打补丁，更新 asset。因此应用程序通常只需要一个 package 即可。在 loading 界面更新整个程序的资源（也可以不下载，因为后续 load asset 会自动下载它以及它的依赖，只要更新了 Manifest）。每个 package 按照不同的资源划分策略（按类型还是角色）划分多个 group。每个 group 只需要一个 MainAssetCollector，可选设置一个 DependAssetCollector/StaticAssetCollector。

一个 package 内，一旦完成打包，bundle 之间的依赖关系就设置好了。下载时，可以只下载部分 bundle（tags）。但是加载资源时，如果一个 asset 的依赖在另一个还没有下载的 bundle 中（同一个 package，因为加载接口是放在 package 中的），会自动下载那个 bundle 并缓存到本地。也可以全部下载。

二进制资源在 Unity 中的类型是 TextAsset，通过 TextAsset.bytes 访问字节数据。

每次打包，都会删除之前的结果，然后生成新的 bundles。但是如果资源 asset 没有更新，新生成的打包中 bundle 版本仍然不变，加载时也不会重新下载。但是如果新的 build 改变了 pack 策略，导致 asset 打包的 bundle 改不了，仍然会重新下载。

一个 Package 中的 assets 是自包含的，它们彼此依赖，但是不依赖外部资源。包含的 assets 结构依赖 Group Collector 的设置，与 assets 在 Editor 中的目录位置无关。

