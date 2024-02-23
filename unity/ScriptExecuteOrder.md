# Script Execution Order

Script Execution Order 设置指定 Unity 调用不同 MonoBehaviour 类的事件函数 event functions 的相对顺序。以类 class(MonoBehaviour) 为单位指定。

例如可以指定 Unity 运行 MoveForward MonoBehaviour 的 event function 之前先运行 Rotation MonoBehaviour 的 event function。

Order 对每个 event function 分别应用。因此 Unity 在一帧中按照指定的顺序调用 Awake functions，之后，按照相同的顺序对 active GameObjects 每一帧调用 Update functions。

如果挂载多个 script types 到多个 GameObjects，script execution order 指示一个类型的所有脚本在另一个类型的所有脚本之前执行，而不是按照 GameObject 的顺序执行。

在 Setting panel，使用 + 按钮添加脚本，选择一个 MonoBehaviour class 名字。使用 - 按钮移除一项。

要指定执行顺序，在list 中拖拽 item 到希望的位置。指定的数值表示相对顺序。Unity 从上到下执行每个 item（从最小数值的 class 到最大数值的 class 执行）。对任何没有指定顺序的 class，Unity 在 Default Time 中执行，它在所有负数 class 都执行完，所有正数 class 还未开始执行前执行。

顺序数值是任意的，没有任何实际物理意义。Editor 存储这些值到脚本的元数据中。可以在数值之间留下空隙以为将来使用。

指定的执行顺序不影响使用 RuntimeInitializeOnLoadMethod 属性标记的函数的执行顺序，不能为 runtime initialization 指定任何顺序。

很多第三方脚本（例如 Quick Outline）都是用静态变量缓存数据。如果禁止 Editor Domain Reload，静态数据会在 PlayMode 和 EditorMode 之前保持，造成各种意料之外的问题。因此，如果禁止了 Editor Domain Reload，一旦出现一些奇怪的问题，先尝试开启 Editor Domain Reload，看是否是静态数据导致的，如果不是再排除其他方面的问题。

