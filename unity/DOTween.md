# DOTween

Kill(bool complete) complete 指示是否立即完成动画：

- true：立即完成动画，动画属性立即变成 endvalue，并且调用 OnComplete 回调
- false：直接停止动画，动画属性保持在当前的 value，并且不调用 OnComplete 回调

无论是 kill 动画还是动画 complete，都会调用 OnKill 回调。

Complete() 立即完成动画，并调用 OnComplete 回调函数。

Sequence 中包含的 Tweener 必须在 Sequence 开始运行之前添加好，Sequence 开始之后就不能再添加新的 Tweener 了。

被添加到 Sequence 的 Tweener 被 Sequence 完全控制，对它进行 Kill 等 Control 操作都没有任何效果，就好像它们在 Sequence 外面不存在，只存在于 Sequence 内部一样。每个 Tweener 在 Sequence 中有意义的东西都正常运行，例如自身的回调、循环等。

任何嵌套的 Tweener/Sequence 在添加到 Sequence 之前必须被完全创建，因为之后它们将被 Locked。Delays 和 非无限的 Loops 在 nested tweens 都能正常工作。

Sequence 和 Tweener 的 Target 都保持它们各自 Set 的 target。

Tweener 被 Sequence 保存管理，每个 Tweener 可以单独 Complete，但是所有 Tweener 要等到 Sequence Kill 时才被 Kill。

Tween 动画需要一个 start 值，一个 end 值。DOTween 动画一个特点是创建 Tweener 时只提供其中一个，另一个总使用动画属性的当前值。例如通常 To 动画只提供 endValue，startValue 使用属性的当前值。From 动画只提供 startValue，endValue 使用属性的当前值。这也导致了 startValue 和 endValue 只在动画过程中被保存。一旦动画结束后再想重新播放动画（rewind 或 restart）就不可能了，属性的当前值被设置为了 End Value，此后再次开始动画时，这个值就变成了动画的当前值。因此 Restart() 和 Rewind() 只在动画过程中有效，一旦动画结束再调用它们，看不见任何动画，并不是没有创建 tweener，tweener 正常创建，而是新的 tweener 的 startValue 和 endValue 是相同值。PlayBackwards 也是一样，只要是需要 startValue 和 endValue，就只能在动画过程中有效。

Rewind 和 Restart 是相似的，都是重新开始动画，只是 Rewind 将属性重置到 startValue 的同时还 Pause，后面需要显式调用 Play 播放动画，而 Restart 则是重置后立即播放动画。无论 Rewind 还是 Restart 都会触发 OnRewind。

Sequence 的 PlayBackwards 可以对整体 Sequence 动画正确地反向播放：正在播放的动画立即 backward，tween 之间的 interval 被保持，然后对已经播放完毕的 tween 依次 backward。

Tween 回调

- OnStart
- OnComplete(End)
- OnRewind
- OnKill

Nested tweens 的 callbacks 仍然可以按照正确的顺序工作。

DOTween 会创建一个“全局” not destroy on load 的 gameobject 来保存所有 Tween。如果不及时销毁 Tween，它们将会跨 Scene 执行，而产生各种意外的 bug。尤其是任何设计静态全局的变量（例如 UnityEngine.cursor.visible）都必须考虑 Scene 切换的问题。因此要注意 kill tweens。

autoKill = true 使得 tween 在 complete 时自动销毁，而 autoKill = false 使得 tween 在 complete 时仍然保留在内存中，之后可以重新 restart/rewind。

Tween Control Methods:

- Complete
- Flip
- Goto
- Kill
- Play
- PlayBackwards
- Restart
- Rewind
- TogglePause

DOTween 提供了 Path 动画，支持直线、贝塞尔曲线。

Sequence Insert 可以在任意位置插入 Tween，不仅仅限制在当前已经定义的时间段内。Join 在最后添加的 Tween 的开始位置再插入一个 Tween，使它们可以一起播放。

DOTween 还支持多段动画，以数组的形式为每个 segment 提供 endValue 和 duration。

DOTween 为 TextMeshPro 动画提供支持。

AutoKill 是让 Tween 在播放 complete 后自动 kill（否则可以被重复利用，例如 restart or rewind），而不是让 Tween 随着 target 销毁而销毁。

Tween 和 GameObject/Component 是两个独立的东西，声明周期默认也是没有关联的，有可能 GameObject/Component 还存在，但是 Tween 销毁（kill，这是通常正确的行为），也有可能 Tween 还在运行，而 CameObject/Component 已经销毁（这是使用 DOTween 最需要注意的错误）。

DOTween 有很多 static 方法可以通过指定一个 filter 操作一组 Tween（Play、Pause、Resume、Kill）。这个 filter 是一个 id 或 target。即 DOTween 有两种方法为 tween 指定一个唯一标识：id 和 target。这个两个方法从文档上看没有太大区别，可能是开发过程中造成的历史问题（为了兼容性而同时存在两种方法）。两个标识符的类型都是 object。唯一的区别是：SetId 只能通过手动调用设置的，SetTarget 既可以通过手动调用设置，另外 shortcut 方法也会调用 SetTarget 将组件设置为 tween 的 target。另外如果使用 int 或 string 作为标识符，则 id 比 target 要快。仅此如果没有特殊需求，使用 SetId。在使用带有 filter 的 static 方法时，filter 传递 id 或 target 都可以。

SetId/SetTarget 是两个可互换的等价方法。id 或 target 是 object 类型，因此和 GameObject/Component 没有关系。为 Tween 设置 target 只是为找到它们提供了一种方法，不会使它们随着操作的 GameObject/Component 销毁而销毁，这必须显式维护：

- 在 Component 的 OnDestroy 中 Kill，直接调用 Tween.Kill() 或者 DOTween.Kill(idOrTarget)
- SetLink(GameObject target, LinkBehaviour linkBehaviour = LinkBehaviour.KillOnDestroy) 将 Tween 和 GameObject 连接在一起
- 开启 safeMode，这是个全局属性，开启后，DOTween 会自动检测 tween 的 target 是否被销毁

