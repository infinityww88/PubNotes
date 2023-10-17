# PanelSettings

定义一个 Panel Settings asset，其在运行时实例化一个 panel。Panel 使 Unity 可以在 Game view 中显示一个 UXML 文件定义的 UI。

## 属性

- bool clearColor

  panel 渲染之前是否清空 color buffer。

- bool clearDepthStencil

  panel 渲染前是否清空 depth/stencil buffer。

- Color colorClearValue

  用于清空 color buffer 的 color。

- float depthColorValue

  用于清空 depth/stencil buffer 的 depth。

- DynamicAtlasSettings dynamicAtlasSettings

  dynamic atlas 的设置。

- float fallbackDpi

  当 Unity 不能确定 screen DPI 时使用的 DPI。

- float match

  当缩放 panel area 时，Unity 使用 width，height 还是使用二者的一个混合，作为参考。

- float referenceDpi

  UI 设计用于的 DPI。

  当 scaleMode 设置为 ConstantPhysicalSize 时，Unity 比较这个值和实际的 screen DPI，然后相应在 GameView 中缩放 UI。

  如果 Unity 不能确定屏幕的 DPI，则使用 fallbackDpi。

- Vector2Int referenceResolution

  UI 设计用于的 Resolution（分辨率）。

  如果 screen Resolution 比 reference Resolution 更大，Unity 在 GameView 中放大 UI。反之，Unity 缩小 UI。

  Unity 根据 PanelSettings.screenMatchMode 缩放 UI。

- float referenceSpritePixelsPerUnit

  Sprites 有一个 Pixels Per Unit value 控制 sprite 的像素密度（多少个像素显示为一个 world unit）。对于与这个值相同的 sprite，像素密度和 UI 坐标系是 1:1。

- float scale

  Unity 对 panel 中的元素应用的一致 scale factor。

- PanelScaleMode scaleMode

  当屏幕 size 改变时，panel 中的 elements 如何缩放：

  - ConstantPixelSize

    无视 screen size，元素总是基于 pixel size。

  - ConstantPhysicalSize

    无视 screen size 和 resolution，元素总是基于 physical size。

  - ScaleWithScreenSize

    元素随着 screen size 增加而变大，反之亦然。

- PanelScreenMatchMode screenMatchMode

  当 screen 分辨率的宽高比 aspect ratio 和 reference resolution 指示如何缩放 panel area

  - MatchWidthOrHeight

    使用 width，height，或者它们的混合，作为参考，来缩放 panel，以达成特定的宽高比。

  - Shrink

    保持宽高比，缩小 panel area，使得 panel size 不会超过 reference resolution。

  - Expand

    保持宽高比，放大 panel area，使得 panel size 不会小于 reference resolution。

- float sortingOrder

  当 Scene 使用多个 panel，这个值决定 panel 之间的渲染顺序。更大的 sortingOrder 的 panel 渲染在更小的 sortingOrder 的 panel 上面。

- int targetDisplay

  用于渲染这个 panel 的 display，除非指定了 render texture（此时 render texture 优先）。

- RenderTexture targetTexture

  指定一个 Render Texture 来渲染这个 panel 的 UI。

  这可以用于在 Scene 中的 3D geometry 上显示 UI，来执行手动 UI post-processing，或者在一个 MSAA-enabled Render Texture 上渲染 UI。

  如果 project color space 是线性的，则应该使用一个格式为 GraphicsFormat.R8G8B8A8_SRGB。

  如果 project color space 是 gamma，则应该使用一个格式为 GraphicsFormat.R8G8B8A8_UNorm。

- PanelTextSettings textSetting

  指定一个应用附加到这个 panel 的每个 UI Docuemnt 的 UI。

  一个 PanelSettings 在运行时生成一个 Panel 来渲染 UI。Scene 中多个 UIDocument 可以使用同一个 PanelSettings，这些 UIDocument 则渲染在同一个 panel 中。VisualElement 的 panel 引用元素渲染所在的 panel。

- ThemeStyleSheet themeStyleSheet

  指定一个 style sheet，Unity 将它应用到附加到这个 panel 的每个 UIDocument。

  默认它是 main Unity style sheet，其包含 Unity 提供的元素（例如 buttons，sliders，text fields 等）的默认 styles。

## 委托

- screenPanelSpaceFunction

  设置这个函数，来处理从 screen space 到 panel space 的坐标转换。对于 overlay panels，这个函数直接返回输入 value。这里 screen space 一个单位就是屏幕的一个像素，但是坐标系原点在左上角，y 轴向下（如果是从 Input/InputSystem 获取的 pointer 的 screenPosition，需要用 Screen.height 减去 y 值来转换 y 轴方向）。

  如果 panel 显示到 render texture，render texture 渲染到 3D objects，则需要使用这个函数来转换屏幕像素位置到 panel space 的位置。一种方法是使用 raycasts 投射 scene 中的 MeshColliders。这个函数可以先检查 ray hit 到的 GameObject 是否有一个 MeshRenderer，其带有一个使用这个 render texture 的 shader。然后它可以已返回转换到 texture pixel space 的 RaycastHit.textureCoord。

  设置为 null 来转换到 default behavior。


