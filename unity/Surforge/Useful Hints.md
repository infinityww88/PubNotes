# Useful Hints

1. 一般到特殊。首先创建 texture 的整体 layout，然后添加细节是非常高效的。

2. 为眼睛提供休息区域。尽管 Surforge 允许你闪电般迅速地使用细节填充 texture（豪横，一般软件添加大量细节是十分耗时的），让一些纹理区域保持简单是非常好的。还有在真实世界中，小的细节倾向于围绕在大的特征周围，很少出现在空白区域的中间。

3. 当工作时，在不同的 skyboxes 之间切换。这允许你得到材质属性更准确的 idea。

4. Texture 高质量 UVs 的模型更加容易。尽可能使用使用叠加（重叠），小心对齐的，完美对称的 UV islands。Surforge 有很多 UV islands 相关的工具，可以加速你的 workflow。

5. Surforge 允许在 material sets 之间迅速切换，以及同事操作多个 material sets，因此使用它们就是了。尝试不同的 color schemes，而不是在一个 scheme 中实现所有的 efforts。在 material sets 中滚动，洗牌 set 中的 materials，使用 duplicate material set 按钮创建副本。你可以在任何时间在它们之间切换，比较并选择最好的。Surforge material system 的核心本质是一个复杂的具有大量参数的 shader。所有 material set 中的 materials 都是使用这个 shader，因此每个 material 只是包含这个 shader 不同参数的数据资源而已。

6. copy/paste 与 向上移动并缩小 poly lasso objects 的组合是非常高效的。只需要一个 Ctrl+C/Ctrl+V 的组合，按几次 Up Arrow 和 Left Arrow 键，你就可以得到好看的 border 效果。使用 Split tool cutting detail 并改变结果 parts 的垂直位置同样非常高效。

7. 要添加令人印象深刻的细节到 sci-fi 纹理上，使用 Greebles tool 填充一些矩形区域，使用重叠的 Poly Lasso panels 保卫它们，并且使用 Add Detail tool 在 greebles 上面放置一些 detail。使用 Poly Lasso tool 选择 tube profiles 添加一些 tubes 和 cables。

8. 对于 sci-fi 纹理，不要忘记添加带有 emission 的细节。只需要使用 Add Detail tool 设置一些小的 objects，选择它们并按下 9 或 0 键为它们赋予 emission mask。

9. 对于奇幻纹理 fantasy textures，你可能想要在模型的 border 散布一些装饰。填充 UV island，用作 Warp shape。创建一些凯尔特装饰物或者其他细节，并使用 repeated warp 功能，来讲它们无缝地散布到 UV island border 周围。然后使用 convex gem poly lasso profile 添加一些体积化外观宝石。这对于快速 texturing 多个 fantasy game assets 非常高效。

10. 自由地使用 Unity transform tools 操作 Poly Lasso 和 Add Detail 创建的 objects（它们只是简单的具有 mesh 的 gameobjects）。你可以选择一个或多个 objects，复制粘贴，以及改变它们的的 X 或 Z 的 scale 为 -1 来得到对称的副本。它们都会被正确地渲染。

11. 当自己的 textures 和 Surforge materials 一起使用时，不要忘记设置它们的 compression 为 ”automatic turecolor“。你可以在一个 project 中使用不同分辨率的 textures。因为是 GPU based 的，Surforge 将会正确的缩放适配它们。通过使用 specular 和 glossiness 特征提取和内置的 noise，Surforge 即使对低分辨率的纹理也可以添加清晰的细节。还有，你可以改变 Surforge materials 中纹理的 tiling/offset 属性，如果使用 seamless 纹理的话。所有 Surforge 内置的纹理都是 seamless 的，并且很好地处理了 tiling。

12. 因为 Surforge textures 是完全基于 3D 的，作为额外奖励，你可以得到完美的高度图。你可以将它用在你的高级 shaders 中，以及 DirectX 11 的 tessellation（曲面细分）。

13. Surforge 有非常方便的截屏工具，因此展示你的作品！轻松地得到你的 model，maps，和 materials 的预览。不会浪费时间或打断工作，只需要按下一个键，Surforge 就会保存具有良好 layout 的 screenshot。

