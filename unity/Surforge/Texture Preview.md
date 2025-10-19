# Texture Previewtuning

预览选择的 model 的 texture 的 viewport，快速切换 set 中的 materials，materials 拖放，复制/粘贴和交互 materials。

要改变用于 texture previewing 的 model，选择 Render toolbar，并拖放想要的 mesh 到 “Open Model” 字段中。

Texture preview 导航操作:

1. Reset camera (Double Click).

   双击窗口，重置 Texture Preview 相机到默认位置

2. Rotate (Left Button)

   左键拖拽进行选择

3. Pan (Middle Button)

   中间拖拽进行平移

4. Zoom (Scroll or Alt + Right Button).

   滚轮，或者 Alt + 右键，Zoom 视角

5. Select material under cursor (Ctrl).

   设置 cursor 下面的 texture area 的 material 为当前选择的 material。被选择的 material 的属性展示在 Material Editor，并准备好进行调整。你还可以在 Material Editor 顶部的 dropdown menu 中选择 material。

6. Copy material under the cursor (Ctrl + C).

   复制 cursor 下面的 material

7. Paste material under the cursor (Ctrl + V).

   粘贴复制的 material 到 cursor 下面的 material

8. Swap material under the cursor with last copied (Ctrl + X).

   将 cursor 下面的 material 和最后一次复制的 material 进行交互。对于在 material set 中整理你的 materials 非常方便。

9. Cycle material under cursor (Ctrl + Scroll).

   在一个 cycle 中，改变 cursor 下面的 material 为其他 material sets 中的不同 material。Material 是通过 Mask（材质集合中的索引）赋予 Surforge 创建的 objects 的。这个操作不改变 objects 的 material mask，而是改变 Material Set。类似调色板技术。对于实时地快速找到适合 texture 的 color 和 material scheme 非常好。

10. Cycle dirts (Shift + Scroll).

    改变当前 material set 的 dirt settings 为 cycle material set 下一个 set 的 dirt settings。快速选择适合 texture 的 dirt style。
