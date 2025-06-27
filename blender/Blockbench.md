Blockbench Edit 和 Paint 模式下，模型上不同颜色的部分不是随机渲染的，每个相同颜色的区域块是一个 uv island，通过颜色可以在 uv 和 face 进行对应。

![](image/uv_island1.png)
![](image/uv_island2.png)

将 Blockbench 的 key_binding 设置为 blender，就可以让 blockbench 的编辑基本与 blender 一致。还可以通过 alt + 左键 选择循环的 face 或 edge。

![](image/blender_key_binding.png)

此外 Blockbench 为所有功能都提供了快捷键绑定，包括诸如文件导出这样的功能，这可以加快与 Unity 交互迭代的速度。

![](image/key_binding.png)

工具技术限制在 Blockbench + Gimp + Blender + Unity，不再扩展，专注精通它们的细节功能。例如 blender gimp 还有很多基础功能还没有熟悉甚至知道，而它们对提供工作效率有很大辅助。例如 gimp 的选区、滤镜、图层蒙版等功能，blender 菜单中的基本功能还没有全部尝试一遍，各种 modifier 还没有熟悉。Unity NavMesh 的 OffMeshLink 还没有尝试。

例如，Blender 可以根据选中的 mesh 生成 wireframe 模型，这些都是在菜单中的基础功能，在某些情况下非常方便。

![](image/blender_wireframe.png)

Blender 和 Unity 支持非共面的 quad（Unity 应该是在导入的时候自动进行三角化），即四边形的点不共面。但是 Blockbench 和 Godot 都不支持。将存在非共面 quad 的模型导入到 Blockbench 和 Godot 是模型出现破缺的原因。解决办法是在 Blender 中选择所有的面，然后在 Face 菜单中选择 Triangulate Faces，将所有面三角化，这样再导入到 Blockbench 和 Godot 中就不会出现破损了。还可以再选择 Tris to Quads，将共面的三角面合并为 Quad，这样会生成更美观更合理的 wireframe，导入到 BB 和 GD 中仍然不会有问题。

Blockbench 还在更新，值得投资。Blockbench 作为主力，Blender 和 Gimp 作为辅助。Gimp 可以为纹理绘制和处理提供更高级的功能。Blender 可以处理在 Blockbench 不方便建模的模型。另外还可以在 Blender 中完全创建模型，只将 Blockbench 作为 uv 展开和绘制的工具。这样的好处包括：

- Blender 包含更强大更流畅的建模功能
- Blender 文件可以直接保存到 Unity 中，不需要额外导出为 Obj 或 Fbx，作为中间产物
- Blender 中可以进行骨骼蒙皮和 IK 动画

不要再 Blockbench 或 Blender 中创建完全的游戏世界甚至模型。只创建组件，然后在 Unity 中进行组装，查看最终效果。因为很多物体包含很多重复（对称或多重）的部件，这些部件只需要创建一次，然后 Unity 中重复就可以。如果再 BB 或 Blender 中创建完整的模型，会导致 mesh 中包含重复的面，还会导致需要重复对这些组件绘制纹理，而它们本来只需要绘制一次。还有模型要尽量拆分成子部件，这样每个部件都足够简单，便于建模和绘制纹理，还会带来再游戏游戏方便替换的好处，例如对物体进行升级，或生成变体等等。

总之在 BB 或 Blender 中只创建部件，将每个部件导入到 Unity 中，在 Unity 中组装查看效果。如果比例不对，就回到 BB 或 Blender 中调整，然后重新导入，如此迭代。注意不要再 Unity 中进行缩放，因为这会导致 pixel 纹理的 block 不一致。

这样看来还是在 Blender 中创建更方便，因为它不需要导出为 obj 或 fbx 作为中转，而且建模功能更强大。另外 UModeler 在 Unity 中直接建模则更进一步方便。但是在 Unity 可以直接导入 Blend 文件后，这个优势不再那么明显了。正如刚才说的，建模只创建部件，在 Unity 中组装。但是仍然不失为一种选项，看你自己的选择。

可以先尝试在 Blender 中建模部件，在 Unity 中组装，最后将所有部件导入到 Blockbench 中统一绘制纹理。

也可以尝试 UModeler，UModeler 也可以导出 obj。但是 UModeler X 就不必了，它提供的高级功能在 Blender 中都包含，而且它主要用途是创建高面数模型，跟 lowpoly 目标不一致，对于低面数模型，UModeler 足够用了。如果是创建高面数模型，它节省下来的导入导出时间相比于模型创建本身已经不值一提了。创建高面数模型是非常费时费力的。还有最重要一点，UModeler X 会显著拖累 Unity 进入 PlayMode 的速度。但是 UModeler 则没有这个问题，即使安装了 UModeler，也不会明显影响 Unity 进入 PlayMode 的速度。

而 Unity 迭代速度至关重要，因此使用外部软件的就不要用 Unity 插件，能自己实现的就不要安装第三方包。因此还是不要用 UModeler。Blender 的编辑功能非常强大，而且 UModeler 节省下来的时间已经不显著了。

无论是在 Blockbench 还是在 Blender 中创建部件，都需要先创建标准，例如标准立方体，确定游戏世界的 unit 和 pixel block size 的标准，然后一切根据这些标准来创建。

vscode 中文输入标点符合，会产生两个重复的标点。在 settings 中关闭 editor.experimentalEditContextEnabled。
