# DOTween

Kill(bool complete) complete 指示是否立即完成动画：

- true：立即完成动画，动画属性立即变成 endvalue，并且调用 OnComplete 回调
- false：直接停止动画，动画属性保持在当前的 value，并且不调用 OnComplete 回调

无论是 kill 动画还是动画 complete，都会调用 OnKill 回调。

Complete() 立即完成动画，并调用 OnComplete 回调函数。
