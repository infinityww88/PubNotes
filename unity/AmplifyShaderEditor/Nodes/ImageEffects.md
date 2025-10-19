# Image Effects

## Blend Operations

- 使用Blend Op混合两个输入的颜色（float4），就像图像编辑工具中的图层混合操作
- Source：first layer，Destiny：second layer
- 19种Op
- Saturate（饱和度）：将最终结果截取到0～1之间

## Desaturate

- 去饱和（色彩鲜艳程度，色彩越鲜艳，饱和度越高，反之灰度越高）
- 按照指定到百分比（Fraction）将RGB属性向灰度转换

## GammaToLinear/LinearToGamma

- 将sRGB（Gamma）空间到颜色转换到Linear空间

## Grayscale

- 将RGB颜色值转换为灰度值

## HSVToRGB/RGBToHSV

- 将HSV颜色值转换为RGB颜色值

## Posterize

- 色调分离
- 将RGB属性按照指定的Power值将连续的色调转换为离散的色调区域（阶梯色彩）

## SimpleContrast

- 引用一个Value指定的对比度到RGB颜色上
