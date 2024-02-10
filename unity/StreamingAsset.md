# Streaming Assets

Unity 在构建项目时合并 Scenes 和 Asset 到生成的 Player 中的二进制文件中。但是可以将文件放在目标设备的正常的文件系统中，使它们可以通过路径名使用。例如，要部署一个 movie 文件到 iOS 设备上，原始的 movie 文件必须在文件系统重可用，才能使用 PlayMovie 播放它们。这个目录还可以包含 AssetBundles，使它们直接随着 Player 安装分发，而不是运行时去下载。

Unity 复制放置在 Unity Project 中的 StreamingAsset（大小写敏感）目录下的文件到目标机器的特定目录中。可以通过 Application.streamingAssetsPath 得到这个目录，它在不同的设备上是不同的。

- 绝大多数平台上（Unity Editor，Windows，Linux）上使用 Application.dataPath + "/StreamingAssets"
- macOS 上使用 Application.dataPath + "/Resources/Data/StreamingAssets"
- iOS 上使用 Application.dataPath + "/Raw"
- Android 上使用 APK/JAR 文件中的文件 "jar:file://" +Application.dataPath + "!/assets"
- 对于 WebGL，Application.streamingAssetsPath 返回一个 HTTP URL，指向 web server 的 StreamingAssets 路径

## 访问 streamng assets

在 Android 和 WebGL 平台上，不可能通过文件系统 APIs 和 streamingAssetsPath 访问 streaming asset files，因为这些平台返回一个 URL。相反，应该使用 UnityWebRequest 访问内容。

- steamingAssetsPath 是只读的。不要在运行时向这个目录中写入文件，或修改文件。
- StreamingAssets 目录中的 .dll 和脚本文件在脚本编译期间不被包含
- AssetBundles 和 Addressables 是访问非常规游戏 build 数据的另一种方法，并且比 Streaming Assets 目录更好

