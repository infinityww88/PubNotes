# Smooth Sync for Unity

执行 interpolation 和 extrapolation，以使 gameobjects 在网络上平滑而精确的移动。高度可配置，只发送你需要的。可选地压缩 floats 以进一步降低带宽。

依赖你的游戏的需求，可定制 interpolation 和 extrapolation。

Comes with a fully functional example scene。提供全部 source code，因此可以查看所有细节。Unity 可以运行的平台都支持。

## Mirror 用法

1. 将 SmoothSync script 放在任何你想要 smooth 的 parent networked object 上面
2. 它将会自动 sync 它所在的 object。要 sync 一个 child object，你必须在 parent gameobject 上有两个 SmoothSync 实例。设置其中一个的 childObjectToSync 指向你想要 sync 的 child，然后另一个保留为空来 sync parent。你不能同步 children 而不同步 parent
3. 它现在在网络上就开始同步

## 工作原理

不想 Unity 提供的 NetworkTransform 脚本，SmoothSync 脚本存储一个 network States 列表来在其间插值。这允许一个更精确，更平滑的 synced objects 的表示。

## 你可能需要的 Methods

- SmoothSync.teleport()：用于 teleport（瞬移）你的 objects，用于诸如 respawning 的情景，使得它们不会插值
- SmoothSync.forceStateSendNextFixedUpdate()：用于你有一个很低的 send rate，但是想在 send rate 其间手动发送一个 transform
- SmoothSync.clearBuffer()：如果你改变了 object 的 network owner，你将需要在所有的 object instance 上手动调用这个方法。或者，选中 Smooth Authority Changes 来自动和平滑地处理 authority changes。当使用 Mirror，你必须在 changing authority 之后在 server 上调用 AssignAuthorityCallback() 
- SmoothSync.validateStateMethod：你必须设置一个 validation 方法来检查 incoming States 以查看可能发生的作弊
