# Network Transform Child

同步具有 Network Transform component 的 gameobject 的 child game object 的 position 和 rotation。你应该在需要同步独立移动一个 Networked gameobject 的 child object 的情景使用这个组件。

要使用这个 Network Transform Child 组件，附加它到和 Network Transform 相同的 gameobject，并使用 Target 字段来定义哪个 child gameobject 来应用这个组件的设置。你可以在一个 parent gameobject 上有多个 Network Transform Child components。

![NetworkTransformChild](../../Image/NetworkTransformChild.png)

你可以修改 Compress Rotation 在同步 rotation 时保存一些带宽。

Network Sync Interval 指定同步的速率（seconds）。

这个组件考虑 authority，因此 local player gameobjects（具有 local authority）从 client 到 server 同步它们的 position，然后由 server 同步到其他 clients。其他 gameobjects（具有 server authority）从 server 到 clients 同步它们的 position。
