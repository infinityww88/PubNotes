# ServerManager

​​ServerManager 是一个核心组件，负责处理所有与服务器相关的数据和操作。​​

它主要承担以下功能：

- ​​维护服务器端 networked objects 的信息并处理相关操作​​
- ​​追踪所有已连接的客户端（包括已认证和未认证的客户端）​​
- ​​监控客户端超时情况，并自动断开无响应的客户端连接​

​​ServerManager 可直接用于启动/停止 FishNet 服务器，同时支持监控服务器状态并向客户端发送广播消息。​

## Settings

### SyncType Rate

这是 SyncTypes 的默认发送速率。将它设置为 0f 会在每个 tick 更新。

这个值可以为独立的 SyncTypes 覆盖。

### Spawn Packing

该设置决定了在生成（Spawn）消息中发送时，变换（Transform）属性的打包优化程度。如果生成的 transform 位置出现轻微偏移，适当降低打包精度可能会有所改善。

可以为位置（Position）、旋转（Rotation）和缩放（Scale）分别独立调整这些参数。

### Change Frame Rate

开启后，这会改变 server only 模式的 frame rate 限制。

帧率（Frame Rate）是指仅服务器运行时采用的帧率设置。客户端帧率可通过 ClientManager 单独配置。当服务器与客户端同时运行时，系统将自动采用两者中的较高帧率值。​

### Start On Headless

开启后，当在 server build(headless) 加载后，FishNet 会自动启动 server，

### Remote Client Timeout

当超过这个时间阈值未响应时，server 是否应该断开 clients。这个功能可以 disable，在 development/release enable，在 release only enable。

开启后显示 Timeout，决定 client 多长时间不响应被认为是未响应的，应该断开。

### Share Ids

​​启用后​​，客户端将能感知游戏内其他玩家的存在及其拥有的对象。但需注意：只有当其他客户端的对象对本地客户端可见时（例如通过观察者系统），这些对象信息才会被同步。客户端ID不属于敏感信息，但保持此选项开启会略微增加网络带宽消耗。

### Authenticator

此处用于指定要使用的身份验证器。若留空，则客户端无需特殊身份验证即可加入服务器。决定 client 如何被 server 校验。

### Allow Predicted Spawning

该选项允许为预制体和场景对象配置预测生成（Predicted Spawning）功能。

通过此设置，你无需逐个修改对象参数即可全局启用或禁用预测生成功能。

该值也支持运行时动态调整，但若在运行时修改，必须同步更新客户端配置——否则客户端尝试使用未启用的功能时可能会被踢出游戏。

- ​​Reserved Object Ids

  指为每个客户端在预测生成（Predicted Spawning）时预分配的对象ID数量。客户端初始将获得指定数量的ID，并在服务器验证其预测生成请求后获取新的ID。

​  ​举例说明​​：若该值设为15，且一个网络延迟为100毫秒的客户端在同一帧内提交了3个预测生成请求，则在服务器返回3个新ID（约50毫秒后）之前，该客户端仅剩12次预测生成可用额度。


