当 git 命令连接 github 出现 ssh 错误

```
ssh: connect to host github.com port 22: Connection timed out
```

当测试 ```ssh -T git@github.com``` 时会出现同样的问题。这意味着无法通过 22 号端口与 github 进行 ssh 连接。

将 ssh 连接端口修改为 443 进行测试 ```ssh -T -p 443 git@ssh.github.com``` 会显示成功，说明可以通过 443 端口进行 ssh 连接。

修改 SSH 的 config 配置文件，位于 .ssh/config，在 Windows 上位于 C:\用户\<用户名>\.ssh\config。

在 config 中添加：

```
Host github.com
  HostName ssh.github.com
  Port 443
```

再次测试连接 ```ssh -T github.com``` 就会显示成功，之后就可以正常使用 git 连接 GitHub 了。
