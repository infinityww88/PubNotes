# DOTween

Kill(bool complete) complete 指示是否立即完成动画：

- true：立即完成动画，动画属性立即变成 endvalue，并且调用 OnComplete 回调
- false：直接停止动画，动画属性保持在当前的 value，并且不调用 OnComplete 回调

无论是 kill 动画还是动画 complete，都会调用 OnKill 回调。

Complete() 立即完成动画，并调用 OnComplete 回调函数。

创建的每个 Tween 都要注意 SetTarget，使 Tween 跟 target GameObject 一起销毁，必要时可以在 OnDestroy 时主动 Kill(target)。DOTween 会创建一个“全局” not destroy on load 的 gameobject 来保存所有 Tween。如果不及时销毁 Tween，它们将会跨 Scene 执行，而产生各种意外的 bug。尤其是任何设计静态全局的变量（例如 UnityEngine.cursor.visible）都必须考虑 Scene 切换的问题。
