# Shadowsocks

windows10 wsl 两个网卡，两个网络

192 172 不通

curl 和 curl.exe go 和 go.exe 在各自的网络运行

wsl 建立的 sock client 不能被 windows 中的程序访问

curl 支持 socks 代理

crul.exe -x sock5h://127.0.0.1:1080 'https://www.google.com'
注意是 socks5h 不是 socks5

https://github.com/shadowsocks/go-shadowsocks2

go run . -s
go.exe run . -c
go.exe build

go-shadowsocks2 -s 'ss://AEAD_CHACHA20_POLY1305:your-password@:8488' -verbose

go-shadowsocks2 -c 'ss://AEAD_CHACHA20_POLY1305:your-password@[server_address]:8488' \
    -verbose -socks :1080 -u -udptun :8053=8.8.8.8:53,:8054=8.8.4.4:53 \
    -tcptun :8053=8.8.8.8:53,:8054=8.8.4.4:53

go run . -h

-cipher string
        available ciphers: AEAD_AES_128_GCM AEAD_AES_256_GCM AEAD_CHACHA20_POLY1305 (default "AEAD_CHACHA20_POLY1305")

shadowsocks-window go-shadowsocks2 不同的程序功能不太一样

shadowsocks-window 是一个 GUI 程序，go-shadowsocks2 是一个命令行程序，而且同时支持 server client

aws ec2 安装 go,git 下载 go-shadowsocks2，直接用 go 运行或构建运行即可，作为 server 端，运行 -s
在 windows（或 linux，mac，wsl）端 作为 client 端，运行 -c

Shadowsocks的运行原理与其他代理工具基本相同，使用特定的中转服务器完成数据传输。例如，用户无法直接访问Google，但代理服务器可以访问，且用户可以直接连接代理服务器，那么用户就可以通过特定软件连接代理服务器，然后由代理服务器获取网站内容并回传给用户，从而实现代理上网的效果。服务器和客户端软件会要求提供密码和加密方式，双方一致后才能成功连接。连接到服务器后，客户端会在本机构建一个本地Socks5代理（或VPN、透明代理等）。浏览网络时，客户端通过这个Socks5（或其他形式）代理收集网络流量，然后再经混淆加密发送到服务器端，以防网络流量被识别和拦截，反之亦然。

Shadowsocks使用自行设计的协议进行加密通信。[16]加密算法有AES-GCM、ChaCha20-Poly1305、2022-BLAKE3-AES-GCM等，除建立TCP连接外无需握手，每次请求只转发一个连接，无需保持“一直连线”的状态，因此在移动设备上相对较为省电。
所有的流量都经过算法加密，允许自行选择加密算法。

server 端作为最终到外网的转发，client 端作为对各种需要访问外网的本地程序的代理，client 在本地是服务器的角色，对 server 端则是客户端的角色，它监听本地代理端口（1080），然后将请求转发给 server 的端口 8488。因为 client 在本地也是服务器，本地程序将流量发给它。本地程序和 client 之间也要有协议，这个协议就是 socks 协议，因此本地程序或操作系统必须支持 socks 协议才能将流量发送给 client。
但是一些 client 可以以其他的协议与本地程序交换流量。windows 10 似乎不支持 socks 代理，只支持 http 代理。shadowsocks-window 对本地应用程序提供了 http 代理，本地应用程序将流量以 http 的形式发送给 client，然后 client 按正常方式与 server 沟通。本地收集端口是必须的，这就是 shadowsocks-window 服务器编辑 代理端口的作用。而 widnows 网络设置中代理总是被它设置为 http://127.0.0.1:1080.

但是 go ss 不支持 http 代理，只提供 socks 代理，因此 windows 上就没法用全局代理的方式使用命令行的 socks，只能有各自软件自行设置。主要的软件就是浏览器，还有终端shell。shell 不检查系统的代理配置，还是需要每个网络程序自己设置代理，例如 go python 编写的程序，curl。

Firefox 浏览器可以直接设置代理
Chrome 浏览器默认只能使用系统代理，但是 windows 系统默认只支持 http 代理，shadowsocks-windows 支持 http 代理，但是 go ss 只支持 socks 代理
Firefox 支持 socks 代理，但是还要选中 dns 解析
chrome 需要安装 SwitchyOmega(前版本 Proxy SwitchySharp），它支持 socks/http/https 代理。

http 请求分为两个环节：dns使用udp解析域名，得到 ip 地址，再使用 ip 地址进行 tcp 连接通信。关于是在本地解析域名还是在 server 端解析的域名还不是很清楚，都有可能。代理理论是基于 tcp 和 udp 层的，它完全不关心上层传输的是 http，https，还是其他什么类型的流量。完全有可能本地程序对流量不做任何处理，直接转发给 server 端，由 server 端进行 dns 解析，然后 tcp 通信。

shadowsocks-window 不需要关心 dns
go ss 不需要关心 dns，如果需要 启动 dns turnnal -u -udp 
firefox socks 代理选中 dns 域名解析代理

'''
这里问的问题是 HTTP/HTTPS 代理的 DNS 解析如何进行。以下说明与 SwitchyOmega 无关，纯粹基于本人对于网络和代理协议的理解。

对于 HTTP/HTTPS 类型的代理服务器而言，请求的域名会作为 HTTP 协议的一部分直接发往代理服务器，不会在本地进行任何解析操作。也就是说，域名的解析与连接目标服务器，是代理服务器的职责。浏览器本身甚至无须知道最终服务器的 IP 地址。据我所知，此行为无法通过浏览器选项等更改。

也就是说，理论上使用 HTTP/HTTPS 类型的代理服务器时，本地的 DNS 解析、缓存、 hosts 文件等都不使用，与本地设置的 DNS 服务器地址无关。DNS 解析完全在代理服务器上进行。

关于 DNS 污染和特定网络环境问题此处不做解答，但相信 OP 能够从以上说明中推断出具体问题的答案。

socks代理不是，DNS解析和连接目标服务器（IP地址，而非域名）是两个环节，所以有使用远程代理做DNS解析（并作结果）的选项。而http代理接收的是包含域名的网址，不受本地DNS、hosts影响。
'''

curl 既支持 http_proxy，也支持 socks proxy
http proxy 可以设置环境变量 HTTP_PROXY=http://127.0.0.1:1080
也可以在命令行中用选项 --proxy http://127.0.0.1:1080 指定
socks 代理通过 -x socks5h://127.0.0.1:1080 指定

curl.exe 只能使用 windows 网卡网络内的代理
curl 只能使用 wsl 虚拟网卡网络内的代理，不互通

go ss 不能直接连接 justmysocks 的 ss server，因为后者提供的是 AES——256-gcm 加密，而 go ss 只支持 aeaaes-256-gcm 加密。
不管语言、平台的 server 端和 client 端，只要支持相同的加密算法，就可以连接（提供主机、密码、端口）。

ec2 注意开启 socks 的端口 8488 入站

入站 就是 进入的 tcp/udp 链接，dest port = 入站端口，对请求的响应不是出站流量，而是 src port = 出站端口 主动发起的才是出站，默认任何出站端口都是开启的。

curl 和 golang（python）的网络接口读取环境变量，使用代理

set HTTP_PROXY=http://127.0.0.1:1080
set HTTPS_PROXY=http://127.0.0.1:1080

localhost 和 127.0.0.1 登记，localhost 是 127.0.0.1 的域名，localhost 被解析为 127.0.0.1

export HTTP_PROXY=http://localhost:1080
export HTTPS_PROXY=http://localhost:1080

HTTP_PROXY 的意思是对 http:// 协议发送到这个地址，HTTPS_PROXY 的意思是对 https:// 协议发送到这个地址。如果系统只有一个 http 代理，两个 HTTP_PROXY 和 HTTPS_PROXY 都发送到这个地址，这与 socks 客户端支持 https 协议不是一件事，如果本地 socks 支持 https 则上面两个应该写为：

export HTTP_PROXY=https://localhost:1083
export HTTPS_PROXY=https://localhost:1083
