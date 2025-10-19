# TexturePaint

对于卡通风格，可以直接使用Texture Paint绘制一些简单线条表现出特点（纹理、石块），而不必使用GIMP绘制纹理

对于lowpoly风格，可以直接填充mesh的区域创建色块风格贴图，亦不必开启GIMP进行绘制

而且Blender还提供程序化纹理

## Introduction

UV texture是一个picture（image，sequence，movie），用于为mesh的表面着色

UV texture使用一个或多个UV maps映射到mesh 上。有3种方式来完成UV texture使用的image

- 在Image Editor中在当前选择的UV texture上绘制一个平面image，使用它的UV map将颜色传输到mesh的faces上
- 在3D View中绘制mesh，让Blender使用当前选择的UV map来更新UV texture（投影绘制）
- 使用任何一个Image Editing Program（GIMP）创建一个image。在Image Editor中选择UV texture，然后加载image。Blender将使用那个texture的UV map来将颜色传输到mesh的faces上

Blender提供来一个内置的paint mode成为Texture Paint，专门设计用来帮助在Image Editor或者3D Viewport中快速编辑UV textures和images。因为UV texture只是一个特殊目的的image，你也可以使用任何外部的绘制程序例如GIMP进行绘制

一个Mesh可以有多个UV textures layers，因此可能有多个images用来给mesh着色。但是，每个UV texture只能有一个image

Texture Paint同时工作于3D Viewport和Image Editor。在3D Viewport Texture Paint模式下，可以直接通过投影到UVs在mesh上进行绘制

要绘制的物体必须先unwrap uv。UVs可以按照传统方式使用Unwrapping Tools添加，或者在Texture Paint Mode通过Simple UVs添加

被修改的texture不会自动保存，必须在Image Editor>Image>Save中保存

## Texture Paint Tools

- Draw：绘制颜色
- Soften：使用blur效果soften或者sharpen图像
  - Direction
    - Soften：绘制模糊效果
      - Kernel Radius（2D only，Image Editor）：模糊半径
    - Sharpen：增强图像的对比度
      - Sharp Threshold：只有pixels和周围pixels差值超过阈值才会应用sharpen
      - Kernel Radius（2D only）：只sharpen半径内的像素
- Blur Mode：模糊效果
  - Gaussian：越接近brush中心的采样权重越高
  - Box：所有采样具有相同的权重
- Smear：GIMP中的涂抹工具

- Clone

  从指定image（或者同一个image到位置）复制颜色到active image

  在3D投影绘制模式下，clone cursor通过Ctrl-LMB设置，之后通过LMB绘制就开始进行复制。复制只是model在3D View中投影的2D纹理，将其作为图像重新绘制到3D模型上

  2D Clone（TODO）

  - Clone from Paint Slot（3D projective only）：使用其他image作为clone source，而不是使用同一个image中到3D cursor位置作为source

    - Source Clone Slot：选择clone source

- Fill

  使用brush color填充大块区域。填充与点击的像素颜色相似的临近像素

  - Fill Threshold（2D only）：决定填充颜色相似的程度

  - Gradient：使用一个渐变填充整个图像。可以设置渐变start和end的颜色。可以使用Linear和Radial两种渐变类型，每种渐变都通过在图像上画一条直线的方式填充。对于Linear，确定渐变的起点终点和渐变方向；对于Radial，确定圆心和渐变完成的半径

- Mask

  映射一个image到mesh上，使用image的intensity来将特定mesh部分在绘制期间mask出去，使其不受影响。只对3D绘制有效。可以New一个Image作为Mask Image，然后绘制它（只使用灰度brush）。然后在绘制正常的texture，则在3D View中，映射到mask区域的颜色就会被mask（如果mask像素=1，则完全不绘制；如果mask像素=0，则完全绘制；如果mask像素=0.5，则绘制一半强度）

## Tool Setting

### Texture Slots

和UV maps关联的images的组合成为slots

选择一个Paints Slots或Canvas Image还会在Image Editor中显示相应的图像

Mode：Slot包含两种绘制模式

- Material：从mesh的materials中检测slots
- Single Image：使用active UV Layer绘制任何一个已存在的image，而不仅是material中的texture。被绘制的图像仍然会使用当前UV maps在3D View中的mesh上显示出来。因此如果只需要绘制Mesh的纹理，而不需要在Blender中进行渲染，是不需要给Mesh创建Material的，只需要选择要使用的UV Maps和要被绘制的纹理
  - Image：选择作为canvas的image（被绘制的image），绘制将修改这个image
    - New：创建一个新的image
  - UV Map：选择用于绘制的UV layer（UV坐标，于Mesh UV Maps panel的当前active UV map相同）
  - Texture Filter Type：设置texture的插值模式，Linear或Closest
- Save All Images：Repack（如果是外部文件则保存）所有被编辑的images

### Brush Settings

- Blend：
  设置Paint应用到下面颜色的方式。除了通用的Blend Modes，还有额外的Mode
  - Add Alpha：在绘制时使image更加不透明
  - Erase Alpha：绘制时使image更加透明，允许背景色和下层纹理显示出来
- Radius：控制brush的半径，以像素衡量。F交互式调整brush半径
- Strength：达到brush目标颜色需要使用的stroke数量
Color Picker
- Color：在image上的任何地方按S键采样那个颜色并设置为当前brush颜色。绘制时按Ctrl临时使用第二颜色绘制（background color）
- Swap Color（Cycle icon）
- Gradient
  使用渐变作为brush的颜色
  - Gradient Colors：Color Ramp控件定义gradient颜色，通过点击+/-按钮添加新的stop点
  - Mode
    - Pressure：根据stylus pressure从color ramp选择一个颜色
    - Clamp：沿着stroke按照Gradient Spacing选项修改颜色。渐变完成后，使用最后一个颜色绘制剩余的stroke
      - Gradient Spacing：指定渐变完成的距离（0-1）
    - Repeat：类似Clamp，但是重复应用渐变
- Color Palette
- Advanced Options
  - Accumulate：累积stroke，就像airbrush
  - AffectAlpha：绘制时阻止alpha channel被修改（3D only）

### Mask

- Stencil Mask

  通过header的checkbox激活和关闭

  - Stencil Image：用作mask的image，它也是可以在Image Editor和3D View中绘制的
  - UV Layer：用于Stencil Image的UV maps
  - Display Color：3D Viewport中显示的Mask color
    - Inverts Stencil

### Symmetry

### Options

- Occlude：只绘制没有被其他mesh surface阻挡的surface
- Backface Culling：只绘制front side faces
- Cavity Mask：brush将被mask如果surface上面有凹陷或凸起。Cavity算法是基于vertex-based

### Tiling（TODO）

当brush移动出Canvas一侧，Wrap Stroke到Image的另一侧。非常方便用来制作seamless texture

- X：left/right
- Y：top/bottom
