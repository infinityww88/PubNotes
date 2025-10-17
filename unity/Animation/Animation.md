一般 Animation Clip 对属性的引用是：```./child0/child1.attribute```。这类似于 Unix 文件路径。

对于 root GameObject，操作它的属性视为 ```..attribute```。因为 root GameObject总是记录为 ```.```，因此这个动画片段如果只操作 root GameObject 的属性，那么即使将这个 clip 用于另一个具有不同名字的 GameObject 也没有问题。

但是对于下级 GameObject 的属性，就必须严格按照 GameObject 名字的路径记录。如果想将在一个 GameObject 记录的 Clip 用于另一个 GameObject，那么后者必须具有和前者一样的，在 Clip 中记录的 GameObject 路径。例如如果 Clip 记录了 ```./child0/child1.attribute``` 的动画数据（动画曲线），那么重用这个 Clip 的 GameObject 下面必须也具有 child0 和 child0/child1 两个 GameObject。否则，播放 Clip 时，动画系统就会找不到 Clip 中动画曲线对应的 GameObject。对于找不到 target 的动画曲线，会被动画系统忽略。注意，root GameObject 的名字可以是不同的，因为它们的属性在 Clip 内部都记录为 ```.``` 的属性。

Unity 创建的动画片段，可以动画以下属性：

- GameObjects 的 position，rotation，scale
- 组件的属性，例如 material color，light intensity，sound volume
- 自己脚本的属性，包括 float，integer，enum，vector，boolean
- event：调用你自己脚本中的函数的时间点

Unity Animation window 可以预览、创建、修改关联到 GameObject 的 animation clips。还可以使用 Animation window 为 animation clip 添加 Animation Events。Animation Event 在一个指定时间点调用一个函数。。