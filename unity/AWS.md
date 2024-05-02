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
			var stream = s3Client.GetObject(BUCKET, s3Obj.Key).ResponseStream;
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

