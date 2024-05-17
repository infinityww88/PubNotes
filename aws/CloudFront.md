# CloudFront

CloudFront 将作为 backend 的 s3 bucket 的内容分发到世界各地的 edge cache。

CloudFront 会缓存内容的，它不可能实时同步 s3 里面的内容。默认的缓存时间是 24 小时，就是上传的 s3 的内容默认需要 24 小时才会在 CloudFront 中看到更新。

要触发立即更新，在 CloudFront 创建 Invalid Policy，指定哪些内容应该变得无效，进而从 s3 中获取新的内容。

