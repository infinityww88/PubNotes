# Animation

Textual animation system 可以创建 visual effects，例如 movement，blending，fading。

## Animation styles

可以应用动画到 styles，动画 offset 可以创建 widget 移动动画，动画 opacity 可以创建 fading 效果。

Apps 和 widgets 都有 animate 方法，它会动画这些 objects 的属性。此外，styles objects 有一个相同的 animate 方法，可以活动 styles。

```py
self.box.styles.animate("opacity", value=0.0, duration=2.0, delay=5.0)
```

## Easing functions

可用 textual easing 查看可用 ease method。animate 方法可以传递一个 easing 参数。默认 ease 是 in_out_cubic.

## Completion callbacks

可以通过 on_complete 参数向 animator 传递一个 callable。Textual 在 animation 完成时运行 callable。

