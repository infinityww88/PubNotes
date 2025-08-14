# Offline Rigidbodies

有时你会想要 player 能够和 non-networked rigidbodies 交互，这需要一个特殊组件。

当使用 prediction 时，如果在游戏中有一个不使用网络同步 rigidbody object，它必须包含一个 OfflineRigidbody 组件。
