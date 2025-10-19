# FizzySteamworks/FizzyFacepunch Transport

FizzySteamworks 是用于 Mirror 的一个 Steam P2P transport，它利用 Steam 的 P2P 服务来直接连接或转发你的连接到另一个 player。FizzySteamworks 是基于 Steamworks.Net 包装器。

## Features

- Multiple Customizable Channels：你可以定制 transport 中的 channels，无论你是想要1个还是5个不可靠或者可靠的 channels（最好保留 channel 0 为可靠的）
- Steam Nat Punching & Relay：transport 将会使用 Steam 来完成 Nat 穿透到你的 destination，并且如果它不工作，steam 的转发服务器（relay Server）将被用来确保你总是可以连接
- 不需要 Code Changes：如果你已经使用 Mirror，你只需要直接切换到这个 transport（可能需要添加你的 steam App ID 在你的 build 中），而所有事情应该和其他 Mirror Transport 一样工作。It Just Works

FizzyFacepunch 和 FizzySteamworks 相似，只是基于 Facepunch.Steamworks 包装器。

![FizzySteamworks](../../Image/FizzySteamworks.png)

![FizzyFacepunch](../../Image/FizzyFacepunch.png)

