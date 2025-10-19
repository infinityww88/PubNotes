# lambda

## CloudWatchLog

- log group对应一个需要日志的service（例如lambda）
- log group中log stream对应一个lambda hot调用打印的日志流，即lambda不关闭的情况下所有使用同一个lambda实例和相同资源的所有调用打印的日志
- lambda需要iam role具有写CloudWatchLog的权限，同时在权限中配置它可以打印到的log group
- 所有打印到控制台的信息都打印到CloudWatchLog

## Limit

Lambda限制你可以用来允许和存储函数的计算和存储资源的数量

- 并发执行数量 1000
- 函数和layer存储 75GB
- 每个VPC的Elastic network interfaces 250

函数配置、部署、和执行的限制。这些限制不可更改

- 函数内存分配 128M-3008M 64M增量
- 函数timeout 900seconds 15 minutes
- 函数环境变量 4K
- /tmp目录存储 512M
- 文件描述符 1024
- 执行进程/线程数 1024
- 部署包大小
  - 50M（zipped for direct upload()
  - 250M（unzipped，including layers）
  - 3M（console editor）

### Lambda函数的并行

Concurrency是任何给定时间function的执行请求数量。但function被调用时，lambda分配它的一个instance来处理event。当函数代码运行完毕，它可以处理其他请求。如果function再次被调用时，之前的request还没有处理完成，另一个instance被分配，这就增加了function的concurrency。

Concurrency是regional范围限制的，一个region的所有function共享这个限制。要确保一个function总是达到一个特定的concurrency，你可以配置function的保留并行数reserved concurrency。当一个function具有reserved concurrency时，没有其他funciton可以使用这个保留并行数。保留并行数同时还限制function的最大并行数，并且应用到整个function，包括version和aliases。

当Lambda分配function的一个实例时，runtime加载function的代码并且运行定义在handler之外的初始化代码。如果你的code和dependencies很大，或者你在初始化期间创建SDK clients，这个过程可能要花一些时间。当你的function scales up时，这将导致部分requests被新instances服务，因此被其他的request有更高的延迟。

要使function的scale避免延迟波动，使用provisioned concurrency（预分配并行数）。通过在调用增加之前申请与预分配并行数，你可以确保所有request被初始化好的instance执行，因此具有很低的延迟。

Lambda还集成了Application Auto Scaling。你可以配置Application Auto Scaling基于计划或者使用率来管理预分配并行数。使用scheduled scaling来在预期的peak traffic中增加预分配并行数。要按需自动增加预分配并行数，使用Application Auto Scaling API注册一个target并且创建一个scaling policy。

预分配并行数将函数的保留并行数和regional限制计算在内。

保留并行数具有一下效果：

- 其他函数不能阻止你的函数进行scaling

- 你的函数不会scale失控，它定义了最大并行数

## Configuration

upstream and downstream资源

- Triggers  
Triggers是你配置的用来调用function的services和resources。选择Add Trigger创建一个Lambda**事件源映射**或者在Lambda Console集成的其他service中配置一个trigger
- Layers  
添加一个layers到应用中。一个layer是一个ZIP archive，其包含库，自定义运行时，或者其他依赖
- Destinations  
向function添加一个目的地来把调用结果细节发送到其他service

Function Setting

- Code

  function的code和依赖。要添加一个库，或者editor不支持的语言的库，上传一个开发包。如果开发包大于50MB，选择“Upload a file from Amazon S3”

- Runtime

  执行function的lambda运行时

- Handler

  当函数被调用时执行的方法名，例如index.handler。index是文件或模块名，handler是方法名

- Environment variables

  Lambda在执行环境中设置的Key-Value pairs。使用环境变量在code之外扩展函数的配置

- Tag

  Lambda附加在function资源上的Key-Value pairs。用来为Lambda console上cost报告和过滤将functions组织成分组

- Execution role

  Lambda执行function时假设的IAM role

- Memory

  function执行时可用的内存

- Timeout

  Lambda运行函数在被停止之前的运行时间

- VPC

  如果function需要访问网络，需要它连接到一个VPC

- Database proxies

  为使用Amazon RDS DB实例或集群的function创建一个database proxy

- Concurrency

  保留并发数。同时可执行的函数数量。预分配并发数保证一个函数没有延迟波动地扩展。保留并发数应用于整个function，包括全部version和aliases

- Asynchronous invocation

  配置错误处理行为来减少Lambda重试的次数，或者未处理的event在Lambda丢弃它们之前保留在队列里的时间。配置一个dead-letter queue来保存丢弃的events。你可以为一个funciton、version、或alias配置错误处理
