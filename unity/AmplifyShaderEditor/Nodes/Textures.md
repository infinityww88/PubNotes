# Textures

## Blend Normals

通过特殊公式在两个法向量之间进行混合

BlendedNormal = normalize( float3( A.xy + B.xy, A.z*B.z )

简单的平均计算会导致法线丢失，因为法向量通常z部分占据最大的值，而这种混合方法尽可能保持法相方向

## HeightMap Texture Blend

输入一个HeightMap，一个表示混合区域的掩码SplatMask，一个混合强度参数Blend Strength，输出一个[0, 1]之间的值表示采样的混合系数，通常用于texture layering

## Substance Sample（TODO）

## Texel Size

输出选择的纹理的大小信息。选择的纹理可以通过Reference属性或者输入端口指定

输出Width，1/Width，Height，1/Height

## Texture Array

特殊类型的sampler，从一个2D textures数组中采样。使用一个array可以节约从多个纹理采样的性能。类似Texture Sample，但是具有一个额外的Index参数，来从数组中获取指定的纹理

ASE提供了一个免费的Texture Array Creator工具。shader model >= 3.5

## Texture Object

应用一个纹理，可以被Texture Sample采样

- Type
  - Property：声明为材质面板属性
  - Global：只能通过script设置，并且定义为一个静态变量，被所有shader共享，可以全局改变value
- Name：可编辑的纹理名字，显示在材质面板上
- Property：通过Name生成的不可编辑的名字，通过script设置纹理属性时使用的名字
- Default Texture：如果没有设置属性，使用的默认纹理
  - White
  - Black
  - Gray
  - Bump
- Auto-Cast Mode：使node根据input texture自动调整类型，或者lock为只接收指定类型
  - Auto
  - Locked To Texture 1D：只接收1D纹理（在unity中1D texture就是通常的2D纹理，但是只有一行像素或者只使用第一行像素
  - Locked To Texture 2D
  - Locked To Texture 3D（Mipmap）
  - Locked To Cube
  - Locked To Texture 2D Array：只接收Texture2DArray asset files
- Attribute：添加改变material显示和行为的属性。可以通过+/-按钮动态添加和移除
  - Hide in Inspector：属性被创建，但是不在Material上显示
  - HDR/Gamma/Per Rendered Data/No Scale Offset/Normal（TODO）

## Texture Sample

使用UV坐标对纹理进行采样。这个节点包含很多小的选项使简单和常用的操作变得容易。例如除了使用它读取albedo或smoothness映射，还可以设置它读取normal映射，而后者需要一些特殊处理

如果拖拽一个texture到editor graph上，将创建一个texture sample节点，并且自动引用这个纹理。如果纹理被标记为normal纹理，这个node也会被设置为normal map，并且输出XYZ向量，而不是RGBA向量，并且出现一个额外的scale端口，以允许normal在切线空间缩放

纹理和纹理采样是通用的概念，纹理可以保存任何逐像素数据，甚至不仅仅是显示相关的

- Mode
  - Object：直接使用一个Texture
  - Reference：引用一个已存在的Texture Sample节点
- UV Set：使用的UV channel，也被成为UV Index。Set 2通常用于Lightmap UV坐标
  - [1, 4]：4个UV通道
- Mip Mode（TODO）
- Unpack Normal Map
- Reference：指向一个已存在的Texture Sample
- Type/Name/Property Name/Default Texture/Auto-Cast Mode参加Texture Node
- Variable Mode：决定当前property/global变量是否在当前shader中创建
  - Create：属性或全局变量在当前shader中创建
  - Fetch：不在当前shader中创建变量或属性，而是引用其他地方的定义的全局变量
- Scale：垂直于表面缩放normal map，可以调整surface的凹凸程度

## Triplanar Sample

三维映射采样。使用3个投影平面投影texture到模型上，每个X/Y/Z坐标轴一个

这个节点只是通用目的triplanar效果到便捷节点。不被用来替换所有类型的triplanar效果，只用于最常用的那些

## Unpack Scale Normal

运行Unity内部的UnpackScaleNormal函数来unpack normal map纹理并相应缩放normal

## Virtual Texture Object（TODO）
