# YooAsset

## Introduce

使用场景：

- 发布不包含不包含任何资源的安装包，然后边玩边下载
- 发布一个体验安装包，玩家选择下载关卡内容
- 发布单机安装包，有网络时正常更新新版本，没网络玩老版本
- 发布一个 mod 游戏安装包，玩家可以把自己制作的 mod 内容上传到服务器，其他玩家可以下载
- 大型项目，包含上百 GB 的资源内容，每次构建需要花费大量时间，进行分工程构建

特点：

- 构建管线无缝切换，支持内置构建管线，也支持可编程构建管线（SBP）
- 支持分布式构建，支持游戏模组 mod
- 支持可寻址资源定位。默认支持完整路径的资源定位，也支持可寻址资源定位，不需要繁琐的过程即可高效的配置寻址路径
- 安全高效的分包。基于资源标签的分包方案，自动对依赖资源包进行分类。可以非常方便的实现零资源安装包，或全量资源安装包
- 强大灵活的打包系统。可以自定义打包策略，自动分析依赖，实现资源零冗余。基于资源对象的资源包依赖管理方案，避免资源包之间循环依赖的问题
- 基于引用计数的管理方案，实现安全的资源卸载策略，避免资源对象冗余。以及强大的分析器可以帮助发现前缀的资源泄露问题
- 多模式自由切换。编辑器模拟模式，单机运行模式，联机运行模式。在编辑器模拟模式下，可以不构建资源包来模拟真实环境，在不修改任何代码的情况下，可以自由切换到其他模式
- 强大安全的加载系统
  - 异步加载：支持协程，Task，委托等多种异步加载方式
  - 同步加载：支持同步和异步加载混合使用
  - 边玩边下载：在加载资源对象的时候，如果资源对象依赖的资源包在本地不存在，会自动从服务器下载到本地，然后加载资源对象
  - 多线程下载：支持断点续传，自动验证下载文件，自动修复损坏文件
  - 多功能下载器：可以按照资源分类标签创建下载器，也可以按照资源对象创建下载器。可以设置同时下载文件数的限制，设置下载失败重试次数，设置下载超时判定时间。多个下载器同时下载不用担心文件重复下载的问题。下载器还提供了下载进度以及下载失败等常用接口
- 原生格式文件管理。无缝衔接资源打包系统，可以很方便的实现原生文件的版本管理和下载
- 灵活多变的版本管理。支持线上版本快速回退，支持区分审核版本，测试版本，线上版本，支持灰度更新及测试

## 使用

先在 Project 中创建一个 AssetBundleCollectorSetting 资源。

打开 AssetBundle Collector，设置资源打包如何打包（分类，bundle 的名字，address 如何生成）。

先创建 package，可以创建多个 package。每个 package 下面创建 group，每个 group 下面可以添加很多个 collector。

每个 collector 设置收集哪些资源（指定一个 path，可以是单个资源，或者一个目录），资源如何打包（每个资源一个 bundle，还是所有资源一个 bundle 等等），打包的资源属于动态资源、静态资源、还是依赖资源。

每个 group 可以指定一组 tags。tag 可以在代码中用来查询 package 中的资源。要查询资源必须指定 tag，用空字符串或 null 查询不到未指定 tag 的资源。

Enable Addressable 开启 address 寻址。

设置好以后点击 save 保存，所有配置保存到 AssetBundleCollectorSetting 中，设置可以在它的 Inspector 中创建。

打开 AssetBundle Builder，进行打包。每次打包以 package 为单位进行，每个 package 都单独打包。

每次打开 Build Version 都会变化。Build Mode 选择全量重新打包还是增量打包等等。Encryption 选择加密方式。Copy Buildin File Option 很重要，它指定这个 package 是否是首包资源，一起被打包到应用程序中，随之一起分发。这样的资源会被打包到 Assets/StreamingData/yoo/ 目录下面，每个 package 一个目录。StreamingData 目录的内容作为二进制文件原封不动的随应用程序安装在设备的硬盘上（移动平台上，这个目录是只读的）。其中的数据例如 bundle 可以被应用程序在运行时动态加载，就像从网络下载到持久数据目录或 cache 目录的 bundle 一样，只是这些 bundle 在安装时就复制到硬盘上了。持久数据目录是不随应用程序卸载而卸载的，而且应用程序可读可写。注意这个步骤不需要手动执行，YooAsset 在 build 时会自动执行，而且在 Editor 中测试时也不需要。

Copy Buildin File Option 设置为设置 None，只会 build 资源，不会打包到应用程序中。

资源打包后存储在 Project/Bundle 目录下，和 Assets 同级，不是在 Assets 下面。之后在构建时 YooAsset 还会使用它们。每个 package 一个目录，其下面的版本号目录就是打包的最终结果。其中包含版本号信息，manifest，以及各个 bundle。远程部署资源时就是复制上传这个目录的内容。

using YooAsset;

初始化 YooAssets.Initialize()。要加载每个 package，都要先创建 package 的内存对象。这通过 YooAssets.CreatePackage("DefaultPackage") 完成。每个 package 必须先 create，然后 get。

创建 package 对象后，进行初始化。package 可以初始化为三种使用方式：Editor 模拟加载，单机本地加载，远程加载。每种都设定不同的参数。注意单机和远程模式一样可以在 Editor 中使用。但是模拟加载只能在 Editor 中使用。

是否必须 UpdatePackageVersion 和 UpdatePackageManifest。

本地测试远程加载时，在 Assets/Bundle/yoo 下面的版本号目录（即包含 bundle 的目录）中启动服务器。每次重新 build 前先停下服务器，因此 YooAsset build 过程需要删除就的目录，然后生成新的。

## 资源配置

Group 用来为一组 collector 收集的资源统一打 tags。在构建的 package 中，没有 group 的存在，只有 bundle。可以开启或关闭一个 group 的所有 collector。例如可以为同一个资源设置两个 group，分别使用不同的 tags，构建时根据需要只开启其中一个。

每个 collector 指定一个 path，可以是一个 asset，也可以是一个目录。

收集器类型：

- MainAssetCollector

  资源的入口类型。应用程序只会通过代码加载这些资源对象。它们写入到资源清单的列表中。

- StaticAssetCollector/DependAssetCollector

  MainAsset 引用的依赖资源类型。它们不写入到资源清单列表中，因此无法通过 code 加载。但是可以被 MainAsset 引用。

  StaticAssetCollector 收集的资源，无论是否被其他资源引用或被多个资源引用，都会按照设定的打包规则打包，并且不被处理为 share 资源。

  DependAssetCollector 收集的资源如果没有被任何 MainAsset 依赖，则在打包的时候会自动剔除。

### 寻址规则

寻址规则可以自定义扩展，下面是内置的规则：

- AddressByFileName：以文件名为定位地址
- AddressByFilePath：以文件路径为定位地址
- AddressByGrouperAndFileName：以收集器分组名+文件名为定位地址
- AddressByFolderAndFileName：以文件夹名+文件名为定位地址

### 打包规则

打包 bundle 的规则可以自定义扩展，下面是内置规则：

- PackSeparately：以文件路径为资源包名，每个资源文件单独打包
- PackDirectory：以文件所在的文件夹路径作为资源包名，该文件夹下所有的文件打包进一个资源包
- PackTopDirectory：以收集器下顶级文件夹作为资源名，该文件夹下所有文件打包进一个资源包
- PathCollector：以收集器路径为资源包名，收集的所有文件打包进一个资源包
- PackGroup：以分组名称为资源包名，收集的所有文件打包进一个资源包
- PackRawFile：目录下的资源文件会被处理为原生资源包

### 过滤规则

过滤规则指定收集哪些类型的文件，可以自定义，内置规则是：

- CollectAll：收集目录下所有资源文件
- CollectScene：只收集目录下所有 scene 文件
- CollectPrefab：只收集目录下的预制体 prefab 文件
- CollectSprite：只收集目录下的 sprite 文件

打包规则可以控制 asset bundle 粒度。要么一个大 bundle 包含一组 asset，要么多个小 bundle 每个包含一个 asset。

## 资源构建

构建模式

- 强制构建模式：删除指定构建平台下的所有构建记录，重新构建所有资源包
- 增量构建模式：以上一次构建的结果为基础，对发生变化的资源进行增量构建
- 演练构建模式：在不生成 AssetBundle 文件的嵌套下，进行演练构建并快速生成构建报告和补丁清单
- 模拟构建模式：在编辑器下配合 EditorSimulateMode 运行模式，来模拟真实运行的环境

### 首包资源拷贝方式 Copy Buildin File Option

构建以逐个 package 的方式构建。资源可以选择跟随 application 一起下发（首包资源），也可以选择放在服务器上，有 application 在运行时下载。运行时 YooAssets 会远程资源的本地缓存，对于最新版本已经位于本地的资源，不会重复下载。

Copy Buildin File Option 就是选择打包首包资源：

- None：不向 StreamingAssets 中复制任何资源，因此资源只能放在 CDN 上动态下载
- ClearAndCopyAll：清空之前已经构建好的资源，然后拷贝所有新构建的文件，所有资源重新构建并随着 application 一起下发
- ClearAndCopyByTags：清空之前已经构建好的资源，然后只拷贝指定标签的资源，只有这些资源随着 application 一起下发
- OnlyCopyAll：不清空已有文件，直接拷贝所有文件，之前构建的，新版本已删除的资源，也会存在，并随着 application 一起下发
- OnlyCopyByTags：不清空已有文件，只复制指定标签的文件，旧有没有被覆盖的文件，和指定标签新打包的文件，随着 application 一起下发

### 补丁包

构建成功后会在输出目录下直到补丁包文件夹，该文件夹名称为本次构建时指定的资源版本号。补丁包文件夹包含补丁清单文件，资源包文件，构建报告文件等。

- PackageManifest_DefaultPackage_xxx.hash

  记录了补丁清单文件的哈希值。

- PackageManifest_DefaultPackage_xxx.json

  该文件为Json文本格式，主要用于开发者预览信息。

- PackageManifest_DefaultPackage_xxx.bytes

  该文件为二进制格式，主要用于程序内读取加载。

### 首包资源

在构建应用程序时，会希望将某些资源打包到首包（application 分发文件）里，首包资源会被拷贝到 StreamingAssets/yoo/ 目录下。首包资源如果发生变化，也可以通过热更新来更新资源。

### 补丁包

无论是增量构建，还是强制构建，在构建完成后，都会生成一个以包裹版本（PackageVersion）命名的文件夹，统称为补丁包。增量构建只是不重复构建没有变化的资源，只构建有变化的。最终生成的目录还是包含全部的游戏资源。可以无脑将补丁包内容覆盖到 CDN 目录下，也可以编写差分分析工具，只将和线上最新版本之间的差异文件上传。

如果是单机分发，每次只是将补丁包完全打包到 StreamingAssets 目录中。如果是远程分发，YooAssets 会分析哪些资源没有版本变化，最新版本是否在本地已经存在，只有最新版本不存在本地的资源采取远程下载，并缓存到本地。

## 资源部署

远程部署时，每个 app 版本创建一个服务器目录。在 app 没有大的版本更新的情况下，不创建新的资源目录。所有补丁包每次都覆盖到 app 目录中即可。补丁包版本可以另外维护。当需要更新或回退补丁包版本时，只需要将单独维护的补丁包覆盖到当前资源目录即可。

## 运行时

### 初始化

初始化 YooAsset 系统：

```C#
// 初始化资源系统
YooAssets.Initialize();

// 创建默认的资源包
var package = YooAssets.CreatePackage("DefaultPackage");

// 设置该资源包为默认的资源包，可以使用YooAssets相关加载接口加载该资源包内容。
YooAssets.SetDefaultPackage(package);
```

#### 编辑器模拟模式

在编辑器模拟模式中，不需要构建资源包，可以模拟运行游戏。这个模式只能在编辑器下运行。其他模式既可以在运行时运行，也可以在编辑器运行。

```C#
private IEnumerator InitializeYooAsset()
{
    var initParameters = new EditorSimulateModeParameters();
    var simulateManifestFilePath = EditorSimulateModeHelper.SimulateBuild(EDefaultBuildPipeline.BuiltinBuildPipeline, "DefaultPackage");
    initParameters.SimulateManifestFilePath = simulateManifestFilePath;
    yield return package.InitializeAsync(initParameters);
}
```

#### 编辑器运行模式

对于需要热更新资源的游戏，可以使用联机运行模式。

该模式需要构建和部署资源包。

需要提供以下参数：

- DecryptionServices：如果资源在构建时进行了加密，则需要提供 IDecryptionServices 接口的实例类来解密
- QueryServices：查询一个 package 是否是 Builtin 资源包，是的话从 StreamingAssets/yoo 加载，否则从远程 CDN 加载
- RemoteServices：进行远程服务器查询时获取远程文件地址的接口

```C#
public class BuildQuery : IBuildinQueryServices {
   public bool Query(string packageName, string fileName, string fileCRC) {
      return false;
   }
}

public class RemoteServ : IRemoteServices {

    public string GetRemoteMainURL(string fileName) {
        return $"http://127.0.0.1:9090/{fileName}";
    }

    public string GetRemoteFallbackURL(string fileName) {
        return $"http://127.0.0.1:9090/{fileName}";
    }
}

private IEnumerator InitializeYooAsset()
{
    var initParameters = new HostPlayModeParameters();
    initParameters.BuildinQueryServices = new BuildQuery(); 
    initParameters.DecryptionServices = new FileOffsetDecryption();
    initParameters.RemoteServices = new RemoteServ();
    var initOperation = package.InitializeAsync(initParameters);
    yield return initOperation;
}
```

### 资源更新

#### 获取资源版本

对于联机运行模式，在更新补丁清单之前，需要获取一个资源版本。

补丁就是从 CDN 下载覆盖到本地 cache 的资源。它在 CDN 总是全量的，但是下载时可能是全部的，也可能是部分的，即只更新一部分资源，其他资源保持原来版本。

资源版本可以通过 YooAssets 提供的接口来更新，也可以通过 HTTP 访问游戏服务器来获取。

```C#
private IEnumerator UpdatePackageVersion()
{
    var package = YooAssets.GetPackage("DefaultPackage");
    var operation = package.UpdatePackageVersionAsync();
    yield return operation;

    if (operation.Status == EOperationStatus.Succeed)
    {
        //更新成功
        string packageVersion = operation.PackageVersion;
        Debug.Log($"Updated package Version : {packageVersion}");
    }
    else
    {
        //更新失败
        Debug.LogError(operation.Error);
    }
}
```

#### 更新资源清单

对于联机运行模式，在获取到资源版本号之后，就可以更新资源清单了。

```C#
private IEnumerator UpdatePackageManifest()
{
    // 更新成功后自动保存版本号，作为下次初始化的版本。
    // 也可以通过operation.SavePackageVersion()方法保存。
    bool savePackageVersion = true;
    var package = YooAssets.GetPackage("DefaultPackage");
    var operation = package.UpdatePackageManifestAsync(packageVersion, savePackageVersion);
    yield return operation;

    if (operation.Status == EOperationStatus.Succeed)
    {
        //更新成功
    }
    else
    {
        //更新失败
        Debug.LogError(operation.Error);
    }
}
```

#### 资源包下载

在补丁更新完毕后，就可以更新资源文件了。

根据需求，可以选择更新全部资源，或者只更新部分资源。

补丁包下载接口：

- YooAssets.CreateResourceDownloader(int downloadingMaxNumber, int failedTryAgain, int timeout)

  更新全部资源。下载并更新当前资源版本所有的资源包文件。

- YooAssets.CreateResourceDownloader(string[] tags, int downloadingMaxNumber, int failedTryAgain, int timeout)

  只更新指定 tags 的所有资源。

- YooAssets.CreateBundleDownloader(AssetInfo[] assetInfos, int downloadingMaxNumber, int failedTryAgain, int timeout)

  下载并更新 指定资源列表所依赖的资源包文件

```C#
IEnumerator Download()
{
    int downloadingMaxNum = 10;
    int failedTryAgain = 3;
    var package = YooAssets.GetPackage("DefaultPackage");
    var downloader = package.CreateResourceDownloader(downloadingMaxNum, failedTryAgain);
    
    //没有需要下载的资源
    if (downloader.TotalDownloadCount == 0)
    {        
        yield break;
    }

    //需要下载的文件总数和总大小
    int totalDownloadCount = downloader.TotalDownloadCount;
    long totalDownloadBytes = downloader.TotalDownloadBytes;    

    //注册回调方法
    downloader.OnDownloadErrorCallback = OnDownloadErrorFunction;
    downloader.OnDownloadProgressCallback = OnDownloadProgressUpdateFunction;
    downloader.OnDownloadOverCallback = OnDownloadOverFunction;
    downloader.OnStartDownloadFileCallback = OnStartDownloadFileFunction;

    //开启下载
    downloader.BeginDownload();
    yield return downloader;

    //检测下载结果
    if (downloader.Status == EOperationStatus.Succeed)
    {
        //下载成功
    }
    else
    {
        //下载失败
    }
}
```

可以将下载器合并：

```C#
// 例如：把关卡资源下载器和某个指定资源下载器进行合并。
var downloader1 = package.CreateResourceDownloader("level_tag", downloadingMaxNum, failedTryAgain);
var downloader2 = package.CreateBundleDownloader("asset_location", downloadingMaxNum, failedTryAgain);
downloader1.Combine(downloader2);

//开启下载
downloader1.BeginDownload();
```

#### 源代码解析

Package.UpdatePackageManifestAsync()方法解析。

联机运行模式中，通过传入的清单版本，优先比对当前激活清单的版本，如果相同就直接返回成功。如果有差异就从缓存里去查找匹配的清单，如果缓存里不存在，就去远端下载并保存到沙盒里。最后加载沙盒内匹配的清单文件。

## 
