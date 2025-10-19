# Sprites

一旦你导入一些 Sprites，你可以通过拖放它们到 Hierarchy window 来创建一个 animation。

1. 选择 Sprites
2. 拖放它们到 Hierarchy window
3. 使用对话框来选择将 animation 保存在哪里，它的名字是什么
4. 从 scene 中删除创建的 object
5. 删除它创建的 Animator Controller（因为 Animancer 不需要它）

它创建的第三个东西就是保护这些 Sprites 的 animation。

![sprites-to-animation](../../../Image/sprites-to-animation.gif)

Animancer 就像 Unity Animator Controller 系统播放相同的 Animation Clips，因此任何有关创建 Sprite animations 的官方 Unity tutorials 仍然是相关的。

## Automation

上面的 workflow 是有点繁琐，因此 Animancer 开发了一些工具使它更加容易。

其中一个 tool 让你容易地基于 Sprite 名字生成动画：

![generate-animations-by-sprite-name](../../../Image/generate-animations-by-sprite-name.gif)

它基于移除默认数字的 Sprites 的名字进行分组

![SpriteAnimation](../../../Image/SpriteAnimation.png)
