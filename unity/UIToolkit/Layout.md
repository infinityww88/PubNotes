# UIToolkit Layout

UIToolkit 的坐标系：原点在屏幕左上角，x 轴向右，y 轴向下。

Input/InputSystem 的指针设备坐标系：原点在屏幕左下角，x 轴向右，y 轴向下。

将 pointer 坐标转化为 UIToolkit Document 坐标：

```C#
var t = Touch.activeTouches[0];
var pointerPos = t.screenPosition;
var uiPos = pointerPos;
uiPos.y = Screen.height - uiPos.y;
```

元素默认区域 box 包含 margin，border，padding，contentRect。各种坐标计算方法都是基于这个 box 矩形，除非显式指定 contentRect。

VisualElement.worldBound 返回 VisualElement 在 UI Document Panel 中的全局（world）矩形（不管嵌套层级）。
这个矩形是 VisualElement 的 box 区域，包括 margin，padding，border，contentRect。

VisualElement.contentRect 是 VisualElement 的内容区域（子元素容器，不包含 margin，padding，border）相对元素 box 的局部 rect，即在 worldBound 中的局部 rect。

VisualElement.WorldToLocal(worldPos) 将 UI Document Panel 中的全局坐标转换为 VisualElement Box 的 local 坐标。

VisualElement.LocalToWorld(localPos) 将 VisualElement Box 的 local 坐标（相对于  margin box）转化为 UI Document Panel 的全局坐标。

VisualElement.ContainsPoint(localPos) 判断的是 local pos 是否在 contentRect 中。注意 contentRect 是相对于元素 box 的矩形，而不是相对于 content 区域的自身 rect，其左上角位置不一定是 (0, 0)，如果 margin，border，padding 不为 0 的话。

要判断 pointer 位置是否在元素的 content rect 中一个简单的办法是在元素中嵌入一个没有 margin、border、padding，且 grow = 1 的子元素，使子元素完全填充元素的 content rect，然后调用子元素的 ContainsPoint。

无论如何，运行时，屏幕的分辨率是确定不变的，也是最终 UI 输出的目的地。PanelSetting 设置的各种 reference，scaleMode 等等都是在确定，在满足指定的要求的情况下，屏幕像素和 UI 坐标的比例因子，scaleFactor，即一个屏幕像素对应多少 UI Document Panel 坐标单位，或者 UI Document Panel 坐标单位对应一个屏幕像素。这个 scaleFactor 要根据多种模式以及每种模式下多种因素来计算。

VisualElement 没有将屏幕坐标转换为 UIDocument Panel 坐标的函数，因为它们在虚拟坐标系中工作。VisualElement 中的 World 坐标指的是 UIDocument Panel 坐标（左上角为原点）。

如果要将屏幕坐标（例如 pointer 点击屏幕的位置）转化为 UI Document Panel 坐标系，使用 RuntimePanelUtils.ScreenToPanel(VisualElement.panel, screenPos)。注意这里的 screenPos 仍然需要手动将 y 值转化为左上角为原点的坐标系（Screen.height - pos.y）。VisualElement 的 panel 引用显示这个元素的 UI Panel，即一个 UIDocument 在运行时生成的 Panel。同一个 UIDocument 中的每个元素都引用相同的 panel。因此直接使用 UIDocument.rootVisualElement.panel 即可。它总是转化为 UIDocument 的 world 坐标。转换为 world 坐标之后，后续就可以使用 VisualElement 的各种坐标系转换函数了。

RuntimePanelUtils.ScreenToPanel 主要工作就是计算屏幕像素到 PanelSetting 定义的虚拟坐标系的比例因子。

