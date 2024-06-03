# YooAsset

YooAsset 的使用包括 4 或 5 个步骤：

- 初始化 YooAsset 系统

  全局只初始化一次 YooAssets.Initialize()

- 创建 Package 内存对象

  var package = YooAssets.CreatePackage("DefaultPackage");

  每个 package 都要由一个内存对象表示，用来管理这个 package 的各个方面。因此每个 package 必须首先创建内存对象。

  Package 对象只需要创建一次，后续只需要通过 YooAssets.GetPackage 就可以得到这个对象。

  YooAssets.SetDefaultPackage(package);

  可选地，可以将一个 package 设置为 YooAssets 各种静态方法的默认 package。这样 YooAssets.LoadXXX 默认调用这个 package 的 LoadXXX 方法。

  每个 package 都有单独的 LoadXXX 方法可以加载资源。

- 初始化 Package

  package 使用之前必须进行设置。每种模式核心都是设置 Init Parameter，然后用它运行 pkg.InitializeAsync(initParameters)。有两种模式 Offline 和 HostPlay，分别对应两种 Parameter 类型。

  - Offline 模式

    Offline 模式很简单，只需要一个简单的 OfflinePlayModeParameter 对象。

    ```C#
    var initParameters = new OfflinePlayModeParameters();
	await pkg.InitializeAsync(initParameters);
    ```

  - HostPlay 模式

    HostPlay 模式主要是设置各种 service，提供 3 中加载用法：

    - Delivery：自定义 bundle 加载
    - Decryption：解密 bundle 并加载
    - Remote：远程加载 bundle

    ```C#
    var initParameters = new HostPlayModeParameters();
    initParameters.DeliveryQueryServices = new MyDeliveryQueryServices(); 
    initParameters.DeliveryLoadServices = new MyDeliveryLoadServices();
    initParameters.DecryptionServices = new MyDecryptionServices();
    initParameters.BuildinQueryServices = new MyBuildinQueryServices();
    initParameters.RemoteServices = new TestRemoteServices(url);
    var initOperation = pkg.InitializeAsync(initParameters);
    ```

- 更新资源

  这是可选步骤，只针对 remote 加载，而且是针对每个 remote package 执行。这个过程包括 3 个步骤：

  - 更新 package 版本号
  
    pkg.UpdatePackageVersionAsync()

  - 更新 Manifest

    pkg.UpdatePackageManifestAsync()

  - 下载更新列表

    ```C#
    var downloader = pkg.CreateResourceDownloader(downloadingMaxNum, failedTryAgainTimes)
    downloader.BeginDownload();
    await downloader;
    ```

- 加载和卸载资源

  var handle YooAssets.LoadAssetAsync\<Sprite\>(address) 可以加载之前设置的默认包的资源。

  var handle = pkg.LoadAssetAsync(address) 可以加载指定包的资源。

  加载成功后可以调用 handle.Release() 释放引用结束。YooAsset 有自己单独的一天引用计数。每次 Load 都会将加载的资源的引用计数递增 1。计数是在资源上的，而不是 handle 上的。调用 handle.Release() 会递减引用计数。但是注意，YooAsset 并不会在引用计数变成 0 的时候自动销毁资源，这需要显式请求。

  - pkg.UnloadUnusedAssets() 卸载 pkg 内所有引用计数为 0 的资源
  - pkg.TryUnloadUnusedAsset(address) 尝试卸载某个资源，如果它的引用计数为 0 则卸载，否则无作用
  - pkg.ForceUnloadAllAsset() 强行卸载 pkg 内的所有资源，无视它们的引用计数。这可以在 Scene 结束时进行

  Scene 运行时，可以定期调用 UnloadUnusedAsset 来卸载引用计数为 0 的资源，防止资源泄露。

YooAsset 还有一种 Simulate 模式，只用于 Editor 中模拟，在此不提。

YooAsset 加载 StreamingAssets 资源也是使用 http 模式加载的，只不过使用 file:/// 协议：

```C#
Exception: Package initialize failed ! URL : file:///C:/Users/13687/Documents/Unity/Mobile/SpringMatchMobile/Assets/StreamingAssetss/yoo/TestDefaultPackage/PackageManifest_TestDefaultPackage.version Error : HTTP/1.1 404 Not Found
```
## 解释

YooAsset 对 Addressable 资源的组织类似 Docker 的联合文件系统。最上层有一个 address 来标识一个资源，然后这个资源可能有多个版本，每个版本是一个单独的 bundle 文件，按照 Delivery => Remote+Cache => Buildin 层次形成覆盖关系。更高层次的 bundle 覆盖更低层次的 bundle（同一个资源的不同版本的 bundle）。

清单文件就是记录每个资源的 address => bundle 文件的映射关系。每个 bundle 是一个 \[uuid\].bundle 名字的文件。

最高优先级的 Delivery 模式为开发者提供了一种自定义加载资源的方法。例如希望将所有热更资源压缩到一个ZIP包里。玩家第一次启动游戏去下载ZIP包。

这需要提供两个 service 接口：DeliveryQueryServices 和 DeliveryLoadServices。QueryService 告诉一个资源是否是 Delivery 模式提供的资源，以及它的文件名是什么。LoadService 为指定的文件提供加载方法，返回一个 AssetBundle。

但是自定义 Delivery 需要注意：

- ZIP包的下载器需要满足断点续传和文件校验逻辑。
- ZIP包的解压目录需要开发者自己维护，例如解压目录清空等行为。
- ZIP包的下载和解压行为需要在YOO启动之前完成。
- 解压行为建议只执行一次，一般是玩家安装完APP之后启动游戏后执行一次。
- 解压目录下的文件在游戏启动的时候无法保证文件的完整性，需要开发者自己维护。
- YOO的底层机制是会优先查询分发资源，然后是沙盒资源，最后是内置资源。

每个 Package 都有一个 Manifest（清单文件），记录这个 package 的版本号，它包含的所有资源的 address 和 bundle 文件名，以及它的依赖。当 Package 更新时，YooAsset 会依次遍历 Manifest 的每个资源，然后调用各个 service 进行查询，并根据结果决定如何下载它们。

- 如果查询到一个资源是 Delivery 的，就调用 DeliveryLoadServices 来加载它
- 如果它已在缓存中，就跳过忽略
- 如果它是 Buildin 的，就从 StreamingAssets 加载 bundle 到缓存中
- 否则就去 Remote 下载，并保存在缓存中

所有下载到的 bundle 都保存在沙盒（cache）目录中，这样下次就不会重新下载。

HostPlay 总是 Online 模式的，需要从远程加载。因为它无法从本地获取文件。对于 HostPlay 模式，最重要的是 Manifest。Manifest 总是要先更新的，它包含了 package 中所有资源的 address + bundle + 版本号 的信息，只有根据它才能确定那些资源有更新了（和本地 Manifest 记录的资源版本号进行对比）。更新本质就是下载新版本 bundle 到缓存，必须先确定下载列表。下载过程是可以自定义的（Delivery 或 Remote 或 StreamingAssets）。

每次 Build 都会构建完整的 Package（包含 Manifest 和所有资源）。

Offline 模式最简单，直接忽略 cache 和各种 Delivery 或 Remote，直接从 StreamingAssets 加载随应用程序打包的资源。Offline 模式加载的资源包永远不变（除非应用程序本身更新）。

一个 package 就是一组逻辑上组织在一起的资源集合，有一个 Manifest 记录成员信息。一个 package 可以有一部分作为首包资源（Copy 到 StreamingAssets 中）和应用程序一起分发，另一个部分之后放在服务器上远程加载。后续更新的资源，既可以有新增的资源，也可以是对首包进行更新的资源（即对首包资源也可以热更新，但必须是 HostPlay 模式，Offline 是无法更新首包资源的）。如前所述，每个资源的每个版本都是一个单独的 bundle，资源更新并不是修改资源文件本身，而是下载资源新版本的 bundle 文件，并将 Manifest 中将资源的 address 执行新的 bundle 文件名，系统中可能同时存在一个资源的多个 bundle（每个对应不同版本）。可以认为，无论是 remote 下载的，delivery 自定义加载的，还是 StreamingAssets 随应用分发的，都会将资源 bundle 文件 copy 到缓存中统一管理。因此即使一个资源初始作为首包分发，但是后续如果有更新，Manifest 会改变，会下载新的 bundle 版本，address 会指向新的 bundle 文件，再加载的话，就会加载新的版本。但这一切都必须经过 YooAsset 接口，因为一起都是它管理的。

Offline 模式会直接忽略 cache（沙盒），直接从 StreamingAssets 加载。

首包资源既可以作为 Offline 模式使用，也可以作为 HostPlay 使用，但是只有以 HostPlay 使用才可以热更新。

通常在 build 应用程序时，先将 YooAsset Builder 的 Copy 选项设置为 Copy，这会将所有资源复制到 StreamingAssets 目录中，成为首包资源，随应用程序一起分发。之后，无论是添加新的资源，还是首包资源有更新，再次 build package 时，将 Copy 设置为 None。无论 Copy 选项为何，也无论程序将以何种模式使用 YooAsset（自定义 Delivery 还是 Remote），YooAsset 总是先构建 package 的完整结果（完整的 Manifest 和所有新版本的 bundle），如何使用这些 bundle 则视应用程序而定，无论何种模式，最终需要的是这些 bundle 文件，区别只是如何下发它们（自定义，还是 YooAsset 提供的默认 Remote 模式）。如果使用 YooAsset 默认的 Remote 模式，既可以将除首包资源之外的资源放在服务器上，也可以将所有资源一股脑都放在服务器上。因为 Manifest 中记录了每个资源的版本，热更新首先现在 Manifest 文件，对于没有更新的文件，版本号和 bundle 在本地 Manifest 文件和远程新 Manifest 文件中都是一样的，因此不会下载没有更新的资源。

Package 是一个逻辑单位，由一个 Manifest 代表。如果 package 的一部分资源作为首包资源分发，那么在应用程序中就包含了这个初始的 Manifest。初始化 YooAsset 系统和 Package 时，会从 StreamingAssets 加载这个 Manifest。因此之后即使服务器上只有更新的资源，没有首包资源，Package 仍然可以正常加载任何资源（可以认为 HostPlay 模式首先使用 StreamingAssets 首包资源初始化缓存，相当于预下载的远程资源）。也就是即使使用 HostPlay 模式，也可以正常加载首包资源。

YooAsset Builder 每次构建都是生成 package 的完整结果（全量 Manifest 和全部 bundle 文件），如何使用是应用程序的事。增量构建不是只生成新版本的 bundle 文件，仍然是生成完整结果，只是没有改变的资源会直接从之前的构建结果中复制过来。

更新本质就是下载新版本 bundle。一旦下载到缓存后，就没有任何区别，只需要简单地通过 Manifest 查找指定 address 对应哪个 bundle 文件即可。

SteamingAssets 目录逻辑上是只读的，不要在运行时修改或写入新的文件。在 Android/iOS 上是严格只读的，对于 Windows/Linux/Mac 只是不同的目录，程序要自己遵守约束。

如果分包模式变了，并不需要重新发布应用程序，仍然可以直接使用热更新，只是可能会重新下载所有资源。因为每个 address 的 bundle 文件变了，就像普通的资源更新一样，直接下载新的 bundle 文件即可，即使资源本身可能没有任何更新。

IBuildinQueryServices 查询一个资源是否是内置资源（即首包资源）。如果是，则不会下载，而是去 StreamingAssets 加载。这发生在更新 package 生成下载列表的时候，一旦本地 Manifest 和远程 Manifest 一样，则根本不会触发下载这个过程，也就不会进行查询了。对每个发现版本更新资源，进行查询，以确定是否下载它。这个接口为程序提供了一个入口，可以控制一个资源是否下载，还是从 StreamingAssets 加载。但是如果资源有了新的版本，bundle 文件会有不同的名字（新 uuid）。如果通知 YooAsset 系统这个资源是 Buildin 资源，那么 StreamingAssets 目录中必须包含这个 bundle 文件，否则就会抛出错误，bundle 文件找不到。由于 StreamingAssets 目录逻辑上甚至物理上是只读的，很难在它里面写入新 bundle 文件。目前在 Windows 测试，将新的 bundle 直接复制到 StreamingAssets 目录，可以正常加载。但是对于 Android 或 iOS 这样的平台就不可能了。因此不知道这个接口的具体目的是什么，但是它还是必须提供的。当前只需要提供一个总是返回 false 的实现即可，所有资源都不认为是 Buildin 的。不用担心这会触发下载本来已经在 StreamingAssets 的首包资源，YooAsset 会用 StreamingAssets 中的 Manifest 和 bundles 初始化缓存沙盒。 

如果程序两次运行，第一次 IBuildingQueryServices 报告资源不是首包资源，导致资源本更新，第二次报告是首包资源，这样不会触发错误，因为资源在第一次已经被下载，第二次根本不会触发下载过程，而本地 Manifest 已经更新为新版本，资源新 bundle 也已经下载到本地，因此一起都可以正常运行。

## Code

```C#
// 查询相关
private bool IsDeliveryPackageBundle(PackageBundle packageBundle)
{
    if (_deliveryQueryServices == null)
        return false;
    return _deliveryQueryServices.Query(PackageName, packageBundle.FileName, packageBundle.FileCRC);
}
private bool IsCachedPackageBundle(PackageBundle packageBundle)
{
    return _assist.Cache.IsCached(packageBundle.CacheGUID);
}
private bool IsBuildinPackageBundle(PackageBundle packageBundle)
{
    return _buildinQueryServices.Query(PackageName, packageBundle.FileName, packageBundle.FileCRC);
}

public List<BundleInfo> GetDownloadListByAll(PackageManifest manifest)
{
    List<PackageBundle> downloadList = new List<PackageBundle>(1000);
    foreach (var packageBundle in manifest.BundleList)
    {
        // 忽略分发文件
        if (IsDeliveryPackageBundle(packageBundle))
            continue;

        // 忽略缓存文件
        if (IsCachedPackageBundle(packageBundle))
            continue;

        // 忽略APP资源
        if (IsBuildinPackageBundle(packageBundle))
            continue;

        downloadList.Add(packageBundle);
    }

    return ConvertToDownloadList(downloadList);
}

private BundleInfo CreateBundleInfo(PackageBundle packageBundle)
{
    if (packageBundle == null)
        throw new Exception("Should never get here !");

    // 查询分发资源
    if (IsDeliveryPackageBundle(packageBundle))
    {
        string deliveryFilePath = _deliveryQueryServices.GetFilePath(PackageName, packageBundle.FileName);
        BundleInfo bundleInfo = new BundleInfo(_assist, packageBundle, BundleInfo.ELoadMode.LoadFromDelivery, deliveryFilePath);
        return bundleInfo;
    }

    // 查询沙盒资源
    if (IsCachedPackageBundle(packageBundle))
    {
        BundleInfo bundleInfo = new BundleInfo(_assist, packageBundle, BundleInfo.ELoadMode.LoadFromCache);
        return bundleInfo;
    }

    // 查询APP资源
    if (IsBuildinPackageBundle(packageBundle))
    {
        BundleInfo bundleInfo = new BundleInfo(_assist, packageBundle, BundleInfo.ELoadMode.LoadFromStreaming);
        return bundleInfo;
    }

    // 从服务端下载
    return ConvertToDownloadInfo(packageBundle);
}
```
