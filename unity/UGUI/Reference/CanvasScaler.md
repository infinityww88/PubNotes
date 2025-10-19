# Canvas Scaler

控制整个scale和UI元素的像素密度。

提供了多种方法，但只有一个目的，计算出一个Canvas.scaleFactor，它是UI单位和世界单位的比值。UI单位乘以这个factor就可以得到世界空间的单位。

UI size保持不变的情况下，ScaleFactor越大，World size越大。

ScaleFactor = World Unit / UI Unit

ScaleFactor缩放Canvas的原理很简单，可以理解为使用Rect Tool将Canvas拖拽到ScreenSize * ScaleFactor大小，就像拖拽普通的UI元素一样，Canvas中所有的子元素都按照正常的Anchor/Auto布局随之变化，这期间UI元素大小可能保持不变，因为anchors可能都在一起，最后整个Canvas缩放为ScreenSize大小（这次是真正意义的缩放）。

## Constant Pixel Size

手动设置World Unit到UI Unit的映射比例，即手动设置Scale Factor。

每个Sprite资源具有一个Pixels Per Unit（一个世界单位对应多少像素），用来计算一个Sprite在world中是多大。

Sprite图像具有一个分辨率（ResImage），Sprite资源有一个Pixels Per Unit（PPU），CanvasScaler具有一个Reference Pixels Per Unit（RPPU）。

当把一个Sprite放在场景中作为一个精灵物体时，它在world的大小等于ResImage/PPU。

当把Sprite作为Canvas中的Image时，它在Canvas中的大小是ResImage * RPPU / PPU。

当改变PPU或RPPU时，点击Image的Set Native Size来重置Image在Canvas的大小。这个按钮就是按照上面的公式重新设置RectTransform的size。

RPPU的主要作用就是Image的Set Native Size

## Scale With Screen Size

预先定义一个参考分辨率。可以认为就在屏幕中心周围划出一块和参考分辨率相同大小的屏幕空间，作为canvas大小。然后在这个canvas中设计UI。然后就像使用ScaleFactor缩放Canvas的原理一样，假想使用Rect Tool等比例拖拽Canvas，拖拽的大小由Screen Match Mode定义：

- Shrink：使得Screen恰好包围Canvas，Screen会有Canvas覆盖不到的区域
- Expand：使得Canvas恰好包围Screen，Canvas会有超出Screen的区域
- Match Width Or Height：在Shrink和Expand之间做插值

所有Scale Mode都是确定ScaleFactor和RPPU的，其中

- RPPU确定Sprite在UI中大小（UI单位）
- ScaleFactor确定UI在World中的大小（世界单位）

## Constant Physical Size

UI元素的position和size使用物理单位指定，例如millimeters，points，或picas。UI中的单位将变成厘米、点。这样UI元素将保持物理大小的不变，而不管设备的DPI。

原理和上面两个缩放Canvas的原理相同，只是通过另一种计算ScaleFactor的公式，这个公式使用物理单位计算。

Physical Unit：指定使用何种物理单位，厘米/毫米/英寸/点

DPI：每英寸的点数。点就是设备屏幕上的一个像素点。不同的设备报告各自的DPI，就可能在不同的设备上实现物理单位的对应关系，因为通过点数可以转换为物理单位——英寸，进而就可以转化为各种其他物理单位（厘米/毫米）

RPPU用来确定一个Sprite有多少个点，即图像像素和设备点直接的映射比例。这样就知道图像在设备上显示的英寸数。

## World UI

对于世界模式UI，RPPU和Sprite作为精灵物体时的作用一样，确定Sprite在场景中的时间单位大小。


