# AWS SDK for Unity

## 安装

### 使用 NuGet 安装 AWSSDK

NuGet 是 .NET 平台的包管理系统，就像 python 的 pip，golang 的 go get。使用 NuGet，可以安装 AWSSDK，以及其他一些扩展到项目中。

NuGet 总是具有最新版本的 AWSSDK。NuGet 可以识别 packages 之间的依赖，并自动安装它们。

NuGet 安装的包存储在项目中，而不是一个中心位置。这允许对给定的 application 安装指定版本的 assembly，而不会对其他 application 造成兼容性问题。

使用 Visual Studio 打开 Unity 项目，使用 NuGet 管理器安装 package 到项目中。

### 直接安装 AWSSDK assemblies

不建议使用这种方法，但是在一些环境中是需要的，例如在 Unity 中。


在[这里](https://docs.aws.amazon.com/sdk-for-net/v3/developer-guide/net-dg-obtain-assemblies.html#download-zip-files)下载特定版本的 AWSSDK，其中包含每种 AWS service 的 dll。要使用某个 service，将其 dll 导入到 Unity 中即可。

所有 AWS Service dll 到依赖 AWSSDK.Core，要先导入 AWSSDK.Core.dll 到项目中。

### 从头构建 AWSSDK

从 [Github](https://github.com/aws/aws-sdk-net/tree/main) 上下载 AWSSDK 仓库。使用 Visual Studio 打开项目。最外层的解决方案 sln 包含了全部的 service，每个 service 里面还有自己的 sln。最外层的 sln 是 AWS 团队构建整体 SDK 的解决方案。但是如果只想要某个 service 的 sdk，只需要打开相应 service 的 sln。注意每个 service 都依赖 AWSSDK.Core，要先编译这个 dll。Core 里面没有解决方案，只有项目 cproj，只需要单独创建一个解决方案，添加这个项目即可。

因为 AWSSDK 支持 asynchronous calls，还需要安装 NuGet package AsyncInterfaces。

## 在 Unity 中使用 NuGet packages

在 Unity 中使用 NuGet 并不直截了当，因为 Unity 并没有用来设计和 NuGet 一起协作。为此有几种方法

- [Github 上的 NuGetForUnity](https://github.com/GlitchEnzo/NuGetForUnity) 插件，可以直接在 Unity 中安装 NuGet
- 在 Unity 中使用 Visual Studio 打开项目，在 VS 中使用 NuGet 安装 package 到项目中
- 创建一个辅助 project 来导入 NuGet packages，然后将它包含到 Unity 解决方案中（用来编译一个 dll）。然后就可以在 Unity code 中使用 NuGet packages 了

在 Unity 中使用第三方 .NET package 最简单的方法是编译好 dll，然后导入到项目中，但是这在项目依赖变化时可能导致一些兼容性问题。

## AWS 配置

每个 aws 请求都是一个 https 请求，都需要将 access key 和 secret key 带上。命令行工具中不需要每次都指定它们是因为它们被存储在一个全局配置文件，每次请求 aws 命令自动将其添加请求中。代码调用既可以像这样全局存储，也可以每次请求显式指定，但运行时本质每次请求都带着它们，aws 需要它们进行认证和鉴权。 

```C#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Amazon.DynamoDBv2.DocumentModel;
using Amazon.S3;
using Amazon.S3.Model;
using Amazon.Lambda;
using Amazon.Lambda.Model;
using Sirenix.OdinInspector;
using Cysharp.Threading.Tasks;
using System.Threading;
using System.IO;
using System.Linq;

public class AWSTest : MonoBehaviour
{
	private const string ACCESS_KEY = "******";
	private const string SECRET_KEY = "******";
	private const string BUCKET = "******";

	[Button]
	async UniTaskVoid TestS3() {
		AmazonS3Config s3Config = new	AmazonS3Config();
		s3Config.RegionEndpoint = Amazon.RegionEndpoint.USWest2;
		IAmazonS3 s3Client = new AmazonS3Client(ACCESS_KEY,
			SECRET_KEY,
			s3Config);
		ListObjectsResponse resp = await s3Client.ListObjectsAsync(BUCKET, CancellationToken.None).AsUniTask();
		foreach (var s3Obj in resp.S3Objects) {
            var objResp = await s3Client.GetObjectAsync(BUCKET, s3Obj.Key).AsUniTask();
			var stream = objResp.ResponseStream;
			TextReader tr = new StreamReader(stream);
			var content = await tr.ReadToEndAsync().AsUniTask();
			Debug.Log($"-- {s3Obj.Key} --");
			Debug.Log(content);
		}
	}
	
	[Button]
	async UniTaskVoid TestLambda() {
		AmazonLambdaConfig lambdaConfig = new	AmazonLambdaConfig();
		lambdaConfig.RegionEndpoint = Amazon.RegionEndpoint.USWest1;
		IAmazonLambda lambdaClient = new AmazonLambdaClient(ACCESS_KEY,
			SECRET_KEY,
			lambdaConfig);
		InvokeRequest req = new InvokeRequest();
		req.FunctionName = "MyUnityFunc";
		req.Payload = "{\"value\":321}";
		req.InvocationType = InvocationType.RequestResponse;
		InvokeResponse resp = await lambdaClient.InvokeAsync(req).AsUniTask();
		TextReader tr = new StreamReader(resp.Payload);
		var content = await tr.ReadToEndAsync().AsUniTask();
		Debug.Log($"http_status_code {resp.HttpStatusCode}, status_code {resp.StatusCode}, payload {content}");
	}
	
	[Button]
	async UniTaskVoid TestDynamodb() {
		AmazonDynamoDBConfig ddbConfig = new	AmazonDynamoDBConfig();
		ddbConfig.RegionEndpoint = Amazon.RegionEndpoint.USWest2;
		IAmazonDynamoDB ddbClient = new AmazonDynamoDBClient(ACCESS_KEY,
			SECRET_KEY,
			ddbConfig);
		Table table = Table.LoadTable(ddbClient, "UserInfo");
		Document doc = await table.GetItemAsync("infinity", CancellationToken.None).AsUniTask();
		foreach (var attr in doc.GetAttributeNames()) {
			string strValue = null;
			var value = doc[attr];
			if (value is Primitive) {
				strValue = value.AsPrimitive().Value.ToString();
				Debug.Log($"{attr} -> {strValue}");
			}
			else {
				Debug.Log($"{attr} -> {string.Join(",", value.AsListOfString())}");
			}
		}
	}
}
```

AWSSDK 中的 async 接口返回的是 C# 版本的 Task，要在 UniTask 中使用，可以通过 AsUniTask() 将其转换为 UniTask。

```
可以进行如下转换

Task -> UniTask: 使用AsUniTask
UniTask -> UniTask<AsyncUnit>: 使用 AsAsyncUnitUniTask
UniTask<T> -> UniTask: 使用 AsUniTask，这两者的转换是无消耗的

如果想将异步转换为协程，你可以使用.ToCoroutine()，如果只想允许使用协程系统，这很有用。
```

测试 AWS API 的时候如果抛出异常，查看日志可以找到详细的问题描述来定位问题，通常是权限问题或配置（region）问题。

```
Rethrow as AmazonDynamoDBException: User: arn:aws:iam::330725368797:user/Unity is not authorized to perform: dynamodb:DescribeTable on resource: arn:aws:dynamodb:us-west-2:330725368797:table/UserInfo because no identity-based policy allows the dynamodb:DescribeTable action
```

## .Net Standard vs .Net Core

- .Net Core 是 .Net 的最新实现。它是开源的，可以运行在很多 OS 上。使用 .Net Core，可以构建各种跨平台的 app 或 web 应用
- .Net Standard 是基础 API 的集合，所有 .Net 实现都必须实现。将 .Net Standard 设为 target，可以构建在所有 .Net 平台都可以共享的 library 或 app，不管哪个 .Net 实现或者运行在哪个 OS 上

.Net Standard 是基础，是最小集合，各种 .Net 实现都是基于这个基础构建的。

使用 .Net Standard 构建的 library 可以运行在任何 .Net 平台上，例如 .Net Core、.Net Framework、Mono/Xamarin，但同时它可能缺少特定 .Net Core 实现具有的特色功能。另一方面，target .Net Core 的库只能运行在 .Net Core 平台上。

Why do both exist?

尽管 .Net Core 已经实现了跨平台，但是还有其他 .Net 实现。为了在这些 .Net 平台之间共享 libraries，定义了一个最小的 API 集合，这个 API 集合的实现就是 .Net Standard。它存在的目的是实现各种 .Net 平台之间可移植性

.Net Core 已经实现了跨平台，不仅包括 Windows、Linux、Mac，还包括 Android、iOS 等移动平台。这意味着使用 .Net Core 编译的 libraries(dll) 可以直接运行在任何 OS 的 .Net Core 上。例如在 Windows 上用 Visual Studio 编译的 .Net Core dll 可以直接运行在 Android 或 iOS 上。而 .Net Standard 则实现了在不同 .Net 实现之间的可移植性。

构建 AWS SDK dll，如果不是 target .Net Standard，在移动设备上会抛出异常 

```
NotSupportedException: System.Configuration.ConfigurationManager::get_AppSettings
```

这是因为 IL2CPP 不支持 System.Configuration.ConfigurationManager，如果 AWS SDK 代码使用了它，就无法运行。不支持的原因是要在 IL2CPP 中支持 System.Configuration.ConfigurationManager 需要大量的代码改动，而 Unity 认为这个功能很少会被使用，因此目前没有计划支持这个功能。要避免这个异常，可以切换到 Mono Scripting Backend，但是这样就无法使用 HybridCLR。

要在 IL2CPP 中支持 AWS SDK，需要编译或下载 target 为 .Net Standard 的 SDK dll。

可能是 .Net Standard 版本的 AWS SDK 还没有使用 System.Configuration.ConfigurationManager。

注意 .Net Standard 版本的 AWS SDK 引用了 Microsoft.Bcl.AsyncInterfaces，需要导入额外的 Microsoft.Bcl.AsyncInterfaces.dll，它在 AWS 官网提供的 SDK 压缩包里已经被编译好了，与 AWSSDK.Core.dll 一起导入到 Unity 中即可。但是其他版本的 sdk，例如 aws-sdk-net45.zip，不包含 Microsoft.Bcl.AsyncInterfaces.dll，直接导入 Core.dll 和 service dll 即可运行。原因可能是 .Net Standard 实现中缺少 AWS SDK 需要的异步编程特性，因此需要额外的 Microsoft.Bcl.AsyncInterfaces 支持，而更高级的 .Net 实现包含了异步编程特性，不再需要 Microsoft.Bcl.AsyncInterfaces 了。但是后者无法在移动设备上运行，只能使用 .Net Standard 版本的 SDK，因此要么下载编译好的 Microsoft.Bcl.AsyncInterfaces.dll，要么手动编译这个 dll。
