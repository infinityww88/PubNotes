# Aws Certificat Manager

为域名请求证书。

首先需要验证 DNS 域名：

- DNS 验证（推荐）
- 电子邮件验证

验证域名比较麻烦，最简单的方式就是在 AWS 上申请域名，在 AWS 验证，在 Route53 配置域名，在 ACM 上为域名请求证书。这一切都在 AWS 中集成的非常好。

为域名请求证书时注意添加通配符条目，这样证书同时域名下面的每个子域名签名。

```plain
netripple.link
*.netripple.link
```

请求的域名证书，可以用在 ELB 上。注意证书上签名的地址是 netripple.link，而 ELB 的域名则是 amazon.com。这样没问题，因为客户端请求的域名是 api.netripple.link，而 Route53 中配置了 api.netripple.link 重新解析为 ELB 的 DNS 地址，这对客户端是透明的，ELB 返回认证 *.netripple.link 的证书，客户端检查后确认证书认证的就是请求的域名 api.netripple.link，因此证书认证通过。
