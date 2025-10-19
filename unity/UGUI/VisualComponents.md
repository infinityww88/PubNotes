# Visual Components

## Text

Label

## Image

source image使用一个sprite。color指定hint颜色，material制定一个用于渲染的材质。

Image Type

- Simple：均匀缩放整个sprite
- Sliced：使用九宫格sprite
- Tiled：类似Sliced九宫格sprite，但不是缩放中间部分，而是堆叠
- Filled：类似Simple，但是以各种方法定义如何填充和填充的百分比
  - Fill Method
    - Horizontal：水平填充，Fill Origin定义为Left/Right
    - Vertical：垂直填充，Fill Origin定位为Top/Bottom
    - Radial 90：90度填充完。Fill Origin定义为四个corner
    - Radial 180：180度填充完。Fill Origin定位为四个edge的中心
    - Radial 360：360度填充完。Fill Origin定位为填充起始线位置，Left/Right/Top/Bottom
  - Fill Amount：填充百分比
  - Clockwise：填充方向
  - Preserve Aspect：保持Image的aspect

## Raw Image

使用纹理而不是Sprite。Sprite是保护很多信息的纹理，例如pivot的位置，sliced sprite的border的位置，使用的texture altas以及在其中的位置等等。Raw Image应该只在必要的时候使用，否则绝大多数情况下使用Image就可以。

## Mask

Mask不是可见的UI元素，而是修改控件子元素的显示。mask限制（mask）剪裁子元素显示为parent rect区域。

## Effects

可视化组件还可以有各种简单的效果，例如shadow或outline。

Text、Image、Mask是所有可视化UI的基础，所有负责UI都是有这几种元素构成。

