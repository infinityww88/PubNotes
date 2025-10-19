使用 Child-Of Constraint 可以动画期间改变一个 joint/transform 的 parent。这可以用于 pick-up，throwing，或者 gun reloading 动画。

由于 Unity 使用 Vector3 用作 scaling，当 parent 被缩放而 child 被旋转时，技术上不可能为 Child-Of constraint 正确扭曲变形 distort 一个 joint/transform。这就是为什么我们决定当新的 parent 的 scale 改变时，scale 不会更新。

每个 joint/transform 只能添加一个 Child-Of constraint。

## Dealing With Spaces

无论何时，任何 object（joint/transform）的 parent 被 Child-Of constraint 改变的时候，需要记住这还会改变 object 的 local position 和 rotation 求值的空间。

当在 animation 中改变 parent（或者通过 keying Parent 或者通过 IK Pinning 属性）时，object 的 position/rotation 空间也将会在这帧改变。这样有必要在同一帧为 object 新的 position 和 rotation value 添加 key。如果不这样做，之前 parent 空间的 position/rotation 值将会被用在新的 parent 空间，这可能产生不正确的结果。

动画片段可以动画任何脚本的属性，包括 transform.parent，在某一帧改变 transform.parent 的值就在动画中改变了 object 的 parent。

还有必要为 object 在之前 parent space 的 position/rotation 创建一个 key，在 parent 被改变的前一帧。没有这个 key，动画曲线将会平滑地从最后一个 position/rotation key（它在之前 parent 的 space）向新 parent 空间的 position/rotation 插值。这将导致插值的 value 既不在之前的 parent space，也不在新的 parent space。

好消息是 UMotion 在创建一个新的 parent key 时会自动创建这些 keys。但是这需要由你保持这些值更新。这意味着无论何时你移动或删除 parent key，你需要相应移动或删除 position/rotation keys。

### Updating Position/Rotation Keys

当你想要在 parent 被 keyed 的那帧（或前一帧）更新 object 的 position/rotation，还有必要相应更新其他空间的 keys。因此，右键点击 Parent 或 IK Pinned property，并点击 "Update Position and Rotation Keys"。这会自动更新在其他空间的相应的 position/rotation keys。如果 keys 已经被删除，它们将会被重新创建。这个 menu item 只在 Parent 或 IK Pinned property 有一个 key 的那帧或前一帧可见。

TODO
